_D='TIMESTAMP WITH TIME ZONE'
_C='TIMESTAMP WITHOUT TIME ZONE'
_B='test'
_A='TEXT'
import atexit,json,logging,time
from localstack import config
from localstack.utils.net import get_free_tcp_port,wait_for_port_open
from localstack_ext.services.rds.engine_postgres import get_type_name
from localstack_ext.utils.postgresql import Postgresql
from snowflake_local import config as sf_config
from snowflake_local.engine.db_engine import DBEngine
from snowflake_local.engine.models import Query,QueryResult,TableColumn
from snowflake_local.engine.packages import postgres_plv8_package
from snowflake_local.engine.postgres.db_state import State
from snowflake_local.engine.postprocess import _get_database_from_drop_query
from snowflake_local.engine.transform_utils import NameType,get_canonical_name
from snowflake_local.engine.transforms import apply_query_transforms
LOG=logging.getLogger(__name__)
PG_VARIANT_TYPE=_A
PG_VARIANT_COMPATIBLE_TYPES='JSONB','FLOAT','BIGINT','BOOLEAN',_A
PG_VARIANT_TYPES_AND_ARRAYS=PG_VARIANT_COMPATIBLE_TYPES+('FLOAT[]','INTEGER[]','BOOLEAN[]','TEXT[]')
BASIC_TYPES=_A,'DECIMAL','INTEGER'
DEFAULT_DATABASE=_B
class DBEnginePostgres(DBEngine):
	def execute_query(G,query):
		A=_execute_query(query)
		if isinstance(A,list):return QueryResult(rows=A)
		if not A._context.columns:return QueryResult()
		B=list(A);B=[tuple(A)for A in B];D=QueryResult(rows=B)
		for C in A._context.columns:E=C['name'].upper();F=TableColumn(name=E,type_name=get_pg_type_name(C['type_oid']),type_size=C['type_size']);D.columns.append(F)
		return D
	def prepare_query(A,query):return apply_query_transforms(query)
def _execute_query(query):
	A=query;G=_start_postgres();E=bool(_get_database_from_drop_query(A.original_query));D=A.query;B=None
	if A.session:
		if A.session.database:B=A.session.database
		if A.session.schema and A.session.schema!='public'and not E:
			C=A.session.schema
			if'.'in C:B,C=C.split('.')
			C=get_canonical_name(C);D=f"SET search_path TO {C}, public; \n{D}"
	B=A.database or B or DEFAULT_DATABASE
	if E:B=None
	else:
		B=get_canonical_name(B,quoted=False,type=NameType.DATABASE)
		try:_define_util_functions(B)
		except Exception as H:LOG.warning('Unable to define Postgres util functions: %s',H);raise
	F=A.params or[];LOG.debug('Running query (DB %s): %s - %s',B,D,F);return G.run_query(D,*F,database=B)
def _start_postgres(user=_B,password=_B,database=_B):
	if not State.server:
		A=get_free_tcp_port();State.server=Postgresql(port=A,user=user,password=password,database=database,boot_timeout=30,include_python_venv_libs=True);time.sleep(1)
		try:B=20;wait_for_port_open(A,retries=B,sleep_time=.8)
		except Exception:raise Exception('Unable to start up Postgres process (health check failed after 10 secs)')
		def C():State.server.terminate()
		atexit.register(C)
	return State.server
