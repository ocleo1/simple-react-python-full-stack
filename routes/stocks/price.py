import time
import math

from http import HTTPStatus
from urllib.request import Request, urlopen
from typing import Any, Tuple

from utils import build_url


__all__ = ["price"]

def post(body: str):
	stock_codes = body.split(",")
	# http://qt.gtimg.cn/?q=s_hk00700,s_hk09988&_=1598277076735
	host = "qt.gtimg.cn"
	stock_code_query = ",".join(map(lambda code: f"s_hk{str(code).zfill(5)}", stock_codes))
	timestamp = math.floor(time.time() * 1000)
	query = {
		'q': stock_code_query,
		'_': timestamp
	}
	url = build_url(f'http://{host}', '/', query)
	headers = {
		'Host': host,
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'
	}
	req = Request(url=url, headers=headers, method='GET')
	with urlopen(req) as res:
		content_type: str = res.info().get('Content-Type')
		mime, charset = content_type.split(';')
		name, charset = charset.split('=')
		body: str = res.read().decode(charset)
		stocks = body.split(';')
		data = list()
		for stock in stocks:
			if stock.strip() == '':
				continue
			current_price = stock.split('~')[3]
			data.append(current_price)

		return data


def price(method, *args) -> Tuple[Tuple[int, str, str], Any]:
	if method == "POST":
		_, body = args
		return post(body)
	else:
		return HTTPStatus.METHOD_NOT_ALLOWED, None
