import collections
import json

"""
DESCRIPTION:

-   Class file to write into TM1 cube
-   Take data as dictionary input (ref: data input format in config_files/sample_cube_input_multiple_cell.json and config_files/sample_cube_input_single_cell.json)
-   Create output data as odata json. This json output can then be used in POST method (cube_cells_write() in papy module) to write into a TM1 cube

"""

class _SingleCell:
    def __init__(self, cube_name, dimensions, elements, value):
        """
        desc: Create each single line for CubeUpdate class

        usage: In CubeUpdate class. CubeUpdate class process dict data and sends single line to process

        :param cube_name: str: name of the cube
        :param dimensions: tuple: dimensions list
        :param elements: tuple: elements list
        :param value: numeric: cell value
        """
        self.cube_name = cube_name
        self.dimensions = dimensions
        self.elements = elements
        self.value = value

    def create_body(self):
        body_as_dict = collections.OrderedDict()
        body_as_dict["Cube@odata.bind"] = "Cubes('{}')".format(self.cube_name)
        body_as_dict["Cells"] = []
        cell = dict()
        body_as_dict["Cells"].append(cell)
        cell["Tuple@odata.bind"] =  list()
        i = 0
        for dim in self.dimensions:
            cell["Tuple@odata.bind"].append("Dimensions('{}')/Hierarchies('{}')/Elements('{}')".format(dim, dim, self.elements[i]))
            i = i + 1
        body_as_dict["Value"] = self.value
        return body_as_dict
        #print(dict(body_as_dict))


class CubeUpdate:
    """
    desc: Process a input dictionary data to write into a cube.

    usage: In cube_cells_write() function in papy module
    """
    def __init__(self, cube_name, data):
        """
        :param cube_name: str: cube_name
        :param data: dict: data as dictionary
            (ref: data input format in config_files/sample_cube_input_multiple_cell.json and config_files/sample_cube_input_single_cell.json)

        data input Format (dict):
       ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            {
              "Dimensions": ["Dim1", "Dim12],
              "Elements": {
                "0": ["Dim1_Element1", "Dim2_Element1"],
                "1":["Dim1_Element2", "Dim2_Element2"]
                },
              "Value": {
                "0": "50",
                "1": "500"
                }
            }

        Output format (json):
        -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            [
                {
                    "Cube@odata.bind":"Cubes('Cube')",
                    "Cells": [
                        {
                        "Tuple@odata.bind": ["Dimensions('Dim1')/Hierarchies('Dim1')/Elements('Dim1_Element1')","Dimensions('Dim2')/Hierarchies('Dim2')/Elements('Dim2_Element1')"]
                        }
                    ],
                    "Value": "50"
                },
                {
                    "Cube@odata.bind":"Cubes('Cube')",
                    "Cells": [
                        {
                        "Tuple@odata.bind": ["Dimensions('Dim1')/Hierarchies('Dim1')/Elements('Dim1_Element2')","Dimensions('Dim2')/Hierarchies('Dim2')/Elements('Dim2_Element2')"]
                        }
                    ],
                    "Value": "500"
                }
            ]
        """
        self.cube_name = cube_name
        self.data = data

    def create_body(self):
        body = list()
        for (index_key, dim_elements) in self.data['Elements'].items():
            _sc = _SingleCell(self.cube_name, tuple(self.data['Dimensions']), tuple(dim_elements), self.data['Value'][index_key])
            body.append(_sc.create_body())
        return body

    def as_json(self):
        return json.dumps(self.create_body())

