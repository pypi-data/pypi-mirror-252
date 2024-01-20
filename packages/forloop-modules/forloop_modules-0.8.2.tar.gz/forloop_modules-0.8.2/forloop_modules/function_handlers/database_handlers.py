from deepdiff import DeepDiff
from tkinter.filedialog import askopenfile
from typing import List, Tuple
import json

import ast
import pandas as pd
import dbhydra.dbhydra_core as dh
from fastapi import HTTPException

import forloop_modules.flog as flog
import forloop_modules.queries.node_context_requests_backend as ncrb

from forloop_modules.function_handlers.auxilliary.node_type_categories_manager import ntcm
from forloop_modules.function_handlers.auxilliary.form_dict_list import FormDictList
from forloop_modules.globals.variable_handler import variable_handler
from forloop_modules.globals.database_utilities_handler import duh
from forloop_modules.globals.docs_categories import DocsCategories

from forloop_modules.function_handlers.auxilliary.abstract_function_handler import AbstractFunctionHandler
from forloop_modules.function_handlers.auxilliary.data_types_validation import validate_input_data_types

# ###### PROBLEMATIC IMPORTS TODO: REFACTOR #######
#from src.gui.gui_layout_context import glc
# ###### PROBLEMATIC IMPORTS TODO: REFACTOR #######


def get_connected_db_tables(db_name:str=None):
    """
    Retrieves all valid tables from the specified database or all databases if no database name is given.

    Args:
        db_name (str, optional): The name of the database to retrieve tables from.
        If not specified, tables from all connected databases will be retrieved.

    Returns:
        dict: A dictionary where keys are database names and values are dictionaries
        containing valid tables within the respective databases.
    """
    if db_name: #this if was not existing in tobias3 branch - There was merge conflict. Tobias, please erase this comment if this is correctly merged
        connected_dbs = []
        for db_connection in duh.db_connections:
            if hasattr(db_connection, "table_dict") and db_connection.database == db_name:
                connected_dbs.append(db_connection)

    else:
      
        connected_dbs = [db_connection for db_connection in duh.db_connections if hasattr(db_connection, "table_dict")]
        #connected_dbs = [db_connection for db_connection in variable_handler.db_connections if hasattr(db_connection, "table_dict")]

    valid_tables = {}
    for db in connected_dbs:
        valid_tables.update(db.table_dict)

    return valid_tables


def get_connected_db_table_names():
    valid_tables = get_connected_db_tables()
    valid_table_names = list(valid_tables.keys())

    return valid_table_names


def get_name_matching_db_tables(dbtable_name, db_name=None):
    # matching_dbtables = [db_table for name, db_table in get_connected_db_tables().items() if name == dbtable_name]
    matching_dbtables = []
    for name, dbtable in get_connected_db_tables(db_name).items():
        if name == dbtable_name:
            matching_dbtables.append(dbtable)

    return matching_dbtables


class DBQueryHandler(AbstractFunctionHandler):
    def __init__(self):
        self.icon_type = "DBQuery"
        self.fn_name = "DB Query"

        self.type_category = ntcm.categories.database
        self.docs_category = DocsCategories.data_sources


    def make_form_dict_list(self, *args, options=None, node_detail_form=None):
        db_tables = get_connected_db_table_names()

        fdl = FormDictList()
        fdl.label(self.fn_name)
        fdl.label("DB table name")
        fdl.comboentry(name="db_table_name", text="", options=db_tables, row=1)
        fdl.label("Query")
        fdl.entry(name="query", text="", input_types=["str"], row=2)
        fdl.label("Specify new variable name with SELECT query")
        fdl.label("New variable")
        fdl.entry(name="new_var_name", text="", category="new_var", input_types=["str"], row=4)
        fdl.button(function=self.execute, function_args=node_detail_form, text="Execute", focused=True)

        return fdl

    def debug(self, dbtable_name, query, new_var_name):
        flog.debug("DB Query")
        flog.debug(f"DB Table Name = {dbtable_name}")
        flog.debug(f"QUERY = {query}")
        flog.debug(f"NEW VAR NAME = {new_var_name}")

    def parse_input(self, dbtable_name: str) -> str:
        return dbtable_name[0] if len(dbtable_name) > 0 else ""

    def direct_execute(self, dbtable_name, query, new_var_name):
        self.debug(dbtable_name, query, new_var_name)
        dbtable_name = self.parse_input(dbtable_name)

        if dbtable_name:
            matching_dbtables = get_name_matching_db_tables(dbtable_name)

            if len(matching_dbtables) == 1:
                dbtable = matching_dbtables[0]
                db_instance = dbtable.db1

                with db_instance.connect_to_db():
                    flog.info(f"Qeury: {query}")
                    flog.info(f'FIRST Query word altered: {query.split(" ")[0].lower().strip()}')
                    if query.split(" ")[0].lower().strip() == "select":
                        # Hotfix for the df Image to show a proper label
                        # TODO Daniel/Tomas: Refactor out
                        new_var_name = variable_handler._set_up_unique_varname(new_var_name)
                        fields = self.generate_shown_dataframe_option_field(new_var_name)   
                        
                        response = ncrb.new_node(pos=[500, 300], typ="DataFrame", fields=fields)
                        if response.status_code in [200, 201]:
                            result = json.loads(response.content.decode('utf-8'))
                            node_uid = result["uid"]

                            try:
                                rows = dbtable.select(query)
                            except Exception as e:
                                flog.error(f"DBTABLE SELECT ERROR {e}")

                            df_new = pd.DataFrame(rows,columns=dbtable.columns)
                            flog.info(f"DF: {df_new}")

                            df_new = validate_input_data_types(df_new)
                            variable_handler.new_variable(new_var_name, df_new)

                            ncrb.update_last_active_dataframe_node_uid(node_uid)
                        else:
                            raise HTTPException(status_code=response.status_code, detail="Error requesting new node from api")
                    else:
                        try:
                            dbtable.db1.execute(query)
                        except Exception as e:
                            flog.error(f"DBTABLE EXECUTE ERROR {e}")

    def execute(self, node_detail_form):
        db_table_name = node_detail_form.get_chosen_value_by_name("db_table_name", variable_handler)
        query = node_detail_form.get_chosen_value_by_name("query", variable_handler)
        new_var_name = node_detail_form.get_chosen_value_by_name("new_var_name", variable_handler)

        new_var_name = variable_handler._set_up_unique_varname(new_var_name)

        self.direct_execute(db_table_name, query, new_var_name)

    def export_code(self, node_detail_form):
        db_table_name = node_detail_form.get_variable_name_or_input_value_by_element_name("db_table_name")
        query = node_detail_form.get_variable_name_or_input_value_by_element_name("query")
        new_var_name = node_detail_form.get_variable_name_or_input_value_by_element_name("new_var_name", is_input_variable_name=True)

        code = ""

        return code

    def export_imports(self, *args):
        imports = []
        return imports


