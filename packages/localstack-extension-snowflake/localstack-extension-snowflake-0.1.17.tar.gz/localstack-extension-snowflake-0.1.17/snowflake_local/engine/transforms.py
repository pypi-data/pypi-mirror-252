_U='OBJECT_CONSTRUCT'
_T='SELECT NULL'
_S='expression'
_R='javascript'
_Q='FUNCTION'
_P='columns'
_O='quoted'
_N='SCHEMA'
_M='db'
_L='alias'
_K='is_string'
_J='TABLE'
_I='properties'
_H='postgres'
_G='TEXT'
_F='expressions'
_E='kind'
_D=None
_C=True
_B=False
_A='this'
import datetime,json,logging,re,textwrap
from aenum import extend_enum
from localstack.utils.collections import ensure_list
from localstack.utils.files import chmod_r,new_tmp_file,save_file
from localstack.utils.strings import short_uid,to_bytes
from localstack.utils.time import timestamp
from sqlglot import TokenType,exp,parse_one,tokens
from sqlglot.dialects import Postgres,Snowflake
from snowflake_local import config
from snowflake_local.engine.db_engine import DBEngine,get_db_engine
from snowflake_local.engine.models import Query
from snowflake_local.engine.query_processors import HandleDollarReferences,QueryProcessor
from snowflake_local.engine.session import APP_STATE
from snowflake_local.engine.transform_utils import convert_function_args_to_variant,get_canonical_name,is_create_table_expression
LOG=logging.getLogger(__name__)
TYPE_MAPPINGS={'VARIANT':_G,'OBJECT':_G,'STRING':_G,'UNKNOWN':_G}
ACCOUNT_ID='TESTACC123'
def apply_query_transforms(query):
	A=query;from snowflake_local.engine.query_processors import QueryProcessor as D;B=parse_one(A.query,read='snowflake')
	for C in D.get_instances():
		if C.should_apply(A):B=B.transform(C.transform_query,query=A)
	A.query=B.sql(dialect=_H);return A
def remove_comments(expression,**B):
	A=expression
	if isinstance(A,exp.Comment):return exp.Literal(this='',is_string=_B)
	if A.comments:A.comments=_D
	return A
class RemoveTransientKeyword(QueryProcessor):
	def transform_query(E,expression,**F):
		B=expression
		if not is_create_table_expression(B):return B
		C=B.copy();A=C.args[_I]
		if A:
			if hasattr(A,_F):A=A.expressions
			D=exp.TransientProperty()
			if D in A:A.remove(D)
		return C
class RemoveIfNotExists(QueryProcessor):
	def transform_query(D,expression,**E):
		C='exists';A=expression
		if not isinstance(A,exp.Create):return A
		B=A.copy()
		if B.args.get(C):B.args[C]=_B
		return B
class RemoveCreateOrReplace(QueryProcessor):
	def transform_query(L,expression,query):
		I='replace';F=query;A=expression
		if not isinstance(A,exp.Create):return A
		G=try_get_db_engine()
		if A.args.get(I):
			D=A.copy();D.args[I]=_B;H=str(D.args.get(_E)).upper()
			if G and H in(_J,_Q):
				B=str(D.this.this);C=B.split('.')
				if len(C)>=2:J=get_canonical_name(C[-2]);K=get_canonical_name(C[-1]);B=f"{J}.{K}"
				else:B=get_canonical_name(B)
				E=Query(query=f"DROP {H} IF EXISTS {B}");E.session=F.session;E.database=F.database
				if len(C)>=3:E.database=C[0]
				G.execute_query(E)
			return D
		return A
class ReplaceUnknownTypes(QueryProcessor):
	def transform_query(F,expression,**G):
		A=expression
		for(C,D)in TYPE_MAPPINGS.items():
			E=getattr(exp.DataType.Type,D.upper());B=A
			if isinstance(B,exp.Alias):B=B.this
			if isinstance(B,exp.Cast)and B.to==exp.DataType.build(C):B.args['to']=exp.DataType.build(E)
			if isinstance(A,exp.ColumnDef):
				if A.args.get(_E)==exp.DataType.build(C):A.args[_E]=exp.DataType.build(E)
			if isinstance(A,exp.Identifier)and isinstance(A.parent,exp.Schema):
				if str(A.this).upper()==C.upper():A.args[_A]=D.upper()
		return A
