# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 10:58:05 2017

@author: MSARAF
"""
import json
# import time
import pprint
from pachore import Chore
from pasession import *
import pandas as pd
from pacubewrite import CubeUpdate
from paprocess import TIProcess

# from IPython.display import display, HTML, Image


class PApy:
    def __init__(self, login):
        self.pa_session = PASession(login)

    def get_tm1server_name(self):
        url = "Configuration/ServerName"
        response = self.pa_session.GET(url)
        return json.loads(response.text)['value']

    def get_cube_names(self, showcontrolobjects = False):
        url = "Cubes?$select=Name"
        response = self.pa_session.GET(url)
        objects = json.loads(response.text)['value']
        obj_lst = []
        for item in objects:
            if showcontrolobjects is True:
                obj_lst.append(item['Name'])
            else:
                if item['Name'][0] != '}':
                    obj_lst.append(item['Name'])
        return obj_lst

    def get_dimension_names(self, showcontrolobjects=False):
        url = "Dimensions?$select=Name"
        response = self.pa_session.GET(url)
        objects = json.loads(response.text)['value']
        obj_lst = []
        for item in objects:
            if showcontrolobjects is True:
                obj_lst.append(item['Name'])
            else:
                if item['Name'][0] != '}':
                    obj_lst.append(item['Name'])
        return obj_lst

    def get_cube_dimension(self, dimensionname):
        # Take dimension name as text
        # Returns tm1dimension object
        url = "Dimensions('" + dimensionname + "')?$expand=Hierarchies($expand=*)"
        response = self.pa_session.GET(url)
        dim_odata = json.loads(response.text)
        tm1dim = tm1dimension(dim_odata)
        return tm1dim

    #TODO: working
    # def search_dim_element_by_attribute(self, dimensionname, attributename, level =[0]):
    #     # dimensionname = text
    #     # attributenames = list
    #     # level = list of integers
    #     # showlevel boolean
    #     # Returs List
    #
    #     #abc = tm1.search_dim_element_by_attribute('Product_Rollup', 'Div Cd', '20', [0, 1, 2])
    #
    #     tm1dim = self.get_cube_dimension(dimensionname)
    #     elements = tm1dim.get_odata_elements_in_list()
    #     dictn = {}
    #     for el in elements:
    #         element = tm1element(el)
    #         for attributename in attributenames:
    #             attibutevalue = element.get_attribute_value(attributename)
    #             if element.level in level and attibutevalue == attributevaluesearch:
    #                 #print(element.name, element.index, element.level, attibutevalue)
    #                 dictn[element.name] = {}
    #                 dictn[element.name]['Attributes'] = {attributename:element.get_attribute_value(attributename)}
    #                 dictn[element.name]['Level'] = element.level
    #                 #dict[element.name][]
    #     return dictn

    #TODO: working
    def get_attribute_values(self, dimensionname):
        tm1dim = self.get_cube_dimension(dimensionname)
        pprint.pprint(tm1dim.odata)


    def get_cube_rule(self, cubename):
        url = "Cubes('" + cubename + "')?$select=Rules"
        response = self.pa_session.GET(url)
        objects = json.loads(response.text)['Rules']
        return objects

    def get_ti_names(self, showcontrolobjects=False):
        url = "Processes?$select=Name"
        response = self.pa_session.GET(url)
        objects = json.loads(response.text)['value']
        obj_lst = []
        for item in objects:
            if showcontrolobjects is True:
                obj_lst.append(item['Name'])
            else:
                if item['Name'][0] != '}':
                    obj_lst.append(item['Name'])
        return obj_lst

    def execute_ti(self, tiname, tiparameters=''):
        data = json.dumps(tiparameters)
        url = "Processes('" + tiname + "')/tm1.Execute"
        response = self.pa_session.POST(url, data=data)
        return response.text

    def get_dimension_names_from_cube(self, cubename):
        url = "Cubes('{}')/Dimensions?$select=Name".format(cubename)
        response = self.pa_session.GET(url)
        dimensions = json.loads(response.text)['value']
        dimension_lst = []
        for item in dimensions:
            dimension_lst.append(item['Name'])
        return dimension_lst

    def get_native_view(self, cubename, viewname):
        url = "Cubes('{}')/Views('{}')/tm1.Execute?$expand=Axes($expand=Hierarchies($select=Name),Tuples($expand=Members($select=Name))),Cells".format(
            cubename, viewname)
        response = self.pa_session.POST(url)
        view_odata = json.loads(response.text)
        tm1vw = tm1view(view_odata)

        return tm1vw

    def get_mdx_view(self, cubename, mdxquery):
        url = 'ExecuteMDX?$expand=Axes($expand=Hierarchies($select=Name),Tuples($expand=Members($select=Name))),Cells($select=Ordinal,Value)'
        response = self.pa_session.POST(url, data=mdxquery)
        view_odata = json.loads(response.text)
        tm1vw = tm1view(view_odata)
        return tm1vw

    def create_view(self, cubename, view):
        """
            desc: Creates a view using view object
            cubename: Text : cube name
            view: View object: contains view information (package: paview)
        """
        url = "Cubes('{}')/Views".format(cubename)
        response = self.pa_session.POST(url, data=view.as_json())
        return response.text

    def delete_view(self, cubename, viewname):
        """
            desc: delete a view
            cubename: Text : cube name
            viewname: Text: view name
        """
        url = "Cubes('{}')/Views('{}')".format(cubename, viewname)
        response = self.pa_session.DELETE(url, data='')
        return response.text

    def disconnect_tm1_user(self, username):
        url = "Users(\'{}\')/tm1.Disconnect".format(username)
        response = self.pa_session.POST(url, data='')
        return response.text

    #********************************************* start: Chores ******************************************************
    def get_chore_names(self, activeonly=False):
        url = "Chores?$select=Name,Active"
        response = self.pa_session.GET(url)
        objects = json.loads(response.text)['value']
        obj_lst = []
        for item in objects:
            if activeonly is False:
                obj_lst.append(item['Name'])
            else:
                if item['Active'] is True:
                    obj_lst.append(item['Name'])
        return obj_lst

    def get_chore(self, chorename):
        pass

    def create_chore(self, data):
        url = "Chores"
        response = self.pa_session.POST(url, data=data)
        return response.text

    def activate_chore(self, chorename):
        url = "Chores('" + chorename + "')/tm1.Activate"
        response = self.pa_session.POST(url, data='')
        return response.text

    def deactivate_chore(self, chorename):
        url = "Chores('" + chorename + "')/tm1.Deactivate"
        response = self.pa_session.POST(url, data='')
        return response.text

    def get_ti_process(self, ti_name):
        url ="Processes('" + ti_name + "')"
        response = self.pa_session.GET(url)
        return response.text

    def update_ti_process(self, ti_name, data):
        """
             desc: Update a process based on data in dict or json format
             ti_name: str: ti process name that needs to be created
             data: dict or json: ti data
         """
        url = "Processes('" + ti_name + "')"
        data = data if type(data) is dict else json.loads(data)
        data['Name'] = ti_name
        response = self.pa_session.PATCH(url, data=json.dumps(data))
        return response.text

    def create_ti_process(self, ti_name, data):
        """
            desc:Create a process based on data in dict or json format
            ti_name: str: ti process name that needs to be created
            data: dict or json: ti data
        """
        url = "Processes"
        data = data if type(data) is dict else json.loads(data)
        data['Name'] = ti_name
        response = self.pa_session.POST(url, data=json.dumps(data))
        return json.loads(response.text)

    def ti_exists(self, ti_name):
        """
            desc: Check if a ti process exists or not

            :param ti_name: str: process name
            Returns Boolean
        """
        if ti_name in self.get_ti_names():
            return True
        else:
            return False

    def copy_ti_process(self, source_ti_name, target_ti_name):
        """
            desc: Copy ti process/ TI process save as

            :param source_ti_name: str: Source ti name
            :param target_ti_name: str: Target ti name

            :return: response as text
        """
        source_odata = self.get_ti_process(source_ti_name)
        src_ti = TIProcess.get_from_dict(source_odata)
        data = src_ti.as_dict()
        if self.ti_exists(target_ti_name):
            response = self.update_ti_process(target_ti_name, data)
        else:
            response = self.create_ti_process(target_ti_name, data)
        return response.text

    def migrate_ti_process(self, ti_name, target_admin_host, target_http, cam, user_id, password):
        """
            desc: Migrate a TI on a server

            ti_name: str: ti process name that needs to be created
            data: dict or json: ti data
        """
        source_odata = json.loads(self.get_ti_process(ti_name))
        src_ti = TIProcess.get_from_dict(source_odata)
        data = src_ti.as_dict()

        target_login = PAlogin.login_using_cam(user_id, password, cam, target_admin_host, target_http)
        print(target_login.password)
        tm1_target = PApy(target_login)
        if tm1_target.ti_exists(ti_name):
            response = tm1_target.update_ti_process(ti_name, data)
        else:
            response = tm1_target.create_ti_process(ti_name, data)

        tm1_target.logout()
        return response

    def cube_cells_write(self, cube_name, data):
        """
            desc: Write dictionary formatted data into TM1 cube
                (ref: data input format in config_files/sample_cube_input_multiple_cell.json and config_files/sample_cube_input_single_cell.json)

            :param cube_name: str: cube_name
            :param data: dict: data as dictionary
                (ref: data input format in config_files/sample_cube_input_multiple_cell.json and config_files/sample_cube_input_single_cell.json)

            :return: response as text
        """
        url = "Update"
        cu = CubeUpdate(cube_name, data)
        response = self.pa_session.POST(url, data=cu.as_json())
        return response.text

    def logout(self):
        """ Logout from TM1"""
        url = "ActiveSession/tm1.Close"
        response = self.pa_session.POST(url, data='')
        return response.text

class tm1view:
    def __init__(self, view_odata):
        self.view_odata = view_odata

    @property
    def odata(self):
        return self.view_odata

    def get_title_elements(self, include_dimension_names=True):
        view_odata = self.odata
        #print(view_odata)
        try:
            title = []
            title_elements = view_odata['Axes'][2]['Tuples'][0]['Members']
            title_dim = view_odata['Axes'][2]['Hierarchies']

            title = []
            i = 0
            if include_dimension_names is True:
                for item in title_elements:
                    title.append({title_dim[i]['Name']: item['Name']})
                    i = i + 1
            else:
                title = [item['Name'] for item in title_elements]
            return title[:]
        # Incase no title elements in the view
        except IndexError:
            title = []

    def get_title_dimension_names(self):
        view_odata = self.view_odata
        try:
            title_dim = view_odata['Axes'][2]['Hierarchies']

            title_dimensions = [i['Name'] for i in title_dim]
            return title_dimensions
            # Incase no title elements in the view
        except IndexError:
            title = []

    def get_view_data_in_dict(self):
        """
            Short desc: Publish a tm1 view into Pandas dataframe
            returns:  Pandas Dataframe
        """

        view_odata = self.view_odata

        # List to hold the dimensions names as cloumn header names
        column_names = []

        # Get Title Elements in a list
        title = self.get_title_elements(include_dimension_names=False)
        column_names.extend(self.get_title_dimension_names())

        # Get Rows in a list
        rows = []
        row_dim_names = view_odata['Axes'][1]['Hierarchies']
        column_names.extend([i['Name'] for i in row_dim_names])
        rows_temp = view_odata['Axes'][1]['Tuples']

        for item in rows_temp:
            rows.append([i['Name'] for i in item['Members']])

        # Get Data in a list
        data_list = []
        data_dict = view_odata['Cells']
        for i in data_dict:
            data_list.append(i['Value'])

        # Get Columns in a list
        columns = []
        col_dim_names = view_odata['Axes'][0]['Hierarchies']
        column_names.extend([i['Name'] for i in col_dim_names])
        col_temp = view_odata['Axes'][0]['Tuples']
        for item in col_temp:
            columns.append([i['Name'] for i in item['Members']])

        # Create a dictionary with title, rows and columns
        view_data = {}
        data_index = 0
        tmp_lst1 = []
        for row in rows:
            for col in columns:
                tmp_lst1.extend(title)
                tmp_lst1.extend(row)
                tmp_lst1.extend(col)

                tmp_lst2 = []
                iterr = 0
                for item in tmp_lst1:
                    tmp_lst2.append("[" + column_names[iterr] + "]" + "." + "[" + item + "]")
                    iterr = iterr + 1

                tmp_lst2.append(data_list[data_index])
                view_data[data_index] = tuple(tmp_lst2[:])

                del tmp_lst1[:]
                del tmp_lst2[:]

                data_index += 1

        return view_data
        # print(view_data)

    def publish_into_pandas_dataframe(self):
        """
            Short desc: Publish a tm1 view into Pandas dataframe
            returns:  Pandas Dataframe
        """

        view_odata = self.view_odata

        # List to hold the dimensions names as cloumn header names
        column_names = []

        # Get Title Elements in a list
        title = self.get_title_elements(include_dimension_names=False)
        column_names.extend(self.get_title_dimension_names())

        # Get Rows in a list
        rows = []
        row_dim_names = view_odata['Axes'][1]['Hierarchies']
        column_names.extend([i['Name'] for i in row_dim_names])
        rows_temp = view_odata['Axes'][1]['Tuples']

        for item in rows_temp:
            rows.append([i['Name'] for i in item['Members']])

        # Get Data in a list
        data_list = []
        data_dict = view_odata['Cells']
        for i in data_dict:
            data_list.append(i['Value'])

        # Get Columns in a list
        columns = []
        col_dim_names = view_odata['Axes'][0]['Hierarchies']
        column_names.extend([i['Name'] for i in col_dim_names])
        col_temp = view_odata['Axes'][0]['Tuples']
        for item in col_temp:
            columns.append([i['Name'] for i in item['Members']])

        # Create a dictionary with title, rows and columns
        view_data = {}
        data_index = 0

        tmp_lst = []
        for row in rows:
            for col in columns:
                tmp_lst.extend(title)
                tmp_lst.extend(row)
                tmp_lst.extend(col)
                view_data[data_index] = tmp_lst[:]

                del tmp_lst[:]
                data_index += 1

                # Convert the date dictionary table into PANDA's data frame
        df = pd.DataFrame.from_dict(view_data)
        df = df.transpose()
        df = df.assign(x=data_list)
        column_names.append('Data')
        df.columns = column_names

        # Return Pandas dataframe
        return df

class tm1element:
    #element as dict
    def __init__(self, element):
        self.element = element

    @property
    def name(self):
        return self.element['Name']

    @property
    def uniquename(self):
        return self.element['UniqueName']

    @property
    def type(self):
        return self.element['Type']

    @property
    def level(self):
        return self.element['Level']

    @property
    def index(self):
        return self.element['Index']

    @property
    def attributes(self):
        #return element attribute list - dict
        return self.element['Attributes']

    def get_attribute_value(self, attributename):
        #attributenames = dictionary
        #return text
        if attributename in self.attributes:
            return self.attributes[attributename]
        else:
            return ''

class tm1dimension:
    # Dimension from odata
    def __init__(self, dimensionodata):
        self.dimensionodata = dimensionodata

    @property
    def name(self):
        return self.dimensionodata['Name']

    @property
    def odata(self):
        return self.dimensionodata

    def get_elementattributes_list(self):
        return self.dimensionodata['Hierarchies'][0]['ElementAttributes']

    #TODO:
    def get_odata_elements_in_list(self):
        #data = [[i['Attributes']['Caption'], i['Attributes']['Name']] for i in self.odata['Hierarchies'][0]['Elements']]
        return self.odata['Hierarchies'][0]['Elements']