class DBSelectHandler(AbstractFunctionHandler):
    def __init__(self):
        self.icon_type = "DBSelect"
        self.fn_name = "DB Select"

        self.type_category = ntcm.categories.database
        self.docs_category = DocsCategories.data_sources

    def make_form_dict_list(self, *args, options=None, node_detail_form=None):
        if options is not None:
            databases = options["databases"]
        else:
            databases = []

        operators = ["=", "<", ">", ">=", "<=", "<>", " IN "]
        db_tables = []


        # TODO: Add Distinct checkbox
        fdl = FormDictList()
        fdl.label("DB Select")
        fdl.label("Database")
        databases_names = [database["database_name"] for database in databases]
        fdl.comboentry(name="db_name", text="", options=databases_names, row=1)
        fdl.label("From")
        fdl.comboentry(name="db_table_name", text="", options=db_tables, row=2)
        fdl.label("Select")
        fdl.comboentry(name="select", text="*", options=[], row=3)
        fdl.label("Where")
        fdl.label("Column")
        fdl.comboentry(name="where_column_name", text="", options=[], row=5)
        fdl.label("Operator")
        fdl.combobox(name="where_operator", options=operators, default=operators[0], row=6)
        fdl.label("Value")
        fdl.entry(name="where_value", text="", input_types=["str"], row=7)
        fdl.label("Limit")
        fdl.entry(name="limit", text="", input_types=["str"], row=8)
        fdl.label("New variable")
        fdl.entry(name="new_var_name", text="", category="new_var", input_types=["str"], row=9)
        fdl.button(function=self.execute, function_args=node_detail_form, text="Execute", focused=True)

        return fdl


    def debug(self, dbtable_name, select, column_name, operator, value, limit, new_var_name):
        flog.debug("DB Select")
        flog.debug(f"DB Table Name = {dbtable_name}")
        flog.debug(f"SELECT = {select}")
        flog.debug(f"where_column_name = {column_name}")
        flog.debug(f"where_operator = {operator}")
        flog.debug(f"where_value = {value}")
        flog.debug(f"LIMIT = {limit}")
        flog.debug(f"NEW VAR NAME = {new_var_name}")

    def parse_input(self, dbtable_name: List[str], select: List[str]) -> Tuple[str, str]:
        if len(dbtable_name) > 0:
            dbtable_name = dbtable_name[0]
        else:
            dbtable_name = ""

        if len(select) > 0:
            select = select[0]
        else:
            select = "*"

        return dbtable_name, select

    def select(self, db_instance, dbtable, query, cols_to_be_selected):
        if type(db_instance) is dh.MongoDb:
            dbtable.update_collection()
            resp = dbtable.select(query, cols_to_be_selected)
            resp_df = pd.DataFrame(list(resp))
            resp_df_without_id_column = resp_df.drop(columns=['_id'])
            return resp_df_without_id_column
        elif type(db_instance) is dh.BigQueryDb:
            rows = dbtable.select(query)
            df_new = rows.to_dataframe()
            return df_new
        else:
            # TODO: PROBABLY RETURNS ID COLUMNS AS WELL
            rows = dbtable.select(query)
            df_new = pd.DataFrame(rows, columns=dbtable.columns)
            return df_new

    def _get_query(self, db_instance, dbtable_name, cols_to_be_selected, column_name, value, operator, limit):
        value = parse_float_db(db_instance, value)

        if type(db_instance) is dh.MongoDb:
            query = get_condition_mongo(column_name, value, operator)
        elif type(db_instance) is dh.BigQueryDb:
            query = generate_sql_condition(cols_to_be_selected, dbtable_name, column_name, value, operator, limit, db_instance.dataset)
        else:
            query = generate_sql_condition(cols_to_be_selected, dbtable_name, column_name, value, operator, limit)

        return query

    def _get_df(self, cols_to_be_selected, dbtable_name, db_instance, dbtable, column_name, operator, value, limit):
        query = self._get_query(db_instance, dbtable_name, cols_to_be_selected, column_name, value, operator, limit)

        with db_instance.connect_to_db():
            try:
                df = self.select(db_instance, dbtable, query, cols_to_be_selected)
            except Exception as e:
                flog.error("DBTABLE SELECT ERROR")
                df = pd.DataFrame()

        return df

    # def _get_mongo_df(self, db_instance, dbtable, column_name, operator, value, limit):
    #
    #     condition = get_condition_mongo(column_name, value, operator)
    #
    #     with db_instance.connect_to_db():
    #         try:
    #             dbtable.update_collection()
    #             resp = dbtable.select(condition)
    #             resp_df = pd.DataFrame(list(resp))
    #             resp_df_without_id_column = resp_df.drop(columns=['_id'])
    #             return resp_df_without_id_column
    #         except Exception as e:
    #             flog.error("DBTABLE SELECT ERROR")
    #             return pd.DataFrame()
    #
    # def _get_sql_df(self, cols_to_be_selected, dbtable_name, db_instance, dbtable, column_name, operator, value, limit):
    #
    #     condition = get_condition_sql(cols_to_be_selected, dbtable_name, column_name, value, operator, limit)
    #     flog.debug(condition)
    #
    #     with db_instance.connect_to_db():
    #         try:
    #             rows = dbtable.select(condition)
    #         except Exception as e:
    #             flog.error(f"DBTABLE SELECT ERROR {e}")
    #
    #     if rows:
    #         return pd.DataFrame(rows, columns=dbtable.columns)
    #     else:
    #         return pd.DataFrame(columns=dbtable.columns)

    def direct_execute(self, db_name, dbtable_name, selected_columns, column_name, operator, value, limit, new_var_name):
        self.debug(dbtable_name, selected_columns, column_name, operator, value, limit, new_var_name)
        dbtable_name, selected_columns = self.parse_input(dbtable_name, selected_columns)

        df_new = pd.DataFrame()

        if dbtable_name:
            matching_dbtables = get_name_matching_db_tables(dbtable_name, db_name)

            if len(matching_dbtables) == 1:
                dbtable = matching_dbtables[0]
                db_instance = dbtable.db1

                df_new = self._get_df(selected_columns, dbtable_name, db_instance, dbtable, column_name, operator,
                                      value, limit)

                df_new = validate_input_data_types(df_new)
                variable_handler.new_variable(new_var_name, df_new)
                #variable_handler.update_data_in_variable_explorer(glc)

    def execute_with_params(self, params):
        db_table_name = params["db_table_name"]
        select = params["select"]
        where_column_name = params["where_column_name"]
        where_operator = params["where_operator"]
        where_value = params["where_value"]
        limit = params["limit"]
        new_var_name = params["new_var_name"]

        self.direct_execute(db_table_name, select, where_column_name, where_operator, where_value, limit, new_var_name)

    def execute(self, node_detail_form):
        db_name = node_detail_form.get_chosen_value_by_name("db_name", variable_handler)[0]
        db_table_name = node_detail_form.get_chosen_value_by_name("db_table_name", variable_handler)
        select = node_detail_form.get_chosen_value_by_name("select", variable_handler)
        where_column_name = node_detail_form.get_chosen_value_by_name("where_column_name", variable_handler)
        where_operator = node_detail_form.get_chosen_value_by_name("where_operator", variable_handler)
        where_value = node_detail_form.get_chosen_value_by_name("where_value", variable_handler)
        limit = node_detail_form.get_chosen_value_by_name("limit", variable_handler)
        new_var_name = node_detail_form.get_chosen_value_by_name("new_var_name", variable_handler)

        new_var_name = variable_handler._set_up_unique_varname(new_var_name)
        fields = self.generate_shown_dataframe_option_field(new_var_name)

        response = ncrb.new_node(pos=[500, 300], typ="DataFrame", fields=fields)
        if response.status_code in [200, 201]:
            result = json.loads(response.content.decode('utf-8'))
            node_uid = result["uid"]

            self.direct_execute(db_name, db_table_name, select, where_column_name, where_operator, where_value, limit, new_var_name)

            ncrb.update_last_active_dataframe_node_uid(node_uid)
        else:
            raise HTTPException(status_code=response.status_code, detail="Error requesting new node from api")

    def export_code(self, node_detail_form):
        db_table_name = node_detail_form.get_chosen_value_by_name("db_table_name")
        select = node_detail_form.get_chosen_value_by_name("select")
        where_column_name = node_detail_form.get_chosen_value_by_name("where_column_name")
        where_operator = node_detail_form.get_chosen_value_by_name("where_operator")
        where_value = node_detail_form.get_variable_name_or_input_value_by_element_name("where_value")
        limit = node_detail_form.get_variable_name_or_input_value_by_element_name("limit")
        new_var_name = node_detail_form.get_variable_name_or_input_value_by_element_name("new_var_name", is_input_variable_name=True)

        code = """
        df = glc.tables.elements[0].df


        matching_dbtables = [x for x in glc.dbtables if x.name == {db_table_name}]

        if len(matching_dbtables) == 1:
            dbtable = matching_dbtables[0]
            print(dbtable,dbtable.name)
            db_instance=dbtable.db_connection.db_instance
            db_instance.connect_remotely() #TODO
            dh_table = dbtable.db_connection.table_dict[dbtable.name]
            #print(dh_table.columns)
            #print(data_transformation.transformed_df.columns)
            #print(len(dh_table.columns))
            #print(len(data_transformation.transformed_df.columns))
            #print(len(data_transformation.transformed_df.iloc[0,2:]))
            #print(len(pd.DataFrame(data_transformation.transformed_df.iloc[0,2:])))
            index=0
            print(df.columns,len(df.columns))
            print(dh_table.columns,len(dh_table.columns))
            print(df.iloc[index,0:].to_frame().T)
            dh_table.insert_from_df(df.iloc[index,0:].to_frame().T)
            db_instance.close_connection()
        """

        return code.format(db_table_name='"' + db_table_name + '"')

    def export_imports(self, *args):
        imports = ["from gui_layout_context import glc"]
        return imports