class ReplaceUnknownUserConfigParams(QueryProcessor):
	def transform_query(E,expression,**F):
		A=expression
		if isinstance(A,exp.Command)and str(A.this).upper()=='ALTER':
			C=str(A.expression).strip();D='\\s*USER\\s+\\w+\\s+SET\\s+\\w+\\s*=\\s*[\'\\"]?(.*?)[\'\\"]?\\s*$';B=re.match(D,C,flags=re.I)
			if B:return parse_one(f"SELECT '{B.group(1)}'")
		return A
class ReplaceCreateSchema(QueryProcessor):
	def transform_query(C,expression,query):
		A=expression
		if not isinstance(A,exp.Create):return A
		A=A.copy();B=A.args.get(_E)
		if str(B).upper()==_N:query.database=A.this.db;A.this.args[_M]=_D
		return A
class InsertCreateTablePlaceholder(QueryProcessor):
	def transform_query(C,expression,query):
		A=expression
		if not is_create_table_expression(A):return A
		if isinstance(A.this.this,exp.Placeholder)or str(A.this.this)=='?':A=A.copy();B=query.params.pop(0);A.this.args[_A]=exp.Identifier(this=B,quoted=_B)
		return A
	def get_priority(A):return ReplaceIdentifierFunction().get_priority()-1
class ReplaceIdentifierFunction(QueryProcessor):
	def transform_query(C,expression,**D):
		A=expression
		if isinstance(A,exp.Func)and str(A.this).upper()=='IDENTIFIER'and A.expressions:B=A.expressions[0].copy();B.args[_K]=_B;return B
		return A
	def get_priority(A):return 100
class ReplaceDbReferences(QueryProcessor):
	def transform_query(F,expression,query):
		E='catalog';C=query;A=expression;D=A.args.get(E)
		if isinstance(A,exp.Table)and A.args.get(_M)and D:C.database=D.this;A.args[E]=_D
		if isinstance(A,exp.UserDefinedFunction):
			B=str(A.this).split('.')
			if len(B)==3:A.this.args[_A]=B[1];C.database=B[0]
		return A
class ReplaceCurrentWarehouse(QueryProcessor):
	def transform_query(D,expression,query):
		C=query;A=expression
		if isinstance(A,exp.Func)and str(A.this).upper()=='CURRENT_WAREHOUSE':B=exp.Literal();B.args[_A]=C.session and C.session.warehouse or'TEST';B.args[_K]=_C;return B
		return A
class ReplaceCurrentAccount(QueryProcessor):
	def transform_query(D,expression,**E):
		B=expression;C=['CURRENT_ACCOUNT','CURRENT_ACCOUNT_NAME']
		if isinstance(B,exp.Func)and str(B.this).upper()in C:A=exp.Literal();A.args[_A]=ACCOUNT_ID;A.args[_K]=_C;return A
		if isinstance(B,exp.CurrentUser):A=exp.Literal();A.args[_A]='TEST';A.args[_K]=_C;return A
		return B
class ReplaceCurrentStatement(QueryProcessor):
	def transform_query(C,expression,query):
		A=expression
		if isinstance(A,exp.Func)and str(A.this).upper()=='CURRENT_STATEMENT':B=exp.Literal();B.args[_A]=query.original_query;B.args[_K]=_C;return B
		return A
class ReplaceCurrentTime(QueryProcessor):
	def transform_query(D,expression,**E):
		A=expression
		if isinstance(A,(exp.CurrentTime,exp.CurrentTimestamp)):
			B=exp.Literal();C=timestamp()
			if isinstance(A,exp.CurrentTime):C=str(datetime.datetime.utcnow().time())
			B.args[_A]=C;B.args[_K]=_C;return B
		return A
