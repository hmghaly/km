import os, time, json, re, sys, math
from cgi import parse_qs
import traceback
from sqlitedict import SqliteDict #Make sure to install it 
from lxml import html #Make sure to install it 
from bs4 import BeautifulSoup #Make sure to install it 



sys.path.insert(0, os.path.dirname(__file__))
km_utils_dir='/home/sod9mlnmvhfv/km_code/utils'
sys.path.insert(0,km_utils_dir)
from file_utils import *
from template_utils import *
from extraction_utils import *
#import gensim

country_version_dict={} #specifying where is the working version for the AI data for each language
country_version_dict["au"]="oct21"
country_version_dict["nz"]="oct21"

country_name_dict={} #Getting the country name from the country code
country_name_dict["au"]="Australia"
country_name_dict["nz"]="New Zealand"

error="No error"
trace="No trace"

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

def create_selection_options(list_vals_labels): # create selection drop down from a list of labels and vals
    cur_dropdown_content=''
    for val0,label0 in list_vals_labels:
        cur_op_tag='<option value="%s">%s</option>'%(val0,label0)
        cur_dropdown_content+=cur_op_tag
    return cur_dropdown_content 
# def get_stdin():
#     try: 
#         stdin_str=sys.stdin.read()
#         stdin_dict=json.loads(stdin_str)
#     except:  stdin_dict={}
#     return stdin_dict

# sys.path.insert(km_code_dir)
cwd=os.getcwd()
cwd=km_utils_dir

#Interface template directory
version_name="ui2"
interface_dir="../b2web_ui"
dir_path=os.path.join(interface_dir,version_name)

#Data directory
km_data_dir='/home/sod9mlnmvhfv/km_data'

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
#now recursively get all the children        
# def get_children(child_dict0,cat_id0):
#     for child in child_dict0.get(cat_id0,[]): #node['children']:
#         yield child
#         for grandchild in get_children(child_dict0,child[0]):
#             yield grandchild
# rec_child_dict={}
# for key in child_dict:
#     rec_child_dict[key]=list(get_children(child_dict,key))

#experiment with new things
# try:
#     pass
#     test_content=""
#     # for k,v in rec_child_dict.items(): 
#     #     test_content+=str(k)+"<br>"
# except Exception as e:
#   error=str(e)
#   trace=traceback.format_exc() results_retrieval(cat, start_i, country,data_version,domain,n_results_per_page,km_data_dir,recursive_child_dict)
def gen_pagination(start_i,n_results_per_page,n_full):
    displayed_pages=[]
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
        