class DBInsertHandler(AbstractFunctionHandler):
    def __init__(self):
        self.icon_type = "DBInsert"
        self.fn_name = "DB Insert"

        self.type_category = ntcm.categories.database
        self.docs_category = DocsCategories.data_sources

    def make_form_dict_list(self, *args, options=None, node_detail_form=None):
        db_tables = []
        if options is not None:
            databases = options["databases"]
        else:
            databases = []

        fdl = FormDictList()
        fdl.label(self.fn_name)
        fdl.label("Database")
        databases_names = [database["database_name"] for database in databases]
        fdl.comboentry(name="db_name", text="", options=databases_names, row=1)
        fdl.label("Table name")
        fdl.comboentry(name="db_table_name", text="", options=db_tables, row=2)
        fdl.label("Inserted Data")
        fdl.entry(name="inserted_dataframe", text="", input_types=["list", "dict", "DataFrame"], row=3)
        fdl.button(function=self.execute, function_args=node_detail_form, text="Execute", focused=True)


        return fdl

    def debug(self, dbtable_name, inserted_dataframe):
        flog.debug("DB Insert")
        flog.debug(f"DB Table Name = {dbtable_name}")
        flog.debug(f"DF = {inserted_dataframe}")

    def parse_input(self, dbtable_name: str) -> str:
        return dbtable_name[0] if len(dbtable_name) > 0 else ""

    def _convert_data_variable_to_df(self, inserted_data, columns):
        converted_inserted_dataframe = inserted_data
        if isinstance(inserted_data, list):
            if all(isinstance(el, list) for el in inserted_data): #list of lists
                converted_inserted_dataframe = pd.DataFrame(inserted_data, columns=columns[1:])
            else:
                converted_inserted_dataframe = pd.DataFrame([inserted_data], columns=columns[1:])

        elif isinstance(inserted_data, dict):
            converted_inserted_dataframe = pd.DataFrame.from_dict(converted_inserted_dataframe)

        return converted_inserted_dataframe

    def direct_execute(self, db_name, dbtable_name, inserted_dataframe):


        self.debug(dbtable_name, inserted_dataframe)
        dbtable_name = self.parse_input(dbtable_name)

        if dbtable_name:
            matching_dbtables = get_name_matching_db_tables(dbtable_name, db_name)

            if len(matching_dbtables) == 1:
                dbtable = matching_dbtables[0]
                db_instance = dbtable.db1

                if type(dbtable) is dh.MongoTable:
                    cols = None
                else:
                    cols = dbtable.columns

                try:
                    inserted_dataframe = self._convert_data_variable_to_df(inserted_dataframe, cols)
                except ValueError:
                    #glc.show_warning_popup_message('Wrong number of columns')
                    flog.error('Wrong number of columns',self)
                    return

                connect_to_db_and_run_operation("INSERT", db_instance, dbtable, inserted_dataframe=inserted_dataframe)




                    # TEMPORARY DISABLED
                    # var_name = f"{dbtable.db_connection.database}.{dbtable.name}"
                    # update forloop variable if db table downloaded in platform
                    # if var_name in variable_handler.variables:
                    #     df = dh_table.select_to_df()

                # TEMPORARY DISABLED
                # if len(df) > 0:
                #     variable_handler.new_variable(var_name, df)
                #     #variable_handler.update_data_in_variable_explorer(glc)
                #     glc.last_active_dataframe_icon = df_image  # needs to be after update node detail form (ask Tom) and after variable handler update
                #     check if correct before uncommenting
                #     variable_handler.last_active_dataframe_node_uid = node_detail_form.node_uid


    def execute(self, node_detail_form):
        db_name = node_detail_form.get_chosen_value_by_name("db_name", variable_handler)[0]
        db_table_name = node_detail_form.get_chosen_value_by_name("db_table_name", variable_handler)
        inserted_dataframe = node_detail_form.get_chosen_value_by_name("inserted_dataframe", variable_handler)

        self.direct_execute(db_name, db_table_name, inserted_dataframe)

        # used as data in pipeline_function - processing pipeline
        """
        filename=args[0]
        df=pd.read_excel(filename)
        print("DF",df)
        with open("excel.pickle", 'wb') as pickle_file:
            pickle.dump(df,pickle_file)
        """

    def export_code(self, node_detail_form):
        db_table_name = node_detail_form.get_variable_name_or_input_value_by_element_name("db_table_name")
        inserted_dataframe = node_detail_form.get_variable_name_or_input_value_by_element_name("inserted_dataframe")

        code = """
        df = glc.tables.elements[0].df


        matching_dbtables = [x for x in glc.dbtables if x.name == {dbtable_name}]

        if len(matching_dbtables) == 1:
            dbtable = matching_dbtables[0]
            print(dbtable,dbtable.name)
            db_instance=dbtable.db_connection.db_instance
            db_instance.connect_remotely() #TODO
            dh_table = dbtable.db_connection.table_dict[dbtable.name]
            #print(dh_table.columns)
            #print(data_transformation.transformed_df.columns)
            #print(len(dh_table.columns))
            #print(len(data_transformation.transformed_df.columns))
            #print(len(data_transformation.transformed_df.iloc[0,2:]))
            #print(len(pd.DataFrame(data_transformation.transformed_df.iloc[0,2:])))
            index=0
            print(df.columns,len(df.columns))
            print(dh_table.columns,len(dh_table.columns))
            print(df.iloc[index,0:].to_frame().T)
            dh_table.insert_from_df(df.iloc[index,0:].to_frame().T)
            db_instance.close_connection()
        """

        return code.format(dbtable_name='"' + db_table_name + '"')

    def export_imports(self, *args):
        imports = ["from gui_layout_context import glc"]
        return imports