class UpdateFunctionLanguageIdentifier(QueryProcessor):
	def transform_query(Q,expression,**R):
		L='python';A=expression;M={_R:'plv8',L:'plpython3u'}
		if isinstance(A,exp.Create)and isinstance(A.this,exp.UserDefinedFunction):
			E=A.args[_I];C=E.expressions;B=[A for A in C if isinstance(A,exp.LanguageProperty)]
			if not B:F=exp.LanguageProperty();F.args[_A]='SQL';C.append(F);return A
			G=str(B[0].this).lower();N=G==L
			for(O,H)in M.items():
				if G!=O:continue
				if isinstance(B[0].this,exp.Identifier):B[0].this.args[_A]=H
				else:B[0].args[_A]=H
			I=[];J=[A for A in C if str(A.this).lower()=='handler']
			for K in C:
				if isinstance(K,(exp.LanguageProperty,exp.ReturnsProperty)):I.append(K)
			E.args[_F]=I
			if N and J:P=J[0].args['value'].this;D=textwrap.dedent(A.expression.this);D=D+f"\nreturn {P}(*args)";A.expression.args[_A]=D
		return A
class UpdateIdentifiersInSqlFunctionCode(QueryProcessor):
	def transform_query(G,expression,**H):
		A=expression
		if not isinstance(A,exp.Create)or not isinstance(A.this,exp.UserDefinedFunction):return A
		E=A.args[_I];F=E.expressions;C=[A for A in F if isinstance(A,exp.LanguageProperty)]
		if not C or str(C[0].this).upper()!='SQL':return A
		if not A.expression:return A
		D=str(A.expression)
		if isinstance(A.expression,(exp.Literal,exp.RawString)):D=A.expression.this
		B=Query(query=D);B=apply_query_transforms(B);A.expression.args[_A]=B.query;return A
	def get_priority(A):return UpdateFunctionLanguageIdentifier().get_priority()-1
class ConvertFunctionArgsToLowercase(QueryProcessor):
	def transform_query(H,expression,**I):
		A=expression
		if config.CONVERT_NAME_CASING:return A
		if not isinstance(A,exp.Create):return A
		if not isinstance(A.this,exp.UserDefinedFunction):return A
		D=A.args[_I].expressions;B=[A for A in D if isinstance(A,exp.LanguageProperty)];B=str(B[0].this).lower()if B else _D
		if B not in(_R,'plv8'):return A
		E=[A for A in A.this.expressions if isinstance(A,exp.ColumnDef)]
		for F in E:
			if not A.expression:continue
			C=str(F.this);G=A.expression.this;A.expression.args[_A]=G.replace(C.upper(),C.lower())
		return A
class CreateTmpTableForResultScan(QueryProcessor):
	def transform_query(K,expression,**L):
		A=expression
		if isinstance(A,exp.Func)and str(A.this).upper()=='RESULT_SCAN':
			E=A.expressions[0];F=E.this;B=APP_STATE.queries.get(F)
			if not B:LOG.info("Unable to find state for query ID '%s'",F);return A
			C=new_tmp_file();G=json.dumps(B.result.rows);save_file(C,G);chmod_r(C,511);E.args[_A]=C
			def H(idx,col):B=col;A=B.type_name.upper();A=TYPE_MAPPINGS.get(A)or A;return f"{f'_col{idx+1}'if B.name.lower()=='?column?'else B.name} {A}"
			D=exp.Alias();D.args[_A]=A;I=B.result.columns;J=', '.join([H(A,B)for(A,B)in enumerate(I)]);D.args[_L]=f"({J})";return D
		return A
class RemoveTableClusterBy(QueryProcessor):
	def transform_query(F,expression,**G):
		A=expression
		if is_create_table_expression(A):
			B=A.args[_I]
			if B:D=[A for A in B if not isinstance(A,exp.Cluster)];A.args[_I].args[_F]=D
		elif isinstance(A,exp.Command)and A.this=='ALTER':
			E='(.+)\\s*CLUSTER\\s+BY([\\w\\s,]+)(.*)';C=re.sub(E,'\\1\\3',A.expression,flags=re.I);A.args[_S]=C
			if re.match('\\s*TABLE\\s+\\w+',C,flags=re.I):return parse_one(_T,read=_H)
		return A
class InsertSessionId(QueryProcessor):
	def transform_query(B,expression,query):
		A=expression
		if isinstance(A,exp.Func)and str(A.this).lower()=='current_session':return exp.Literal(this=query.session.session_id,is_string=_C)
		return A
class AdjustCasingOfTableRefs(QueryProcessor):
	def transform_query(D,expression,query):
		A=expression
		if isinstance(A,exp.From):
			B=A.this
			if isinstance(B,exp.Expression)and B.args.get(_M):
				C=B.args[_M]
				if C.args.get(_O):C.args[_O]=_B
		return A
