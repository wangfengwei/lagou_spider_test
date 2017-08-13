# /usr/bin/env python3
#-*- coding=utf-8 -*-

from multiprocessing import Process
import urls_manager
import time
import urllib
import json
import redis
import urllib.request
import urls_manager,html_download,parser


class SpiderMain(Process):
	def __init__(self,pool):
		super().__init__()
		self.url_manager=urls_manager.UrlManager(pool)
		self.html_download=html_download.HtmlDownload()
		self.parser=parser.Parser()

	def run(self):
		while True:
			url=self.url_manager.get_queue_url()
			if url is not None:
				try:
					html=self.html_download.download(url)
				except:
					print('地址：%s,下载失败' % url)
				self.parser.parser(html)
				time.sleep(3)
			else:
				#服务器可选择continue,url_queue 为空的话进程将等待
				time.sleep(3)
				break
#				continue
		

#向url仓库中添加url
def add_root_url(city,keyword,pool):
	redis=urls_manager.UrlManager(pool)

	data_json=get_json(city,keyword)
	if data_json is None:
		return
	parse_json_addurl(data_json,redis)

	total=(data_json['content']['positionResult']['totalCount'])
	resultSize=(data_json['content']['positionResult']['resultSize'])
	pages=int(total)//int(resultSize)
	if int(total)%int(resultSize)!=0:
		pages=pages+1

	n=2
	while n<=pages:
		time.sleep(2)
		data_json=get_json(city,keyword,n)
		try:
			parse_json_addurl(data_json,redis)
		except:
			time.sleep(5)
			continue

		n=n+1


def get_json(city,keyword,page=1):
	url_city=urllib.parse.quote(city)
	url_keyword=urllib.parse.quote(keyword)
	req=urllib.request.Request('https://www.lagou.com/jobs/positionAjax.json?city='+url_city+'&needAddtionalResult=false&isSchoolJob=0')
	req.add_header('Cookie','user_trace_token=20170526191346-630cb507-4204-11e7-9bb3-525400f775ce; LGUID=20170526191346-630cbb78-4204-11e7-9bb3-525400f775ce; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=73; index_location_city=%E5%8C%97%E4%BA%AC; TG-TRACK-CODE=search_code; X_HTTP_TOKEN=5d75183d2adf3d5b433d13450476db33; JSESSIONID=ABAAABAAAGFABEFCD45F1AE046E575BCC9D226C71CECD3D; SEARCH_ID=614e2372a81c495c8e62d3e4e5587618; _gid=GA1.2.2058702331.1502428711; _ga=GA1.2.1544395687.1495797226; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502503674,1502503682,1502547590,1502587732; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502610648; LGSID=20170813155048-1ec76679-7ffc-11e7-ab97-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%3Fcity%3D%25E5%258C%2597%25E4%25BA%25AC%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E7%2588%25AC%25E8%2599%25AB%3Fcity%3D%25E5%258C%2597%25E4%25BA%25AC%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; LGRID=20170813155048-1ec767f9-7ffc-11e7-ab97-525400f775ce')
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
	req.add_header('Host','www.lagou.com')
	req.add_header('Referer','https://www.lagou.com/jobs/list_'+url_keyword+'?labelWords=&fromSearch=true&suginput=')
	data=urllib.parse.urlencode({'pn':page,'kd':keyword})
	data=data.encode('ascii')
	r=urllib.request.urlopen(req,data)
	if r.getcode()==200:
		try:
			data_json=json.loads(r.read().decode('utf-8'))
		except:
			time.sleep(3)
			data_json=json.loads(r.read().decode('utf-8'))
		return data_json
	else:
		return None

def parse_json_addurl(data_json,redis):
	l=data_json['content']['positionResult']['result']

	url_root='https://www.lagou.com/jobs/'
	for n in l:
		positionId=n['positionId']
		url=url_root+str(positionId)+'.html'
		redis.add_url(url)	

	
#主程序入口
if __name__=='__main__':
	pool=redis.ConnectionPool(host='localhost',port='6379',db=0)
	
	#选择搜索关键字，keyword为空将搜索所以岗位
	city='全国'
	keyword='爬虫'	
	#用于更新url_manager数据的url数据。
#	add_root_url(city,keyword,pool)
	

	#开启5个进程运行爬虫
	for i in range(5):
		p=SpiderMain(pool)
		p.start()
		
	