class DBDeleteHandler(AbstractFunctionHandler):
    def __init__(self):
        self.icon_type = "DBDelete"
        self.fn_name = "DB Delete"

        self.type_category = ntcm.categories.database
        self.docs_category = DocsCategories.data_sources

    def make_form_dict_list(self, *args, options=None, node_detail_form=None):
        operators = ["=", "<", ">", ">=", "<=", "<>", " IN "]

        if options is not None:
            databases = options["databases"]
        else:
            databases = []
        db_tables = []

        fdl = FormDictList()
        fdl.label("DB Delete")
        fdl.label("Database")
        databases_names = [database["database_name"] for database in databases]
        fdl.comboentry(name="db_name", text="", options=databases_names, row=1)
        fdl.label("From")
        fdl.comboentry(name="db_table_name", text="", options=db_tables, row=2)
        fdl.label("Where")
        fdl.label("Column")
        fdl.comboentry(name="column_name", text="", options=[], row=4)
        fdl.label("Operator")
        fdl.combobox(name="operator", options=operators, default=operators[0], row=5)
        fdl.label("Value")
        fdl.entry(name="value", text="", input_types=["str"], row=6)
        fdl.button(function=self.execute, function_args=node_detail_form, text="Execute", focused=True)

        return fdl

    def debug(self, dbtable_name, column_name, operator, value):
        flog.debug("DB Delete")
        flog.debug(f"DB Table Name = {dbtable_name}")
        flog.debug(f"column_name = {column_name}")
        flog.debug(f"operator = {operator}")
        flog.debug(f"value = {value}")

    def parse_input(self, dbtable_name: str) -> str:
        return dbtable_name[0] if len(dbtable_name) > 0 else ""


    def direct_execute(self, db_name,  dbtable_name, column_name, operator, value):

        self.debug(dbtable_name, column_name, operator, value)
        dbtable_name = self.parse_input(dbtable_name)

        if dbtable_name:
            matching_dbtables = get_name_matching_db_tables(dbtable_name, db_name)

            if len(matching_dbtables) == 1:
                dbtable = matching_dbtables[0]
                db_instance = dbtable.db1

                if type(db_instance) is dh.MongoDb:
                    value = parse_float_mongo(value)
                    where_statement = get_condition_mongo(column_name, value, operator)
                else:
                    value = parse_float_sql(value)
                    where_statement = f"{column_name[0]}{operator}{value}"
                    if where_statement == "*='*'": #delete all data from table -> column_name = ["*"], operator = "=", value = '*'
                        where_statement = None

                connect_to_db_and_run_operation("DELETE", db_instance, dbtable, where_statement=where_statement)


                    # var_name = f"DB.{dbtable.name}"
                    # if var_name in variable_handler.variables:
                    #     df = pd.concat([variable_handler.variables[var_name].value, inserted_dataframe])
                    #     variable_handler.new_variable(var_name, df)
                    #     #variable_handler.update_data_in_variable_explorer(glc)

    def execute(self, node_detail_form):
        db_name = node_detail_form.get_chosen_value_by_name("db_name", variable_handler)[0]
        db_table_name = node_detail_form.get_chosen_value_by_name("db_table_name", variable_handler)
        column_name = node_detail_form.get_chosen_value_by_name("column_name", variable_handler)
        operator = node_detail_form.get_chosen_value_by_name("operator", variable_handler)
        value = node_detail_form.get_chosen_value_by_name("value", variable_handler)

        self.direct_execute(db_name, db_table_name, column_name, operator, value)

    def export_code(self, node_detail_form):
        db_table_name = node_detail_form.get_variable_name_or_input_value_by_element_name("db_table_name")
        column_name = node_detail_form.get_variable_name_or_input_value_by_element_name("column_name")
        operator = node_detail_form.get_variable_name_or_input_value_by_element_name("operator")
        value = node_detail_form.get_variable_name_or_input_value_by_element_name("value")

    def export_imports(self, *args):
        pass