class ReplaceDescribeTable(QueryProcessor):
	def transform_query(G,expression,**H):
		A=expression
		if not isinstance(A,exp.Describe):return A
		C=A.args.get(_E)or _J
		if str(C).upper()==_J:B=A.this.name;B=B and get_canonical_name(B,quoted=_B);D=f"'{B}'"if B else'?';E=f"SELECT * FROM information_schema.columns WHERE table_name={D}";F=parse_one(E,read=_H);return F
		return A
class ReplaceShowEntities(QueryProcessor):
	def transform_query(M,expression,**N):
		E='tables';B=expression
		if not isinstance(B,(exp.Command,exp.Show)):return B
		A=''
		if isinstance(B,exp.Command):
			G=str(B.this).upper()
			if G!='SHOW':return B
			A=str(B.args.get(_S)).strip().lower()
		elif isinstance(B,exp.Show):A=str(B.this).strip().lower()
		A=A.removeprefix('terse').strip()
		if A.startswith('primary keys'):H='\n            SELECT a.attname as column_name, format_type(a.atttypid, a.atttypmod) AS data_type, c.relname AS table_name\n            FROM   pg_index i\n            JOIN   pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)\n            JOIN   pg_class as c ON c.oid = i.indrelid\n            WHERE  i.indisprimary;\n            ';return parse_one(H,read=_H)
		if A.startswith('imported keys'):return parse_one(_T,read=_H)
		D=[];I='^\\s*\\S+\\s+(\\S+)\\.(\\S+)(.*)';F=re.match(I,A)
		if F:D.append(f"table_schema = '{F.group(2)}'")
		if A.startswith(E):C=E
		elif A.startswith('schemas'):C='schemata'
		elif A.startswith('objects'):C=E
		elif A.startswith(_P):C=_P
		elif A.startswith('procedures'):C='routines';D.append("specific_schema <> 'pg_catalog'")
		else:return B
		J=f"WHERE {' AND '.join(A for A in D)}"if D else'';K=f"SELECT * FROM information_schema.{C} {J}";L=parse_one(K,read=_H);return L
class ReplaceQuestionMarkPlaceholder(QueryProcessor):
	def transform_query(B,expression,**C):
		A=expression
		if isinstance(A,exp.Placeholder):return exp.Literal(this='%s',is_string=_B)
		return A
	def get_priority(A):return InsertCreateTablePlaceholder().get_priority()-1
class ReplaceObjectConstruct(QueryProcessor):
	def transform_query(E,expression,**F):
		A=expression
		if isinstance(A,exp.Func)and str(A.this).upper()==_U:
			B=A.args[_F]
			for C in range(1,len(B),2):D=B[C];B[C]=exp.Anonymous(this='to_variant',expressions=ensure_list(D))
		return A
class RenameReservedKeywordFunctions(QueryProcessor):
	def transform_query(E,expression,**F):
		A=expression
		if isinstance(A,exp.Func)and isinstance(A.this,str):
			B={'current_role':'get_current_role'}
			for(C,D)in B.items():
				if str(A.this).lower()==C:A.args[_A]=D
		return A
class ReturnInsertedItems(QueryProcessor):
	def transform_query(B,expression,**C):
		A=expression
		if isinstance(A,exp.Insert):A.args['returning']=' RETURNING 1'
		return A
class RemoveTableFuncWrapper(QueryProcessor):
	def transform_query(D,expression,**E):
		B=expression
		if isinstance(B,exp.Table):
			A=B.this;C=A
			if hasattr(A,_A):C=A.this
			if str(C).upper()==_J:return A.expressions[0]
		return B
	def get_priority(A):return 10
class ConvertArrayAggParams(QueryProcessor):
	def transform_query(F,expression,**G):
		E='from';B=expression
		if not isinstance(B,exp.Select):return B
		C=[A for A in B.expressions if isinstance(A,exp.WithinGroup)];A=_D
		if C:
			if isinstance(C[0].this,exp.ArrayAgg):C[0].args[_A]=f"{get_canonical_name('array_agg_ordered')}()";A=B.args.get(E)
		else:
			D=[A for A in B.expressions if isinstance(A,exp.ArrayAgg)]
			if D:
				A=B.args.get(E)
				if isinstance(A.this,exp.Values)and not A.this.args.get(_L):D[0].args[_A]='_tmp_col1'
		if A and isinstance(A.this,exp.Values)and not A.this.args.get(_L):A.this.args[_L]='_tmp_table(_tmp_col1)'
		return B
