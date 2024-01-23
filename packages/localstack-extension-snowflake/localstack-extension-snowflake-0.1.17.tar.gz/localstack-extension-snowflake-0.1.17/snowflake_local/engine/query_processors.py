_I='array_insert'
_H='is_array'
_G='expression'
_F='SELECT NULL'
_E='default'
_D=True
_C='this'
_B='postgres'
_A=None
import logging,re
from abc import ABC
from functools import cmp_to_key
from typing import Any
from localstack.utils.numbers import is_number
from localstack.utils.objects import get_all_subclasses
from sqlglot import exp,parse_one
from snowflake_local import config
from snowflake_local.engine.extension_functions import VARIANT,_unwrap_potential_variant_type,_unwrap_variant_type,to_variant
from snowflake_local.engine.models import Query
from snowflake_local.engine.postgres.db_state import State
from snowflake_local.engine.transform_utils import INTERNAL_IDENTIFIERS,convert_function_args_to_variant,get_canonical_name
from snowflake_local.server.models import QueryResponse
from snowflake_local.utils.strings import parse_comma_separated_variable_assignments
LOG=logging.getLogger(__name__)
class QueryProcessor(ABC):
	def initialize_db_resources(A,database):0
	def should_apply(A,query):return _D
	def transform_query(A,expression,query):return expression
	def postprocess_result(A,query,result):0
	def get_priority(A):return 0
	@classmethod
	def get_instances(B):A=[A()for A in get_all_subclasses(QueryProcessor)];A=sorted([A for A in A],key=lambda item:item.get_priority(),reverse=_D);return A
class HandleShowParameters(QueryProcessor):
	REGEX=re.compile('^\\s*SHOW\\s+PARAMETERS',flags=re.I);SUPPORTED_PARAMS={'AUTOCOMMIT':{_E:'true'},'TIMEZONE':{_E:'America/Los_Angeles'},'TIMESTAMP_NTZ_OUTPUT_FORMAT':{_E:'YYYY-MM-DD HH24:MI:SS.FF3'},'TIMESTAMP_LTZ_OUTPUT_FORMAT':{},'TIMESTAMP_TZ_OUTPUT_FORMAT':{}}
	def should_apply(A,query):return bool(A.REGEX.match(query.original_query))
	def transform_query(C,expression,**D):
		A=expression
		if isinstance(A,exp.Command)and str(A.this).upper()=='SHOW':
			B=str(A.args.get(_G)).strip().lower()
			if B.startswith('parameters'):return parse_one(_F,read=_B)
		return A
	def postprocess_result(H,query,result):
		D=result;C=query;B='TEXT';I={'key':B,'value':B,_E:B,'level':B,'description':B};D.data.rowtype=[]
		for(J,K)in I.items():D.data.rowtype.append({'name':J,'precision':_A,'scale':_A,'type':K,'nullable':_D,'length':_A})
		D.data.rowset=[]
		for(A,L)in H.SUPPORTED_PARAMS.items():
			G=L.get(_E,'');E='';F=G
			if A in C.session.system_state.parameters:F=C.session.system_state.parameters[A];E='SYSTEM'
			if A in C.session.parameters:F=C.session.parameters[A];E='SESSION'
			M=A,F,G,E,'test description ...';D.data.rowset.append(M)
class HandleAlterSession(QueryProcessor):
	REGEX=re.compile('^\\s*ALTER\\s+SESSION\\s+SET\\s+(.+)',flags=re.I)
	def should_apply(A,query):return bool(A.REGEX.match(query.original_query))
	def transform_query(B,expression,query):
		A=expression
		if isinstance(A,exp.Command)and str(A.this).upper()=='ALTER':
			D=str(A.args.get(_G)).strip().lower()
			if D.startswith('session'):
				C=B.REGEX.match(str(A).replace('\n',''))
				if C:B._set_parameters(query,C.group(1))
				return parse_one(_F,read=_B)
		return A
	def _set_parameters(E,query,expression):
		B=parse_comma_separated_variable_assignments(expression)
		for(A,C)in B.items():
			A=A.strip().upper();D=HandleShowParameters.SUPPORTED_PARAMS.get(A)
			if D is _A:return
			query.session.parameters[A]=C
