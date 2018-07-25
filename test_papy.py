# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 16:06:46 2018

@author: MSARAF
"""

# import PaAaPy
from papy import PAlogin, PApy, tm1element
import pprint

import json
from pachore import Chore, ProcessParameter, ChoreTask
from paview import Columns, Rows, Titles, View
from paprocess import *

def LOGIN():
    # DEV2
    login = PAlogin.login_using_cam('A.Cognos.MPT', 'S3RVIC3ADM!N', 'nikeads', 'tm1-plan-ah-dev.edf.nikecloud.net', 30002)
    tm1 = PApy(login)
    return tm1

def example_view_data_in_dict(tm1):
    # Get the view
    tm1view = tm1.get_native_view('Plan_Gross_To_Net', 'zMs_Test2')

    v = tm1view.get_view_data_in_dict()
    pprint.pprint(v)


def example_data_frame(tm1):

    # Get the view
    tm1view = tm1.get_native_view('Plan_Consolidated', 'NA_CONS_G2N Metrics')

    # Publish the view into dataframe
    df = tm1view.publish_into_pandas_dataframe()
    import pandas as pd

    # Create a pivot
    df = pd.pivot_table(df, index=['Metric_Plan_Consolidated', 'Measure_Plan'], columns=['Calendar'], aggfunc='sum',
                        margins=True, values='Data')

    df = df.query('Metric_Plan_Consolidated == "AA Qty"')['BY 2018']

    # 2nd view
    tm1view2 = tm1.get_native_view('Plan_Consolidated', 'zMS.NA_CONS_G2N Metrics.Temp')
    df2 = tm1view2.publish_into_pandas_dataframe()
    df2 = pd.pivot_table(df2, index=['Metric_Plan_Consolidated', 'Measure_Plan'], columns=['Calendar'], aggfunc='sum',
                         margins=True, values='Data')
    df2 = df2.query('Metric_Plan_Consolidated == "AA Qty"')['BY 2018']

    pd.options.display.width = 180
    pprint.pprint(df2)


def example_mdx_view_data_in_dict(tm1):

    data = """{
               "MDX":"SELECT 
            	{
            		([Version].[FCST-A], [Measure_Plan].[Input]),
            		([Version].[FCST-A], [Measure_Plan].[LY])
            	} ON COLUMNS,
                {
                    ([Calendar].[BY 2018], [Planning_Group].[GC], [Product_Rollup].[FOOTWEAR]),
                    ([Calendar].[BY 2018], [Planning_Group].[GC], [Product_Rollup].[APPAREL]),
                    ([Calendar].[BY 2019], [Planning_Group].[GC], [Product_Rollup].[FOOTWEAR]),
                    ([Calendar].[BY 2019], [Planning_Group].[GC_CHINA],[Product_Rollup].[FOOTWEAR]), 
                    ([Calendar].[BY 2019], [Planning_Group].[GC], [Product_Rollup].[APPAREL]),
                    ([Calendar].[BY 2019], [Planning_Group].[NA], [Product_Rollup].[APPAREL])
                }  ON ROWS FROM [Plan_Gross_To_Net]
                WHERE ([Currency_Type].[PC],  [Metric_Plan_Gross_To_Net].[AF Whlsl Amt])"
            }"""

    data2 = """{
               "MDX":"SELECT 
            	{
            		([Measure_Sys_Control].[String])
            	} ON COLUMNS,
                {
                    ([Sys_Control].[Booking Season])
                }  ON ROWS FROM [Sys_Control]
                "
            }"""
    # print(data)

    # Get the view
    tm1view = tm1.get_mdx_view('Plan_Gross_To_Net', data2)
    v = tm1view.get_view_data_in_dict()
    pprint.pprint(v)


def test_execute_ti(tm1):
    ti_param = {"Parameters": [ { "Name": "pTestParam1", "Value": "test_from_papy1" }, {"Name": "pTestParam2", "Value": "another test"}] }
    print(tm1.execute_ti('zms_test3', ti_param))

#TODO - working
def test_get_dimension_hierarchies(tm1):
    x1 = tm1.activate_chore()
    print(x1)

def test_create_chore_1(tm1):
    data1 = {
            "Name": "myChore",
            "StartTime": "2012-07-27T23:03:00-04:00",
            "Frequency": "P223DT10H12M23S",
            "ExecutionMode": "MultipleCommit",
            "Tasks": [
                {
                    "Process@odata.bind": "Processes('data.Stage.Planning_Group_Map.Week.Wrapper')",
                    "Parameters": [
                        {
                            "Name": "pPeriod",
                            "Value": "201401"
                        },
                        {
                            "Name": "pSysCycle",
                            "Value": ""
                        }
                    ]
                },
                {
                    "Process@odata.bind": "Processes('Dim.Update.Stage_Planning_Group_Product_Rollup.Wrapper')",
                    "Parameters": [
                        {
                            "Name": "pSysCycle",
                            "Value": ""
                        }
                    ]
                }
            ]
        }

    json_data = json.dumps(data1)
    print(json_data)
    a = tm1.create_chore('abx', json_data)

#TODO: Few things needs to be modified. Put frequency and start time in a class or method
def test_create_chore_2(tm1):
    param1 = ProcessParameter("pPeriod", "201401")
    param2 = ProcessParameter("pSysCycle", "")

    ct = ChoreTask(1, "data.Stage.Planning_Group_Map.Week.Wrapper", [param1, param2])

    chore_data = Chore("myChore", "2012-07-27T23:03:00-04:00", False, False, "P223DT10H12M23S", "MultipleCommit", [ct])
    json_data = json.dumps(chore_data.as_dict())
    print(json_data)
    a = tm1.create_chore(json_data)

# Working - fine
def test_create_view(tm1):
    row = Rows()
    row.add_body('Metric_Plan_Gross_To_Net', 'G2N Metrics')
    row.add_body('Measure_Plan', 'Default')

    col = Columns()
    col.add_body('Calendar', 'Calendar')

    title = Titles()
    title.add_body('Planning_Group', 'Default', 'TRAINING PG')
    title.add_body('Product_Rollup', 'Default', 'DIVISION')
    title.add_body('Version', 'Default', 'Fcst-A')
    title.add_body('Currency_Type', 'Default', 'PC')

    view = View('MyView-REST API', col.as_list(), row.as_list(), title.as_list(), True, True, r'0.#########\fG|0|')

    #print(view.as_json())

    res = tm1.create_view('Plan_Gross_To_Net', view)
    print(res.text)

def test_delete_view(tm1):
    res = tm1.delete_view('Plan_Gross_To_Net', 'MyView-REST API')
    print(res)

def test_get_ti_process(tm1):
    ti = tm1.get_ti_process('data.load.FX_Rate')
    ti_obj = TIProcess.get_from_dict(ti)
    print(ti_obj.PrologProcedure)

def test_create_ti_process(tm1):
    ti_odata_dict = tm1.get_ti_process('data.load.FX_Rate')
    ti_obj = TIProcess.get_from_dict(ti_odata_dict)
    res = tm1.create_ti_process('zms_test_rest', ti_obj.as_json())
    print(res)

def test_update_ti_process(tm1):
    ti_odata_dict = tm1.get_ti_process('data.load.FX_Rate')
    ti_obj = TIProcess.get_from_dict(ti_odata_dict)
    res = tm1.update_ti_process('zms_test_rest', ti_obj.as_json())
    print(res)

def test_copy_ti_process(tm1):
    res = tm1.copy_ti_process('data.load.FX_Rate', 'zms_test_rest')
    print(res)

def test_activate_chore(tm1):
    res = tm1.activate_chore('Sys_Daily_Backup')

def test_cube_cell_write(tm1):
    #working for multi cell
    #working for single cell
    #with open("config_files/sample_cube_input_multiple_cell.json", 'r') as f:
    with open("config_files/sample_cube_input_large_file.json", 'r') as f:
        data = json.loads(f.read())
    response = tm1.cube_cells_write('zMS_Temp_G2N', data)
    print(response)


# MAIN Function for Test
if __name__ == "__main__":
    tm1 = LOGIN()

    test_cube_cell_write(tm1)

    tm1.logout()