def _define_util_functions(database):
	G='to_binary';F='array_construct';B=database;from snowflake_local.engine.query_processors import QueryProcessor as H
	if B in State.initialized_dbs:return
	State.initialized_dbs.append(B);D=State.server
	if sf_config.CONVERT_NAME_CASING and B.upper()==DEFAULT_DATABASE.upper():D.run_query(f'CREATE DATABASE "{DEFAULT_DATABASE.upper()}"')
	D.run_query('CREATE EXTENSION IF NOT EXISTS plpython3u',database=B);_install_plv8_extension();D.run_query('CREATE EXTENSION IF NOT EXISTS plv8',database=B);A=[];A.append(f"""
        CREATE OR REPLACE FUNCTION {get_canonical_name("load_data")} (
           file_ref text,
           file_format text
        ) RETURNS SETOF RECORD
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import load_data
            return load_data(file_ref, file_format)
        $$
    """)
	for E in range(10):I=', '.join([f"k{A} TEXT, v{A} TEXT"for A in range(E)]);J=', '.join([f"k{A}, v{A}"for A in range(E)]);A.append(f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name("object_construct")} ({I}) RETURNS {PG_VARIANT_TYPE}
            LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import object_construct
                return object_construct({J})
            $$
        """)
	for C in PG_VARIANT_TYPES_AND_ARRAYS:A.append(f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name("to_variant")} (obj {C}) RETURNS {PG_VARIANT_TYPE}
            LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import to_variant
                return to_variant(obj)
            $$
        """)
	A.append(f"""
        CREATE OR REPLACE FUNCTION {get_canonical_name("get_path")} (obj {PG_VARIANT_TYPE}, path TEXT) RETURNS TEXT
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import get_path
            return get_path(obj, path)
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION {get_canonical_name("parse_json")} (obj TEXT) RETURNS {PG_VARIANT_TYPE}
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import parse_json
            return parse_json(obj)
        $$
    """)
	for C in PG_VARIANT_COMPATIBLE_TYPES+('BYTEA',):A.append(f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name("to_char")} (obj {C}) RETURNS TEXT
            LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import to_char
                return to_char(obj)
            $$
        """)
	for C in PG_VARIANT_COMPATIBLE_TYPES:A.append(f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name("to_boolean")} (obj {C}) RETURNS BOOLEAN
            LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import to_boolean
                return to_boolean(obj)
            $$
        """)
	A.append(f"""
        CREATE OR REPLACE FUNCTION {get_canonical_name("result_scan")}
        (results_file TEXT) RETURNS SETOF RECORD
        LANGUAGE plpython3u IMMUTABLE
        AS $$
            from snowflake_local.engine.extension_functions import result_scan
            return result_scan(results_file)
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION {get_canonical_name("array_append")}
        (_array {PG_VARIANT_TYPE}, _entry TEXT) RETURNS TEXT
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import array_append
            return array_append(_array, _entry)
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION {get_canonical_name("array_cat")}
        (_array1 {PG_VARIANT_TYPE}, _array2 {PG_VARIANT_TYPE}) RETURNS TEXT
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import array_concat
            return array_concat(_array1, _array2)
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION {get_canonical_name(F)}
        (VARIADIC _values {PG_VARIANT_TYPE}[]) RETURNS {PG_VARIANT_TYPE}
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import array_construct
            return array_construct(*_values)
        $$;
        CREATE OR REPLACE FUNCTION {get_canonical_name(F)} () RETURNS {PG_VARIANT_TYPE}
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import array_construct
            return array_construct()
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION {get_canonical_name("array_compact")}
        (_array {PG_VARIANT_TYPE}) RETURNS {PG_VARIANT_TYPE}
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import array_compact
            return array_compact(_array)
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION {get_canonical_name("array_construct_compact")}
        (VARIADIC _values {PG_VARIANT_TYPE}[]) RETURNS {PG_VARIANT_TYPE}
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import array_construct_compact
            return array_construct_compact(*_values)
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION {get_canonical_name("array_distinct")}
        (_array {PG_VARIANT_TYPE}) RETURNS {PG_VARIANT_TYPE}
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import array_distinct
            return array_distinct(_array)
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION {get_canonical_name("array_contains")}
        (_value {PG_VARIANT_TYPE}, _array {PG_VARIANT_TYPE}) RETURNS BOOLEAN
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import array_contains
            return array_contains(_value, _array)
        $$
    """);A.append(f"""
        CREATE OR REPLACE FUNCTION {get_canonical_name(G)} (_obj TEXT) RETURNS BYTEA
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import to_binary
            return to_binary(_obj)
        $$;
        CREATE OR REPLACE FUNCTION {get_canonical_name(G)} (_obj TEXT, _format TEXT) RETURNS BYTEA
        LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import to_binary
            return to_binary(_obj, _format)
        $$
    """);A.append(f'''
        CREATE OR REPLACE FUNCTION {get_canonical_name("system$snowpipe_streaming_migrate_channel_offset_token")} (
            tableName TEXT, channelName TEXT, offsetToken TEXT) RETURNS TEXT
        LANGUAGE plpython3u IMMUTABLE AS $$
            # TODO: simply returning hardcoded value for now - may need to get adjusted over time
            return \'{{"responseMessage":"Success","responseCode":50}}\'
        $$
    ''');A.append(f"""
        CREATE OR REPLACE FUNCTION {get_canonical_name("system$cancel_all_queries")} (session TEXT)
        RETURNS {PG_VARIANT_TYPE} LANGUAGE plpython3u IMMUTABLE AS $$
            from snowflake_local.engine.extension_functions import cancel_all_queries
            return cancel_all_queries(session)
        $$
    """);K=';\n'.join(A);D.run_query(K,database=B);_define_hardcoded_return_value_functions(database=B);_define_aggregate_functions(database=B)
	for L in H.get_instances():L.initialize_db_resources(database=B)