class HandleShowKeys(QueryProcessor):
	REGEX=re.compile('^\\s*SHOW\\s+(IMPORTED\\s+)?KEYS(\\s+.+)?',flags=re.I)
	def should_apply(A,query):return bool(A.REGEX.match(query.original_query))
	def transform_query(B,expression,query):
		A=expression
		if isinstance(A,(exp.Command,exp.Show)):return parse_one(_F,read=_B)
		return A
class HandleShowProcedures(QueryProcessor):
	REGEX=re.compile('^\\s*SHOW\\s+PROCEDURES(\\s+.+)?',flags=re.I)
	def should_apply(A,query):return bool(A.REGEX.match(query.original_query))
	def transform_query(B,expression,query):
		A=expression
		if isinstance(A,(exp.Command,exp.Show)):return parse_one(_F,read=_B)
		return A
class HandleIsArray(QueryProcessor):
	def initialize_db_resources(C,database):A=State.server;B=f"""
        CREATE OR REPLACE FUNCTION {get_canonical_name(_H)} (_input TEXT) RETURNS BOOLEAN
        LANGUAGE plpython3u IMMUTABLE
        AS $$
            from snowflake_local.engine.query_processors import HandleIsArray
            return HandleIsArray.is_array(_input)
        $$;
        """;A.run_query(B,database=database)
	def transform_query(C,expression,**B):A=expression;A=A.transform(convert_function_args_to_variant,_H,**B);return A
	@classmethod
	def is_array(B,_input):A=_input;A=_unwrap_variant_type(A);return isinstance(A,list)
class HandleCreateStage(QueryProcessor):
	REGEX=re.compile('CREATE\\s+(OR\\s+REPLACE\\s+)?(TEMP(ORARY)?\\s+)?STAGE\\s+(\\S+)',flags=re.I)
	def should_apply(A,query):return bool(A.REGEX.match(query.original_query))
	def transform_query(C,expression,**E):
		A=expression
		if isinstance(A,exp.Command)and A.this=='CREATE':D=C.REGEX.match(str(A));B=D.group(4).upper();LOG.info("Processing `CREATE STAGE` query to create stage '%s'",B);return parse_one(f"SELECT 'Stage area {B} successfully created.'",read=_B)
		return A
class HandleDropStage(QueryProcessor):
	REGEX=re.compile('DROP\\s+STAGE\\s+(IF\\s+EXISTS\\s+)?(\\S+)',flags=re.I)
	def should_apply(A,query):return bool(A.REGEX.match(query.original_query))
	def transform_query(B,expression,**E):
		A=expression
		if isinstance(A,exp.Command)and A.this=='DROP':C=B.REGEX.match(str(A));D=C.group(2).upper();return parse_one(f"SELECT '{D} successfully dropped.'",read=_B)
class HandleDollarReferences(QueryProcessor):
	def transform_query(G,expression,**H):
		A=expression
		if not isinstance(A,exp.Select):return A
		D=list(A.find_all(exp.Parameter))
		if not D:return A
		C=A.find(exp.From)
		if not C:return A
		if not C.this.alias:C.this.args['alias']=E=exp.TableAlias();E.args[_C]='_tmp';E.args['columns']=[]
		F=[]
		for B in D:
			if hasattr(B.this,_C)and is_number(str(B.this.this)):F.append(B)
		for B in F:B.replace(exp.Identifier(this=f"_col{B.this.this}"))
		return A
class ConvertIdentifiersToUpper(QueryProcessor):
	def transform_query(H,expression,**I):
		A=expression
		if not config.CONVERT_NAME_CASING:return A
		if isinstance(A,exp.UserDefinedFunction)and isinstance(A.this,exp.Dot):
			if isinstance(A.this.this,str):A.this.args[_C]=get_canonical_name(A.this.this);return A
		if isinstance(A,exp.Anonymous):F=getattr(A.this,_C,A.this);C=get_canonical_name(str(F));G=C.lower()not in INTERNAL_IDENTIFIERS;A.args[_C]=exp.Identifier(this=C,quoted=G);return A
		if not isinstance(A,exp.Identifier):return A
		if'information_schema.'in str(A.parent_select).lower():return A
		if A.quoted:return A
		B=A.parent
		if isinstance(B,exp.LanguageProperty):return A
		if isinstance(B,exp.ColumnDef)and A==B.args.get('kind'):return A
		if isinstance(B,exp.Schema)and A in B.expressions and A.find_ancestor(exp.Drop):return A
		D=str(A.this)
		if'.'in D:return A
		A=A.copy();E=get_canonical_name(D,quoted=False);A.args[_C]=E;A.args['quoted']=E.lower()not in INTERNAL_IDENTIFIERS;return A
	def get_priority(F):from snowflake_local.engine.transforms import AddColumnNamesToTableAliases as A,ConvertArrayFunctionArgTypes as B,ReplaceObjectConstruct as C,ReplaceQuestionMarkPlaceholder as D;E=[A().get_priority(),C().get_priority(),B().get_priority(),D().get_priority()];return min(E)-1
