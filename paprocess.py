import collections
import json

class DataSource:
    """ Data source of a TI Process"""
    def __init__(self, Type, dataSourceNameForClient, dataSourceNameForServer, password, query, userName, usesUnicode):
        self.Type = Type
        self.dataSourceNameForClient = dataSourceNameForClient
        self.dataSourceNameForServer = dataSourceNameForServer
        self.__password = password
        self.query = query
        self.userName = userName
        self.usesUnicode = usesUnicode

    def create_body(self):
        body_as_dict = collections.OrderedDict()
        body_as_dict['dataSourceNameForClient'] = self.dataSourceNameForClient
        body_as_dict['dataSourceNameForServer'] = self.dataSourceNameForServer
        body_as_dict['password'] = self.__password
        body_as_dict['query'] = self.query
        body_as_dict['userName'] = self.userName
        body_as_dict['usesUnicode'] = self.usesUnicode

        return dict(body_as_dict)

    def as_dict(self):
        return self.create_body()


class Parameters:
    """ Parameters of a TI Process"""
    def __init__(self):
        self.__titles = []

    def add_body(self, Name, Prompt, Value, Type):
        body_as_dict = collections.OrderedDict()
        body_as_dict.__setitem__('Name', Name)
        body_as_dict.__setitem__('Prompt', Prompt)
        body_as_dict.__setitem__('Value', Value)
        body_as_dict.__setitem__('Type', Type)
        self.__titles.append(body_as_dict)

    def as_list(self):
        return self.__titles


class Variables:
    """Variables of a TI process"""
    def __init__(self):
        self.__titles = []

    def add_body(self, Name, Type, Position, StartByte, EndByte):
        body_as_dict = collections.OrderedDict()
        body_as_dict.__setitem__('Name', Name)
        body_as_dict.__setitem__('Type', Type)
        body_as_dict.__setitem__('Position', Position)
        body_as_dict.__setitem__('StartByte', StartByte)
        body_as_dict.__setitem__('EndByte', EndByte)
        self.__titles.append(body_as_dict)

    def as_list(self):
        return self.__titles


#TODO: what is ui_data?
class TIProcess:
    """TI process"""
    def __init__(self, Name, HasSecurityAccess, PrologProcedure, MetadataProcedure, DataProcedure, EpilogProcedure, DataSource, Parameters, Variables, ui_data = "CubeAction=1511€DataAction=1503€CubeLogChanges=0€"):
        self.Name = Name
        self.HasSecurityAccess = HasSecurityAccess
        self.ui_data = ui_data
        self.PrologProcedure = PrologProcedure
        self.MetadataProcedure = MetadataProcedure
        self.DataProcedure = DataProcedure
        self.EpilogProcedure = EpilogProcedure
        self.DataSource = DataSource
        self.Parameters = Parameters
        self.Variables = Variables
        #self.Attributes = Attributes
        #self.ErrorLogs = ErrorLogs
        #self.LocalizedAttributes = LocalizedAttributes

    @classmethod
    def get_from_dict(cls, data_dict):
        return cls(Name=data_dict['Name'],
                   HasSecurityAccess=data_dict['HasSecurityAccess'],
                   PrologProcedure=data_dict['PrologProcedure'],
                   MetadataProcedure=data_dict['MetadataProcedure'],
                   DataProcedure=data_dict['DataProcedure'],
                   EpilogProcedure=data_dict['EpilogProcedure'],
                   DataSource=data_dict['DataSource'],
                   Parameters=data_dict['Parameters'],
                   Variables=data_dict['Variables']
                   #Attributes=data_dict['Attributes'],
                   #ErrorLogs= data_dict['ErrorLogs'],
                   #LocalizedAttributes = data_dict['LocalizedAttributes']
         )

    def create_body(self):
        body_as_dict = collections.OrderedDict()
        body_as_dict['Name'] = self.Name
        body_as_dict['HasSecurityAccess'] = self.HasSecurityAccess
        body_as_dict['PrologProcedure'] = self.PrologProcedure
        body_as_dict['MetadataProcedure'] = self.MetadataProcedure
        body_as_dict['DataProcedure'] = self.DataProcedure
        body_as_dict['EpilogProcedure'] = self.EpilogProcedure
        body_as_dict['DataSource'] = self.DataSource
        body_as_dict['Parameters'] = self.Parameters if type(self.Parameters) is list else self.Parameters.as_list()
        body_as_dict['Variables'] = self.Variables if type(self.Variables) is list else self.Variables.as_list()
        #body_as_dict['Attributes'] = self.Attributes
        #body_as_dict['ErrorLogs'] = self.ErrorLogs
        #body_as_dict['LocalizedAttributes'] = self.LocalizedAttributes

        return dict(body_as_dict)

    def as_dict(self):
        return self.create_body()

    def as_json(self):
        return json.dumps(self.create_body())








