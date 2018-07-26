import json
import collections
import pprint

#TODO: Few things needs to be modified. Put frequency and start time in a class or method
class ProcessParameter:
    def __init__(self, Name, Value):
        self.Name = Name
        self.Value = Value

    @classmethod
    def get_from_dict(cls, parameter_dict):
        return cls(Name = parameter_dict['Name'],
                   Value = parameter_dict['Value'])

    def as_dict(self):
        return {'Name': self.Name, 'Value': self.Value}


class ChoreTask:
    def __init__(self, step, processname, parameters):
        self.step = step
        self.processname = processname
        self.parameters = parameters

    def create_body(self):
        body_as_dict = collections.OrderedDict()
        body_as_dict['Step'] = self.step
        body_as_dict['Process@odata.bind'] = "Processes('{}')".format(self.processname)
        body_as_dict['Parameters'] = [prm.as_dict() for prm in self.parameters]

        return dict(body_as_dict)

    def as_dict(self):
        return self.create_body()


class Chore:
    def __init__(self, Name, StartTime, DSTSensitive, Active, Frequency, ExecutionMode, ChoreTasks):
        self.Name = Name
        self.StartTime = StartTime
        self.DSTSensitive = DSTSensitive
        self.Active = Active
        self.ExecutionMode = ExecutionMode
        self.Frequency = Frequency
        self.ChoreTasks = ChoreTasks

    @classmethod
    def get_from_dict(cls, chore_dict):
        return cls(Name = chore_dict['Name'],
                   StartTime = chore_dict['StartTime'],
                   DSTSensitive = chore_dict['DSTSensitive'],
                   Active = chore_dict['Active'],
                   Frequency = chore_dict['Frequency'],
                   ExecutionMode=chore_dict['ExecutionMode'],
                   ChoreTasks = chore_dict['Tasks'])

    def create_body(self):
        body_as_dict = collections.OrderedDict()
        body_as_dict['Name'] = self.Name
        body_as_dict['StartTime'] = self.StartTime
        body_as_dict['DSTSensitive'] = self.DSTSensitive
        body_as_dict['Active'] = self.Active
        body_as_dict['Frequency'] = self.Frequency
        body_as_dict['ExecutionMode'] = self.ExecutionMode
        body_as_dict['Tasks'] = [ctm.as_dict() for ctm in self.ChoreTasks]

        return dict(body_as_dict)

    def as_dict(self):
        return self.create_body()