class EncodeMultiDimensionalArraysAsVariant(QueryProcessor):
	def transform_query(E,expression,**F):
		A=expression
		if not isinstance(A,exp.Array):return A
		D=[A for A in A.expressions if isinstance(A,exp.Array)]
		if not D:return A
		def C(obj):
			B=obj;A=str(B)
			if isinstance(B,exp.Array):
				A=[]
				for D in B.expressions:A.append(C(D))
			if isinstance(B,exp.Literal):
				A=B.this
				if B.is_number:
					A=float(B.this)
					if int(A)==A:A=int(A)
			if isinstance(B,exp.Boolean):A=B.this
			if isinstance(B,exp.Null):A=_A
			return A
		B=C(A);B=to_variant(B);return exp.Literal(this=B,is_string=_D)
class HandleArrayExcept(QueryProcessor):
	def initialize_db_resources(D,database):from snowflake_local.engine.postgres.db_engine_postgres import PG_VARIANT_TYPE as A;B=State.server;C=f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name("array_except")}
            (_array {A}, _array_to_exclude {A}) RETURNS {A}
            LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArrayExcept
                return HandleArrayExcept.array_except(_array, _array_to_exclude)
            $$
        """;B.run_query(C,database=database)
	@classmethod
	def array_except(E,_array,_array_to_exclude):
		B=_array;A=_array_to_exclude
		if B is _A or A is _A:return to_variant(_A)
		C=_unwrap_variant_type(B,expected_type=list);A=_unwrap_variant_type(A,expected_type=list)
		for D in A:
			try:C.remove(D)
			except ValueError:pass
		return to_variant(C)
class HandleArrayFlatten(QueryProcessor):
	def initialize_db_resources(D,database):from snowflake_local.engine.postgres.db_engine_postgres import PG_VARIANT_TYPE as A;B=State.server;C=f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name("array_flatten")} (_array {A})
            RETURNS {A} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArrayFlatten
                return HandleArrayFlatten.array_flatten(_array)
            $$
        """;B.run_query(C,database=database)
	@classmethod
	def array_flatten(D,_array):
		A=_array;A=_unwrap_variant_type(A,expected_type=list);C=[]
		for B in A:
			if B is _A:return to_variant(_A)
			if not isinstance(B,list):raise Exception("Not an array: 'Input argument to ARRAY_FLATTEN is not an array of arrays'")
			C.extend(B)
		return to_variant(C)
class HandleArrayGenerateRange(QueryProcessor):
	def initialize_db_resources(E,database):B='array_generate_range';from snowflake_local.engine.postgres.db_engine_postgres import PG_VARIANT_TYPE as A;C=State.server;D=f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name(B)}
            (_start INT, _stop INT) RETURNS {A} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArrayGenerateRange
                return HandleArrayGenerateRange.generate_range(_start, _stop)
            $$;
            CREATE OR REPLACE FUNCTION {get_canonical_name(B)}
            (_start INT, _stop INT, _step INT) RETURNS {A} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArrayGenerateRange
                return HandleArrayGenerateRange.generate_range(_start, _stop, _step)
            $$
        """;C.run_query(D,database=database)
	@classmethod
	def generate_range(B,_start,_stop,_step=1):A=list(range(_start,_stop,_step));return to_variant(A)
class HandleArrayInsert(QueryProcessor):
	def initialize_db_resources(D,database):from snowflake_local.engine.postgres.db_engine_postgres import PG_VARIANT_TYPE as A;B=State.server;C=f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name(_I)}
            (_array {A}, _pos INT, _item {A})
            RETURNS {A} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArrayInsert
                return HandleArrayInsert.array_insert(_array, _pos, _item)
            $$
        """;B.run_query(C,database=database)
	def transform_query(B,expression,query):
		A=expression
		if isinstance(A,exp.Anonymous)and str(A.this).lower()==_I:
			if len(A.expressions)>=3:A.expressions[2]=exp.Anonymous(this='to_variant',expressions=[A.expressions[2]])
		return A
	@classmethod
	def array_insert(D,_array,_pos,_item):
		C=_array;B=_item
		if C is _A:return to_variant(_A)
		A=_unwrap_variant_type(C,expected_type=list);B=_unwrap_variant_type(B)
		while len(A)<_pos:A.append(_A)
		A.insert(_pos,B);return to_variant(A)