class DBUpdateHandler(AbstractFunctionHandler):
    def __init__(self):
        self.icon_type = "DBUpdate"
        self.fn_name = "DB Update"

        self.type_category = ntcm.categories.database
        self.docs_category = DocsCategories.data_sources

    def make_form_dict_list(self, *args, options=None, node_detail_form=None):
        operators = ["=", "<", ">", ">=", "<=", "<>", " IN "]
        if options is not None:
            databases = options["databases"]
        else:
            databases = []

        db_tables = []

        fdl = FormDictList()
        fdl.label("DB Update")
        fdl.label("Database")
        databases_names = [database["database_name"] for database in databases]
        fdl.comboentry(name="db_name", text="", options=databases_names, row=1)
        fdl.label("Table name")
        fdl.comboentry(name="db_table_name", text="", options=db_tables, row=2)
        fdl.label("Set")
        fdl.label("Column")
        fdl.comboentry(name="set_column_name", text="", options=[], row=4)
        fdl.label("Value")
        fdl.entry(name="set_value", text="", input_types=["str"], row=5)
        fdl.label("Where")
        fdl.label("Column")
        fdl.comboentry(name="where_column_name", text="", options=[], row=7)
        fdl.label("Operator")
        fdl.combobox(name="where_operator", options=operators, default=operators[0], row=8)
        fdl.label("Value")
        fdl.entry(name="where_value", text="", input_types=["str"], row=9)
        fdl.button(function=self.execute, function_args=node_detail_form, text="Execute", focused=True)

        return fdl

    def debug(self, dbtable_name, set_column_name, set_value, where_column_name, where_operator, where_value):
        flog.debug("DB Update")
        flog.debug(f"DB Table Name = {dbtable_name}")
        flog.debug(f"set_column_name = {set_column_name}")
        flog.debug(f"set_value = {set_value}")
        flog.debug(f"where_column_name = {where_column_name}")
        flog.debug(f"where_operator = {where_operator}")
        flog.debug(f"where_value = {where_value}")

    def parse_input(self, dbtable_name: str) -> str:
        return dbtable_name[0] if len(dbtable_name) > 0 else ""

    def _get_mongo_update_statements(self, db_instance, dbtable, set_value, set_column_name, where_value, where_column_name, where_operator):
        set_value = parse_float_sql(set_value)

        set_statement = {"$set": {set_column_name[0]: set_value}}

        where_statement = get_condition_mongo(where_column_name, where_value, where_operator)

        return set_statement, where_statement

    def _get_sql_update_statements(self, db_instance, dbtable, set_value, set_column_name, where_value, where_column_name, where_operator):
        set_value = parse_float_sql(set_value)
        set_statement = f"{set_column_name[0]}={set_value}"

        where_value = parse_float_sql(where_value)
        where_statement = f"{where_column_name[0]}{where_operator}{where_value}"

        return set_statement, where_statement


    def direct_execute(self, db_name, dbtable_name, set_column_name, set_value, where_column_name, where_operator, where_value):
        self.debug(dbtable_name, set_column_name, set_value, where_column_name, where_operator, where_value)
        dbtable_name = self.parse_input(dbtable_name)

        if dbtable_name:
            matching_dbtables = get_name_matching_db_tables(dbtable_name, db_name)

            if len(matching_dbtables) == 1:
                dbtable = matching_dbtables[0]
                db_instance = dbtable.db1


                if type(db_instance) is dh.MongoDb:
                    set_statement,where_statement = self._get_mongo_update_statements(db_instance, dbtable, set_value, set_column_name, where_value, where_column_name, where_operator)

                else:
                    set_statement,where_statement = self._get_sql_update_statements(db_instance, dbtable, set_value, set_column_name, where_value, where_column_name, where_operator)

                connect_to_db_and_run_operation("UPDATE", db_instance, dbtable, set_statement=set_statement, where_statement=where_statement)

                    # var_name = f"DB.{dbtable.name}"
                    # if var_name in variable_handler.variables:
                    #     df = pd.concat([variable_handler.variables[var_name].value, inserted_dataframe])
                    #     variable_handler.new_variable(var_name, df)
                    #     #variable_handler.update_data_in_variable_explorer(glc)

    def execute(self, node_detail_form):
        db_name = node_detail_form.get_chosen_value_by_name("db_name", variable_handler)[0]
        db_table_name = node_detail_form.get_chosen_value_by_name("db_table_name", variable_handler)
        set_column_name = node_detail_form.get_chosen_value_by_name("set_column_name", variable_handler)
        set_value = node_detail_form.get_chosen_value_by_name("set_value", variable_handler)
        where_column_name = node_detail_form.get_chosen_value_by_name("where_column_name", variable_handler)
        where_operator = node_detail_form.get_chosen_value_by_name("where_operator", variable_handler)
        where_value = node_detail_form.get_chosen_value_by_name("where_value", variable_handler)

        self.direct_execute(db_name, db_table_name, set_column_name, set_value, where_column_name, where_operator, where_value)

    def export_code(self, node_detail_form):
        db_table_name = node_detail_form.get_variable_name_or_input_value_by_element_name("db_table_name")
        set_column_name = node_detail_form.get_variable_name_or_input_value_by_element_name("set_column_name")
        set_value = node_detail_form.get_variable_name_or_input_value_by_element_name("set_value")
        where_column_name = node_detail_form.get_variable_name_or_input_value_by_element_name("where_column_name")
        where_operator = node_detail_form.get_variable_name_or_input_value_by_element_name("where_operator")
        where_value = node_detail_form.get_variable_name_or_input_value_by_element_name("where_value")

    def export_imports(self, *args):
        pass


class AnalyzeDbTableHandler(AbstractFunctionHandler):
    def __init__(self):
        self.icon_type = 'AnalyzeDbTable'
        self.fn_name = 'Analyze DbTable'

        self.type_category = ntcm.categories.database

    def make_form_dict_list(self, *args, options=None, node_detail_form=None):
        db_tables = []

        if options is not None:
            databases = options["databases"]
        else:
            databases = []

        fdl = FormDictList()
        fdl.label("Analyze DB Table")
        fdl.label("Database")
        databases_names = [database["database_name"] for database in databases]
        fdl.comboentry(name="db_name", text="", options=databases_names, row=1)
        fdl.label("Table name")
        fdl.combobox(name="db_table_name", options=db_tables, multiselect_indices=None, default=" ", row=2)
        fdl.label("New variable:")
        fdl.entry(name="new_var_name", text="", category="new_var", input_types=["str"], row=3)
        fdl.button(function=self.execute, function_args=node_detail_form, text="Execute", focused=True)

        return fdl

    def direct_execute(self,db_name, table_name, new_var_name, dbtable=None):

        if not dbtable:
            matching_dbtables = get_name_matching_db_tables(table_name, db_name)
            if len(matching_dbtables) == 1:
                dbtable = matching_dbtables[0]
            else:
                return

        column_type_pair_dict = dict(zip(dbtable.columns, dbtable.types))

        variable_handler.new_variable(new_var_name, column_type_pair_dict)
        #variable_handler.update_data_in_variable_explorer(glc)

    def execute_with_params(self, params):

        table_name = params["db_table_name"]
        new_var_name = params["new_var_name"]
        flog.info(f'execute table_name = {table_name}')
        self.direct_execute(table_name, new_var_name)

    def execute(self, node_detail_form):
        db_name = node_detail_form.get_chosen_value_by_name("db_name", variable_handler)[0]
        table_name = node_detail_form.get_chosen_value_by_name("db_table_name", variable_handler)
        new_var_name = node_detail_form.get_chosen_value_by_name("new_var_name", variable_handler)

        self.direct_execute(db_name, table_name, new_var_name)

    def export_code(self, node_detail_form):
        table_name = node_detail_form.get_variable_name_or_input_value_by_element_name("db_table_name")
        new_var_name = node_detail_form.get_variable_name_or_input_value_by_element_name("new_var_name", is_input_variable_name=True)

        code = """
        """

        return code

    def export_imports(self, *args):
        imports = []
        return imports

    def make_flpl_node_dict(self, line_dict: dict) -> dict:
        node = {"type": "UseKey",
                "params": {"code_label": {"variable": None, "value": None}}}  # TODO: finish the node var
        return node


