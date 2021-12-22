import os, time, json, re, sys, math
load_t0=time.time()
import datetime
from cgi import parse_qs
from itertools import groupby
import traceback
import hashlib
import requests
#import Cookie
import smtplib #email libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
from smtplib import SMTP_SSL as SMTP
import uuid


from sqlitedict import SqliteDict #Make sure to install it 
from lxml import html #Make sure to install it 
from bs4 import BeautifulSoup #Make sure to install it 
# import gensim #make sure to install it - also install numpy and pandas - install h5py

#============== Variables ================
#Main variables: posted_data_dict
#qs_dict country domain cat start_i n_results_per_page data_version country_name
#structure_dict parent_list child_dict id_dict description_dict recursive_child_dict cat_list keyword_dict
#country_version_dict country_name_dict
#b2web_model vector_dict
#userid is_admin

sys.path.insert(0, os.path.dirname(__file__))
km_utils_dir='/home/sod9mlnmvhfv/km_code/utils'
sys.path.insert(0,km_utils_dir)
from file_utils import *
from template_utils import *
from extraction_utils import *
from h5py_utils import *
# from classification_utils import *

admin_emails=["kmatters.b2web@gmail.com","b2web@kmatters.com","hmghaly@gmail.com","ahmed.ghaly01@gmail.com"]
admin_password="adminKM"
#admin_emails=["kmatters.b2web@gmail.com","b2web@kmatters.com","hmghaly@gmail.com"]


country_version_dict={} #specifying where is the working version for the AI data for each language
#country_version_dict["au"]="oct21"
#country_version_dict["nz"]="oct21"

country_version_dict["au"]="nov21"
country_version_dict["nz"]="nov21"
country_version_dict["my"]="nov21"

country_name_dict={} #Getting the country name from the country code
country_name_dict["au"]="Australia"
country_name_dict["nz"]="New Zealand"
country_name_dict["my"]="Malaysia"

error="No error"
trace="No trace"



def generate_uuid():
    return uuid.uuid4().hex

def read_file(fpath0):
    fopen0=open(fpath0)
    content0=fopen0.read()
    fopen0.close()
    return content0
def split_list(l, n): #split a list into equally sized sublists
    grp_size=math.ceil(len(l)/n)
    for i0 in range(n): yield l[i0*grp_size:(i0+1)*grp_size]

def soup_replace_by_ids(html_content0,repl_dict0,append=False):
    soup0 = BeautifulSoup(html_content0)
    html_content1=str(soup0)
    for id0,repl_val0 in repl_dict0.items():    
        element0 = soup0.find(id=id0)
        element_str0=str(element0)
        el_tags0=list(re.findall('(<[^<>]*?>)', element_str0))
        new_content0=el_tags0[0]+repl_val0+el_tags0[-1]
        html_content1=html_content1.replace(element_str0,new_content0)
    return html_content1

def create_selection_options(list_vals_labels,selected0=None): # create selection drop down from a list of labels and vals
    cur_dropdown_content=''
    for val0,label0 in list_vals_labels:
        cur_op_tag='<option value="%s">%s</option>'%(val0,label0)
        if val0==selected0: cur_op_tag='<option value="%s" selected>%s</option>'%(val0,label0)
        cur_dropdown_content+=cur_op_tag
    return cur_dropdown_content 

def create_time_str(time_tuple):
    time_str="%s/%s/%s - %s:%s:%s"%(time_tuple[0],time_tuple[1],time_tuple[2],time_tuple[3],time_tuple[4],time_tuple[5])
    return time_str

# sys.path.insert(km_code_dir)
cwd=os.getcwd()
cwd=km_utils_dir

#Interface template directory
version_name="ui3"
interface_dir="../b2web_ui"
dir_path=os.path.join(interface_dir,version_name)



#Data directory
#km_data_dir='/home/sod9mlnmvhfv/km_data'
root_dir='/home/sod9mlnmvhfv/km_data'
km_data_dir='/home/sod9mlnmvhfv/km_data/main'
logs_dir='/home/sod9mlnmvhfv/km_data/logs'

business_dir=os.path.join(root_dir,"business")
if not os.path.exists(business_dir): os.makedirs(business_dir)

#classification structure - json file
txt_dir="../txt"
structure_fname="data_dict.json"
structure_fpath=os.path.join(txt_dir,structure_fname)
structure_content=read_file(structure_fpath)
structure_dict=json.loads(structure_content) 
parent_list=structure_dict["parent_list"]
child_dict=structure_dict["child_dict"]
id_dict=structure_dict["id_dict"]
description_dict=structure_dict["description_dict"] #id_dict description_dict child_dict
recursive_child_dict=structure_dict["recursive_child_dict"]
cat_list=structure_dict["cat_list"]
keyword_dict=structure_dict["keyword_dict"]

# Word2Vec model
wv_fpath=os.path.join(txt_dir,"b2web_au.model")
h5_fpath=os.path.join(txt_dir,"au_wv.hdf5")
# b2web_model = gensim.models.Word2Vec.load(wv_fpath)
h5_fopen = h5py.File(h5_fpath, "r")
vector_dict={} 
vector_dict1={}
for cat0,keywords0 in keyword_dict.items():
    if keywords0==[]: continue
    #tmp_vec0,tmp_wd_vec_dict=get_words_vector(keywords0,b2web_model,excluded_words=[])
    tmp_vec0,tmp_wd_vec_dict=get_h5_words_vec(keywords0,h5_fopen)
    vector_dict[cat0]= tmp_vec0
    #vector_dict1[cat0]= tmp_wd_vec_dict
  

#experiment with new things
# try:
#     pass
#     test_content=""
#     # for k,v in rec_child_dict.items(): 
#     #     test_content+=str(k)+"<br>"
# except Exception as e:
#   error=str(e)
#   trace=traceback.format_exc() results_retrieval(cat, start_i, country,data_version,domain,n_results_per_page,km_data_dir,recursive_child_dict)
def log_something(environ0,log_fpath0,log_content_dict0={}):
    user_ip=environ0.get("REMOTE_ADDR","IP")
    cur_log_dict=dict(log_content_dict0)
    cur_log_dict["IP"]=user_ip
    now = datetime.datetime.now()
    cur_log_dict["time"]=(now.year, now.month, now.day, now.hour, now.minute, now.second)
    log_dir0,log_fname0=os.path.split(log_fpath0)
    if not os.path.exists(log_dir0): os.makedirs(log_dir0)
    log_fopen0=open(log_fpath0,"a")
    log_fopen0.write(json.dumps(cur_log_dict)+"\n")
    log_fopen0.close()
    return True

def hash_password(pwd0):
    pwd0=pwd0.encode('utf-8')
    return hashlib.sha256(pwd0).hexdigest()

def get_time_tuple():
    now = datetime.datetime.now()
    return (now.year, now.month, now.day, now.hour, now.minute, now.second) 
#Email Settings
#email_from="noreply@kmatters.com"


#email_from = "B2WEB Team <noreply@kmatters.com>"
email_from = "B2WEB Team <contact@kmatters.com>"
#email_password="vR};4Ix0*K4o"
#email_password="UylWJ!VKZ-A$"
email_password="V9EF#rzC;h(J"
server_name="mail.kmatters.com"
port=587 #465


