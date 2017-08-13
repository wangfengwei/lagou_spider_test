# /urs/bin/env python3
#-*- coding:utf-8 -*-

import redis

class UrlManager(object):
	def __init__(self,pool):
		self.r=redis.Redis(connection_pool=pool)

	def get_queue_url(self):
		url=self.r.rpop('url_queue_lagou')
		return url
	
	def add_url(self,url):
		x=self.r.sadd('url_manager',url)
		#去重判断
		if x==0:
			return 'url is repetition'
		else:		
			self.r.lpush('url_queue_lagou',url)

#	def get_queue_urls(self,num=10)
#		pass

#	def add_urls(self,*args):
#		pass
	
	