class CreateMigrationFileHandler(AbstractFunctionHandler):
    def __init__(self):
        self.icon_type = 'CreateMigrationFile'
        self.fn_name = 'Create Migration File'

        self.type_category = ntcm.categories.database

    def make_form_dict_list(self, *args, options=None, node_detail_form=None):
        db_tables_names = get_connected_db_table_names()
        default_db_table_name = ''
        if db_tables_names:
            default_db_table_name = db_tables_names[0]

        fdl = FormDictList()

        fdl.label("Create Migration File")
        # {"Label": "Table name:", "Entry":{"name":"table_name","text":""})
        fdl.label("Table name")


        fdl.combobox(name="table_name", options=db_tables_names, multiselect_indices=None,
                     default=default_db_table_name, row=1)
        fdl.label("Old structure")
        fdl.label("Dictionary:")
        fdl.entry(name="old_structure_dict", text="", input_types=["dict"], row=3)
        fdl.label("New structure")
        fdl.label("Dictionary:")
        fdl.entry(name="new_structure_dict", text="", input_types=["dict"], row=5)
        fdl.label("Migration file name:")
        fdl.entry(name="filename", text="migration-1", input_types=["str"], row=6)
        fdl.label("Save to json")
        fdl.checkbox("save_to_file", row=7)
        fdl.button(function=self.execute, function_args=node_detail_form, text="Execute", focused=True)
        fdl.button(function=self.open_migration_file, function_args=node_detail_form, text="Prepare to run", name="prepare_migration")

        return fdl

    def open_migration_file(self, node_detail_form):
        response = ncrb.new_node(pos=[500, 300], typ="RunMigrationFile")

    def execute(self, node_detail_form):
        table_name = node_detail_form.get_chosen_value_by_name("table_name", variable_handler)
        old_structure_dict = node_detail_form.get_chosen_value_by_name("old_structure_dict", variable_handler)
        new_structure_dict = node_detail_form.get_chosen_value_by_name("new_structure_dict", variable_handler)
        filename = node_detail_form.get_chosen_value_by_name("filename", variable_handler)
        save_to_file = node_detail_form.get_chosen_value_by_name("save_to_file", variable_handler)

        self.direct_execute(table_name, old_structure_dict, new_structure_dict, filename, save_to_file)

    def execute_with_params(self, params):

        table_name = params["table_name"]
        old_structure_dict = params["old_structure_dict"]
        new_structure_dict = params["new_structure_dict"]
        filename = params["filename"]
        save_to_file = params["save_to_file"]

        self.direct_execute(table_name, old_structure_dict, new_structure_dict, filename, save_to_file)

    def direct_execute(self, table_name, old_structure_dict, new_structure_dict, filename, save_to_file):

        migration_list = get_migration_file(table_name, old_structure_dict, new_structure_dict)
        variable_handler.new_variable(filename, migration_list)

        if save_to_file:
            migrator = dh.Migrator()
            migrator.migration_list = migration_list
            migrator.migration_list_to_json(filename)



    def export_code(self, node_detail_form):
        table_name = node_detail_form.get_variable_name_or_input_value_by_element_name("table_name")
        old_structure_dict = node_detail_form.get_variable_name_or_input_value_by_element_name("old_structure_dict")
        new_structure_dict = node_detail_form.get_variable_name_or_input_value_by_element_name("new_structure_dict")
        filename = node_detail_form.get_variable_name_or_input_value_by_element_name("filename")
        save_to_file = node_detail_form.get_variable_name_or_input_value_by_element_name("save_to_file")

        code = ""

        return code

    def export_imports(self, *args):
        imports = []
        return imports


class RunMigrationFileHandler(AbstractFunctionHandler):
    def __init__(self):
        self.icon_type = 'RunMigrationFile'
        self.fn_name = 'Run Migration File'

        self.type_category = ntcm.categories.database

    def make_form_dict_list(self, *args, node_detail_form=None):
        options = [x.db_details["DB_DATABASE"] for x in duh.db_connections]

        fdl = FormDictList()
        fdl.label(self.fn_name)
        fdl.label("Table name")
        fdl.combobox(name="db_name", options=options, row=1)
        fdl.label("Migration list:")
        fdl.entry(name="migration_list", text="migration-1", input_types=["str", "list"], row=2)
        # fdl.label("Migration file name:")
        # fdl.entry(name="filename", text="migration-1", input_types=["str"], row=3)

        fdl.button(function=self.open_migration_file, function_args=node_detail_form, text="Load file", name="lookup_json_file")
        fdl.button(function=self.execute, function_args=node_detail_form, text="Execute", focused=True)

        return fdl

    def open_migration_file(self, node_detail_form):
        file = askopenfile(mode='r', filetypes=[('JSON files', '*.json')])

        if file is not None:
            filename = file.name
            params_dict = node_detail_form.assign_value_by_name(name='filename', value=filename)
            ncrb.update_node_by_uid(node_detail_form.node_uid, params=params_dict)

    def execute(self, node_detail_form):
        db_name = node_detail_form.get_chosen_value_by_name("db_name", variable_handler)
        migration_list = node_detail_form.get_chosen_value_by_name("migration_list", variable_handler)

        self.direct_execute(db_name, migration_list)

    def _force_execute(self, args):
        image = args[0]
        item_detail_form = image.item_detail_form

        db_name = item_detail_form.get_chosen_value_by_name('db_name', variable_handler)
        migration_list = item_detail_form.get_chosen_value_by_name('migration_list', variable_handler)

        self.direct_execute(db_name, migration_list)

    def execute_with_params(self, params):

        db_name = params["db_name"]
        filename = params["filename"]
        migration_list = params["migration_list"]

        self.direct_execute(db_name, filename)



    def direct_execute(self, db_name, migration_list):

        db_connection = duh.get_db_connection(db_name)
        db_connection.test_database_connection()
        db_instance = db_connection.db_instance
        

        db_instance.initialize_migrator()
        db_instance.connect_locally()


        if isinstance(migration_list, list):
            db_instance.migrator.migrate(migration_list)
        elif isinstance(migration_list, str):
            db_instance.migrator.migrate_from_json(migration_list)

        db_instance.close_connection()


    def export_code(self, node_detail_form):
        db_name = node_detail_form.get_variable_name_or_input_value_by_element_name("db_name")
        migration_list = node_detail_form.get_variable_name_or_input_value_by_element_name("migration_list")

        code = """
        """

        return code

    def export_imports(self, *args):
        imports = []
        return imports