def _define_hardcoded_return_value_functions(database):
	E='PUBLIC';C=database;D=State.server;F=['ACCOUNTADMIN','ORGADMIN',E,'SECURITYADMIN','SYSADMIN','USERADMIN'];G={'current_account':'TEST001','current_account_name':'TEST002','current_available_roles':json.dumps(F),'current_client':'test-client','current_ip_address':'127.0.0.1','current_organization_name':'TESTORG','current_region':'TEST_LOCAL','get_current_role':E,'get_current_user':'TEST','current_role_type':'ROLE','current_secondary_roles':json.dumps({'roles':'','value':''}),'current_version':'0.0.0','current_transaction':None}
	for(H,A)in G.items():A=A and f"'{A}'";B=f"\n            CREATE OR REPLACE FUNCTION {get_canonical_name(H)} ()\n            RETURNS TEXT LANGUAGE plpython3u IMMUTABLE AS\n            $$ return {A} $$;\n            ";D.run_query(B,database=C)
	B='\n    CREATE OR REPLACE FUNCTION information_schema.CURRENT_TASK_GRAPHS() RETURNS\n    TABLE(\n        ROOT_TASK_NAME TEXT, DATABASE_NAME TEXT, SCHEMA_NAME TEXT, STATE TEXT, SCHEDULED_FROM TEXT,\n        FIRST_ERROR_TASK_NAME TEXT, FIRST_ERROR_CODE NUMERIC, FIRST_ERROR_MESSAGE TEXT,\n        SCHEDULED_TIME TIMESTAMP, QUERY_START_TIME TIMESTAMP, NEXT_SCHEDULED_TIME TIMESTAMP,\n        ROOT_TASK_ID TEXT, GRAPH_VERSION NUMERIC, RUN_ID NUMERIC, ATTEMPT_NUMBER NUMERIC,\n        CONFIG TEXT, GRAPH_RUN_GROUP_ID NUMERIC\n    )\n    LANGUAGE plpython3u IMMUTABLE AS $$ return [] $$;\n    ';D.run_query(B,database=C)