def send_email(email_to0,email_subject0,email_html0,email_from0="contact@kmatters.com",email_password0="V9EF#rzC;h(J", from_name0="B2WEB Team",server_name0="a2plcpnl0342.prod.iad2.secureserver.net",port0=465):
    server = SMTP(server_name0)
    server.set_debuglevel(False)
    server.login(email_from0, email_password0)
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = email_subject0 #"Registration Successful!"
    email_from_full = "%s <%s>"%(from_name0,email_from0)
    msg['From'] = email_from_full
    msg['To'] = email_to0
    msg['Message-ID'] = make_msgid()

    email_txt0=email_html0.replace("<br>","\n")

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(email_txt0, 'plain')
    part2 = MIMEText(email_html0, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    #s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    server.sendmail(email_from0, email_to0, msg.as_string())
    server.quit()  
    return str(msg)

def gen_pagination(start_i,n_results_per_page,n_full):
    displayed_pages=[]
    if n_full==0: return displayed_pages
    cur_page_j=int(start_i/n_results_per_page)+1 #if start_i is 20, then we're talking about page 3 (p1: 0, p2: 10, p3: 20)
    last_page_j=math.ceil(n_full/n_results_per_page) #the actual number of result pages is the number of lines of the cat file/n_results per page
    #last_page_i=n_results_per_page*(n_pages-1) #the start_i value for the last page
    next_page_j=cur_page_j+1
    prev_page_j=cur_page_j-1
    #displayed_pages=[prev_page_j,cur_page_j,next_page_j,last_page_j]
    displayed_pages=[cur_page_j,last_page_j]
    if prev_page_j>0: displayed_pages.append(prev_page_j)
    if next_page_j<last_page_j: displayed_pages.append(next_page_j)
    
    for j0 in range(1,4): 
        if j0>last_page_j: continue
        if not j0 in displayed_pages: displayed_pages.append(j0)
    displayed_pages=sorted(list(set(displayed_pages)))
    return displayed_pages



def get_cat_size(cat,domain,country,km_data_dir,data_version,recursive_child_dict): #get recursive size of a category/domain 
    ai_dir=os.path.join(km_data_dir,country,data_version,domain)
    manual_dir=os.path.join(km_data_dir,country,"manual",domain)
    cat_children=recursive_child_dict.get(cat,[[cat,cat]])
    list_cat_ids=[v[0] for v in cat_children]
    if not cat in list_cat_ids: list_cat_ids.append(cat)
    cat_size_dict={}
    total_n_results=0
    total_manual_results=0
    list_manual_fpaths=[]
    list_ai_fpaths=[]
    for cat_id0 in list_cat_ids: #first do manual results
        manual_cat_fpath=os.path.join(manual_dir,cat_id0+".txt")
        tmp_n_results=get_file_n_lines(manual_cat_fpath)
        #cat_size_dict[manual_cat_fpath]=tmp_n_results
        total_manual_results+=tmp_n_results
        total_n_results+=tmp_n_results
        #if tmp_n_results>0: list_manual_fpaths.append(manual_cat_fpath)

    for cat_id0 in list_cat_ids: #then AI results
        cat_fpath=os.path.join(ai_dir,cat_id0+".txt")
        tmp_n_results=get_file_n_lines(cat_fpath)
        cat_size_dict[cat_fpath]=tmp_n_results
        total_n_results+=tmp_n_results
        #if tmp_n_results>0: list_ai_fpaths.append(cat_fpath)
        
    largest_child_cat=max(cat_size_dict.keys(),key=lambda x:cat_size_dict[x])
    num_ai_results_displayed=cat_size_dict[largest_child_cat] #the maximum num of AI results displayed is the size of the largst child category
    full_n_results_displayed=num_ai_results_displayed+total_manual_results
    return full_n_results_displayed

class results_retrieval:
    """docstring for results_retrieval"""
    def __init__(self,cat, start_i, country,data_version,domain,n_results_per_page,km_data_dir,recursive_child_dict):
        ai_dir=os.path.join(km_data_dir,country,data_version,domain)
        manual_dir=os.path.join(km_data_dir,country,"manual",domain)

        t0=time.time()

        cat_children=recursive_child_dict.get(cat,[[cat,cat]])
        list_cat_ids=[v[0] for v in cat_children]
        if not cat in list_cat_ids: list_cat_ids.append(cat)
        cat_size_dict={}
        total_n_results=0
        total_manual_results=0
        list_manual_fpaths=[]
        list_ai_fpaths=[]
        for cat_id0 in list_cat_ids: #first do manual results
            manual_cat_fpath=os.path.join(manual_dir,cat_id0+".txt")
            tmp_n_results=get_file_n_lines(manual_cat_fpath)
            cat_size_dict[manual_cat_fpath]=tmp_n_results
            total_manual_results+=tmp_n_results
            total_n_results+=tmp_n_results
            if tmp_n_results>0: list_manual_fpaths.append(manual_cat_fpath)
        self.list_manual_fpaths=list_manual_fpaths
        self.list_cat_ids=list_cat_ids
        self.cat_size_dict=cat_size_dict #cat_size_dict list_cat_ids

        for cat_id0 in list_cat_ids: #then AI results
            cat_fpath=os.path.join(ai_dir,cat_id0+".txt")
            tmp_n_results=get_file_n_lines(cat_fpath)
            cat_size_dict[cat_fpath]=tmp_n_results
            total_n_results+=tmp_n_results
            if tmp_n_results>0: list_ai_fpaths.append(cat_fpath)
            
        largest_child_cat=max(cat_size_dict.keys(),key=lambda x:cat_size_dict[x])
        num_ai_results_displayed=cat_size_dict[largest_child_cat] #the maximum num of AI results displayed is the size of the largst child category
        full_n_results_displayed=num_ai_results_displayed+total_manual_results
        cat_size_dict["max"]=num_ai_results_displayed
        cat_size_dict["full"]=full_n_results_displayed

        self.n_ai=num_ai_results_displayed
        self.n_manual=total_manual_results
        self.n_full=full_n_results_displayed
        self.manual_dir=manual_dir

        # cat_size_dict["manual"]=total_manual_results
        # cat_size_dict["all"]=total_n_results
        # cat_size_dict["cat_children"]=cat_children
        # cat_size_dict["list_cat_ids"]=list_cat_ids
        # cat_size_dict["list_manual_fpaths"]=list_manual_fpaths
        # cat_size_dict["list_ai_fpaths"]=list_ai_fpaths
        #start_i=0
        self.cur_results=[]
        all_manual=[]
        if start_i<total_manual_results:
            for fpath0 in list_manual_fpaths:
                fopen0=open(fpath0)
                for f0 in fopen0:
                    all_manual.append(f0.strip())
                fopen0.close()
            all_manual.sort()
            self.cur_results.extend(all_manual[start_i:start_i+n_results_per_page])
        self.all_manual=all_manual
        if len(self.cur_results)<n_results_per_page:
            new_start_i=max(0,start_i-len(self.cur_results)) # @start_i=0 > new_start_i=0, start_i=10 > new_start_i=7, start_i=20, new= 17
            remaining_n_results=n_results_per_page-len(self.cur_results)
            ai_combined=[]
            for ai_fpath0 in list_ai_fpaths:
                tmp_ai_lines=get_multiple_lines(new_start_i,n_results_per_page,ai_fpath0)
                ai_combined.extend(tmp_ai_lines)
            ai_combined=list(set(ai_combined))
            if len(list_ai_fpaths)>1: ai_combined.sort() #if we have multiple categories, sort the results alphabetically
            self.cur_results.extend(ai_combined[:remaining_n_results])

        
        t1=time.time()
        self.query_time=t1-t0
        

load_t1=time.time() #Keep track of every time the script is loaded
load_log_dict={}
load_log_dict["elapsed"]=load_t1-load_t0
load_log_dict["message"]="loaded"
now = datetime.datetime.now()
log_fname="%s-%s-%s.txt"%(now.year, now.month, now.day)    
tmp_log_fpath=os.path.join(logs_dir,log_fname)
log_something({},tmp_log_fpath,load_log_dict)

def app(environ, start_response):
    #start_response('200 OK', [('Content-Type', 'text/plain')])
    start_time=time.time()
    start_response('200 OK', [('Content-Type', 'text/html')])
    # message = 'It works!\n'
    # version = 'Python v' + sys.version.split()[0] + '\n'
    # response = '\n'.join([message, version, str(environ)])
    #https://kmatters.com/b2web_dev/about?country=au&admin=true&user=admin&category=accounting-services
    

    #We start by identifying the script name and the query string from the URL
    qs=environ["QUERY_STRING"]
    qs_dict=parse_qs(qs) 
    country=qs_dict.get("country",["au"])[0] 
    domain=qs_dict.get("domain",["com"])[0] 
    cat=qs_dict.get("cat",["electric-maintenance-contracting-services"])[0] 
    start_i_str=qs_dict.get("start_i",["0"])[0]
    start_i=int(start_i_str)
    n_results_str=qs_dict.get("n_results_per_page",["10"])[0]
    n_results_per_page=int(n_results_str)        
    data_version=country_version_dict[country]
    country_name=country_name_dict[country]



    #posted data - data received through POST method
    posted_data=""
    posted_data_dict={}
    if environ['REQUEST_METHOD'] == 'POST': 
        posted_data=environ['wsgi.input'].read().decode("utf-8")
        posted_data_dict=json.loads(posted_data)

    #Cookie data
    #cookie_str=environ["HTTP_COOKIE"] 
    cookie_str=environ.get("HTTP_COOKIE","")
    #parsed_cookie = Cookie.SimpleCookie(cookie_str)

    cookie_split=cookie_str.split(";")
    cookie_dict={}
    # for cookie in parsed_cookie.values():
    #     cookie_dict[cookie.key] = cookie.coded_value 
    for sp in cookie_split:
        key_val=sp.split("=")
        if len(key_val)!=2: continue
        key,val=key_val
        key,val=key.strip(),val.strip()
        cookie_dict[key]=val
    userid=cookie_dict.get("userid","")
    is_admin=False
    if userid in admin_emails: is_admin=True
    #userid=str(cookie_split)




    #Get list of cities in the current country
    locations_fpath=os.path.join(txt_dir,"locations",country+".json")
    city_list=[]
    if os.path.exists(locations_fpath):
        locations_fopen=open(locations_fpath)
        locations_obj=json.load(locations_fopen)
        locations_fopen.close()
        city_list=locations_obj["city_list"]

    #now creating a script name from the URL b2web/index = b2web/about ... etc

    script_url=environ["SCRIPT_URL"].strip("/")
    script_split=script_url.split("/")
    if len(script_split)==1: script_name="intro"
    else: script_name=script_split[-1]

    #page_content="<html><body><h1>Hello World 12345</h1> </body></html>"
    if script_name=="index":
        #country=qs_dict.get("country",["au"])[0]
        cur_fpath=os.path.join(dir_path,"index.html")
        page_content=read_file(cur_fpath)
        page_content=page_content.replace("_country_code_",country)
        page_content=page_content.replace("_country_name_",country_name)

        page_obj=html_page(cur_fpath)
        repl_dict={}

        try:
            soup = BeautifulSoup(page_content)
            page_content=str(soup)

            repl_dict1={}
            
            parent_groups=list(split_list(parent_list,3))
            col_ids=["directory_col1","directory_col2","directory_col3"]
            for col0,grp0 in zip(col_ids,parent_groups):
                element = soup.find(id=col0)
                element_str=str(element)
                el_tags=list(re.findall('(<[^<>]*?>)', element_str))
                new_content=el_tags[0]
                tmp_content=""
                for g0 in grp0:
                    parent_name,parent_id=g0
                    template='<div class="accrodion  "><div class="accrodion-inner"><div class="accrodion-title"><h4><a href="#!"><i class="fa fa-tag"></i> _parent_</a></h4></div><div class="accrodion-content"><div class="inner pricing-one__single "><div class="pricig-body"><ul> _children_</ul></div></div></div></div></div>'
                    template_copy=str(template)
                    template_copy=template_copy.replace("_parent_",parent_name)
                    children_str=""
                    cur_children=child_dict.get(parent_id,[])
                    for child0 in cur_children:
                        child_id,child_name=child0
                        child_link="category?country=%s&domain=com&cat=%s"%(country,child_id)
                        child_template='<li><a href="_link_"><i class="fal fa-check"></i> _child_name_</a></li>'
                        child_template_copy=str(child_template)
                        child_template_copy=child_template_copy.replace("_child_name_",child_name)
                        child_template_copy=child_template_copy.replace("_link_",child_link)
                        children_str+=child_template_copy


                    template_copy=template_copy.replace("_children_",children_str)
                    new_content+=template_copy
                    tmp_content+=template_copy

                new_content+=el_tags[-1]
                repl_dict1[col0]=new_content
                page_content=page_content.replace(element_str,new_content)



            #Updating the dropdown for category select
            repl_dict2={}
            cat_select_id='category_select_dropdown'
            cur_dropdown_list=[["","Business Category"]]+[(v[1],v[0]) for v in cat_list]
            repl_dict2[cat_select_id]=create_selection_options(cur_dropdown_list)
            location_select_id='location_select_dropdown'
            cur_dropdown_list=[["","Nearest City"]]+[(v,v) for v in city_list]
            repl_dict2[location_select_id]=create_selection_options(cur_dropdown_list)

            page_content=soup_replace_by_ids(page_content,repl_dict2)


        except Exception as e:
          error=str(e)
          trace=traceback.format_exc()
          page_content="<html><body><h1>Test Page</h1> Error: %s <br> Trace: %s </body></html>"%(error,trace)        
        #page_content=page_obj.update_replace(repl_dict,"our new title","and a description as well")        

        


    elif script_name=="intro" or script_name=="country" or script_name=="directory":
        cur_fpath=os.path.join(dir_path,"country-selection.html")
        page_content=read_file(cur_fpath)
    elif script_name=="privacy":
        cur_fpath=os.path.join(dir_path,"privacy.html")
        page_content=read_file(cur_fpath)
    elif script_name=="about":
        cur_fpath=os.path.join(dir_path,"about.html")
        template_content=read_file(cur_fpath)
        filler_fpath=os.path.join(dir_path,"about-content.txt")
        filler_content=read_file(filler_fpath)
        filler_content=filler_content.replace("\n","<br>")
        filler_content=filler_content.replace("><br>",">")
        repl_dict2={"main_content":filler_content}
        page_content=soup_replace_by_ids(template_content,repl_dict2)


        #page_content=read_file(cur_fpath)
    elif script_name=="terms":
        # cur_fpath=os.path.join(dir_path,"terms.html")
        # page_content=read_file(cur_fpath)
        cur_fpath=os.path.join(dir_path,"about.html")
        template_content=read_file(cur_fpath)
        filler_fpath=os.path.join(dir_path,"tc-content.txt")
        filler_content=read_file(filler_fpath)
        filler_content=filler_content.replace("\n","<br>")
        filler_content=filler_content.replace("><br>",">")
        repl_dict2={"main_content":filler_content}
        page_content=soup_replace_by_ids(template_content,repl_dict2)

    elif script_name=="inspect":

        #cat="electric-maintenance-contracting-services"
        #?country=au&domain=com&cat=electric-maintenance-contracting-services&start_i=50&n_results=10
        ai_dir=os.path.join(km_data_dir,country,data_version,domain)
        manual_dir=os.path.join(km_data_dir,country,"manual",domain)
        cat_fpath=os.path.join(ai_dir,cat+".txt")
        cat_fpath=os.path.join(manual_dir,cat+".txt")
        manual_cat_fpath=os.path.join(manual_dir,cat+".txt")
        info_dict_path=os.path.join(km_data_dir,country,"info_dict.sqlite")

        t0=time.time()
        mydict = SqliteDict(info_dict_path, autocommit=True)

        num_lines=get_file_n_lines(cat_fpath)
        m_lines=get_multiple_lines(start_i,n_results_per_page,cat_fpath)
        results_list=[]
        for line_item in m_lines:
            out=mydict.get(line_item)
            results_list.append(out)
        # for tmp_line in m_lines:
        #     corr=mydict.get(tmp_line,"")
        #     results_list.append(tmp_line,corr)
        #test=mydict.get("au.com.hydraulicresource")
        t1=time.time()
        elapsed=t1-t0
        #print(m_lines,num_lines, t1-t0)

        page_content='<html><body><h1>Inspect Page</h1>'
        page_content+="Working directory: %s <br>"%ai_dir
        page_content+="cat_fpath: %s <br>"%cat_fpath
        page_content+="num_lines: %s <br>"%num_lines
        page_content+="elapsed: %s seconds<br>"%elapsed
        #page_content+="test: %s<br>"%str(test)
        for item in results_list:
            local_dict=json.loads(item)
            cur_url='<a href="%s" target="new">%s</a>'%(local_dict.get("url",""),local_dict.get("url",""))
            top_words_list=local_dict.get("top_words",[])

            cur_description=" ".join(top_words_list)
            cur_result=cur_url + " "+ cur_description
            #page_content+=str(item) +"<br>"
            #page_content+=cur_url +"<br>"
            page_content+=cur_result +"<br>"
        # for line_item in m_lines:
        #     #page_content+=str(line_item) +"<br>"
        #     out=mydict.get(line_item)
        #     page_content+=str(out) +"<br>"
        page_content+='</body></html>'
        mydict.close()


        #page_content="<html><body><h1>Inspect Page</h1> Working dir: %s </body></html>"%working_dir
        # cur_fpath=os.path.join(dir_path,"terms.html")
        # page_content=read_file(cur_fpath)

    elif script_name=="inspect2":

        #cat="electric-maintenance-contracting-services"
        #?country=au&domain=com&cat=electric-maintenance-contracting-services&start_i=50&n_results=10
        #cur_cat="plant-farming"
        #cur_cat="media-entertainment"
        test=get_cat_size(cat,domain,country,km_data_dir,data_version,recursive_child_dict)

     
        cat_res_dict={}
        res_obj=results_retrieval(cat, start_i, country,data_version,domain,n_results_per_page,km_data_dir,recursive_child_dict)
        cat_res_dict["cur_results"]=res_obj.cur_results
        cat_res_dict["n_full"]=res_obj.n_full
        cat_res_dict["n_manual"]=res_obj.n_manual
        cat_res_dict["query_time"]=res_obj.query_time
        cat_res_dict["test-cat"]=test
        cat_res_dict["all_manual"]=res_obj.all_manual
        cat_res_dict["manual_dir"]=res_obj.manual_dir
        cat_res_dict["list_manual_fpaths"]=res_obj.list_manual_fpaths
        cat_res_dict["cat_size_dict"]=res_obj.cat_size_dict
        cat_res_dict["list_cat_ids"]=res_obj.list_cat_ids

        #cat_size_dict list_cat_ids

        
        
        
        pagination1=gen_pagination(start_i,n_results_per_page,res_obj.n_full)
        cat_res_dict["pagination"]=pagination1

        page_content=str(cat_res_dict)

    elif script_name=="category":
        repl_dict1={}
        cur_fpath=os.path.join(dir_path,"category.html")
        page_content=read_file(cur_fpath)
        page_content=page_content.replace("_country_code_",country)
        page_content=page_content.replace("_country_name_",country_name)
        #populating tabs
        domains=["com","gov","edu","org"]
        for dom0 in domains:
            #updating tab links
            page_content=page_content.replace("_%s_link_"%dom0,"category?country=%s&domain=%s&cat=%s"%(country,dom0,cat))
            cur_dom_cat_count=get_cat_size(cat,dom0,country,km_data_dir,data_version,recursive_child_dict)
            repl_key=dom0+"_category_count" #updating category count in this domain
            repl_dict1[repl_key]="(%s)"%cur_dom_cat_count
        
        #Populating category name and description
        cat_name=id_dict.get(cat,cat) #First get cat name and descriptions
        cat_description=description_dict.get(cat, cat_name)
        cur_children=child_dict.get(cat,[])
        repl_dict1["cat_name"]=cat_name
        repl_dict1["cat_description"]=cat_description +" in %s"%country_name 
        child_link_list=[]
        for child_cat_id,child_cat_name in cur_children:
            link_href="category?country=%s&cat=%s"%(country,child_cat_id)
            cur_link='<a href="%s"> %s </a>'%(link_href,child_cat_name)
            child_link_list.append(cur_link)
        subcategory_content=""
        if child_link_list: subcategory_content+="Websites shown below reflect all of the following subcategories. Click on each subcategory for more focused results.<br>"
        subcategory_content+=" - ".join(child_link_list)

        repl_dict1["cat_children"]= subcategory_content#" - ".join(child_link_list) #str(cur_children)
        #cat_children      

        #Now getting the actual results
        t0=time.time() # Start running the actual query
        cat_res_dict={} #to get the query results: just the list of website IDs
        res_obj=results_retrieval(cat, start_i, country,data_version,domain,n_results_per_page,km_data_dir,recursive_child_dict)
        cat_res_dict["cur_results"]=res_obj.cur_results
        cat_res_dict["n_full"]=res_obj.n_full
        cat_res_dict["n_manual"]=res_obj.n_manual

        cur_page_j=int(start_i/n_results_per_page)+1

        #cat_res_dict["query_time"]=res_obj.query_time
        # cat_res_dict["test-cat"]=test
        pagination1=gen_pagination(start_i,n_results_per_page,res_obj.n_full)
        cat_res_dict["pagination"]=pagination1
        info_dict_path=os.path.join(km_data_dir,country,"info_dict.sqlite") #now we get the info from each result
        mydict = SqliteDict(info_dict_path, autocommit=True) 
        results_list=[]
        for line_item in res_obj.cur_results:
            out=mydict.get(line_item,"{}")
            tmp_out_dict=json.loads(out)
            tmp_out_dict["id"]=line_item
            out=json.dumps(tmp_out_dict)
            results_list.append(out)
        mydict.close()
        t1=time.time()
        elapsed=t1-t0

        #Now we start populating the results content in the results section
        user_allowed=True #check if the user is allowed to view results
        if userid=="" and cur_page_j>3: 
            user_allowed=False
            pagination1=gen_pagination(0,n_results_per_page,res_obj.n_full)



        results_content=""
        for r0, item in enumerate(results_list):
            if not user_allowed: continue
            local_dict=json.loads(item)
            cur_url=local_dict.get("url","")
            found_title=local_dict.get("title",cur_url)
            cur_id=local_dict.get("id","")
            cur_title=cur_url
            cur_title=cur_title.replace("http://","").replace("https://","")
            #cur_url='<a href="%s" target="new">%s</a>'%(local_dict.get("url",""),local_dict.get("url",""))
            top_words_list=local_dict.get("top_words",[])

            preds_list=local_dict.get("top_preds",[])
            preds_dict=dict(iter([v[:2] for v in preds_list]))
            cur_score=preds_dict.get(cat,0)

            keywords_str="<b>Keywords:</b> "+" ".join(top_words_list)
            #keywords_str+="- <b>score</b>: %s"%cur_score #temporary

            cur_description=local_dict.get("description","")
            if found_title: cur_description=found_title+" - "+ cur_description
            if len(top_words_list)>0 and len(cur_description.strip())<30: cur_description=keywords_str

            result_number=start_i+r0 #start_i is the index of the first result - r0 is how many results after that link_id

            link_id="r"+str(result_number)

            remove_link=''
            if is_admin: remove_link='<a href="javascript:void(0);" name="%s" class="remove_result" onclick="remove_website(this)"> <i class="fa fa-times"></i> </a>'%cur_id


            cur_template='<blockquote><p><a rel="nofollow" href="_url_" class="results_link" id="_link_id_" target="new"> _title_ </a> _remove_link_</p><cite>_description_</cite></blockquote>'
            #<a href="javascript:void(0);" class="remove_result"> <i class="fa fa-times"></i> </a>
            cur_template_copy=cur_template.replace("_url_",cur_url).replace("_title_",cur_title).replace("_description_",cur_description).replace("_link_id_",link_id).replace("_remove_link_",remove_link)
            results_content+=cur_template_copy+"\n"

        if not user_allowed: results_content="Please Login to view more results."
        repl_dict1["result_list"]=results_content #id_dict description_dict child_dict

        #Now doing the pagination

        pagination_content=""
        link_template="category?country=%s&domain=%s&cat=%s&start_i=_s_i_"%(country,domain,cat)
        #link_template_copy=link_template.replace("_s_i_","20")
        #pagination_content+='<a href="%s">02</a>'%link_template_copy
        pagination_content=str(pagination1)
        pagination_content=""
        cur_page_j=int(start_i/n_results_per_page)+1
        for i0,pag_j0 in enumerate(pagination1):
            if i0>0 and pag_j0>pagination1[i0-1]+1: pagination_content+=" ... "
            if pag_j0==cur_page_j: pagination_content+='<span class="current">%s</span>'%pag_j0
            else: 
                pag_i0=n_results_per_page*(pag_j0-1) #get the start_i of the pagination page from the pagination j
                link_template_copy=link_template.replace("_s_i_",str(pag_i0))
                pagination_content+='<a href="%s">%s</a>'%(link_template_copy,pag_j0)

        
        repl_dict1["pagination"]=pagination_content





        page_content=soup_replace_by_ids(page_content,repl_dict1)

        #Updating the dropdown for category select
        repl_dict2={}
        cat_select_id='category_select_dropdown'
        cur_dropdown_list=[["","Business Category"]]+[(v[1],v[0]) for v in cat_list]
        repl_dict2[cat_select_id]=create_selection_options(cur_dropdown_list)
        location_select_id='location_select_dropdown'
        cur_dropdown_list=[["","Nearest City"]]+[(v,v) for v in city_list]
        repl_dict2[location_select_id]=create_selection_options(cur_dropdown_list)

        page_content=soup_replace_by_ids(page_content,repl_dict2)
        
        page_title=cat_description +" in %s"%country_name #Now updating page title and description
        page_description=page_title+ " - B2WEB directory listing of business websites for industries and service providers"
        new_title="<title>"+page_title+"</title>" 
        new_description='<meta name="description" content="%s">'%page_description #"<title>"+title+"</title>" 
        page_content=re.sub('(?i)<title.+?/title>',new_title,page_content)
        #page_content=page_content.replace('<meta content="" name="description"/>',new_description)
        #page_content=re.sub('(?i)<meta name="description".+?>',new_description,page_content)
    # elif script_name=="w2v":
    #     query_word="glass"
    #     query_word=qs_dict.get("word",[query_word])[0]
    #     try: similar=b2web_model.wv.most_similar(query_word)
    #     except: similar=[]
    #     page_content=str(similar)
    elif script_name=="profile":
        cur_fpath=os.path.join(dir_path,"about.html")
        template_content=read_file(cur_fpath)

        # filler_fpath=os.path.join(dir_path,"about-content.txt")
        # filler_content=read_file(filler_fpath)
        # filler_content=filler_content.replace("\n","<br>")
        # filler_content=filler_content.replace("><br>",">")
        submissions_content='<table class="table" border="1">'
        line='<tr><td>'+'</td><td>'.join(["url","title","description","category","status"])+'</td></tr>'
        submissions_content+=line

        if userid!="":
            business_dir=os.path.join(root_dir,"business")
            if not os.path.exists(business_dir): os.makedirs(business_dir)          
            user_submissions_dict_path=os.path.join(business_dir,"user-submissions.sqlite")
            mydict = SqliteDict(user_submissions_dict_path, autocommit=True)
            cur_submissions=mydict.get(userid,[])
            
            #submission_dict_path=os.path.join(business_dir,"pending.sqlite") #we will need to change this to submissions.sqlite
            submission_dict_path=os.path.join(business_dir,"submissions.sqlite")
            
            submission_dict = SqliteDict(submission_dict_path, autocommit=True)
            for sub_id in cur_submissions:
                cur_obj_str=submission_dict.get(sub_id,"{}")
                #line=cur_obj_str
                try:
                    cur_obj_dict=json.loads(cur_obj_str)
                    url0=cur_obj_dict.get("url","")
                    title0=cur_obj_dict.get("title","")
                    description0=cur_obj_dict.get("description","")
                    cat0=cur_obj_dict.get("cat","")
                    status0=cur_obj_dict.get("status","")
                    line='<tr><td>'+'</td><td>'.join([url0,title0,description0,cat0,status0])+'</td></tr>'
                except:
                    line='<tr><td>%s</td><td>%s</td></tr>'%(sub_id,cur_obj_str)
                submissions_content+=line
                #submissions_content+=cur_obj+"<br>"
            submission_dict.close()
            submissions_content+="</table>"

            #mydict[cur_user_email]=cur_submissions#found_submissions+[submission_id]
            mydict.close()  
            #submissions_content=str(cur_submissions)

        repl_dict2={}
        repl_dict2["main_content"]="Profile"
        repl_dict2["about_content"]="<h2>My Submissions</h2>"+submissions_content


        page_content=soup_replace_by_ids(template_content,repl_dict2) 
    
    elif script_name=="send_click": #logging all the clicks
        cur_dict={}
        cur_dict["message"]="success"
        cur_dict["success"]=True
        clicks_dir=os.path.join(root_dir,"clicks")
        if not os.path.exists(clicks_dir): os.makedirs(clicks_dir)
        clicks_log_path=os.path.join(clicks_dir,"clicks_log.txt")
        log_something(environ,clicks_log_path,posted_data_dict)        
        page_content=json.dumps(cur_dict)


    elif script_name=="verify": #verify that en email is valid
        cur_dict={}
        cur_dict["message"]="success"
        cur_dict["success"]=True
        cur_email=qs_dict.get("email",[""])[0] #we will need to fix this for all qs_dict instances - just get the string not a list
        if cur_email!="":
            user_dir=os.path.join(root_dir,"users")
            user_dict_path=os.path.join(user_dir,"user_dict.sqlite")
            user_dict = SqliteDict(user_dict_path, autocommit=True)
            #cur_dict["message"]="test: "+cur_email
            check_user_entry=user_dict.get(cur_email,"{}")
            check_user_entry_dict=json.loads(check_user_entry)
            is_already_verified=check_user_entry_dict.get("verified",False)
            if is_already_verified: cur_dict["message"]+= " - already verified"
            check_user_entry_dict["verified"]=True
            user_dict[cur_email]=json.dumps(check_user_entry_dict)

            user_dict.close()
        else:
            cur_dict["message"]="no email provided to verify"
            cur_dict["success"]=False





        #user_dir=os.path.join(root_dir,"users") user_dict_path=os.path.join(user_dir,"user_dict.sqlite") user_dict = SqliteDict(user_dict_path, autocommit=True) check_user_entry=user_dict.get(signup_email) 

        # clicks_dir=os.path.join(root_dir,"clicks")
        # if not os.path.exists(clicks_dir): os.makedirs(clicks_dir)
        # clicks_log_path=os.path.join(clicks_dir,"clicks_log.txt")
        # log_something(environ,clicks_log_path,posted_data_dict)        
        page_content=json.dumps(cur_dict)        

    elif script_name=="approve": #approve website submission
        cur_dict={}
        cur_dict["message"]="success"
        cur_dict["success"]=True
        submission_id=posted_data_dict.get("id")
        cur_cat=""
        cur_description=""
        cur_domain=""
        cur_country=""
        cur_url=""
        user_email=""
        country_domain=""

        submission_obj={}
        if submission_id==None:
            cur_dict["message"]="No submission ID"
            cur_dict["success"]=False
        else:           
            #cur_url_id=qs_dict.get("url",[""])[0]
            cur_cat=posted_data_dict.get("cat","")
            cur_description=posted_data_dict.get("description","")#qs_dict.get("country",[""])[0]
            cur_title=posted_data_dict.get("title","")#qs_dict.get("country",[""])[0]
        if cur_cat=="":
            cur_dict["message"]="No category specified"
            cur_dict["success"]=False
        if cur_description=="":
            cur_dict["message"]="Please add description"
            cur_dict["success"]=False
        if cur_title=="":
            cur_dict["message"]="Please add title"
            cur_dict["success"]=False
        if cur_dict["success"]:
            business_dir=os.path.join(root_dir,"business")
            if not os.path.exists(business_dir): os.makedirs(business_dir)

            pending_fpath=os.path.join(business_dir,"pending.txt") #remove the website from pending submissions
            # pending_fopen=open(pending_fpath,"a")
            # pending_fopen.write(submission_id+"\n")
            # pending_fopen.close()
            #submission_dict_path=os.path.join(business_dir,"pending.sqlite")
            submission_dict_path=os.path.join(business_dir,"submissions.sqlite")
            submission_dict = SqliteDict(submission_dict_path, autocommit=True)
            submission_obj_str=submission_dict.get(submission_id,"{}")
            submission_obj=json.loads(submission_obj_str)
            submission_dict.close()
            cur_dict["submission"]=submission_obj

            # business_log_path=os.path.join(business_dir,"approved_business_log.txt")
            # log_something(environ,business_log_path,json_dict) 
            # manual_domain_dir=os.path.join(km_data_dir,cur_country,"manual",cur_domain) #log submission
            # if not os.path.exists(manual_domain_dir): os.makedirs(manual_domain_dir)
            # cat_fpath=os.path.join(manual_domain_dir,cur_cat+".txt")
            # insert_sorted(cur_rev_url,cat_fpath,line_size=100)
            # info_dict_path=os.path.join(km_data_dir,cur_country,"info_dict.sqlite")
            # mydict = SqliteDict(info_dict_path, autocommit=True)
            # mydict[cur_rev_url]=info_json_obj
            # mydict.close()
        if submission_obj=={}:
            cur_dict["message"]="No submission info"
            cur_dict["success"]=False
        if cur_dict["success"]:
            submission_obj["cat"]=cur_cat #update category and description as necessary by admins
            submission_obj["description"]=cur_description
            submission_obj["title"]=cur_title
            cur_domain=submission_obj.get("domain","com")  #adjust
            cur_country=submission_obj.get("country","")
            cur_url=submission_obj.get("url","")
            user_email=submission_obj.get("user_email","") #
            cur_rev_url=reverse_url(cur_url)
            country_domain=cur_rev_url.split(".")[0]
            if cur_country=="" and country_domain in list(country_name_dict.keys()): cur_country= country_domain


        if cur_country=="":
            cur_dict["message"]="No country info "+country_domain
            cur_dict["success"]=False
        if user_email=="":
            cur_dict["message"]="No user email info"
            cur_dict["success"]=False

        if cur_dict["success"]: #if all info is provided correctly
            manual_domain_dir=os.path.join(km_data_dir,cur_country,"manual",cur_domain) #log submission
            if not os.path.exists(manual_domain_dir): os.makedirs(manual_domain_dir)
            cat_fpath=os.path.join(manual_domain_dir,cur_cat+".txt")
            
            insert_sorted(cur_rev_url,cat_fpath,line_size=100)
            info_dict_path=os.path.join(km_data_dir,cur_country,"info_dict.sqlite")
            mydict = SqliteDict(info_dict_path, autocommit=True)
            submission_obj["status"]="approved"
            submission_obj["approved_time"]=get_time_tuple()
            mydict[cur_rev_url]=json.dumps(submission_obj) 
            mydict.close()
            
            submission_dict = SqliteDict(submission_dict_path, autocommit=True)
            submission_dict[submission_id]=json.dumps(submission_obj)
            submission_dict.close()

            #user_email

            #add the website to the approved file - remove from pending file
            approved_fpath=os.path.join(business_dir,"approved.txt")
            submission_obj["id"]=submission_id
            approved_fopen=open(approved_fpath,"a")
            approved_fopen.write(json.dumps(submission_obj)+"\n")
            approved_fopen.close()


            remove_line(submission_id,pending_fpath)
            
            
            #send email to submitter
            cat_name=id_dict.get(cur_cat,cur_cat) 
            country_name=country_name_dict.get(cur_country,cur_country)
            cat_country_full="%s in %s"%(cat_name,country_name)
            cur_href='http://kmatters.com/b2web/category?country=%s&domain=com&cat=%s'%(cur_country,cur_cat)
            cat_hyperlink='<a href="%s">%s</a>'%(cur_href,cat_country_full)
            email_subject1="Submission approved at B2WEB - %s"%cur_url
            email_content1="""Hello,<br>Congratulations! Your website submission to B2WEB was approved. Here are the details:<br><br>
            Your Website Address: %s <br>
            B2B Website Category: %s <br><br>

            Thank you for your interest in joining B2WEB and for enriching our platform with your valuable business,<br>
            For any questions, please email us at b2web@kmatters.com<br><br>
            Best regards,<br>
            B2WEB Team 
            """%(cur_url,cat_hyperlink) 
            send_email(user_email,email_subject1,email_content1)
            #send_email()      

        
        # clicks_dir=os.path.join(root_dir,"clicks")
        # if not os.path.exists(clicks_dir): os.makedirs(clicks_dir)
        # clicks_log_path=os.path.join(clicks_dir,"clicks_log.txt")
        # log_something(environ,clicks_log_path,posted_data_dict)        
        page_content=json.dumps(cur_dict) 

    elif script_name=="delete": #delete website from category
        cur_dict=dict(posted_data_dict)

        cur_dict["user_email"]=userid
        cur_country=cur_dict.get("country")
        cur_id=cur_dict.get("id")
        cur_domain=cur_dict.get("domain")
        cur_cat=cur_dict.get("cat")
        out_dict={}
        #ai_dir=os.path.join(km_data_dir,cur_country,data_version,domain)
        out_dict["message"]="Not Removed"
        out_dict["success"]=False
        
        if cur_country!=None and cur_id!=None and cur_domain!=None and cur_cat!=None:
            # info_dict_path=os.path.join(km_data_dir,cur_country,"info_dict.sqlite") #now we get the info from each result
            # mydict = SqliteDict(info_dict_path, autocommit=True)
            # item_info=mydict.get(cur_id,"{}")
            # out_dict=json.loads(item_info)
            # mydict.close()
            data_version=country_version_dict[cur_country]
            ai_dir=os.path.join(km_data_dir,cur_country,data_version,domain)
            cat_fpath=os.path.join(ai_dir,cur_cat+".txt")
            deletions_fpath=os.path.join(km_data_dir,cur_country,"deleted.txt")
            #if not os.path.exists(deletions_dir): os.makedirs(deletions_dir)
            #log_something(cur_dict)
            if os.path.exists(cat_fpath): 
                log_something(environ,deletions_fpath,cur_dict)
                remove_line(cur_id,cat_fpath)
                out_dict["path"]=cat_fpath
                out_dict["id"]=cur_id
                out_dict["message"]="Sent successfully to removal - please refresh"
                out_dict["success"]=True
        #cur_email=qs_dict.get("email")
        
        # clicks_dir=os.path.join(root_dir,"clicks")
        # if not os.path.exists(clicks_dir): os.makedirs(clicks_dir)
        # clicks_log_path=os.path.join(clicks_dir,"clicks_log.txt")
        # log_something(environ,clicks_log_path,posted_data_dict)        
        page_content=json.dumps(out_dict) 

    elif script_name=="check_entry": #check website information
        cur_dict={}
        cur_dict["message"]="success"
        cur_dict["success"]=True
        cur_email=qs_dict.get("email")
        # info_dict_path=os.path.join(km_data_dir,cur_country,"info_dict.sqlite") #now we get the info from each result
        # mydict = SqliteDict(info_dict_path, autocommit=True)
        # item_info=mydict.get(cur_id,"{}")
        # out_dict=json.loads(item_info)
        # mydict.close() 

        page_content=json.dumps(cur_dict) 

    elif script_name=="update": #update website information
        cur_dict={}
        cur_dict["message"]="success"
        cur_dict["success"]=True
        cur_email=qs_dict.get("email")
        
        # clicks_dir=os.path.join(root_dir,"clicks")
        # if not os.path.exists(clicks_dir): os.makedirs(clicks_dir)
        # clicks_log_path=os.path.join(clicks_dir,"clicks_log.txt")
        # log_something(environ,clicks_log_path,posted_data_dict)        
        page_content=json.dumps(cur_dict) 

    elif script_name=="cat_vec":
        #vector_dict tmp_vec0,tmp_wd_vec_dict=get_words_vector(keywords0,b2web_model,excluded_words=[])

        # test_json='{"business_name":"vxcv","business_email":"ab@dd.com","business_url":"https://www.packagingdirect.com.au/","business_category":"food-beverages-packaging","business_location":"Albury, New South Wales","business_description":"Located in Brisbane, Packaging Direct provides the Australian hospitality industry schools, corporate functions and anyone having a celebration/party with a wide variety of high-quality catering supplies.","country":"au","user_email":"test@test.com"}'
        # if posted_data: test_json=posted_data
        # json_dict=json.loads(test_json)
        
        query="cattle sheep"
        query=qs_dict.get("query",[query])[0]
        posted_query=posted_data_dict.get("query")
        if posted_query!=None: query=posted_query

        
        #query=posted_data_dict.get("query",query)
        query_words=re.findall("\w+",query)

        #query_words=[query_word]
        #query_vec0,query_wd_vec_dict=get_words_vector(query_words,b2web_model,excluded_words=[])
        query_vec0,query_wd_vec_dict=get_h5_words_vec(query_words,h5_fopen)
        tmp_cat_list=[]
        for cat0, cat_vec0 in vector_dict.items():
            score0=cos_sim(query_vec0,cat_vec0)
            cat_name=id_dict.get(cat0)
            if cat_name==None: continue
            tmp_cat_list.append((str(cat0),cat_name,round(float(score0),3) ))
        tmp_cat_list.sort(key=lambda x:-x[-1])
        # tmp_content="You searched for: %s <br>"%str(query_words)
        # for a0,b0 in tmp_cat_list[:10]:
        #   tmp_content+="<b>%s</b>: %s<br>"%(a0,round(b0,3))

        json_content=json.dumps(tmp_cat_list[:10])

        # cur_url=json_dict.get("business_url","")        
        # query_word="glass"
        # query_word=qs_dict.get("word",[query_word])[0]
        # try: similar=b2web_model.wv.most_similar(query_word)
        # except: similar=[]
        page_content=json_content#tmp_content #str(tmp_cat_list)
        searches_dir=os.path.join(root_dir,"searches")
        if not os.path.exists(searches_dir): os.makedirs(searches_dir)
        searches_log_path=os.path.join(searches_dir,"searches_log.txt")

        log_something(environ,searches_log_path,{"query":query})

        #signup_user
    elif script_name=="signup_user":
        output={}
        output["message"]="success"
        output["success"]=True        
        #posted_email=posted_data_dict.get("email")
        signup_password=posted_data_dict.get("password","")
        signup_email=posted_data_dict.get("email","")
        signup_name=posted_data_dict.get("name","User")
        signup_password=str(signup_password).strip()
        signup_email=str(signup_email).strip()
        hashed_password=""
        if signup_password=="" or signup_email=="":
            output["message"]="No email or no password"
            output["success"]=False
        else:
            hashed_password=hash_password(signup_password)

        #if email is found  
        user_dir=os.path.join(root_dir,"users") #user_dir=os.path.join(root_dir,"users") user_dict_path=os.path.join(user_dir,"user_dict.sqlite") user_dict = SqliteDict(user_dict_path, autocommit=True) check_user_entry=user_dict.get(signup_email) 
        if not os.path.exists(user_dir): os.makedirs(user_dir)
        user_dict_path=os.path.join(user_dir,"user_dict.sqlite")
        user_log_path=os.path.join(user_dir,"user_log.txt")

        user_dict = SqliteDict(user_dict_path, autocommit=True)
        check_user_entry=user_dict.get(signup_email) 
        if check_user_entry!=None:
            output["message"]="User with the same email already exists"
            output["success"]=False            



        if output["success"]:
            posted_data_dict.pop("password",None)
            posted_data_dict.pop("password2",None)
            posted_data_dict["hashed_password"]=hashed_password
            now = datetime.datetime.now()
            posted_data_dict["time"]=(now.year, now.month, now.day, now.hour, now.minute, now.second)
            user_dict[signup_email]=json.dumps(posted_data_dict)
            log_something(environ,user_log_path,posted_data_dict)
            email_subject1="Welcome to B2WEB"
            email_content1="""
            Hello %s,<br>Welcome to B2WEB, the first AI-powered webscale business directory. <br>

            Please verify your email by clicking on this link: <a href="http://kmatters.com/b2web/verify?email=%s">Verify Email</a><br>

            Visit our website any time: <a href="http://kmatters.com/b2web">B2WEB Directory</a> <br>
            Make sure to bookmark the website to easier future access. <br>

            For any questions, please email us at b2web@kmatters.com <br>

            Best Regards,<br>
            KMatters B2WEB Team
            """%(signup_name,signup_email)

            send_email(signup_email,email_subject1,email_content1)

        
        user_dict.close()

        output["email"]=signup_email
        page_content=json.dumps(output)#str(recursive_child_dict)#+"<br><br>"+str(child_dict)

    elif script_name=="login_user":
        output={}
      
        #posted_email=posted_data_dict.get("email")
        login_password=posted_data_dict.get("password")
        login_email=posted_data_dict.get("email")

        # login_email="cc@cc.cc"
        # login_password="123"
        login_password=str(login_password).strip()
        login_email=str(login_email).strip()

        hashed_login_password=hash_password(login_password)
        output["email"]=login_email

        hashed_admin_password=hash_password(admin_password)



        user_dir=os.path.join(root_dir,"users")
        if not os.path.exists(user_dir): os.makedirs(user_dir)
        user_dict_path=os.path.join(user_dir,"user_dict.sqlite")
        login_log_path=os.path.join(user_dir,"login_log.txt")

        user_dict = SqliteDict(user_dict_path, autocommit=True)
        check_user_entry=user_dict.get(login_email,"{}")
        check_user_entry=json.loads(check_user_entry)
        output["check_user_entry"]=check_user_entry
        stored_hashed_password= check_user_entry.get("hashed_password") 
        # stored_password= check_user_entry.get("password") 
        # test_hash_stored=hash_password(stored_password)
        # output["test_hash_stored"]=test_hash_stored

        if stored_hashed_password==hashed_login_password or hashed_login_password==hashed_admin_password:
            output["message"]="success"
            output["success"]=True   
            log_something(environ,login_log_path,{"email":login_email})
        else:
            output["message"]="Invalid Username or Password"
            output["success"]=False
        user_dict.close()                      

        page_content=json.dumps(output)

    elif script_name=="send_feedback":
        output={}
        feedback_email=posted_data_dict.get("email")
        feedback_name=posted_data_dict.get("name")
        feedback_message=posted_data_dict.get("message")

        output["message"]="success"
        output["success"]=True   
        output["name"]=feedback_name   
        output["email"]=feedback_email
        feedback_dir=os.path.join(root_dir,"feedback")
        if not os.path.exists(feedback_dir): os.makedirs(feedback_dir)
        feedback_log_path=os.path.join(feedback_dir,"feedback_log.txt")
        log_something(environ,feedback_log_path,posted_data_dict)

        email_subject1="Feedback from user %s - %s"%(feedback_name,feedback_email)
        recepients=admin_emails+[feedback_email]
        email_content1="""
        This is a notification that we received the following feedback from user: %s - %s <br>
        <b>Message:</b>: <br>====<br> %s <br>====<br>
        Best Regards, <br> B2WEB Team

        """%(feedback_name,feedback_email,feedback_message)

        sent_msg=send_email("kmatters.b2web@gmail.com",email_subject1,email_content1)
        sent_msg=send_email(feedback_email,email_subject1,email_content1)
        output["sent_msg"]=sent_msg
        #admin_emails


        page_content=json.dumps(output)
    elif script_name=="traffic_overview":
        file_list=os.listdir(logs_dir)
        file_list.sort()
        #tmp_content="<html><body>"
        tmp_content="<h2>Select which day</h2>"
        for fname in file_list:
            just_date=fname.split(".")[0]
            href="traffic?day="+just_date
            tmp_content+='<a href="%s">%s</a><br>'%(href,just_date)

        #tmp_content+="</body></html>"
        #page_content=tmp_content #json.dumps(output)
        
        cur_fpath=os.path.join(dir_path,"dashboard-template.html")
        template_content=read_file(cur_fpath)
        repl_dict2={"main_content":tmp_content}
        page_content=soup_replace_by_ids(template_content,repl_dict2) 


    elif script_name=="traffic":
        #output={}
        #output["title"]="Traffic Dashboard"
        #logs_dir=os.path.join(root_dir,"logs")
        day=qs_dict.get("day",[""])[0]
        #fname="2021-11-25.txt"
        fname=day+".txt"
        fpath=os.path.join(logs_dir,fname)
        cur_list=[]
        fopen=open(fpath)
        for line in fopen:
            line=line.strip()
            if line=="": continue
            line_dict=json.loads(line)
            cur_ip=line_dict.get("IP")
            cur_time=line_dict.get("time")
            qs=line_dict.get("qs",{})
            cat=qs.get("cat",[""])[0]
            country=qs.get("country",[""])[0]
            domain=qs.get("domain",[""])[0]
            start_i=qs.get("start_i",[""])[0]
            script_url=line_dict.get("script_url")


            cur_list.append((cur_ip,cur_time,cat,country,domain,start_i,script_url))
        cur_list.sort()
        grouped=[(key,[v[1:] for v in list(group)]) for key,group in groupby(cur_list,lambda x:x[0])]
        #content="<html><body><table>"
        tmp_content="<table>"
        for ip0,grp in grouped:
            ip_rquest_url="https://geolocation-db.com/json/%s&position=true"%ip0
            loc_str='<a href="%s" target="new">Where?</a>'%ip_rquest_url
            # response = requests.get(ip_rquest_url).json()
            # country_name=response.get("country_name","")
            # city_name=response.get("city","")
            # loc_str="%s, %s"%(city_name,country_name)


            tmp_content+="<tr><td><h2>%s</h2></td><td>%s</td></tr>"%(ip0,loc_str)
            for gr in grp:
                cur_list=list(gr)
                time_tuple=cur_list[0]
                time_str="%s/%s/%s - %s:%s:%s"%(time_tuple[0],time_tuple[1],time_tuple[2],time_tuple[3],time_tuple[4],time_tuple[5])
                cur_list[0]=time_str
                tmp_content+="<tr><td>"+"</td><td>".join([str(c0) for c0 in cur_list])+"</td></tr>"
        tmp_content+="</table>"


        fopen.close()
        #output["ip_list"]=cur_list

        #page_content=content #json.dumps(output)
        cur_fpath=os.path.join(dir_path,"dashboard-template.html")
        template_content=read_file(cur_fpath)
        repl_dict2={"main_content":tmp_content}
        page_content=soup_replace_by_ids(template_content,repl_dict2) 

    # elif script_name=="send_email":
    #     #vR};4Ix0*K4o noreply@kmatters.com a2plcpnl0342.prod.iad2.secureserver.net 465
    #     email_to1="champolu.game@gmail.com"
    #     email_subject1="Testing"
    #     email_html_content1="Testing Email Function - from KMatters"
    #     message="Hello"
    #     #send_email(email_to1,email_subject1,"",email_html_content1,email_from="noreply@kmatters.com",email_password="vR};4Ix0*K4o",server_name="mail.kmatters.com",port=25)
    #     send_email(email_to1,email_subject1,"",email_html_content1,email_from="noreply@kmatters.com",email_password="vR};4Ix0*K4o",server_name="a2plcpnl0342.prod.iad2.secureserver.net",port=465)

        # try:
        #     send_email(email_to1,email_subject1,email_html_content1,email_html_content="",email_from="noreply@kmatters.com",email_password="vR};4Ix0*K4o",server_name="mail.kmatters.com",port=25):
        #     message="Sent Successfully"
        # except Exception as e:
        #     error=str(e)
        #     trace=traceback.format_exc()
        #     message= "%s - %s"%(error,trace)
        #page_content=message #"email sent" #str(recursive_child_dict)#+"<br><br>"+str(child_dict)

    elif script_name=="json":
        page_content=str(recursive_child_dict)#+"<br><br>"+str(child_dict)

    elif script_name=="environ":
        page_content=str(environ)#+"<br><br>"+str(child_dict)

    elif script_name=="logging":
        user_ip=environ.get("REMOTE_ADDR","IP")
        cur_log_dict=dict(posted_data_dict)
        cur_log_dict["IP"]=user_ip
        now = datetime.datetime.now()
        cur_log_dict["time"]=(now.year, now.month, now.day, now.hour, now.minute, now.second)
        log_fname="%s-%s-%s.txt"%(now.year, now.month, now.day)
        log_dir=os.path.join(km_data_dir,"logs")
        if not os.path.exists(log_dir): os.makedirs(log_dir)

# except Exception as e:
#   error=str(e)
#   trace=traceback.format_exc() results_retrieval(cat, start_i, country,data_version,domain,n_results_per_page,km_data_dir,recursive_child_dict)


        log_fpath=os.path.join(log_dir,log_fname)
        #cur_log_dict["path"]=log_fpath
        outcome={}
        cur_log_content_dict={"something":123,"also":"what"}
        error,trace="",""
        try: success=log_something(environ,log_fpath,cur_log_content_dict)
        except Exception as e: 
            error=str(e)
            trace=traceback.format_exc()

            success=False
        outcome["success"]=success
        outcome["trace"]=trace
        outcome["error"]=error

        #print(now.year, now.month, now.day, now.hour, now.minute, now.second)

        #page_content=str(cur_log_dict)#+"<br><br>"+str(child_dict)
        #page_content=json.dumps(cur_log_dict)#+"<br><br>"+str(child_dict)
        page_content=json.dumps(outcome)#+"<br><br>"+str(child_dict)
        


    elif script_name=="stdin":
        #page_content=str(std_in)#+"<br><br>"+str(child_dict)
        #cur_stdin_dict=get_stdin()
        #print(str(environ))
        #cur_stdin_dict=environ['wsgi.input'].read()
        #page_content="<html><body><h1>Standard Input</h1> Testing </body></html>"
        page_content=str(posted_data)

    elif script_name=="add_business":
        test_json='{"business_name":"vxcv","business_email":"ab@dd.com","business_url":"https://www.packagingdirect.com.au/","business_category":"food-beverages-packaging","business_location":"Albury, New South Wales","business_description":"Located in Brisbane, Packaging Direct provides the Australian hospitality industry schools, corporate functions and anyone having a celebration/party with a wide variety of high-quality catering supplies.","country":"au","user_email":"test@test.com"}'
        if posted_data: test_json=posted_data
        json_dict=json.loads(test_json)
        cur_url=json_dict.get("business_url","")
        cur_country=json_dict.get("country","")
        cur_business_email=json_dict.get("business_email","")
        cur_user_email=json_dict.get("user_email","")

        cur_cat=json_dict.get("business_category","")
        cur_loc=json_dict.get("business_location","") #we will need to adjust to multiple locations
        info_json_dict={}
        info_json_dict["url"]=cur_url
        info_json_dict["title"]=json_dict.get("business_name","")        
        info_json_dict["description"]=json_dict.get("business_description","")
        info_json_dict["business_email"]=cur_business_email
        info_json_dict["user_email"]=cur_user_email
        info_json_dict["submitted_time"]=get_time_tuple()
        info_json_dict["cat"]=cur_cat
        info_json_dict["loc"]=[cur_loc]
        info_json_dict["action"]="add"
        info_json_dict["manual"]=True
        info_json_dict["country"]=cur_country
        info_json_dict["status"]="submitted"
        #info_json_dict["submitted_time"]=get_time_tuple()
        


        
        
        #cur_loc=json_dict.get("business_location","")
        
        cur_domain="com"
        bare_url=get_bare_url(cur_url)
        url_split=bare_url.split(".")
        if len(url_split)>2 and url_split[-2].lower() in ["org"]: cur_domain=url_split[-2].lower() #adjust govt ac .. etc
        if len(url_split)>2 and url_split[-2].lower() in ["gov","govt"]: cur_domain="gov"
        if len(url_split)>2 and url_split[-2].lower() in ["edu","ac"]: cur_domain="edu"
        cur_rev_url=reverse_url(cur_url.lower())
        
        info_json_dict["domain"]=cur_domain
        info_json_dict["url_id"]=cur_rev_url
        submission_id=generate_uuid()

        info_json_obj=json.dumps(info_json_dict)

        #TODO - check country domain of the submission to match the intended country
        
        #Instead of adding the website directly to the backend, it will go through the approval process
        # if False: #directly add to the backend - not activated
        #     manual_domain_dir=os.path.join(km_data_dir,cur_country,"manual",cur_domain) #log submission
        #     if not os.path.exists(manual_domain_dir): os.makedirs(manual_domain_dir)
        #     cat_fpath=os.path.join(manual_domain_dir,cur_cat+".txt")
        #     insert_sorted(cur_rev_url,cat_fpath,line_size=100)
        #     info_dict_path=os.path.join(km_data_dir,cur_country,"info_dict.sqlite")
        #     mydict = SqliteDict(info_dict_path, autocommit=True)
        #     mydict[cur_rev_url]=info_json_obj
        #     mydict.close()





        business_dir=os.path.join(root_dir,"business")
        if not os.path.exists(business_dir): os.makedirs(business_dir)
        business_log_path=os.path.join(business_dir,"added_business_log.txt")
        log_something(environ,business_log_path,json_dict) 
        pending_fpath=os.path.join(business_dir,"pending.txt") #Add the website to pending submissions
        pending_fopen=open(pending_fpath,"a")
        pending_fopen.write(submission_id+"\n")
        pending_fopen.close()
        #submission_dict_path=os.path.join(business_dir,"pending.sqlite")
        submission_dict_path=os.path.join(business_dir,"submissions.sqlite")
        mydict = SqliteDict(submission_dict_path, autocommit=True)
        mydict[submission_id]=info_json_obj
        mydict.close()

        user_submissions_dict_path=os.path.join(business_dir,"user-submissions.sqlite")
        mydict = SqliteDict(user_submissions_dict_path, autocommit=True)
        cur_submissions=mydict.get(cur_user_email,[])+[submission_id]
        mydict[cur_user_email]=cur_submissions#found_submissions+[submission_id]
        mydict.close()        





        #Now sending an email with the notification
        email_to1=cur_user_email
        email_subject1="Website Submission to B2WEB Directory: "+cur_url[:20]
        email_html1="""Hello,<br>
        This is a notification that you have submitted the following website to B2WEB directory:<br>%s<br>
        You will be notified with the progress, verification and approval of your submission. Meanwhile, you can continue browing the directory at 
        <a href="http://kmatters.com/b2web">B2WEB</a><br><br>
        Best Regards, <br> B2WEB Team
        """%(cur_url)

        send_email(email_to1,email_subject1,email_html1)  

        page_content=info_json_obj
# cur_url=local_dict.get("url","")
#             cur_title=local_dict.get("title",cur_url)
#             #cur_url='<a href="%s" target="new">%s</a>'%(local_dict.get("url",""),local_dict.get("url",""))
#             top_words_list=local_dict.get("top_words",[])

#             preds_list=local_dict.get("top_preds",[])
#             preds_dict=dict(iter([v[:2] for v in preds_list]))
#             cur_score=preds_dict.get(cat,0)

#             keywords_str="<b>Keywords:</b> "+" ".join(top_words_list)
#             keywords_str+="- <b>score</b>: %s"%cur_score #temporary

#             cur_description=local_dict.get("description",keywords_str)
    elif script_name=="pending": #The dashboard for submitted websites currently pending
        business_dir=os.path.join(root_dir,"business")
        pending_fpath=os.path.join(business_dir,"pending.txt")
        pending_content=read_file(pending_fpath)
        pending_items=reversed(pending_content.split("\n"))
        
        #submission_dict_path=os.path.join(business_dir,"pending.sqlite")
        submission_dict_path=os.path.join(business_dir,"submissions.sqlite")
        mydict = SqliteDict(submission_dict_path, autocommit=True)
        #mydict[cur_rev_url]=info_json_obj
        
        # tmp_content='<html><head>'
        # tmp_content+="""
        # <meta charset="utf-8">
        # <meta name="viewport" content="width=device-width, initial-scale=1">
        # <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        # <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        # <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
        # <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        # <script src="../b2web_ui/js/script.js"></script>
        # <script src="../b2web_ui/js/b2web.js"></script>
        # """
        #tmp_content+='</head>'
        #tmp_content+='<body>'
        tmp_content='<h3 class="text-center">Pending Website Submissions</h3><hr>' 
        #tmp_content+='<table border="1">'       
        for item_id in pending_items:
            if item_id.strip()=="": continue
            cur_info=mydict.get(item_id,"{}")
            cur_info_dict=json.loads(cur_info)
            cur_url=cur_info_dict.get("url","")
            cur_url_id=cur_info_dict.get("url_id","") #get the reversed URL ID from the submission info
            cur_cat=cur_info_dict.get("cat","")
            cur_time=cur_info_dict.get("time")
            cur_user_email=cur_info_dict.get("user_email","")
            cur_title=cur_info_dict.get("title","")
            

            cur_description=cur_info_dict.get("description","")
            link_str='<a href="%s" target="new">%s</a>'%(cur_url,cur_url)

            #tmp_content+=link
            #create_selection_options
            cur_dropdown_list=[["","Business Category"]]+[(v[1],v[0]) for v in cat_list]

            select_str_open_tag='<select name="cat" class="approval %s" id="cat_dropdown">'%item_id

            #select_str='<select name="cat" class="approval" id="cat_dropdown">'+create_selection_options(cur_dropdown_list,cur_cat)+"</select>"
            select_str=select_str_open_tag+create_selection_options(cur_dropdown_list,cur_cat)+"</select>"

            #tmp_content+="<br>"+cur_info
            tmp_content+='<div class="row text-center"><div class="col">%s</div><div class="col">%s</div></div>'%(link_str,select_str)
            #tmp_content+="<br>"
            tmp_input='<input type="text" class="form-control" id="submission_id" name="id" value="%s" hidden>'%item_id
            tmp_input='<b>Title:</b> <input type="text" class="form-control %s" name="title" value="%s">'%(item_id,cur_title)
            #tmp_input+="<b>Title:</b> "+ cur_title+"<br>"
            tmp_input+="<b>Submitter email:</b> "+cur_user_email+"<br>"
            if cur_time!=None: 
                #time_str="/".join(cur_time[:3])+" - "+":".join(cur_time[3:])
                tmp_input+=create_time_str(cur_time) #str(cur_time)
            tmp_desc_text_area='Description:<br><textarea class="form-control approval %s" rows="5" id="description" name="description">%s</textarea>'%(item_id,cur_description)
            tmp_content+='<div class="row text-center"><div class="col">%s</div><div class="col">%s</div></div>'%(tmp_input,tmp_desc_text_area)
            tmp_content+="<br>"
            approve_btn_str='<button class="btn btn-success approve-btn" onclick="approve_item(this)" name="%s">Approve</button>'%item_id
            reject_btn_str='<button class="btn btn-danger reject-btn">Reject</button>'
            tmp_content+='<div class="row text-center"><div class="col"></div><div class="col">%s</div><div class="col">%s</div><div class="col"></div></div>'%(approve_btn_str,reject_btn_str)


            #tmp_content+='<tr><td>%s</td><td>%s</td><td>Approve</td><td>Reject</td></tr>'%(pi,cur_info)
            tmp_content+='<hr>'

        #tmp_content+='</table>'       
        #tmp_content+='</body></html>'


        mydict.close()



        #page_content=tmp_content
        cur_fpath=os.path.join(dir_path,"dashboard-template.html")
        template_content=read_file(cur_fpath)
        repl_dict2={"main_content":tmp_content}
        page_content=soup_replace_by_ids(template_content,repl_dict2) 



        
    else:
        #page_content="<html><body><h1>Test Page</h1> Error: %s <br> Trace: %s </body></html>"%(error,trace)
        page_content="<html><body><h1>Unknown Page</h1> Not clear what this page is. <br> <a href='directory'>Go to B2WEB</a>  </body></html>"


    #We will need to have a page to process the login/signup
    #and a page to process category search requests
    #and a page to process incoming messages
    #and a page to process url add requests
    #and a page to process url remove requests
    #and a page to process changing details


    page_content=page_content.replace("assets/",dir_path+"/assets/")
    response=page_content

    #Final logging of the request/response
    end_time=time.time() 
    elapsed=end_time-start_time
    tmp_log_dict={} #Now log the current request
    tmp_log_dict["qs"]=qs_dict
    tmp_log_dict["posted"]=posted_data_dict
    tmp_log_dict["script_url"]=script_url
    tmp_log_dict["duration"]=round(elapsed,5)
    tmp_log_dict["userid"]=userid
    
    now = datetime.datetime.now()
    log_fname="%s-%s-%s.txt"%(now.year, now.month, now.day)    
    tmp_log_fpath=os.path.join(logs_dir,log_fname)

    log_something(environ,tmp_log_fpath,tmp_log_dict)

    return [response.encode()]