class CopyDbStructureHandler(AbstractFunctionHandler):
    def __init__(self):
        self.icon_type = 'CopyDbStructureHandler'
        self.fn_name = 'Copy db structure'

        self.type_category = ntcm.categories.database

    def make_form_dict_list(self, *args, node_detail_form=None):
        options = [x.db_details["DB_DATABASE"] for x in duh.db_connections]

        fdl = FormDictList()
        fdl.label(self.fn_name)
        fdl.label("Origin database")
        fdl.combobox(name="db_name_origin", options=options, row=1)
        fdl.label("Destination database")
        fdl.combobox(name="db_name_destination", options=options, row=2)
        fdl.label("Migration name")
        fdl.entry(name="migration_name", text="migration-1", input_types=["str"], row=3)
        fdl.label("Save to json")
        fdl.checkbox("save_to_file", row=4)

        fdl.button(function=self.execute, function_args=node_detail_form, text="Execute", focused=True)

        return fdl

    def execute(self, node_detail_form):
        db_name_origin = node_detail_form.get_chosen_value_by_name('db_name_origin', variable_handler)
        db_name_destination = node_detail_form.get_chosen_value_by_name('db_name_destination', variable_handler)
        migration_name = node_detail_form.get_chosen_value_by_name("migration_name", variable_handler)
        save_to_file = node_detail_form.get_chosen_value_by_name('save_to_file', variable_handler)

        self.direct_execute(db_name_origin, db_name_destination, migration_name, save_to_file)

    def direct_execute(self, db_name_origin, db_name_destination, migration_name="migration-1", save_to_file=False):

        db_connection_origin = duh.get_db_connection(db_name_origin)
        db_connection_origin.test_database_connection()

        db_connection_destination = duh.get_db_connection(db_name_destination)
        db_connection_destination.test_database_connection()

        if db_connection_origin is None or db_connection_destination is None:
            #glc.show_warning_popup_message("Db connection not found")
            flog.error("Db connection not found",self)
            return

        if isinstance(db_connection_destination.db_instance, dh.MongoDb):
            #glc.show_warning_popup_message("Cannot copy structure to Mongo")
            flog.error("Db connection not found",self)
            return



        origin_tables = list(db_connection_origin.table_dict.keys())
        destination_tables = list(db_connection_destination.table_dict.keys())


        table_intersection = list(set(origin_tables) & set(destination_tables))
        tables_only_in_origin = list(set(origin_tables) - set(destination_tables))

        migration_list = []

        for table in tables_only_in_origin:
            analyzed_table = dict(zip(db_connection_origin.table_dict[table].columns, db_connection_origin.table_dict[table].types))
            if analyzed_table is None:
                return
            migration = get_migration_file(table, {}, analyzed_table)
            migration_list += migration

        for table in table_intersection:
            analyzed_table_origin = dict(zip(db_connection_origin.table_dict[table].columns, db_connection_origin.table_dict[table].types))
            analyzed_table_destination = dict(zip(db_connection_destination.table_dict[table].columns, db_connection_destination.table_dict[table].types))
            if analyzed_table_origin is None or analyzed_table_destination is None:
                return
            migration = get_migration_file(table, analyzed_table_destination, analyzed_table_origin)
            migration_list += migration

        variable_handler.new_variable(migration_name, migration_list)

        if save_to_file:
            migrator = dh.Migrator()
            migrator.migration_list = migration_list
            migrator.migration_list_to_json(migration_name)

    # def data_type_conversion_to_mysql_default(self, db_connection, analyzed_table):
    #     if isinstance(db_connection.db_instance, dh.Mysqldb):
    #         return analyzed_table
    #     elif isinstance(db_connection.db_instance, dh.PostgresDb):





class CopyDbDataHandler(AbstractFunctionHandler):
    def __init__(self):
        self.icon_type = 'CopyDbDataHandler'
        self.fn_name = 'Copy db data'

        self.type_category = ntcm.categories.database

    def make_form_dict_list(self, *args, node_detail_form=None):
        options = [x.db_details["DB_DATABASE"] for x in duh.db_connections]

        fdl = FormDictList()
        fdl.label(self.fn_name)
        fdl.label("Origin database")
        fdl.combobox(name="db_name_origin", options=options, row=1)
        fdl.label("Destination database")
        fdl.combobox(name="db_name_destination", options=options, row=2)
        fdl.label("Migration name")
        fdl.entry(name="migration_name", text="migration-1", input_types=["str"], row=3)
        fdl.label("Save to json")
        fdl.checkbox("save_to_file", row=4)

        fdl.button(function=self.execute, function_args=node_detail_form, text="Execute", focused=True)

        return fdl

    def execute(self, node_detail_form):
        db_name_origin = node_detail_form.get_chosen_value_by_name('db_name_origin', variable_handler)
        db_name_destination = node_detail_form.get_chosen_value_by_name('db_name_destination', variable_handler)
        migration_name = node_detail_form.get_chosen_value_by_name("migration_name", variable_handler)
        save_to_file = node_detail_form.get_chosen_value_by_name('save_to_file', variable_handler)

        self.direct_execute(db_name_origin, db_name_destination, migration_name, save_to_file)

    def direct_execute(self, db_name_origin, db_name_destination, migration_name="migration-1", save_to_file=False):

        db_connection_origin = duh.get_selected_db_connection(db_name_origin)
        db_connection_origin.test_database_connection()

        db_connection_destination = duh.get_db_connection(db_name_destination)
        db_connection_destination.test_database_connection()

        if db_connection_origin is None or db_connection_destination is None:
            #glc.show_warning_popup_message("Db connection not found")
            flog.error("Db connection not found",self)
            return

        with db_connection_origin.db_instance.connect_to_db():
            with db_connection_destination.db_instance.connect_to_db():

                if isinstance(db_connection_destination.db_instance, dh.MongoDb) or isinstance(db_connection_origin.db_instance, dh.MongoDb):
                    self._copy_mongo_data(db_connection_origin, db_connection_destination)
                else:
                    self._copy_sql_data(db_connection_origin, db_connection_destination)

    def _copy_sql_data(self, db_connection_origin, db_connection_destination):
        origin_tables = set(db_connection_origin.table_dict.keys())
        destination_tables = set(db_connection_destination.table_dict.keys())

        if not origin_tables.issubset(destination_tables):
            #glc.show_warning_popup_message("Error")
            flog.error("Error",self)
            
            return

        for table_name in origin_tables:
            origin_table = db_connection_origin.table_dict[table_name]
            origin_table_structure = dict(zip(origin_table.columns, origin_table.types))

            destination_table = db_connection_destination.table_dict[table_name]
            destination_table_structure = dict(zip(destination_table.columns, destination_table.types))

            if origin_table_structure != destination_table_structure:
                #glc.show_warning_popup_message(f"Wrong structure for table {table_name}, please migrate structure first")
                flog.error(f"Wrong structure for table {table_name}, please migrate structure first",self)
                
                continue

            df_to_copy = origin_table.select_to_df()
            destination_table.delete()

            #TODO: discuss what to do with duplicate ids (maybe on DUPLICATE KEY UPDATE? )

            destination_table.insert_from_df(df_to_copy, insert_id=True)



    def _copy_mongo_data(self, db_connection_origin, db_connection_destination):

        origin_tables = set(db_connection_origin.table_dict.keys())
        insert_id=True
        for table_name in origin_tables:

            origin_table = db_connection_origin.table_dict[table_name]
            if isinstance(db_connection_destination.db_instance, dh.MongoDb):
                destination_table = dh.MongoTable(db_connection_destination.db_instance, table_name)
            else:
                destination_table = db_connection_destination.table_dict[table_name]

            if isinstance(db_connection_origin.db_instance, dh.MongoDb):
                origin_table.update_collection()
                df_to_copy = origin_table.select_to_df()
                insert_id=False
                df_to_copy = self._clear_mongo_dataframe_from_ids(df_to_copy)
            else:
                df_to_copy = origin_table.select_to_df()

            destination_table.delete()
            destination_table.insert_from_df(df_to_copy, insert_id=insert_id)


    def _clear_mongo_dataframe_from_ids(self, df_to_copy):
        if "_id" in df_to_copy.columns:
            df_to_copy = df_to_copy.drop(["_id"], axis=1)
        if "id" in df_to_copy.columns:
            df_to_copy = df_to_copy.drop(["id"], axis=1)
        return df_to_copy




def get_db_table(table_name):
    matching_dbtables = [db_table for name, db_table in get_connected_db_tables().items() if name == table_name]
    if len(matching_dbtables) == 1:
        dbtable = matching_dbtables[0]
        return dbtable
    else:
        #glc.show_warning_popup_message("Error")
        flog.error("Error")
        
        return

