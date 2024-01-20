

IS_EXECUTION_CORE=True

#if IS_EXECUTION_CORE:
#    from src.core.variable_handler import variable_handler

import json
import pandas as pd
import ast 
import inspect

from typing import Dict, Set, Any
from dataclasses import dataclass, field

import forloop_modules.flog as flog

#from src.df_column_category_predictor import classify_df_column_categories, DataFrameColumnCategoryAnalysis

from forloop_modules.utils.pickle_serializer import save_data_dict_to_pickle_folder
from forloop_modules.utils.pickle_serializer import load_data_dict_from_pickle_folder
from forloop_modules.globals.active_entity_tracker import aet
from forloop_modules.redis.redis_connection import kv_redis
from forloop_modules.utils.definitions import JSON_SERIALIZABLE_TYPES, JSON_SERIALIZABLE_TYPES_AS_STRINGS, REDIS_STORED_TYPES, REDIS_STORED_TYPES_AS_STRINGS
#import src.forloop_code_eval as fce
import forloop_modules.queries.node_context_requests_backend as ncrb

@dataclass
class File:
    path: str = ""
    file_name: str=""
    # suffix: str=""
    data: Any=None

    def to_dict(self):
        return {"path": self.path, "file_name": self.file_name, "data": self.data}  # , "suffix": self.suffix


@dataclass
class DataFrameWizardScanAnalysis:
    is_analyzed: bool = False
    empty_rows: Set[int] = field(default_factory=set)
    duplicated_rows: Set[int] = field(default_factory=set)
    empty_columns: Set[str] = field(default_factory=set)
    id_columns: Set[str] = field(default_factory=set)
    result: Dict = field(default_factory=dict)

    
