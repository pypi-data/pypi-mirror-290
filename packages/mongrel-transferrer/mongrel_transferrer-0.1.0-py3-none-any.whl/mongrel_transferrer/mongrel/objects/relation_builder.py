"""
    MONGREL: MONgodb Going RELational
    Copyright (C) 2023 Ricardo Prida

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

manages the creation of tables and their relations from the configuration file
"""
from .table import Table, TableInfo
from ..helpers.constants import TRAN_OPTIONS


class RelationBuilder:
    """
    This class builds and manages the relations created from the config files
    """

    @staticmethod
    def walk_paths(json_tracks: dict) -> list:
        """
        Walk all possible paths of a dict and makes lists out of it
        example:
        {
            "a":{
                "n:1":
                {
                    "b":{}
                },
                "n:m":
                {
                    "c":{}
                }
            }
        }
        has the paths
        ["a", "n:1", "b"]
        ["a", "n:m", "c"]
        :param json_tracks: the dictionary to be walked
        :return: yields all paths in the dictionaries as a set of lists
        """
        if isinstance(json_tracks, dict):
            for key, value in json_tracks.items():
                if len(value) == 0:
                    yield [key]
                for p in RelationBuilder.walk_paths(value):
                    ret = [key]
                    ret.extend(p)
                    yield ret

    @staticmethod
    def get_relation_lists(relation_json_dict: dict) -> list:
        """
        Get all possible relation lists that are in the configuration file
        :param relation_json_dict: the mapping json dict of the configuration file
        :return: returns all possible paths of the json in the configuration file
        """
        relation_lists = []
        for pathee in RelationBuilder.walk_paths(relation_json_dict):
            relation_lists.append(pathee)
        return relation_lists

    @staticmethod
    def fetch_unique_relations(relation_lists: list, mapping_dict: dict):
        """
        Puts all relations in a list as Relation objects
        :param relation_lists: all unique relations in the configuration file
        :param mapping_dict:
        :return: all unique relations in a list
        """
        relations = []
        for relation_list in relation_lists:
            for idx, val in enumerate(relation_list):
                if idx % 2 == 0:
                    if TableInfo(val) not in relations:
                        if TRAN_OPTIONS in mapping_dict[val]:
                            relations.append(Table(TableInfo(val), mapping_dict[val][TRAN_OPTIONS]))
                        else:
                            relations.append(Table(TableInfo(val)))
        return relations

    @staticmethod
    def calculate_relations(relations_dict: dict, mapping_dict: dict) -> list:
        """
        Fetches all relations from the config and how they are linked
        :param relations_dict: Information on the relations and how they are linked. Basically the relations config.
        :param mapping_dict: Information on the relations themselves
        :return: returns the unique and initialized relations as a list with their links to other relations
        """
        relation_lists = RelationBuilder.get_relation_lists(relations_dict)
        unique_relations = RelationBuilder.fetch_unique_relations(relation_lists, mapping_dict)
        for relation in unique_relations:
            for relation_list in relation_lists:
                if str(relation.info) in relation_list:
                    parsed_relations = RelationBuilder.parse_relations(relation.info, relation_list)
                    relation.add_relations(parsed_relations)
        return unique_relations

    @staticmethod
    def parse_relations(info: TableInfo, relation_list: list[str]) -> list[tuple[str, str]]:
        """
        For a list of relations, calculates all relations it has to other tables
        example for the following paths:
        ["b", "n:1", "a"]
        ["a", "n:m", "c"]
        yields the following relations for a
        ("n:1", "b")
        ("n:m", "c")
        :param info: the relation Info of the relation to check the other relations for
        :param relation_list: the list of all possible paths in the relation configuration
        :return: the list of all relations in the correct order
        """

        def parse_left(location, lis):
            rel = lis[location - 1]
            rel_arr = rel.split(":")
            inverted = rel_arr[-1] + ':' + rel_arr[0]
            return inverted, lis[location - 2]

        def parse_right(location, lis):
            rel = lis[location + 1]
            return rel, lis[location + 2]

        relation = []
        idx = relation_list.index(str(info))
        if idx > 1:
            parsed_inv, parsed_val = parse_left(idx, relation_list)
            relation.append((str(parsed_inv), str(parsed_val)))
        if idx < len(relation_list) - 2:
            parsed_rel, parsed_val = parse_right(idx, relation_list)
            relation.append((str(parsed_rel), str(parsed_val)))
        return relation