class HandleArrayIntersection(QueryProcessor):
	def initialize_db_resources(D,database):from snowflake_local.engine.postgres.db_engine_postgres import PG_VARIANT_TYPE as A;B=State.server;C=f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name("array_intersection")}
            (_array1 {A}, _array2 {A})
            RETURNS {A} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArrayIntersection
                return HandleArrayIntersection.array_intersection(_array1, _array2)
            $$
        """;B.run_query(C,database=database)
	@classmethod
	def array_intersection(E,_array1,_array2):
		B=_array2;A=_array1
		if A is _A or B is _A:return to_variant(_A)
		A=_unwrap_variant_type(A,expected_type=list);B=_unwrap_variant_type(B,expected_type=list);C=[]
		for D in A:
			try:B.remove(D);C.append(D)
			except ValueError:pass
		return to_variant(C)
class HandleArrayMax(QueryProcessor):
	def initialize_db_resources(D,database):from snowflake_local.engine.postgres.db_engine_postgres import PG_VARIANT_TYPE as A;B=State.server;C=f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name("array_max")} (_array {A})
            RETURNS {A} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArrayMax
                return HandleArrayMax.array_max(_array)
            $$
        """;B.run_query(C,database=database)
	@classmethod
	def array_max(C,_array):
		A=_array
		if A is _A:return to_variant(_A)
		A=_unwrap_variant_type(A,expected_type=list);A=[_unwrap_potential_variant_type(A)for A in A];A=[A for A in A if A is not _A]
		if not A:return to_variant(_A)
		try:B=max(A)
		except TypeError:A=[str(A)for A in A];B=max(A)
		return to_variant(str(B))
class HandleArrayMin(QueryProcessor):
	def initialize_db_resources(D,database):from snowflake_local.engine.postgres.db_engine_postgres import PG_VARIANT_TYPE as A;B=State.server;C=f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name("array_min")} (_array {A})
            RETURNS {A} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArrayMin
                return HandleArrayMin.array_min(_array)
            $$
        """;B.run_query(C,database=database)
	@classmethod
	def array_min(C,_array):
		A=_array
		if A is _A:return to_variant(_A)
		A=_unwrap_variant_type(A,expected_type=list);A=[_unwrap_potential_variant_type(A)for A in A];A=[A for A in A if A is not _A]
		if not A:return to_variant(_A)
		try:B=min(A)
		except TypeError:A=[str(A)for A in A];B=min(A)
		return to_variant(str(B))
class HandleArrayPosition(QueryProcessor):
	def initialize_db_resources(D,database):from snowflake_local.engine.postgres.db_engine_postgres import PG_VARIANT_TYPE as A;B=State.server;C=f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name("array_position")}
            (_item {A}, _array {A})
            RETURNS INTEGER LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArrayPosition
                return HandleArrayPosition.array_position(_item, _array)
            $$
        """;B.run_query(C,database=database)
	@classmethod
	def array_position(B,_item,_array):
		A=_array
		if A is _A:return
		A=_unwrap_variant_type(A,expected_type=list)
		try:return A.index(_item)
		except Exception:return
class HandleArrayPrepend(QueryProcessor):
	def initialize_db_resources(D,database):from snowflake_local.engine.postgres.db_engine_postgres import PG_VARIANT_TYPE as A;B=State.server;C=f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name("array_prepend")}
            (_array {A}, _item {A})
            RETURNS {A} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArrayPrepend
                return HandleArrayPrepend.array_prepend(_array, _item)
            $$
        """;B.run_query(C,database=database)
	@classmethod
	def array_prepend(C,_array,_item):
		B=_item;A=_array
		if A is _A:return to_variant(_A)
		B=_unwrap_variant_type(B);A=_unwrap_variant_type(A,expected_type=list);A.insert(0,B);return to_variant(A)
class HandleArrayRemove(QueryProcessor):
	def initialize_db_resources(D,database):from snowflake_local.engine.postgres.db_engine_postgres import PG_VARIANT_TYPE as A;B=State.server;C=f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name("array_remove")}
            (_array {A}, _item {A})
            RETURNS {A} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArrayRemove
                return HandleArrayRemove.array_remove(_array, _item)
            $$
        """;B.run_query(C,database=database)
	@classmethod
	def array_remove(D,_array,_item):
		B=_item;A=_array
		if A is _A:return to_variant(_A)
		B=_unwrap_variant_type(B);A=_unwrap_variant_type(A,expected_type=list);C=[A for A in A if A!=B];return to_variant(C)
