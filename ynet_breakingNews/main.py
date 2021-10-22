import lxml.html
import requests
import logging
import sys, os
import http.server
import socketserver



URL = "http://www.ynet.co.il/Integration/StoryRss2.xml"


def read_url(url=URL):
	res = requests.get(url)
	doc = lxml.etree.fromstring(res.content)
	return doc.xpath("//item")
	


def HTML_table(cells):
	title = description = link = pubDate = guid = tags = ""
	list_html = index_html = ""
	_LIST_HTML = \
		'''
		<tr>
			<td style="border:1px solid red;">{title}</td>
			<td style="border:1px solid red;">{description}</td>
			<td style="border:1px solid red;">{link}</td>
			<td style="border:1px solid red;">{pubDate}</td>
			<td style="border:1px solid red;">{guid}</td>
			<td style="border:1px solid red;">{tags}</td>
		</tr>
		'''
	_INDEX_HTML = \
		'''
		<html>
			<head>
				<meta content="text/html;charset=utf-8" http-equiv="Content-Type">
				<meta content="utf-8" http-equiv="encoding">
				<center>
					<h1>Breaking news<h1>
				</center>
			</head>
			<body>
				<table style="border:1px solid black;border-collapse:collapse;">
					<tr>
					<th style="border:1px solid red;">title</th>
					<th style="border:1px solid red;">description</th>
					<th style="border:1px solid red;">link</th>
					<th style="border:1px solid red;">pubDate</th>
					<th style="border:1px solid red;">guid</th>
					<th style="border:1px solid red;">tags</th>
					</tr>
					{list}
				</table>
			</body>
		</html>
		'''
	lists = []
	for cell in cells:
		title = cell.xpath(".//title/text()")[0]
		description = cell.xpath("./description/text()")[0]
		link = cell.xpath("./link/text()")[0]
		link = f'<a href="url">{link}</a>'
		pubDate = cell.xpath("./pubDate/text()")[0]
		guid = cell.xpath("./guid/text()")[0]
		guid = f'<a href="url">{guid}</a>'
		tags = cell.xpath("./tags/text()")[0]
		list_html = _LIST_HTML.format(
			title=title,
			description=description,
			link=link,
			pubDate=pubDate,
			guid=guid,
			tags=tags
		)
		lists.append(list_html)
	index_html = _INDEX_HTML.format(list='\n'.join(lists))
	return index_html



def parser():
	breaking_news = read_url()
	html_table = HTML_table(breaking_news)
	with open('index.html', 'w+') as writer:
		writer.write(html_table)

class Handler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		os.system("python main.py")
		if self.path == '/':
			self.path = 'index.html'
		return http.server.SimpleHTTPRequestHandler.do_GET(self)


def web():
	server = socketserver.TCPServer(("", 5000), Handler)
	print(f'Starting at http://localhost:5000/')
	server.serve_forever()



if __name__ == '__main__':
	parser()
	web()
