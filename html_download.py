# /urs/bin/env python3
#-*- coding:utf-8 -*-

import urllib.request
import time

class HtmlDownload(object):
	def __init__(self):
		pass

	def download(self,url):
		url=url.decode('utf-8')
		req=urllib.request.Request(url)
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36')
		req.add_header('Host','www.lagou.com')
		req.add_header('Upgrade-Insecure-Requests',1)
		req.add_header('Cookie','user_trace_token=20170526191346-630cb507-4204-11e7-9bb3-525400f775ce; LGUID=20170526191346-630cbb78-4204-11e7-9bb3-525400f775ce; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=73; index_location_city=%E5%8C%97%E4%BA%AC; X_HTTP_TOKEN=5d75183d2adf3d5b433d13450476db33; JSESSIONID=ABAAABAAAGFABEFCD45F1AE046E575BCC9D226C71CECD3D; TG-TRACK-CODE=search_code; SEARCH_ID=baa017f759f540828a89b5ca2ec6a701; LGSID=20170813214459-99c410f9-802d-11e7-acad-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F3447938.html; LGRID=20170813214459-99c412f4-802d-11e7-acad-525400f775ce; _ga=GA1.2.1544395687.1495797226; _gid=GA1.2.2058702331.1502428711; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502503674,1502503682,1502547590,1502587732; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502631900')
		r=urllib.request.urlopen(req)
		if r.getcode()==200:
			try:
				return r.read()
			except:
				print('200,但不能读取')
				time.sleep(3)
				return r.read()

		

