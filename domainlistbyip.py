import lxml.html
import socket
import json
import requests
from lxml import html
from lxml import etree
class domainlistbyip(object):
    ipaddress = None
    s = requests.session()
    query = ""
    finish_list = []
    root = None
    def run(self):
        
        print "---===---===---===---===---===---===---===---===---===---===---===---===---===---"
        print "---===---===---===---===---===---===---===---===---===---===---===---===---===---"
        
        ipaddr = raw_input("Insert IP address or domain name : ")
        while  not ipaddr :
            ipaddr = raw_input("Insert IP address or domain name : ")
        self.requestip(ipaddr)

    def requestip(self,ipaddr):
        if(ipaddr is None) or (not ipaddr):
            while not ipaddr:
                ipaddr = raw_input("Insert IP address or domain name : ")
            self.requestip(ipaddr) 
        else:
            try:
                ipaddr = socket.gethostbyname(ipaddr)
                self.lookupdomain(ipaddr)
            except:
                self.ip = raw_input("Insert IP address or domain name : ")
                self.requestip(self.ip) 

    def lookupdomain(self,ipaddr):
        print "looking up => " + ipaddr

        try:
            req = requests.session()
            callback = "http://www.bing.com/search?q=ip%3a" + ipaddr
            response = req.get(callback)
            page = html.fromstring(response.text)
            self.root = page
            text = page.xpath("//cite")
            
            for elem in text:
                domain = self.stringreplace(etree.tostring(elem, pretty_print=True))
                print "http://"+domain.replace("\n","")
            page_at = 1
        
            try:
                te = self.root.xpath("//a[@aria-label='Page 2']/text()")
                for t in te:
                    for tt in t:
                        tf = True
                        if tt == "2":
                            self.paginate(page_at,ipaddr)
                        else:
                            print "fuck"
            except:
                tf = False

        except:
            print "fucking failed"
    def paginate(self,pageat,ipaddr):
        count = (pageat * 10)+1

        req = requests.session()
        callback = "http://www.bing.com/search?q=ip%3a" + ipaddr + "&first="+str(count)
        #print callback
        response = req.get(callback)
        page = html.fromstring(response.text)
        self.root = page
        text = page.xpath("//cite")
        for elem in text:
            domain = self.stringreplace(etree.tostring(elem, pretty_print=True))
            try: 
                print "http://"+domain.replace("\n","")
            except:
                error = "no"
        
        try:
            nextpage =pageat+2
            filters = "//a[@aria-label='Page "+str(nextpage)+"']/text()"
            te = self.root.xpath(filters)
            for t in te:
                pageat = pageat + 1
                if t == str(pageat+1):
                    self.paginate(pageat,ipaddr)
                    
                else:
                    print "fuck"
                    
        except:
            tf = False

    def stringreplace(self,text):
        replacement = ['http://','https://','<cite>','</cite>','<strong>','</strong>','\n']
        for r in replacement:
            text = text.replace(r,"")
        return text.split("/")[0]


if __name__ == '__main__':
    domainlistbyip().run()
