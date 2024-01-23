_A='array_cat'
import logging
from enum import Enum
from localstack.utils.collections import ensure_list
from sqlglot import exp
from snowflake_local import config
LOG=logging.getLogger(__name__)
INTERNAL_IDENTIFIERS={'attname','attnum','atttypid','atttypmod','attrelid','arg_min','arg_max','array_agg',_A,'array_size','array_sort','current_database','current_schema','current_task_graphs','format_type','get_path','indisprimary','indkey','indrelid','is_array','lead','oid','parse_json','pg_class','pg_index','pg_attribute','plpython3u','plv8','relname','to_char','to_date'}
class NameType(Enum):DATABASE=0;SCHEMA=1;RESOURCE=2
def convert_function_args_to_variant(expression,function,**F):
	D='to_variant';A=expression
	if not isinstance(A,exp.Func):return A
	C=str(A.this).lower()
	if isinstance(A,exp.ArrayConcat):C=_A
	if C!=function:return A
	for(E,B)in enumerate(A.expressions):A.expressions[E]=exp.Anonymous(this=D,expressions=ensure_list(B))
	if isinstance(A,exp.ArrayConcat):B=A.this;A.args['this']=exp.Anonymous(this=D,expressions=ensure_list(B))
	return A
def is_create_table_expression(expression):A=expression;return isinstance(A,exp.Create)and(B:=A.args.get('kind'))and isinstance(B,str)and B.upper()=='TABLE'
def get_canonical_name(name,type=None,quoted=True):
	E='public';C=quoted;B='"';A=name;A=A.strip()
	if not config.CONVERT_NAME_CASING:
		if type==NameType.DATABASE and not C:return A.lower()
		if'$'in A:return f'"{A}"'
		return A
	if A.startswith(B)and A.endswith(B):return A
	if'.'in A:LOG.info('Found dot in resource name, could hint at a potential name parsing issue: %s',A)
	if A.lower()in INTERNAL_IDENTIFIERS:return A
	if A.startswith(B)and A.endswith(B):return A
	if type in[None,NameType.SCHEMA]and A.lower()==E:return E
	D=A.upper()
	if C:return f'"{D}"'
	return D