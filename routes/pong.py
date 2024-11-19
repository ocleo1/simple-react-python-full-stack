from http import HTTPStatus


__all__ = ["pong"]

def pong(method, *_):
	if method == "GET":
		return "pong"
	else:
		return HTTPStatus.METHOD_NOT_ALLOWED, None