class LocalVariableHandler:
    def __init__(self):
        self.is_refresh_needed = False  # When VariableHandler gets set with a button, this is toggled to True - Frontend then can react to state changes
        self.last_dataframe = None  # stores DF, not variable name, this is temporary - should be replaced with self.last_active_df_variable but carefully - the latter one stores variable not DF
        self.last_active_df_variable = None  # is assigned when df or cleaning icon selected
        self._last_active_dataframe_node_uid = None
        self.dataframe_scan_analyses_records: Dict[str, DataFrameWizardScanAnalysis] = dict()
        self.dataframe_column_category_predictions: Dict[str, Any] = dict() #Dict[str, DataFrameColumnCategoryAnalysis]
        self.variables_to_be_created_in_subpipeline = []
        self.variables={}
        self.variable_uid_variable_dict={} #ANALOGY of dicts in GLC, new implementation - contains nodes in API -> reflecting status of server nodes via API
        
    @property
    def is_empty(self):
        return len(self.variables) == 0

     
    def _set_up_unique_varname(self, name: str) -> str:
        i = 2

        if not name:
            name = 'untitled1'
            # If untitled_i already exists -> try untitled_i+1
            while self._is_varname_duplicated(name):
                name = f'untitled{i}'
                i += 1
        elif " " in name:
            name = "_".join(name.split())
        
        return name

    def _is_varname_duplicated(self, name: str) -> bool:
        # names = [x.value for x in self.variables.values()]#self.stored_variable_df['Name'].tolist()  # All current variables' names
        names = list(self.variables.keys())
        checker = name in names
        return checker
     
    def get_variable_by_name(self, name):
        """new function because of serialization"""
        variable = self.variables.get(name)
        #TODO: Get request from API
    
        if variable is None:
            flog.warning(f"A variable '{name}' was not found in LocalVariableHandler.")
            return
  
        #serialization for objects
        if variable.typ in REDIS_STORED_TYPES_AS_STRINGS:
            value = kv_redis.get("stored_variable_" + variable.name)
            value.attrs["name"] = variable.name

            response = ncrb.get_variable_by_name(variable.name)
            result = json.loads(response.content)
            uid = result["uid"]
            is_result = result["is_result"]
            
            variable = LocalVariable(uid, variable.name, value, is_result)
            return(variable)
        else:
            return(variable)
        
    def get_int_to_str_col_name_mapping(self, df: pd.DataFrame) -> Dict[int, str]:
        """
        find columns whose name type is int and create mapping between their int name and its string form
        :param df:
        :type df:
        :return:
        :rtype:
        """
        int_columns = []
        for column_name in df.columns:
            if isinstance(column_name, int):
                int_columns.append(column_name)

        return {column_name: str(column_name) for column_name in int_columns}

    def new_file(self, path):
        # TODO is temporary until workflow for files is introduced
        name, *suffix = path.split(".")
        suffix = ".".join(suffix)
        name = path.split("/")[-1]
        file = File(path, name)  # suffix
        file_variable = self.create_file(file)
    
    def create_file(self, file: File, project_uid=None):
        # TODO is temporary until workflow for files is introduced

        # TODO: NEVER USED, NOT TESTED (NCRB + LOCAL VARIABLE CALL WITH 4 PARAMETERS INSTEAD OF 2)
        response = ncrb.get_variable_by_name(file.file_name)
        result = json.loads(response.content)
        uid = result["uid"]
        is_result = result["is_result"]

        variable = LocalVariable(uid, file.file_name, file, is_result)

        ncrb.new_file(file.file_name)
        ncrb.upload_urls_from_file(file.path)

        return(variable)
    def process_dataframe_variable_on_initialization(self, name, value):
        self.dataframe_scan_analyses_records[name] = DataFrameWizardScanAnalysis()
        value = value.rename(columns=self.get_int_to_str_col_name_mapping(value))
        # self.dataframe_column_category_predictions[name] = classify_df_column_categories(value)
        value.attrs["name"] = name

        return value

        
    def new_variable(self, name, value, additional_params: dict = None, project_uid=None):
        if additional_params is None:
            additional_params = {}
        
        if project_uid is None:
            project_uid=aet.project_uid
        name = self._set_up_unique_varname(name)

        if isinstance(value, pd.DataFrame):
            value = self.process_dataframe_variable_on_initialization(name, value)
        
        if name in self.variables.keys():
            variable = self.update_variable(name, value, additional_params)
            is_new_variable=False
        else:
            variable=self.create_variable(name, value, additional_params)
            is_new_variable=True
        
            
        return variable, is_new_variable
    
    def is_value_serializable(self, value):
        is_value_serializable = True if type(value) in JSON_SERIALIZABLE_TYPES else False

        return is_value_serializable
    
    def is_value_redis_compatible(self, value):
        is_redis_compatible = type(value) in REDIS_STORED_TYPES or inspect.isfunction(value) or inspect.isclass(value)
        
        return is_redis_compatible
 
    def create_variable(self, name, value, additional_params: dict = None, project_uid=None):
        #self.variable_uid_project_uid_dict[variable.uid]=project_uid #is used in API call
        if additional_params is None:
            additional_params = {}
        
        #serialization for objects
        # TODO: FFS FIXME:
        value_serializable = self.is_value_serializable(value)
        
        if value_serializable:
            response = ncrb.new_variable(name, value)
        else:
            if self.is_value_redis_compatible(value):
                kv_redis.set("stored_variable_" + name, value, additional_params)
            else:
                data_dict={}
                data_dict[name]=value
                folder=".//file_transfer"
                save_data_dict_to_pickle_folder(data_dict,folder,clean_existing_folder=False)
            #TODO: FILE TRANSFER MISSING
            response = ncrb.new_variable(name, "", type=type(value).__name__)
            
        result = response.content.decode('utf-8')
            
        return result
    
    def create_local_variable(self, uid: str, name, value, is_result: bool, type=None):
        if type in JSON_SERIALIZABLE_TYPES_AS_STRINGS and type != "str":
            value=ast.literal_eval(str(value))
        elif type in REDIS_STORED_TYPES_AS_STRINGS:
            value = kv_redis.get("stored_variable_" + name)

            if isinstance(value, pd.DataFrame):
                value = self.process_dataframe_variable_on_initialization(name, value)

        variable=LocalVariable(uid, name, value, is_result) #Create new 
        self.variables[name]=variable
        return(variable)
        
    
    def update_variable(self, name, value, additional_params: dict = None, project_uid=None):
        if additional_params is None:
            additional_params = {}
        #ncrb.update_variable_by_uid(variable_uid, name, value)(name, value)
        
        #TODO - replace by "update_variable_by_name"
        
        response = ncrb.get_variable_by_name(name)
        result = json.loads(response.content)
        if "uid" in result:
            # HOTFIX TOMAS
            variable_uid=result["uid"]
            value_serializable = self.is_value_serializable(value)
            
            if value_serializable:
                response = ncrb.update_variable_by_uid(variable_uid, name, value, result["is_result"])
            else:
                if self.is_value_redis_compatible(value):
                    kv_redis.set("stored_variable_" + name, value, additional_params)
                else:
                    data_dict={}
                    data_dict[name]=value
                    folder=".//file_transfer"
                    save_data_dict_to_pickle_folder(data_dict,folder,clean_existing_folder=False)
                response = ncrb.update_variable_by_uid(variable_uid, name, "", is_result=result["is_result"], type=type(value).__name__)
            
            result = response.content.decode('utf-8')
            
        return result
        
        #else:
        #    self.variables.pop(name)
        #    self.create_variable(name, value)
            
        #variable=self.variables[name]
        #self.variables[name].value=value #Update
        #return(variable)
    
    def update_local_variable(self, name, value, is_result: bool, type=None):
        if type in JSON_SERIALIZABLE_TYPES_AS_STRINGS and type != "str":
            value=ast.literal_eval(str(value))
        elif type in REDIS_STORED_TYPES_AS_STRINGS:
            value = kv_redis.get("stored_variable_" + name)
        
        variable=self.variables[name]
        self.variables[name].value=value #Update
        self.variables[name].is_result = is_result #Update

        return(variable)
        
    def delete_variable(self, var_name: str):
        if self.last_active_df_variable is not None and var_name == self.last_active_df_variable.name:
            self.last_active_df_variable = None
            
        response=ncrb.get_variable_by_name(var_name)
        results=json.loads(response.content)
        variable_uid=results["uid"]
        response=ncrb.delete_variable_by_uid(variable_uid)
        self.delete_local_variable(var_name)
        
        
    def delete_local_variable(self, var_name:str):
        self.variables.pop(var_name)
    
    
    @property
    def last_active_dataframe_node_uid(self):
        return self._last_active_dataframe_node_uid
    
    # temporary until cyclic import of ncrb in cleaning handlers is resolved
    @last_active_dataframe_node_uid.setter
    def last_active_dataframe_node_uid(self, node_uid:int):
        self._last_active_dataframe_node_uid = node_uid
    
    #   TODO: fix dependencies
    #def update_data_in_variable_explorer(self, glc): #TODO Dominik: Refactor out, shouldnt be here
    #    self.is_refresh_needed = False
    #    if hasattr(glc, "variable_explorer"):
            
    #        glc.variable_explorer.update_data(self.stored_variable_df)

        # stored_variables_list = [[x.name, x.typ, x.size, x.value] for x in self.values()]
        # stored_variable_df = pd.DataFrame(stored_variables_list, columns=["Name", "Type", "Size", "Value"])
        # glc.variable_explorer.update_data(stored_variable_df)


    def populate_df_analysis_record(self, name, empty_rows, duplicated_rows, empty_columns, id_columns, result):
        df_analysis = DataFrameWizardScanAnalysis()
        df_analysis.is_analyzed = True
        df_analysis.empty_rows = empty_rows
        df_analysis.duplicated_rows = duplicated_rows
        df_analysis.empty_columns = empty_columns
        df_analysis.id_columns = id_columns
        df_analysis.result = result

        self.dataframe_scan_analyses_records[name] = df_analysis

    def empty_df_analysis_record(self, name):
        self.dataframe_scan_analyses_records[name] = DataFrameWizardScanAnalysis()

    def df_already_scanned(self, name):
        if name in self.dataframe_scan_analyses_records:
            return self.dataframe_scan_analyses_records[name].is_analyzed
        return False

    # DB Connections
    # TODO: IT IS POSSIBLE TO HAVE DUPLICATE DB NAMES
    def new_database_connection(self, db_connection):
        # TODO: should check whether db connection is valid and raise exception if not -> Dominik: I dont agree
        #assert db_connection.is_valid_db_connection
        self.db_connections.append(db_connection)


    def get_selected_db_connection(self, selected_db_name):
        valid_dbs = {x.database + " (" + x.server + ")": x for x in self.db_connections if hasattr(x, "database")}
        db_connection = valid_dbs.get(selected_db_name, None)

        return db_connection

    def get_db_connection(self, db_name):
        for connection in self.db_connections:
            if connection.database == db_name:
                return connection


class LocalVariable:
    """
    Formerly ForloopStoredVariable - renamed to LocalVariable
    Dfs, Lists, Dicts (JSON) - objects visible and possible to manipulate
    """
    instance_counter = 0

    def __init__(self, uid: str, name: str, value: Any, is_result: bool):
        self.name = name
        self.value = value
        self.is_result = is_result
        self.uid = uid

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'{self.value}'

    @property
    def typ(self):
        return type(self.value).__name__

    @property
    def size(self) -> int:
        try:
            return len(self.value)
        except:
            return 1

    def __len__(self):
        return self.size
