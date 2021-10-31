#!/usr/bin/env python
#step 1 - main functions to get the content from web pages 
import requests, re, os
from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup
#from lxml.html import parse
import time


# url='https://www.australianpotash.com.au/site/content/'
# url='https://www.irmau.com/site/content/'
#url='https://www.1300smiles.com.au/'
#url='https://360capital.com.au/investment-strategies/real-assets/real-estate/'
#url='https://www.adherium.com/'
#url='https://www.1stgrp.com/'
def norm(str0):
  str0=str0.lower().strip()
  normalized=re.sub("\W+","-",str0)
  return normalized.strip("-")
  
class web_page:
  def __init__(self,url):
    self.url=url
    try: self.tld=urlsplit(url).netloc #not sure if it is TLD 
    except: self.tld=""
    self.all_text_items=[self.url,"_br_"] #add the page url and a line break at the beginning of the text items

    self.html_content=""
    self.title=""
    self.text=""
    self.status_code=None
    self.segs=[]
    self.clean_text=""
    self.all_links,self.internal_links,self.externl_links=[],[],[]
    self.meta_content=[]
    try:
      op=requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
      self.status_code=op.status_code
      self.html_content=op.text
      self.html_content=self.html_content.replace("</p>","_br_</p>") #to put a line break at the end of paragraph elements
      self.html_content=self.html_content.replace("<p>","_br_<p>")
      self.html_content=self.html_content.replace("</li>","</li>_br_")
      
      self.html_content=re.sub('(</h\d>)',r'_br_\1',self.html_content)
      self.html_content=re.sub('(<h\d\b.*?>)',r'_br_\1',self.html_content)
      self.html_content=re.sub('(<p\b.*?>)',r'_br_\1',self.html_content)
      self.html_content=re.sub('(<li\b.*?>)',r'_br_\1',self.html_content)
      self.html_content=self.html_content.replace("<br>","_br_")
      soup=BeautifulSoup(self.html_content,features="html.parser")
      if soup==None: return
    except:
      return

    if soup.title: self.title=soup.title.string #Find the title
    self.all_text_items.append(self.title)
    self.all_text_items.append("_br_")


    for script in soup(["script", "style"]):
        script.decompose()
    self.strips = list(soup.stripped_strings)
    
    self.all_text_items.extend(self.strips) #add text strips from page HTML
    self.all_text_items.append("_br_")

    meta_content_found=re.findall('content="(.+?)"', self.html_content)
    self.meta_content=[]
    for mc in meta_content_found:
      if "=" in mc: continue
      self.meta_content.append(mc)
      self.all_text_items.append(mc)
      self.all_text_items.append("_br_")

    #self.all_text_items=[self.url,"_br_"]+self.all_text_items
    #self.all_text_items.append("_br_")

    self.text=" ".join([v for v in self.all_text_items if v])
    #self.text=self.text.replace("_br_","\n")
    self.clean_text=re.sub("[\r\n\r\s]+"," ",self.text).strip() #clean breaks and tabs
    self.clean_text=self.clean_text.replace("_br_","\n")
    self.segs=[v.strip() for v in self.clean_text.split("\n") if v.strip()]
    self.clean_text="\n".join(self.segs)
    self.links_text=[] #links with their text
    links_found=[]
    for link in soup.findAll('a'):
      link_str=link.string
      if link_str: link_str=link_str.strip()
      cur_href=link.get('href')
      if cur_href!=None: 
        links_found.append(cur_href)
        if link_str: self.links_text.append((cur_href,link_str))
    links_found=list(set(links_found))
    self.all_links=[]
    self.internal_links=[]
    self.external_links=[]
    for li in links_found:
      if li.endswith(".js"): continue
      if li.endswith(".css"): continue
      if li.endswith(".png"): continue
      if li.endswith(".pdf"): continue
      if li.startswith("http"): cur_link=li
      else: 
        cur_link=urljoin(self.url,li)
      self.all_links.append(cur_link)
      if self.tld in cur_link: self.internal_links.append(cur_link)
      else: self.external_links.append(cur_link)

def get_bare_url(full_url): #the the top level domain of the url, stripping http, https, www, slash and colons
  bare_url=full_url.replace("http://","").replace("https://","")
  if bare_url.startswith("www."): bare_url=bare_url.replace("www.","")
  if bare_url.startswith("www1."): bare_url=bare_url.replace("www1.","")
  if bare_url.startswith("www2."): bare_url=bare_url.replace("www2.","")  
  bare_url=bare_url.strip("/")
  bare_url=bare_url.split("/")[0]
  bare_url=bare_url.split(":")[0]
  return bare_url

def reverse_url(full_url): #make site.abc.gov.au > au.gov.abc.site to sort by the last part of the url
  bare_url=full_url.replace("http://","").replace("https://","")
  if bare_url.startswith("www."): bare_url=bare_url.replace("www.","")
  if bare_url.startswith("www1."): bare_url=bare_url.replace("www1.","")
  if bare_url.startswith("www2."): bare_url=bare_url.replace("www2.","")  
  url_split=bare_url.split("/")
  first_part=url_split[0]
  second_part="/".join(url_split[1:])
  first_part=".".join(reversed(first_part.split(".")))
  if second_part: r_url=first_part+"/"+second_part #return first_part+"/"+second_part
  else: r_url=first_part #return first_part
  return r_url.strip("/")


def get_content(webpage_url):
  #print(webpage_url)
  cur_page_obj=web_page(webpage_url)
  return "<br>".join(cur_page_obj.segs) 

def file_len(fname): #get the number of lines in the cache file
  try:
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
  except: return 0

if __name__=="__main__":
  print(os.getcwd())
  test_url='https://anteristech.com/news/ASX_SMID_Conference_March21'
  #page_obj=web_page(test_url)
  t0=time.time()
  cur_bare_url=get_bare_url(test_url)
  fopen=open("edu.au.txt")
  for i,f in enumerate(fopen):
    if i>100: break
    url=f.strip("\n\r\t")
    content=get_content(test_url)
    #print(url)
  fopen.close()
  # for _ in range(10):
  #   content=get_content(test_url)
  t1=time.time()
  elapsed=t1-t0

  print(cur_bare_url)
  print(content)  
  print("elapsed",t1-t0)
