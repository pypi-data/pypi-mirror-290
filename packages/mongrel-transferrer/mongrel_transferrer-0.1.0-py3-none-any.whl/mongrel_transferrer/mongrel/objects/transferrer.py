"""
Transfer Logic can be found here
"""
from sqlalchemy import create_engine, URL, text
import pandas as pd
import pymongo
from tqdm import tqdm

from ..helpers.map_flattener import flatten
from ..helpers.constants import PATH_SEP
from ..objects.table import Table, TableInfo, Field
from ..objects.relation_builder import RelationBuilder
from ..objects.table_builder import TableBuilder
from ..helpers.database_functions import insert_on_conflict_nothing


class Transferrer:
    """
    The main class that handles the transfer
    """
    dependencies: dict[str, list[TableInfo]]
    batch_size: int
    relations: list[Table]
    length_lookup: dict[TableInfo, int]

    def __init__(self, relation_list: list[Table], mongo_host: str, mongo_database: str, mongo_collection: str,
                 sql_host: str, sql_database: str, mongo_port: int = None, sql_port: int = None, sql_user=None,
                 sql_password=None, mongo_user: str = None, mongo_password: str = None, batch_size=1000):
        """
        Initializes the transfer class with all the required information
        :param relation_list: the list of all prepped relations
        :param mongo_host: the ip address or name of the mongo server
        :param mongo_database: the database name of the source mongo
        :param mongo_collection: the collection that stores the source documents
        :param sql_host: the ip address or name of the postgres server
        :param sql_database: the name of the target postgres database
        :param mongo_port: optional, the port of the source mongo database
        :param sql_port: optional, the port of the target sql database
        :param sql_user: optional, the user of the target database
        :param sql_password: optional, the password of the user for the target database
        :param mongo_user: optional, the user of the source mongo database
        :param mongo_password: optional, the password of the user for the source database
        :param batch_size: the batch size used
        """
        self.mongo_collection = mongo_collection
        self.sql_password = sql_password
        self.sql_user = sql_user
        self.sql_port = sql_port
        self.mongo_password = mongo_password
        self.mongo_port = mongo_port
        self.sql_host = sql_host
        self.sql_database = sql_database
        self.mongo_user = mongo_user
        self.mongo_database = mongo_database
        self.mongo_host = mongo_host
        self.dependencies = Transferrer.create_dependencies(relation_list)
        self.relations = relation_list
        self.batch_size = batch_size
        self.length_lookup = {}

    def prepare_database(self, creation_script: str) -> None:
        """
        Runs the creation statement on the target database
        :param creation_script: the creation script to be executed
        """
        url_object = URL.create("postgresql", username=self.sql_user, password=self.sql_password, host=self.sql_host,
                                port=self.sql_port, database=self.sql_database)
        engine_go_brr = create_engine(url_object)
        with engine_go_brr.connect() as connie:
            splitted = creation_script.split(";")
            for statement in splitted:
                statement = statement.strip()
                if len(statement) > 1:
                    connie.execute(text(statement))
                    connie.commit()

    @staticmethod
    def create_dependencies(relation_list: list[Table]) -> dict[str, list[TableInfo]]:
        """
        Creates a dependency lookup for all the tables. This is required so that relations with foreign key relations
        get filled before their children.
        :param relation_list: a list of all relations
        :return: a dictionary lookup of relationInfo containing all tables that need to be filled before insertion
        """
        dependencies: dict[str, list[TableInfo]] = {}
        for relation in relation_list:
            info = f'{relation.info.schema}.{relation.info.table}' if relation.alias is None else relation.alias
            for column in relation.columns:
                if column.foreign_reference is not None:
                    if info in dependencies:
                        dependencies[info].append(column.foreign_reference)
                        # I don't know why but a duplicate check in the if-clause just does not work
                        dependencies[info] = list(set(dependencies[info]))
                    else:
                        dependencies[info] = [column.foreign_reference]
        return dependencies

    def create_data_dict(self):
        """
        Creates the dataframes for all the relations
        :return: a dictionary containing dataframes with RelationInfo lookups
        """
        data: dict[TableInfo, pd.DataFrame] = {}
        for relation in self.relations:
            relation_info = relation.info if not relation.alias else relation.alias
            data[relation_info] = relation.make_df()
        return data

    def filter_dict(self, doc: dict, relation: Table, layer: int = 0):
        """
        Walks the dictionary and only looks at the relevant paths
        :param doc: a source document
        :param relation: the relation to be filled
        :param layer: the current layer of the walk, used in recursion
        :return: the filtered dict containing only relevant information for the relation
        """
        if isinstance(doc, dict):
            rel_dict = {}
            for col in relation.columns:
                if col.path is not None:
                    for key in doc.keys():
                        if len(col.path) > layer and key == col.path[layer]:
                            rel_dict[key] = self.filter_dict(doc[key], relation, layer + 1)
            return rel_dict
        if isinstance(doc, list):
            vals = []
            for entry in doc:
                vals.append(self.filter_dict(entry, relation, layer))
            return vals
        return doc

    def read_document_lines(self, doc: dict, relation: Table) -> dict:
        """
        Reads the document with all the relevant information for the relation
        :param doc: the source document
        :param relation: the relation that uses the information
        :return: the values as a dict for the columns
        """
        return_values = {}
        rel_dict = self.filter_dict(doc, relation)
        flattened = flatten(rel_dict, path_separator=PATH_SEP)
        for row in flattened:
            ok = True
            for col in relation.columns:
                if col.field_type == Field.PRIMARY_KEY:
                    if col.translated_path not in row or row[col.translated_path] is None:
                        ok = False
                        break
            if not ok:
                continue
            for col in relation.columns:
                if col.path:
                    if col.translated_path in row:
                        return_values.setdefault(col.target_name, []).append(col.conversion_function(
                            row[col.translated_path], **col.conversion_args))
                    else:
                        return_values.setdefault(col.target_name, []).append(None)
        return return_values

    def write_cascading(self, relation_info: TableInfo, data: dict[TableInfo, pd.DataFrame],
                        connection: object) -> None:
        """
        Writes the relation and all prerequisite relations to the target database
        :param relation_info: the table to write
        :param data: all the current data stored yet
        :param connection: the connection to the target database
        """
        if relation_info in self.dependencies:
            for info in self.dependencies[relation_info]:
                self.write_cascading(info, data, connection)
        if len(data[relation_info]) > 0:
            data[relation_info].to_sql(name=relation_info.table, schema=relation_info.schema, if_exists="append",
                                       method=insert_on_conflict_nothing, con=connection, index=False)
            data[relation_info] = pd.DataFrame(columns=data[relation_info].columns)

    def transfer_data(self):
        """
        The transfer process itself
        """
        mongo_client = pymongo.MongoClient(host=self.mongo_host, port=self.mongo_port, username=self.mongo_user,
                                           password=self.mongo_password)
        db = mongo_client[self.mongo_database]
        collie = db[self.mongo_collection]
        data: dict[TableInfo, pd.DataFrame] = self.create_data_dict()
        url_object = URL.create("postgresql", username=self.sql_user, password=self.sql_password,
                                host=self.sql_host, port=self.sql_port, database=self.sql_database)
        engine_go_brr = create_engine(url_object)
        with engine_go_brr.connect() as connie:
            for doc in tqdm(collie.find()):
                for relation in self.relations:
                    vals = self.read_document_lines(doc, relation)
                    if vals:
                        df = pd.DataFrame.from_dict(vals, orient='index').transpose()
                        relation_info = relation.info if not relation.alias else relation.alias
                        df = df.dropna(axis=0, how='all')
                        data[relation_info] = pd.concat([data[relation_info], df], ignore_index=True)
                        data[relation_info].drop_duplicates(relation.pks)
                for relation in self.relations:
                    relation_info = relation.info if not relation.alias else relation.alias
                    if len(data[relation_info].index) > self.batch_size:
                        self.write_cascading(relation_info, data, connie)
            for relation in self.relations:
                relation_info = relation.info if not relation.alias else relation.alias
                self.write_cascading(relation_info, data, connie)
        mongo_client.close()


