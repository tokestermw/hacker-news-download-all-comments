from __future__ import unicode_literals

import io
import unidecode
import ftfy
import urllib2
import json
import datetime
import time
import pytz
# import pandas as pd
import os
import re
# from pandas import DataFrame

from HTMLParser import HTMLParser  # python 2.x

filename = 'hacker_news_comments.txt'

html_parser = HTMLParser()

html_tags = re.compile(r'<.*?>')
square_brackets = re.compile(r'\[.*?\]')

remove_html_tags = lambda x: re.sub(html_tags, " ", x)
remove_square_brackets = lambda x: re.sub(square_brackets, " ", x)

if os.path.isfile(filename):
    os.remove(filename)

ts = str(int(time.time()))
# df = DataFrame()
hitsPerPage = 1000
requested_keys = ["author", "comment_text", "created_at_i", "objectID", "points"]

i = 0

while True:
	with io.open(filename, 'a', encoding='utf8') as f:
	# try:
		url = 'https://hn.algolia.com/api/v1/search_by_date?tags=comment&hitsPerPage=%s&numericFilters=created_at_i<%s' % (hitsPerPage, ts)
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		data = json.loads(response.read())
		last = data["nbHits"] < hitsPerPage
		# data = DataFrame(data["hits"])[requested_keys]
		# df = df.append(data,ignore_index=True)
		# ts = data.created_at_i.min()
		hits = data["hits"]
		print ("query", i, "n hits", len(hits))

		for hit in hits:
			# import pdb
			# pdb.set_trace()
			comment_text = unicode(hit["comment_text"])
			comment_text = comment_text.strip()
			comment_text = html_parser.unescape(comment_text)
			comment_text = remove_html_tags(comment_text)
			comment_text = remove_square_brackets(comment_text)
			comment_text = ftfy.fix_text(comment_text)
			comment_text = unidecode.unidecode(comment_text)
			# comment_text = comment_text.translate(dict.fromkeys([0x201c, 0x201d, 0x2011, 0x2013, 0x2014, 0x2018, 0x2019, 0x2026, 0x2032]))
			comment_text = u" ".join(comment_text.split())
			comment_text = unicode(comment_text)				

			if len(comment_text) == 0:
				continue

			f.write(comment_text)
			f.write(u'\n')

		if (last):
			break
		# if (i % 2 == 0): # We write occasionally
			# update_csv(f, df)
			# df = DataFrame()				

		time.sleep(3.6)
		i += 1

		# except Exception as e:
		# 	print ("Exception")
		# 	import pdb
		# 	pdb.set_trace()
		# 	# print (e)
		# 	raise e