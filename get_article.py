#/usr/local/bin/python

import requests
import xml.etree.ElementTree as ET

def getIds( xmlTree ):
    idList = []
    for id in xmlTree.find('IdList').findall('Id'):
        idList.append(id.text)
    return idList

def getQuerySession( xmlTree ):
    return SessionInfo( xmlTree.find('Count').text, xmlTree.find('QueryKey').text, xmlTree.find('WebEnv').text )

class SessionInfo(object):
    count = ""
    queryKey = ""
    webEnv = ""
    def __init__(self, count, queryKey, webEnv):
        self.count = count
        self.queryKey = queryKey
        self.webEnv = webEnv

start_date="2014/10/01"
end_date="2014/10/31"

r = requests.get("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cancer&datetype=mhda&retmax=10&usehistory=y&mindate="+start_date+"&maxdate="+end_date+"&usehistory=y")
xmlTree = ET.fromstring(r.content)

if r.status_code != 200 :
    print "Errors in getting result"
    exit


count = "count"
queryKey = ""
webEnv = ""
session_info = getQuerySession( xmlTree)
print session_info.count
print session_info.queryKey
print session_info.webEnv

idList = getIds(xmlTree)
for id in idList:
    print id

r = requests.get("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?retmode=xml&retmax=2&db=pubmed&retstart=5&query_key="+session_info.queryKey+"&WebEnv="+session_info.webEnv)
print r.content
if r.status_code != 200 :
    print "Errors in getting result"
    exit