def get_table_structure(dbtable=None):
    if dbtable is None:
        return None
    db_instance = dbtable.db1

    with db_instance.connect_to_db():
        if isinstance(db_instance, dh.MongoDb):
            dbtable.update_collection()
            df = dbtable.select_to_df()
            if '_id' in df:
                df = df.drop(['_id'], axis=1)
            columns, types = dh.Migrator().extract_columns_and_types_from_df(df)
            structure = dict(zip(columns, types))
        else:
            columns = dbtable.get_all_columns()
            types = dbtable.get_all_types()
            flog.info(f'INSTANCE CONNECTION = {db_instance.connection}')

            structure = dict(zip(columns, types))
    return structure



def get_migration_file(table_name, old_structure_dict, new_structure_dict):
    is_empty = lambda x: str(x) == "{}" or str(x).isspace()
    # drop_table_condition1 = not is_empty(old_structure_dict) and is_empty(new_structure_dict)
    # drop_table_condition2 = is_empty(old_structure_dict) and is_empty(new_structure_dict)

    if is_empty(old_structure_dict) and not is_empty(new_structure_dict):
        columns = list(new_structure_dict.keys())
        types = list(new_structure_dict.values())
        migration_list = [{"create": {"table_name": table_name, "columns": columns, "types": types}}]
    elif is_empty(new_structure_dict):
        migration_list = [{"drop": {"table_name": table_name}}]
    else:
        structure_changes = DeepDiff(old_structure_dict, new_structure_dict, verbose_level=2)
        migration_list = _convert_deepdiff_dict_into_migration_list(table_name, structure_changes)

    return migration_list


def _convert_deepdiff_dict_into_migration_list(table_name, deepdiff_dict) -> list:
    migration_list = []

    convert_dict = {"dictionary_item_added": "add_column", "dictionary_item_removed": "drop_column", "values_changed": "modify_column"}

    for key in deepdiff_dict.keys():
        for item_key in deepdiff_dict[key].keys():
            column_name = item_key[6:-2]
            if key=="dictionary_item_added":    
                column_type = deepdiff_dict[key][item_key]
                migration_list.append({convert_dict[key]: {"table_name": table_name, "column_name": column_name,"column_type": column_type}})
            elif key=="dictionary_item_removed":    
                migration_list.append(
                    {"drop_column": {"table_name": table_name, "column_name": column_name}})
            elif key=="values_changed":
                column_new_type = deepdiff_dict[key][item_key]["new_value"]
                migration_list.append({"modify_column": {"table_name": table_name, "column_name": column_name,
                                                     "column_type": column_new_type}})
        
    return migration_list



    #
    # for key in deepdiff_dict.keys():
    #     if key == 'dictionary_item_added':
    #         for add_item_key in deepdiff_dict[key].keys():
    #             new_column_name = add_item_key[
    #                               6:-2]  # thats because DeepDiff gives this format --> root['new_column_name']
    #             new_column_type = deepdiff_dict[key][add_item_key]
    #             migration_list.append({"add_column": {"table_name": table_name, "column_name": new_column_name,
    #                                                   "column_type": new_column_type}})
    #     elif key == 'dictionary_item_removed':
    #         for remove_item_key in deepdiff_dict[key].keys():
    #             removed_column_name = remove_item_key[
    #                                   6:-2]  # thats because DeepDiff gives this format --> root['new_column_name']
    #             migration_list.append(
    #                 {"drop_column": {"table_name": table_name, "column_name": removed_column_name}})
    #     elif key == 'values_changed':
    #         for changed_item_key in deepdiff_dict[key].keys():
    #             column_name = changed_item_key[
    #                           6:-2]  # thats because DeepDiff gives this format --> root['new_column_name']
    #             column_new_type = deepdiff_dict[key][changed_item_key]["new_value"]
    #             migration_list.append({"modify_column": {"table_name": table_name, "column_name": column_name,
    #                                                      "column_type": column_new_type}})
    #
    # return migration_list




def parse_float_db(db_instance, value):
    if type(db_instance) is dh.MongoDb:
        value = parse_float_mongo(value)
    else:
        value = parse_float_sql(value)

    return value


def parse_float_mongo(value):
    try:
        value = float(value)
    except (ValueError, TypeError):
        pass

    return value


def parse_float_sql(value):
    try:
        value = float(value)
    except (ValueError, TypeError):
        value = "'" + str(value) + "'"

    return value


def get_condition_mongo(column_name, value, operator):
    condition = {}
    if column_name and value and operator:
        if operator == " IN ":
            value = ast.literal_eval(value)

        condition = {column_name[0]: {dh.MONGO_OPERATOR_DICT[operator]: value}}

    return condition


def generate_sql_condition(cols_to_be_selected, dbtable_name, column_name, value, operator, limit, dataset=None):
    """
    Generates an SQL query string with optional filtering and limit.

    Args:
    cols_to_be_selected (str): Comma-separated column names.
    dbtable_name (str): Database table name.
    column_name (str): Filter column name.
    value (str, int, float): Value for comparison.
    operator (str): SQL comparison operator (e.g., "=", "<>", ">", "<", ">=", "<=").
    limit (int): Maximum number of rows returned.
    dataset (str, optional): Dataset name for BigQuery tables.

    Returns:
    query (str): Generated SQL query string.
    """

    if dataset is not None:
        query = f"SELECT {cols_to_be_selected} FROM {dataset}.{dbtable_name}"
    else:
        query = f"SELECT {cols_to_be_selected} FROM {dbtable_name}"

    if column_name and operator and value:
        where_statement = f"{column_name[0]}{operator}{value}"
        query += f" WHERE {where_statement}"
    if limit:
        query += f" LIMIT {limit}"
    query += ";"

    return query


def connect_to_db_and_run_operation(operation, db_instance, dbtable, **kwargs):
    with db_instance.connect_to_db():
        try:
            if type(db_instance) is dh.MongoDb:
                dbtable.update_collection()

            if operation == "DELETE":
                dbtable.delete(kwargs['where_statement'])

            elif operation == "INSERT":
                 dbtable.insert_from_df(kwargs['inserted_dataframe'])

            elif operation == "UPDATE":
                dbtable.update(kwargs['set_statement'], kwargs['where_statement'])

        except AssertionError:
            flog.error(f"Different number of imputed columns")
        except Exception as e:
            flog.error(f"{operation} ERROR: {e}")


database_handlers_dict = {
    "DBSelect": DBSelectHandler(),
    "DBInsert": DBInsertHandler(),
    "DBDelete": DBDeleteHandler(),
    "DBUpdate": DBUpdateHandler(),
    "DBQuery": DBQueryHandler(),
    'AnalyzeDbTable': AnalyzeDbTableHandler(),
    'CreateMigrationFile': CreateMigrationFileHandler(),
    'RunMigrationFile': RunMigrationFileHandler(),
    'CopyDbStructureHandler': CopyDbStructureHandler(),
    'CopyDbDataHandler': CopyDbDataHandler()
}