class ConvertArrayConstructor(QueryProcessor):
	def transform_query(C,expression,**D):
		A=expression
		if isinstance(A,exp.Array):B=exp.Anonymous(this='ARRAY_CONSTRUCT',expressions=A.expressions);return B
		return A
	def get_priority(A):return 10
class ConvertArrayContainsOperators(QueryProcessor):
	def transform_query(C,expression,**D):
		A=expression
		if isinstance(A,exp.ArrayContains):B=exp.Anonymous(this='ARRAY_CONTAINS',expressions=[A.expression,A.this]);return B
		return A
	def get_priority(A):return 10
class ConvertArrayFunctionArgTypes(QueryProcessor):
	def transform_query(E,expression,**B):
		A=expression;C='array_append','array_cat','array_construct','array_construct_compact','array_contains','array_prepend','array_remove'
		for D in C:A=A.transform(convert_function_args_to_variant,D,**B)
		return A
	def get_priority(B):A=[ConvertArrayContainsOperators().get_priority(),ConvertArrayConstructor().get_priority()];return min(A)-1
class AddAliasToSubquery(QueryProcessor):
	def transform_query(B,expression,**C):
		A=expression
		if isinstance(A,(exp.Subquery,exp.Values)):
			if not A.alias and A.parent_select:A.args[_L]=exp.TableAlias(this=f"_tmp{short_uid()}")
		return A
	def get_priority(A):return ConvertArrayAggParams().get_priority()-1
class AddColumnNamesToTableAliases(QueryProcessor):
	def transform_query(J,expression,**K):
		A=expression
		if not isinstance(A,exp.From):return A
		C=A.this;F=isinstance(C,exp.Table)and isinstance(C.this,exp.Anonymous)and str(C.this.this).lower()=='load_data'
		if not F and not isinstance(A.this,exp.Values):return A
		if not A.parent_select:return A
		G=[]
		for B in A.parent_select.expressions or[]:
			if isinstance(B,exp.Alias):B=B.this
			if isinstance(B,exp.Cast):B=B.this
			if isinstance(B,exp.Identifier):G.append(B.this)
		D=A.this.args.get(_L)
		if not isinstance(D,exp.TableAlias):return A
		H=D.args[_P]=D.columns or[]
		for I in G:
			E=exp.ColumnDef();E.args[_A]=exp.Identifier(this=I,quoted=_B)
			if F:E.args[_E]=exp.DataType.build(_G)
			H.append(E)
		return A
	def get_priority(B):A=[HandleDollarReferences().get_priority(),AddAliasToSubquery().get_priority()];return min(A)-1
class ConvertTimestampTypes(QueryProcessor):
	def transform_query(C,expression,**D):
		A=expression
		if isinstance(A,exp.ColumnDef):
			B=str(A.args.get(_E,'')).upper()
			if B=='TIMESTAMP':A.args[_E]=exp.Identifier(this='TIMESTAMP WITHOUT TIME ZONE',quoted=_B)
		return A
class TrackCaseSensitiveIdentifiers(QueryProcessor):
	def transform_query(I,expression,query):
		D='DATABASE';B=expression;from snowflake_local.engine.postgres.db_state import State
		if isinstance(B,exp.Create):
			C=str(B.args.get(_E)).upper()
			if C in(D,_N,_J):
				A=B
				while isinstance(A.this,exp.Expression):A=A.this
				if A.args.get(_O):E=A.this if C==D else query.database;F=A.this if C==_N else _D;G=A.this if C==_J else _D;H=E,F,G;State.identifier_overrides.entries.append(H)
		return B
