from urllib.parse import urlparse, urlunparse, urlencode, unquote
from typing import Dict


'''
https://stackoverflow.com/a/44552191/6277806
'''
def build_url(base_url, path, args_dict = None, need_unquote = False):
	# https://docs.python.org/3.7/library/urllib.parse.html#url-parsing
	url_parts = list(urlparse(base_url))
	url_parts[2] = path
	if isinstance(args_dict, Dict):
		qs = urlencode(args_dict)
		url_parts[4] = qs if need_unquote is False else unquote(qs)
	return urlunparse(url_parts)
