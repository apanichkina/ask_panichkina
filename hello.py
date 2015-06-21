def application(environ, start_response):
	output = '<b>Hello world</b>\n<br />'
	if environ['REQUEST_METHOD'] == 'GET':
		output += 'Get query: '
		output += environ['QUERY_STRING']
	else:
		output += 'Post query: '
		try:
			request_body_size = int(environ.get('CONTENT_LENGTH', 0))
		except (ValueError):
			request_body_size = 0
		request_body = environ['wsgi.input'].read(request_body_size)
		output += request_body

	start_response('200 OK', [('Content-type', 'text/html')])
	return [output]
