# - *- coding: utf-8 - *-

import optparse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote, ParseResult
from functools import reduce
from inspect import isfunction
from typing import Dict, Callable, List, Tuple

from routes import routes
from config import SERVER_HOSTNAME, SERVER_PORT


class MyServer(BaseHTTPRequestHandler):
	def __get_charset(self):
		charset = "utf-8"
		content_type: str | None = self.headers.get("content-type")
		if content_type is not None:
			parts = content_type.split("=")
			if len(parts) == 2:
				charset = parts[-1]
		return charset

	def __write_response(self, http_status: Tuple[int, str, str], result: str | None):
		self.protocol_version = "HTTP/1.1"
		self.send_response(http_status)
		if 400 <= http_status[0] and http_status[0] < 600:
			return
		charset = self.__get_charset()
		mime = self.headers.get("accept")
		if mime is not None:
			self.send_header("Content-type", f"{mime};charset={charset}")
		else:
			self.send_header("Content-type", f"application/json;charset={charset}")
		self.end_headers()
		data = bytes(result, charset)
		self.wfile.write(data)

	def __router(self, parsed_url: ParseResult) -> Callable | None:
		self.__params = list()
		path_chunks = parsed_url.path.split('/')
		def reducer(acc: Dict | Callable | None, curr: str):
			if isfunction(acc) or acc is None:
				return acc
			handler = acc.get(curr)
			if handler is not None:
				return handler
			handler = acc.get("[]")
			if handler is not None:
				self.__params.append(curr)
				return handler
			handler = acc.get("/")
			if handler is not None:
				return handler
			return None
		func = reduce(reducer, path_chunks[1:], routes)
		if isinstance(func, Dict):
			func = func.get('/')
		if not isfunction(func):
			return None
		return func
	
	def __handle(self, method: str, body = None):
		route_handler = self.__router()
		if route_handler is None:
			self.__write_response(HTTPStatus.INTERNAL_SERVER_ERROR, None)
		else:
			parsed_url = urlparse(self.path)
			http_status, result = route_handler(method, self.__params, body, parsed_url=parsed_url)
			self.__write_response(http_status, result)

	def log_request(self, code='-', size='-'):
		if self.path == '/ping':
			return
		super().log_request(code, size)

	def do_GET(self):
		self.__handle("GET")

	def do_POST(self):
		charset = self.__get_charset()
		content_length = self.headers.get("content-length")
		body = None
		if content_length is not None:
			body = self.rfile.read(int(content_length)).decode(charset)
		else:
			body = self.rfile.read().decode(charset)
		body = unquote(body, charset)
		self.__handle("POST", body)


if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option(
		"--hostname",
		help="Hostname for the app " + "[default %s]" % SERVER_HOSTNAME,
		default=SERVER_HOSTNAME
	)
	args, _ = parser.parse_args()

	web_server = HTTPServer((args.hostname, int(SERVER_PORT)), MyServer)
	print("Server started http://%s:%s" % (args.hostname, SERVER_PORT))

	try:
		web_server.serve_forever()
	except KeyboardInterrupt:
		pass

	web_server.server_close()
	print("Server stopped.")