def app(environ, start_response):
    #start_response('200 OK', [('Content-Type', 'text/plain')])
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

    #Get list of cities in the current country
    locations_fpath=os.path.join(txt_dir,"locations",country+".json")
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

    elif script_name=="category_old":
        cur_fpath=os.path.join(dir_path,"category.html")
        page_content=read_file(cur_fpath)
        page_content=page_content.replace("_country_code_",country)
        page_content=page_content.replace("_country_name_",country_name)
        page_content=page_content.replace("_com_link_","category?country=%s&domain=com&cat=%s"%(country,cat))
        page_content=page_content.replace("_gov_link_","category?country=%s&domain=gov&cat=%s"%(country,cat))
        page_content=page_content.replace("_edu_link_","category?country=%s&domain=edu&cat=%s"%(country,cat))
        page_content=page_content.replace("_org_link_","category?country=%s&domain=org&cat=%s"%(country,cat))
        
        

        ai_dir=os.path.join(km_data_dir,country,data_version,domain)
        manual_dir=os.path.join(km_data_dir,country,"manual",domain)
        sponsored_dir=os.path.join(km_data_dir,country,"sponsored",domain)
        cat_fpath=os.path.join(ai_dir,cat+".txt")
        #cat_fpath=os.path.join(manual_dir,cat+".txt")
        manual_cat_fpath=os.path.join(manual_dir,cat+".txt")
        info_dict_path=os.path.join(km_data_dir,country,"info_dict.sqlite")

        repl_dict1={}
        
        cat_name=id_dict.get(cat,cat) #First get cat name and descriptions
        cat_description=description_dict.get(cat, cat_name)
        repl_dict1["cat_name"]=cat_name
        repl_dict1["cat_description"]=cat_description +" in %s"%country_name

        domains=["com","gov","edu","org"] #then get the number of results per domain
        domain_count_dict={}
        for dom0 in domains:
            cur_domain_fpath=os.path.join(km_data_dir,country,data_version,dom0,cat+".txt")
            domain_num_lines=get_file_n_lines(cur_domain_fpath)
            domain_count_dict[dom0]=domain_num_lines
            repl_key=dom0+"_category_count"
            repl_dict1[repl_key]="(%s)"%domain_num_lines
            

        t0=time.time() # Start running the actual query
        mydict = SqliteDict(info_dict_path, autocommit=True)
        
        num_lines=get_file_n_lines(cat_fpath)
        m_lines=get_multiple_lines(start_i,n_results_per_page,cat_fpath)

        results_list=[]
        for line_item in m_lines:
            out=mydict.get(line_item)
            results_list.append(out)
        t1=time.time()
        elapsed=t1-t0


        results_content=""
        for item in results_list:
            local_dict=json.loads(item)
            cur_url=local_dict.get("url","")
            cur_title=local_dict.get("title",cur_url)
            #cur_url='<a href="%s" target="new">%s</a>'%(local_dict.get("url",""),local_dict.get("url",""))
            top_words_list=local_dict.get("top_words",[])

            preds_list=local_dict.get("top_preds",[])
            preds_dict=dict(iter([v[:2] for v in preds_list]))
            cur_score=preds_dict.get(cat,0)

            keywords_str="<b>Keywords:</b> "+" ".join(top_words_list)
            keywords_str+="- <b>score</b>: %s"%cur_score #temporary

            cur_description=local_dict.get("description",keywords_str)

            #cur_description=str(local_dict.get("top_preds",[]))
            #cur_description=str(list(local_dict.keys()))
            #cur_description=str(preds_dict)
            cur_template='<blockquote><p><a href="_url_" target="new"> _title_ </a></p><cite>_description_</cite></blockquote>'
            cur_template_copy=cur_template.replace("_url_",cur_url).replace("_title_",cur_title).replace("_description_",cur_description)
            results_content+=cur_template_copy+"\n"
        repl_dict1["result_list"]=results_content #id_dict description_dict child_dict

        pagination_content=""
        link_template="category?country=%s&domain=%s&cat=%s&start_i=_s_i_"%(country,domain,cat)
        #link_template_copy=link_template.replace("_s_i_","20")
        #pagination_content+='<a href="%s">02</a>'%link_template_copy

        #let's make a distinction between i, the index of an individual result in the results file
        #and j, the index of the page
        #we should
        cur_page_j=int(start_i/n_results_per_page)+1 #if start_i is 20, then we're talking about page 3 (p1: 0, p2: 10, p3: 20)
        n_pages=math.ceil(num_lines/n_results_per_page) #the actual number of result pages is the number of lines of the cat file/n_results per page
        last_page_i=n_results_per_page*(n_pages-1) #the start_i value for the last page
        next_page_j=cur_page_j+1
        prev_page_j=cur_page_j-1

        used_js=[]
        for j0 in range(3): #initial pagination, for first three pages
            tmp_page_j=j0+1
            tmp_start_i=j0*n_results_per_page #if j0=0 : start_i=0, 
            if tmp_start_i>num_lines: continue
            used_js.append(j0)
            if tmp_page_j==cur_page_j: 
                pagination_content+='<span class="current">%s</span>'%tmp_page_j
            else: 
                link_template_copy=link_template.replace("_s_i_",str(tmp_start_i))
                pagination_content+='<a href="%s">%s</a>'%(link_template_copy,tmp_page_j)
        
        if cur_page_j>4: pagination_content+="..." #now doing middle pagination
        for j0 in [prev_page_j,cur_page_j,next_page_j]:
            if j0<3: continue
            tmp_page_j=j0+1
            #tmp_start_i=j0*n_results_per_page #if j0=0 : start_i=0, 
            tmp_start_i=n_results_per_page*(tmp_page_j-1)
            if tmp_start_i>num_lines: continue
            if tmp_page_j==n_pages: continue
            used_js.append(j0)
            if tmp_page_j==cur_page_j: 
                pagination_content+='<span class="current">%s</span>'%tmp_page_j
            else: 
                link_template_copy=link_template.replace("_s_i_",str(tmp_start_i))
                pagination_content+='<a href="%s">%s</a>'%(link_template_copy,tmp_page_j)

        if cur_page_j==n_pages and not prev_page_j in used_js:
            #tmp_start_i=prev_page_j*n_results_per_page
            tmp_start_i=n_results_per_page*(prev_page_j-1)

            link_template_copy=link_template.replace("_s_i_",str(tmp_start_i))
            pagination_content+='<a href="%s">%s</a>'%(link_template_copy,prev_page_j)


        if not n_pages in used_js: #now doing the last page
            if n_pages>next_page_j+2: pagination_content+="..."
            tmp_page_j=n_pages
            #tmp_start_i=tmp_page_j*n_results_per_page
            if tmp_page_j==cur_page_j: 
                pagination_content+='<span class="current">%s</span>'%tmp_page_j
            else: 
                link_template_copy=link_template.replace("_s_i_",str(last_page_i))
                pagination_content+='<a href="%s">%s</a>'%(link_template_copy,tmp_page_j)




            
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
        #category_select_dropdown


        # fname="test.html"
        


    elif script_name=="intro" or script_name=="country" or script_name=="directory":
        cur_fpath=os.path.join(dir_path,"country-selection.html")
        page_content=read_file(cur_fpath)
    elif script_name=="privacy":
        cur_fpath=os.path.join(dir_path,"privacy.html")
        page_content=read_file(cur_fpath)
    elif script_name=="about":
        cur_fpath=os.path.join(dir_path,"about.html")
        page_content=read_file(cur_fpath)
    elif script_name=="terms":
        cur_fpath=os.path.join(dir_path,"terms.html")
        page_content=read_file(cur_fpath)
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

        repl_dict1["cat_children"]=" - ".join(child_link_list) #str(cur_children)
        #cat_children      

        #Now getting the actual results
        t0=time.time() # Start running the actual query
        cat_res_dict={} #to get the query results: just the list of website IDs
        res_obj=results_retrieval(cat, start_i, country,data_version,domain,n_results_per_page,km_data_dir,recursive_child_dict)
        cat_res_dict["cur_results"]=res_obj.cur_results
        cat_res_dict["n_full"]=res_obj.n_full
        cat_res_dict["n_manual"]=res_obj.n_manual
        #cat_res_dict["query_time"]=res_obj.query_time
        # cat_res_dict["test-cat"]=test
        pagination1=gen_pagination(start_i,n_results_per_page,res_obj.n_full)
        cat_res_dict["pagination"]=pagination1
        info_dict_path=os.path.join(km_data_dir,country,"info_dict.sqlite") #now we get the info from each result
        mydict = SqliteDict(info_dict_path, autocommit=True) 
        results_list=[]
        for line_item in res_obj.cur_results:
            out=mydict.get(line_item,"{}")
            results_list.append(out)
        mydict.close()
        t1=time.time()
        elapsed=t1-t0

        #Now we start populating the results content in the results section


        results_content=""
        for item in results_list:
            local_dict=json.loads(item)
            cur_url=local_dict.get("url","")
            cur_title=local_dict.get("title",cur_url)
            #cur_url='<a href="%s" target="new">%s</a>'%(local_dict.get("url",""),local_dict.get("url",""))
            top_words_list=local_dict.get("top_words",[])

            preds_list=local_dict.get("top_preds",[])
            preds_dict=dict(iter([v[:2] for v in preds_list]))
            cur_score=preds_dict.get(cat,0)

            keywords_str="<b>Keywords:</b> "+" ".join(top_words_list)
            keywords_str+="- <b>score</b>: %s"%cur_score #temporary

            cur_description=local_dict.get("description",keywords_str)

            cur_template='<blockquote><p><a href="_url_" target="new"> _title_ </a></p><cite>_description_</cite></blockquote>'
            cur_template_copy=cur_template.replace("_url_",cur_url).replace("_title_",cur_title).replace("_description_",cur_description)
            results_content+=cur_template_copy+"\n"
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

    elif script_name=="json":
        page_content=str(recursive_child_dict)#+"<br><br>"+str(child_dict)
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
        cur_cat=json_dict.get("business_category","")
        cur_loc=json_dict.get("business_location","") #we will need to adjust to multiple locations
        info_json_dict={}
        info_json_dict["url"]=cur_url
        info_json_dict["title"]=json_dict.get("business_name","")        
        info_json_dict["description"]=json_dict.get("business_description","")
        info_json_dict["locations"]=[cur_loc]

        info_json_obj=json.dumps(info_json_dict)
        
        #cur_loc=json_dict.get("business_location","")
        
        cur_domain="com"
        bare_url=get_bare_url(cur_url)
        url_split=bare_url.split(".")
        if len(url_split)>2 and url_split[-2].lower() in ["gov","edu","org"]: cur_domain=url_split[-2].lower()
        cur_rev_url=reverse_url(cur_url.lower())
        

        manual_domain_dir=os.path.join(km_data_dir,cur_country,"manual",cur_domain)
        if not os.path.exists(manual_domain_dir): os.makedirs(manual_domain_dir)
        cat_fpath=os.path.join(manual_domain_dir,cur_cat+".txt")




        # if posted_data: page_content=str(posted_data)
        # else: page_content=info_json_obj#str([bare_url,cur_domain,cur_country,cur_cat,cur_loc,cur_description])
        insert_sorted(cur_rev_url,cat_fpath,line_size=100)
        info_dict_path=os.path.join(km_data_dir,cur_country,"info_dict.sqlite")
        mydict = SqliteDict(info_dict_path, autocommit=True)
        mydict[cur_rev_url]=info_json_obj
        mydict.close()

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

        
    else:
        page_content="<html><body><h1>Test Page</h1> Error: %s <br> Trace: %s </body></html>"%(error,trace)

    #We will need to have a page to process the login/signup
    #and a page to process category search requests
    #and a page to process incoming messages
    #and a page to process url add requests
    #and a page to process url remove requests
    #and a page to process changing details


    page_content=page_content.replace("assets/",dir_path+"/assets/")
    response=page_content

    return [response.encode()]