class HandleArrayRemoveAt(QueryProcessor):
	def initialize_db_resources(D,database):from snowflake_local.engine.postgres.db_engine_postgres import PG_VARIANT_TYPE as A;B=State.server;C=f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name("array_remove_at")}
            (_array {A}, _position INT)
            RETURNS {A} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArrayRemoveAt
                return HandleArrayRemoveAt.array_remove_at(_array, _position)
            $$
        """;B.run_query(C,database=database)
	@classmethod
	def array_remove_at(D,_array,_position):
		C=_position;B=_array
		if B is _A:return to_variant(_A)
		A=_unwrap_variant_type(B,expected_type=list)
		if C<len(A):A.pop(C)
		return to_variant(A)
class HandleArraySize(QueryProcessor):
	def initialize_db_resources(D,database):from snowflake_local.engine.postgres.db_engine_postgres import PG_VARIANT_TYPE as A;B=State.server;C=f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name("array_size")}
            (_array {A}) RETURNS INT LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArraySize
                return HandleArraySize.array_size(_array)
            $$
        """;B.run_query(C,database=database)
	@classmethod
	def array_size(C,_array):
		A=_array
		if A is _A:return
		B=_unwrap_variant_type(A,expected_type=list);return len(B)
class HandleArraySlice(QueryProcessor):
	def initialize_db_resources(D,database):from snowflake_local.engine.postgres.db_engine_postgres import PG_VARIANT_TYPE as A;B=State.server;C=f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name("array_slice")}
            (_array {A}, _from INT, _to INT)
            RETURNS {A} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArraySlice
                return HandleArraySlice.array_slice(_array, _from, _to)
            $$
        """;B.run_query(C,database=database)
	@classmethod
	def array_slice(D,_array,_from,_to):
		C=_from;B=_array
		if B is _A or C is _A or _to is _A:return to_variant(_A)
		A=_unwrap_variant_type(B,expected_type=list);A=A[C:_to];return to_variant(A)
class HandleArraySort(QueryProcessor):
	def initialize_db_resources(E,database):B='array_sort';from snowflake_local.engine.postgres.db_engine_postgres import PG_VARIANT_TYPE as A;C=State.server;D=f"""
            CREATE OR REPLACE FUNCTION {get_canonical_name(B)} (_array {A})
            RETURNS {A} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArraySort
                return HandleArraySort.array_sort(_array)
            $$;
            CREATE OR REPLACE FUNCTION {get_canonical_name(B)} (_array {A}, _ascending BOOL)
            RETURNS {A} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArraySort
                return HandleArraySort.array_sort(_array, _ascending)
            $$;
            CREATE OR REPLACE FUNCTION {get_canonical_name(B)}
            (_array {A}, _ascending BOOL, _nulls_first BOOL)
            RETURNS {A} LANGUAGE plpython3u IMMUTABLE AS $$
                from snowflake_local.engine.query_processors import HandleArraySort
                return HandleArraySort.array_sort(_array, _ascending, _nulls_first)
            $$
        """;C.run_query(D,database=database)
	@classmethod
	def array_sort(H,_array,_ascending=_D,_nulls_first=_A):
		D=_ascending;C=_array;B=_nulls_first
		if C is _A:return to_variant(_A)
		if B is _A:B=not D
		A=_unwrap_variant_type(C,expected_type=list);A=[_A if A=='null'else A for A in A];E=[A for A in A if A is _A];F=[A for A in A if A is not _A]
		def G(item1,item2):
			B=item1;A=item2
			if is_number(B):
				if is_number(A):return-1 if float(B)<float(A)else 1
				return 1
			if is_number(A):return-1
			return-1 if str(B)<str(A)else 1
		A=sorted(F,key=cmp_to_key(G),reverse=not D)
		if B:A=E+A
		else:A=A+E
		return to_variant(A)