def _define_aggregate_functions(database):
	S='string_agg_nogroup_distinct';R='string_agg_nogroup';Q='string_agg_ordered_distinct';P='string_agg_ordered';O='TIMESTAMP';N='NUMERIC';K='array_agg_aggregate';G=database;F='string_agg_aggregate_distinct';E='string_agg_aggregate';D='string_agg_aggregate_ordered_finalize';C='string_agg_aggregate_finalize';H=State.server
	for B in('arg_min','arg_max'):
		for(L,J)in enumerate((N,_A,O)):
			I=f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name(f"{B}_finalize_{L}")} (
               _result TEXT[]
            ) RETURNS {J} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import arg_min_max_finalize
                return arg_min_max_finalize(_result)
            $$;
            """;H.run_query(I,database=G)
			for M in(N,O):I=f"""
                CREATE OR REPLACE FUNCTION {get_canonical_name(f"{B}_aggregate")} (
                   _result TEXT[],
                   _input1 {J},
                   _input2 {M}
                ) RETURNS TEXT[] LANGUAGE plpython3u IMMUTABLE AS $$
                    from snowflake_local.engine.extension_functions import {B}_aggregate
                    return {B}_aggregate(_result, _input1, _input2)
                $$;
                CREATE AGGREGATE {get_canonical_name(B)} ({J}, {M}) (
                    INITCOND = '{{null,null}}',
                    STYPE = TEXT[],
                    SFUNC = {get_canonical_name(f"{B}_aggregate")},
                    FINALFUNC = {get_canonical_name(f"{B}_finalize_{L}")}
                );
                """;H.run_query(I,database=G)
	for A in BASIC_TYPES:I=f"""
        CREATE OR REPLACE FUNCTION {get_canonical_name(K)} (_result TEXT, _input1 {A})
        RETURNS TEXT LANGUAGE plpython3u IMMUTABLE
        AS $$
            from snowflake_local.engine.extension_functions import array_agg_aggregate
            return array_agg_aggregate(_result, _input1)
        $$;
        CREATE AGGREGATE {get_canonical_name("array_agg_ordered")} (ORDER BY {A}) (
            STYPE = TEXT,
            SFUNC = {get_canonical_name(K)}
        );
        CREATE AGGREGATE {get_canonical_name("array_agg")} ({A}) (
            STYPE = TEXT,
            SFUNC = {get_canonical_name(K)}
        );
        """;H.run_query(I,database=G)
	H.run_query(f"""
    CREATE OR REPLACE FUNCTION {get_canonical_name(C)} (
       _result {PG_VARIANT_TYPE}, _separator TEXT) RETURNS {PG_VARIANT_TYPE}
    LANGUAGE plpython3u IMMUTABLE AS $$
        from snowflake_local.engine.extension_functions import string_agg_aggregate_finalize
        return string_agg_aggregate_finalize(_result, _separator)
    $$;
    CREATE OR REPLACE FUNCTION {get_canonical_name(C)} (
       _result {PG_VARIANT_TYPE} ) RETURNS {PG_VARIANT_TYPE}
    LANGUAGE plpython3u IMMUTABLE AS $$
        from snowflake_local.engine.extension_functions import string_agg_aggregate_finalize
        return string_agg_aggregate_finalize(_result)
    $$;
    CREATE OR REPLACE FUNCTION {get_canonical_name(D)} (
       _result {PG_VARIANT_TYPE}, _separator TEXT) RETURNS {PG_VARIANT_TYPE}
    LANGUAGE plpython3u IMMUTABLE AS $$
        from snowflake_local.engine.extension_functions import string_agg_aggregate_ordered_finalize
        return string_agg_aggregate_ordered_finalize(_result, _separator)
    $$;
    CREATE OR REPLACE FUNCTION {get_canonical_name(D)} (
       _result {PG_VARIANT_TYPE} ) RETURNS {PG_VARIANT_TYPE}
    LANGUAGE plpython3u IMMUTABLE AS $$
        from snowflake_local.engine.extension_functions import string_agg_aggregate_ordered_finalize
        return string_agg_aggregate_ordered_finalize(_result)
    $$;
    """,database=G)
	for A in BASIC_TYPES:H.run_query(f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name(E)}
                (_result {PG_VARIANT_TYPE}, _input {A})
            RETURNS {PG_VARIANT_TYPE} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import string_agg_aggregate
                return string_agg_aggregate(_result, _input)
            $$;
            CREATE OR REPLACE FUNCTION {get_canonical_name(E)}
                (_result {PG_VARIANT_TYPE}, _input {A}, _separator TEXT)
            RETURNS {PG_VARIANT_TYPE} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import string_agg_aggregate
                return string_agg_aggregate(_result, _input, _separator)
            $$;
            CREATE OR REPLACE FUNCTION {get_canonical_name(F)}
                (_result {PG_VARIANT_TYPE}, _input {A})
            RETURNS {PG_VARIANT_TYPE} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import string_agg_aggregate_distinct
                return string_agg_aggregate_distinct(_result, _input)
            $$;
            CREATE OR REPLACE FUNCTION {get_canonical_name(F)}
                (_result {PG_VARIANT_TYPE}, _input {A}, _separator TEXT)
            RETURNS {PG_VARIANT_TYPE} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.extension_functions import string_agg_aggregate_distinct
                return string_agg_aggregate_distinct(_result, _input, _separator)
            $$;
            CREATE AGGREGATE {get_canonical_name(P)} (_separator TEXT ORDER BY {A}) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = {get_canonical_name(E)},
                FINALFUNC = {get_canonical_name(D)}
            );
            CREATE AGGREGATE {get_canonical_name(P)} (ORDER BY {A}) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = {get_canonical_name(E)},
                FINALFUNC = {get_canonical_name(D)}
            );
            CREATE AGGREGATE {get_canonical_name(Q)} (_separator TEXT ORDER BY {A}) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = {get_canonical_name(F)},
                FINALFUNC = {get_canonical_name(D)}
            );
            CREATE AGGREGATE {get_canonical_name(Q)} (ORDER BY {A}) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = {get_canonical_name(F)},
                FINALFUNC = {get_canonical_name(D)}
            );

            CREATE AGGREGATE {get_canonical_name(R)} (_value {A}) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = {get_canonical_name(E)},
                FINALFUNC = {get_canonical_name(C)}
            );
            CREATE AGGREGATE {get_canonical_name(R)} (_value {A}, _separator TEXT) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = {get_canonical_name(E)},
                FINALFUNC = {get_canonical_name(C)}
            );
            CREATE AGGREGATE {get_canonical_name(S)} (_value {A}) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = {get_canonical_name(F)},
                FINALFUNC = {get_canonical_name(C)}
            );
            CREATE AGGREGATE {get_canonical_name(S)} (_value {A}, _separator TEXT) (
                STYPE = {PG_VARIANT_TYPE},
                SFUNC = {get_canonical_name(F)},
                FINALFUNC = {get_canonical_name(C)}
            );""",database=G)
def _install_plv8_extension():
	if config.is_in_docker:postgres_plv8_package.install()
def get_pg_type_name(scalar_type):
	C='VARCHAR';A=scalar_type;D={'19':C,'25':C,'1114':_C,'1184':_D};B=D.get(str(A))
	if B:return B
	return get_type_name(A)
def convert_pg_to_snowflake_type(pg_type):
	A=pg_type;A=str(A).upper()
	if A==_C:return'TIMESTAMP_NTZ'
	if A==_D:return'TIMESTAMP_TZ'
	return A