class CastParamsForStringAgg(QueryProcessor):
	def transform_query(L,expression,**M):
		E='separator';A=expression
		if not isinstance(A,exp.GroupConcat):return A
		B=''
		def H(expr):
			C=expr;nonlocal B;D=C.this;A=C
			if isinstance(D,exp.Distinct):D=C.this.expressions[0];A=C.this.expressions
			if not isinstance(D,exp.Cast):
				E=exp.Cast();E.args[_A]=D;E.args['to']=exp.DataType.build(_G)
				if isinstance(A,list):
					A[0]=E
					if len(A)>1:F=A.pop(1);B=str(F.this)
				else:A.args[_A]=E
		H(A)
		if A.args.get(E)is _D:A.args[E]=exp.Literal(this=B,is_string=_C)
		if not A.parent_select:return A
		F=isinstance(A.this,exp.Distinct)
		if F:
			G=A.parent_select.find(exp.WithinGroup)
			if G:
				if len(A.this.expressions)!=1:raise Exception(f"Expected a single DISTINCT clause in combination with WITHIN GROUP, got: {A.this.expressions}")
				if isinstance(G.this,exp.GroupConcat):
					I='STRING_AGG_ORDERED_DISTINCT'if F else'STRING_AGG_ORDERED';C=exp.Anonymous(this=I,expressions=G.this.expressions)
					if B:C.args[_F]=[exp.Literal(this=B,is_string=_C)]
					return C
		if not B and A.args.get(E):B=A.args[E].this
		J='STRING_AGG_NOGROUP_DISTINCT'if F else'STRING_AGG_NOGROUP';C=exp.Anonymous(this=J,expressions=ensure_list(A.this))
		if isinstance(C.args[_F][0],exp.Distinct):
			D=C.args[_F][0].expressions
			if isinstance(D,list)and len(D)==1:D=D[0]
			C.args[_F][0]=D
		if B:K=exp.Literal(this=B,is_string=_C);C.args[_F]+=[K]
		return C
class CastParamsForToDate(QueryProcessor):
	def transform_query(C,expression,**D):
		A=expression
		if isinstance(A,exp.Func)and str(A.this).lower()=='to_date':
			A=A.copy();B=exp.Cast();B.args[_A]=A.expressions[0];B.args['to']=exp.DataType.build(_G);A.expressions[0]=B
			if len(A.expressions)<=1:LOG.info('Auto-detection of date format in TO_DATE(..) not yet supported');A.expressions.append(exp.Literal(this='YYYY/MM/DD',is_string=_C))
		return A
class GetAvailableSchemas(QueryProcessor):
	def transform_query(I,expression,query):
		B=query;A=expression
		if isinstance(A,exp.Func)and str(A.this).lower()=='current_schemas':
			C=try_get_db_engine()
			if C:from snowflake_local.engine.postgres.db_engine_postgres import DEFAULT_DATABASE as D;E=Query(query='SELECT schema_name FROM information_schema.schemata',database=B.database);F=B.database or D;G=C.execute_query(E);H=[f"{F}.{A[0]}".upper()for A in G.rows];return exp.Literal(this=json.dumps(H),is_string=_C)
		return A
class FixFunctionCodeEscaping(QueryProcessor):
	def transform_query(C,expression,**D):
		A=expression
		if isinstance(A,exp.Create)and str(A.args.get(_E)).upper()==_Q and isinstance(A.expression,exp.Literal):B=to_bytes(A.expression.this).decode('unicode_escape');A.expression.args[_A]=B
		return A
def try_get_db_engine():
	try:return get_db_engine()
	except ImportError:return
def _patch_sqlglot():
	Snowflake.Parser.FUNCTIONS.pop(_U,_D);Snowflake.Parser.FUNCTIONS.pop('ARRAY_GENERATE_RANGE',_D)
	if len(exp.ArraySort.arg_types)<3:exp.ArraySort.arg_types['nulls_first']=_B
	for A in('ANYARRAY','ANYELEMENT'):
		extend_enum(TokenType,A,A);extend_enum(exp.DataType.Type,A,A);D=getattr(exp.DataType.Type,A);B=getattr(exp.DataType.Type,A);tokens.Tokenizer.KEYWORDS[A]=B
		for C in(Postgres,Snowflake):C.Parser.TYPE_TOKENS.add(B);C.Parser.ID_VAR_TOKENS.add(B);C.Parser.FUNC_TOKENS.add(B);C.Generator.TYPE_MAPPING[D]=A;C.Tokenizer.KEYWORDS[A]=B
_patch_sqlglot()