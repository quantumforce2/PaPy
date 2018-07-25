import collections
import json

class Columns:
    def __init__(self):
        self.__titles = []

    def add_body(self, dimension, subset, hierarchy=''):
        body_as_dict = collections.OrderedDict()
        if hierarchy == '':
            hierarchy = dimension
        body_as_dict.__setitem__('Subset@odata.bind',
                                 "Dimensions('{}')/Hierarchies('{}')/Subsets('{}')".format(dimension, hierarchy, subset))
        self.__titles.append(body_as_dict)

    def as_list(self):
        return self.__titles


class Rows:
    def __init__(self):
        self.__titles = []

    def add_body(self, dimension, subset, hierarchy=''):
        body_as_dict = collections.OrderedDict()
        if hierarchy == '':
            hierarchy = dimension
        body_as_dict.__setitem__('Subset@odata.bind',
                                 "Dimensions('{}')/Hierarchies('{}')/Subsets('{}')".format(dimension, hierarchy, subset))
        self.__titles.append(body_as_dict)

    def as_list(self):
        return self.__titles


class Titles:
    def __init__(self):
        self.__titles = []

    def add_body(self, dimension, subset, element, hierarchy=''):
        body_as_dict = collections.OrderedDict()
        if hierarchy == '':
            hierarchy = dimension
        body_as_dict.__setitem__('Subset@odata.bind',
                                 "Dimensions('{}')/Hierarchies('{}')/Subsets('{}')".format(dimension, hierarchy, subset))
        body_as_dict.__setitem__('Selected@odata.bind',
                                 "Dimensions('{}')/Hierarchies('{}')/Elements('{}')".format(dimension, hierarchy,element))
        self.__titles.append(body_as_dict)

    def as_list(self):
        return self.__titles


class View:
    def __init__(self, name, columns, rows, titles, suppressemptycolumns, suppressemptyrows, formatstring, private = False):
        self.name = name
        self.columns = columns
        self.rows = rows
        self.titles = titles
        self.suppressemptycolumns = suppressemptycolumns
        self.suppressemptyrows = suppressemptyrows
        self.formatstring = formatstring
        self.private = private

    def body(self):
        body_as_dict = collections.OrderedDict()
        body_as_dict['@odata.type'] = 'ibm.tm1.api.v1.NativeView'
        body_as_dict['Name'] = self.name
        body_as_dict['Columns'] = self.columns
        body_as_dict['Rows'] = self.rows
        body_as_dict['Titles'] = self.titles
        body_as_dict['SuppressEmptyColumns'] = self.suppressemptycolumns
        body_as_dict['SuppressEmptyRows'] = self.suppressemptyrows
        body_as_dict['FormatString'] = self.formatstring

        return body_as_dict

    def as_json(self):
        return json.dumps(self.body())




