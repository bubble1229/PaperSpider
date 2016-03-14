import random
import base64
import MySQLdb

class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""
    def __init__(self, agents):
        self.agents = agents
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))
		#pass

    def process_request(self, request, spider):
        print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class ProxyMiddleware(object):
	
	def process_request(self, request, spider):
		proxy = self.getIP()
        #proxy = random.choice(PROXIES)
		if proxy['user_pass'] is not None:
			request.meta['proxy'] = "http://%s" % proxy['ip_port']
			encoded_user_pass = base64.encodestring(proxy['user_pass'])
			request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
			print request.headers
			print request.meta
			print "**************ProxyMiddleware have pass************" + proxy['ip_port']
		else:
			print "**************ProxyMiddleware no pass************" + proxy['ip_port']
			request.meta['proxy'] = "http://%s" % proxy['ip_port']
		
	def getIP(self):
		coon = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'root', port = 3306, use_unicode = True, charset = 'utf8')
		cur = coon.cursor()
		coon.select_db('agent_ip')
		cur.execute('SELECT * FROM ips ORDER BY verify_time DESC LIMIT 5')
		result = cur.fetchall()
		randomResult = result[random.randint(0,4)]
		cur.close()
		coon.close()
		p =  {}
		p['ip_port'] = bytes(randomResult[1])+":"+bytes(randomResult[2])
		p['user_pass'] = ''
		#return "{'ip_port':'" + bytes(randomResult[1])+":"+bytes(randomResult[2])+"','user_pass':''}"
		return p
