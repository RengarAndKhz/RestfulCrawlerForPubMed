#/usr/local/bin/python

import sys
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

pmid = sys.argv[1]
url = "http://www.ncbi.nlm.nih.gov/pubmed/"+pmid+"?format=xml&report=xml"
r = requests.get(url)
xmlTree = ET.fromstring(r.content)

if r.status_code != 200 :
    print "Errors in getting result"
    exit

articleXml = ET.fromstring('<?xml version="1.0" encoding="utf-8"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'+xmlTree.text.encode('utf-8'))
title=articleXml.find('MedlineCitation').find('Article').find('ArticleTitle')
abstract=articleXml.find('MedlineCitation').find('Article').find('Abstract')
title_text=''
if (title is not None):
    title_text=title.text.encode('utf-8')
abstract_text=''
if (abstract is not None):
    abstract_text=abstract.find('AbstractText').text.encode('utf-8')

print title_text + '\t'+ abstract_text