def transfer_data_from_mongo_to_postgres(relation_config_dict: dict, mapping_config_path_dict: dict, mongo_host: str,
                                         mongo_database: str, mongo_collection: str,
                                         sql_host: str, sql_database: str, mongo_port: int = None, sql_port: int = None,
                                         sql_user: str = None, sql_password: str = None, mongo_user: str = None,
                                         mongo_password: str = None, batch_size: int = 1000,
                                         keep_list_alias_relations: bool = True) -> None:
    """
    A wrapper for all the required steps taken for a transfer
    :param relation_config_dict: dict of the relation config file
    :param mapping_config_path_dict: dict of the mapping config file
    :param mongo_host: the ip address or name of the mongo server
    :param mongo_database: the database name of the source mongo
    :param mongo_collection: the collection that stores the source documents
    :param sql_host: the ip address or name of the postgres server
    :param sql_database: the name of the target postgres database
    :param mongo_port: optional, the port of the source mongo database
    :param sql_port: optional, the port of the target sql database
    :param sql_user: optional, the user of the target database
    :param sql_password: optional, the password of the user for the target database
    :param mongo_user: optional, the user of the source mongo database
    :param mongo_password: optional, the password of the user for the source database
    :param batch_size: the batch size used
    :param keep_list_alias_relations: Flag if alias relations of lists should be kept. Their information can be
                                            retrieved from aggregating all n:m helper tables
    """
    relation_builder = RelationBuilder()
    relations = relation_builder.calculate_relations(relation_config_dict, mapping_config_path_dict)
    table_builder = TableBuilder(relations, mapping_config_path_dict, keep_list_alias_relations)
    creation_stmt = table_builder.make_creation_script()
    transferrer = Transferrer(table_builder.get_relations(), mongo_host, mongo_database, mongo_collection, sql_host,
                              sql_database, mongo_port, sql_port, sql_user, sql_password, mongo_user, mongo_password,
                              batch_size)
    transferrer.prepare_database(creation_stmt)
    transferrer.transfer_data()
