# -*- coding:utf-8 -*-

import lxml
from pymongo import MongoClient
import re
from bs4 import BeautifulSoup
import json
class Parser(object):
	def parser(self,html):
		if html is  None:
			return None
		#采用lxml解析html
		tr=BeautifulSoup(html,'lxml')
		name=tr.find('span',class_='name').get_text()
		company=tr.find('div',class_='company').get_text()
		salary=tr.find('span',class_='ceil-salary').get_text()
		text=tr.find('dd',class_='job_bt').get_text()
		workAddress=tr.find('input',attrs={'name':'workAddress'}).get('value')
		positionAddress=tr.find('input',attrs={'name':'positionAddress'}).get('value')
		addr=workAddress+positionAddress

		data={'company':company,'name':name,'salary':salary,'addr':addr,'text':text}

		json_str=json.dumps(data)
		
		conn=MongoClient('localhost',27017)
		db=conn.test
		db.lagou_spider.insert({'company':company,'name':name,'salary':    salary,'addr':addr,'text':text})

		print('添加数据成功')
