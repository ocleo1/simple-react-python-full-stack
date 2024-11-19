from http import HTTPStatus
from urllib.parse import parse_qs, ParseResult
from typing import Any, Tuple

from futu import *


__all__ = ["stocks"]

def get(parsed_url: ParseResult):
	query = parsed_url.query
	mode = ""
	if query != "":
		parsed_query = parse_qs(query)
		if parsed_query["mode"][0] == "closed":
			mode = parsed_query["mode"][0]
	quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)  # 创建行情对象

	ret, data = quote_ctx.get_market_snapshot(['HK.00700'])
	if ret == RET_OK:
		code_list = data['code'].values.tolist()
		name_list = data['name'].values.tolist()
		last_price_list = data['last_price'].values.tolist()
		dividend_ratio_ttm_list = data['dividend_ratio_ttm'].values.tolist()
		print(dividend_ratio_ttm_list)
		dividend_lfy_ratio_list = data['dividend_lfy_ratio'].values.tolist()
		print(dividend_lfy_ratio_list)
	else:
		print('error:', data)

	quote_ctx.close() # 关闭对象，防止连接条数用尽

def stocks(method, *_, **kwargs) -> Tuple[Tuple[int, str, str], Any]:
	if method == "GET":
		parsed_url = kwargs.get('parsed_url')
		return get(parsed_url)
	else:
		return HTTPStatus.METHOD_NOT_ALLOWED, None
