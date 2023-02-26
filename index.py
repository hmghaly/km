import os, time, json, re, sys, math, shelve
load_t0=time.time()
import datetime
import traceback
import hashlib
from itertools import groupby
import requests #pip install requests
basic_load_elapsed=time.time()-load_t0
load_t0=time.time()


sys.path.insert(0, os.path.dirname(__file__))
#code_base_dir='/home/sod9mlnmvhfv/www/code_utils'
code_base_dir='code_utils'
sys.path.insert(0,code_base_dir)

from backend_utils import *
from web_lib import *
from general import *
# from excel_utils import *
from geo_utils import *
from file_utils import *
from sqld_utils import *






#pip install openpyxl
#pip install sqlitedict
#source /home/sod9mlnmvhfv/virtualenv/public_html/itrade360/app/3.7/bin/activate && cd /home/sod9mlnmvhfv/public_html/itrade360/app
custom_load_elapsed=time.time()-load_t0

load_t0=time.time()

root_dir='/home/sod9mlnmvhfv/itrade360'
production_dir=os.path.join(root_dir,"production")
dev_dir=os.path.join(root_dir,"dev")
if not os.path.exists(production_dir): os.makedirs(production_dir)
if not os.path.exists(dev_dir): os.makedirs(dev_dir)



working_dir=dev_dir
db_data_dir=os.path.join(working_dir,"db_data")
users_dir=os.path.join(working_dir,"users")
stat_dir=os.path.join(working_dir,"stat")
historical_stat_dir=os.path.join(stat_dir,"historical")

workflow_dir=os.path.join(working_dir,"workflow")
logs_dir=os.path.join(working_dir,"logs")
country_dir=os.path.join(db_data_dir,"country")
hs_dir=os.path.join(db_data_dir,"hs")
services_dir=os.path.join(db_data_dir,"services")
comm_dir=os.path.join(working_dir,"comm")
cur_dirs=[db_data_dir,users_dir,stat_dir,workflow_dir,logs_dir,country_dir,hs_dir,services_dir,comm_dir,historical_stat_dir]
for dir0 in cur_dirs:
  if not os.path.exists(dir0): os.makedirs(dir0)



ui_dir=""
# wb_fpath='data/world-geo-info.xlsx'
# wb_data_output=xl2data(wb_fpath)
# geo_output=get_geo_dict(wb_data_output)

# geo_fpath='data/geo_data.json'
# geo_fopen=open(geo_fpath)
# geo_dict=json.load(geo_fopen)
# geo_fopen.close()

city_loc_dict=read_json("data/city_loc_dict.json")
country_drawing_info_dict=read_json("data/country_drawing_info_dict.json")
geo_child_dict=read_json("data/geo_child_dict.json")
geo_text_info_dict=read_json("data/geo_text_info_dict.json")
hs_data_dict=read_json("data/hs_data_dict.json")

# geo_fpath_shelve='data/geo_data.shelve'
# if os.path.exists(geo_fpath_shelve):
#   geo_dict=shelve.open(geo_fpath_shelve)
# else:
#   geo_fpath='data/geo_data.json'
#   geo_fopen=open(geo_fpath)
#   geo_dict=json.load(geo_fopen)
#   geo_fopen.close()


data_file_load_elapsed=time.time()-load_t0

        # try: success=log_something(environ,log_fpath,cur_log_content_dict)
        # except Exception as e: 
        #     error=str(e)
        #     trace=traceback.format_exc()
        #     success=False

#def gen_any_page(visible_ids=[],template_path="template.html")

#functions to generate contents of pages
def gen_index_page(data_dict0): 
  content0=read_file("template.html")
  dom_obj=DOM(content0)
  repl_dict={}
  repl_dict[".not_main"]=" "
  out_content0=dom_obj.replace(repl_dict)
  return out_content0

def gen_add_business_page(data_dict0): 
  content0=read_file("template.html")
  dom_obj=DOM(content0)
  repl_dict={}
  repl_dict[".page_item"]=" "
  #except_id0="add-business-div"
  except_id0="onboarding_form"
  out_content0=dom_obj.replace(repl_dict,except_ids=[except_id0])
  return out_content0

def gen_add_business_success_page(data_dict0): 
  content0=read_file("template.html")
  dom_obj=DOM(content0)
  repl_dict={}
  repl_dict[".page_item"]=" "
  #except_id0="add-business-div"
  list_except_ids0=["add-business-success-message","map-info-div"]
  out_content0=dom_obj.replace(repl_dict,except_ids=list_except_ids0)
  return out_content0

#"map-info-div"
def gen_browse_products_page(data_dict0): 
  content0=read_file("template.html")
  dom_obj=DOM(content0)
  repl_dict={}
  repl_dict[".page_item"]=" "
  except_id0="map-info-div"
  out_content0=dom_obj.replace(repl_dict,except_ids=[except_id0])
  return out_content0

def gen_hs_code_page(data_dict0): 
  content0=read_file("template.html")
  dom_obj=DOM(content0)
  repl_dict={}
  repl_dict[".page_item"]=" "
  except_id0="map-info-div"
  out_content0=dom_obj.replace(repl_dict,except_ids=[except_id0])
  return out_content0

def gen_complete_business_profile_page(data_dict0):
  content0=read_file("template.html")
  dom_obj=DOM(content0)
  repl_dict={}
  repl_dict[".page_item"]=" "
  except_id0="complete-business-profile"
  out_content0=dom_obj.replace(repl_dict,except_ids=[except_id0])
  return out_content0

def gen_add_product(data_dict0):
  content0=read_file("template.html")
  dom_obj=DOM(content0)
  repl_dict={}
  repl_dict[".page_item"]=" "
  except_id0="add-product"
  out_content0=dom_obj.replace(repl_dict,except_ids=[except_id0])
  return out_content0


def gen_add_service(data_dict0):
  content0=read_file("template.html")
  dom_obj=DOM(content0)
  repl_dict={}
  repl_dict[".page_item"]=" "
  except_id0="add-service"
  out_content0=dom_obj.replace(repl_dict,except_ids=[except_id0])
  return out_content0

def gen_add_location(data_dict0):
  content0=read_file("template.html")
  dom_obj=DOM(content0)
  repl_dict={}
  repl_dict[".page_item"]=" "
  except_id0="add-location"
  out_content0=dom_obj.replace(repl_dict,except_ids=[except_id0])
  return out_content0


def gen_results_page(): return

def gen_login_signup_page(): return



#APIs - functions to generate json data 
def get_countries(data_dict0):
  qs_dict=data_dict0.get("qs",{})
  lang0=qs_dict.get("language","en")
  cur_country_list=get_geo_children_name_list("",geo_text_info_dict,geo_child_dict,lang=lang0)
  #cur_country_list=get_geo_query_items(geo_dict,request_type="list_countries",lang=lang0)
  return json.dumps(cur_country_list)

def get_provinces(data_dict0):
  qs_dict=data_dict0.get("qs",{})
  lang0=qs_dict.get("language","en")
  country0=qs_dict.get("country","")
  if country0=="": province_list=[]
  else: 
    #province_list=get_geo_query_items(geo_dict,request_type="list_admin",country_id=country0,lang=lang0)
    province_list=get_geo_children_name_list(country0,geo_text_info_dict,geo_child_dict,lang=lang0)
  return json.dumps(province_list)

def get_cities(data_dict0):
  qs_dict=data_dict0.get("qs",{})
  lang0=qs_dict.get("language","en")
  province0=qs_dict.get("province","")
  if province0=="": city_list=[] #,request_type="list_cities",admin_id=admin_id
  else: 
    #city_list=get_geo_query_items(geo_dict,request_type="list_cities",admin_id=province0,lang=lang0)
    city_list=get_geo_children_name_list(province0,geo_text_info_dict,geo_child_dict,lang=lang0)
  return json.dumps(city_list)

def get_hs_options(data_dict0):
  qs_dict=data_dict0.get("qs",{})
  lang0=qs_dict.get("language","en") 
  hs_code0=qs_dict.get("hs","")  
  hs_code_list=get_hs_list(hs_code0,hs_data_dict,lang=lang0)
  return json.dumps(hs_code_list)

def get_city_info(data_dict0):
  qs_dict=data_dict0["qs"]
  city_id=qs_dict.get("city")
  out_dict={}
  if city_id!=None:
    coords=city_loc_dict.get(city_id)
    out_dict["coordinates"]=coords

  return json.dumps(out_dict) 


def get_business_info(data_dict0):
  out_dict={}
  qs_dict=data_dict0["qs"]
  biz_id_key_names=["company","business"]
  biz_key0,biz_id0=check_dict_multi_keys(qs_dict,biz_id_key_names)
  country0=qs_dict.get("country")
  if biz_id0==None or country0==None: return json.dumps(out_dict)
  country_data_dir=os.path.join(country_dir,country0)
  biz_sqld_fpath0=os.path.join(country_data_dir,"business.sqld") #update local db  
  biz_info0=get_sqld_val(biz_sqld_fpath0,biz_id0)
  if biz_info0==None: return "{}" #out_dict={}
  else: return biz_info0
  #return json.dumps(out_dict)


def test(data_dict0):
  test_out=list(geo_dict.keys())
  return json.dumps(test_out)

#Form Submission processing
def process_onboarding_form(data_dict0):
  biz_id=generate_uuid()
  loc_id=generate_uuid()
  cur_time=str(now())

  today_str=today()
  posted_data=data_dict0["posted_data"]
  cur_user=posted_data.get("user")
  cur_country=posted_data.get("location_0-country")
  cur_province=posted_data.get("location_0-province")
  cur_city=posted_data.get("location_0-city")
  cur_sectors=posted_data.get("sectors",[])
  cur_roles=posted_data.get("roles",[])
  if not type(cur_sectors) is list: 
    cur_sectors=[cur_sectors]
    posted_data["sectors"]=cur_sectors
  if not type(cur_roles) is list: 
    cur_roles=[cur_roles]
    posted_data["roles"]=cur_roles

  loc_dict={"id":loc_id,"type":"hq","added_time":cur_time,"added_by":cur_user}
  loc_dict["location_0-city"]=cur_city #posted_data.get("location_0-city")
  loc_dict["location_0-province"]=cur_province #posted_data.get("location_0-province")
  loc_dict["location_0-country"]=cur_country
  loc_dict["image"]=""


  # posted_data_items=list(posted_data.items())
  posted_data["added_time"]=cur_time
  posted_data["added_by"]=cur_user
  posted_data["locations"]=[loc_dict]
  posted_data["products"]=[]
  posted_data["services"]=[]
  posted_data["admins"]=[cur_user]
  posted_data["social"]={}
  posted_data["legal"]={}
  posted_data["verfication"]={}
  posted_data["ai"]={}
  posted_data["logo"]=""
  posted_data["logs"]="created by %s on %s\n"%(cur_user,cur_time)
  posted_data["country"]=cur_country
  posted_data["city"]=cur_city


  out_dict={}
  out_dict["posted_data"]=posted_data
  out_dict["id"]=biz_id
  out_dict["today"]=today_str
  if cur_country==None: 
    out_dict["success"]=False
    out_dict["message"]="No country selected"
    return json.dumps(out_dict)

  
  country_data_dir=os.path.join(country_dir,cur_country)
  create_dir(country_data_dir) 
  biz_sqld_fpath0=os.path.join(country_data_dir,"business.sqld") #update local db
  update_sqld_val(biz_sqld_fpath0,biz_id,json.dumps(posted_data),overwrite=True)
  id_country_line="%s/%s\n"%(biz_id,cur_country)

  biz_country_list_fpath0=os.path.join(country_data_dir,"business-list.txt") #update listings
  biz_all_list_fpath0=os.path.join(db_data_dir,"business-list.txt")
  append2file(id_country_line,biz_country_list_fpath0)
  append2file(id_country_line,biz_all_list_fpath0)
  

  country_stat_fpath=os.path.join(stat_dir,"country.txt")
  city_stat_fpath=os.path.join(stat_dir,"city.txt")
  province_stat_fpath=os.path.join(stat_dir,"province.txt")
  sector_stat_fpath=os.path.join(stat_dir,"sector.txt")
  role_stat_fpath=os.path.join(stat_dir,"role.txt")
  try:
    today_stat=os.path.join(historical_stat_dir,today_str)
    stat_countries=["total"]+[cur_country]
    inc_count_items(stat_countries,country_stat_fpath)
    inc_count_items([cur_city],city_stat_fpath)
    inc_count_items([cur_province],province_stat_fpath)
    inc_count_items(cur_sectors,sector_stat_fpath)
    inc_count_items(cur_roles,role_stat_fpath)
    out_dict["success"]=True
    create_dir(today_stat)
    for fname in ["country.txt","city.txt","province.txt","sector.txt","role.txt"]:
      src_stat_file=os.path.join(stat_dir,fname)
      if not os.path.exists(src_stat_file): continue
      dst_stat_file=os.path.join(today_stat,fname)
      shutil.copy(src_stat_file,dst_stat_file)
  except Exception as e: 
    error=str(e)
    trace=traceback.format_exc()
    #success=False   
    out_dict["success"]=False 
    out_dict["message"]=str(trace) 
  
  return json.dumps(out_dict)

def process_add_location(data_dict0):
  return json.dumps(data_dict0)

def process_add_product(data_dict0):
  return json.dumps(data_dict0)

def process_add_service(data_dict0):
  return json.dumps(data_dict0)

def process_login(data_dict0):
  return json.dumps(data_dict0)

def process_signup(data_dict0):
  return json.dumps(data_dict0)


def process_business_form(data_dict0):
  biz_id=generate_uuid()
  today_str=today()
  added_by="customer"
  posted_data=data_dict0["posted_data"]
  posted_data_items=list(posted_data.items())
  countries=list(set([val0 for key0,val0 in posted_data_items if key0.split("-")[-1]=="country"]))
  cities=list(set([val0 for key0,val0 in posted_data_items if key0.split("-")[-1]=="city"]))
  provinces=list(set([val0 for key0,val0 in posted_data_items if key0.split("-")[-1]=="province"]))
  hs2_list=list(set([val0 for key0,val0 in posted_data_items if key0.split("-")[-1]=="hs2"]))
  hs4_list=list(set([val0 for key0,val0 in posted_data_items if key0.split("-")[-1]=="hs4"]))
  hs6_list=list(set([val0 for key0,val0 in posted_data_items if key0.split("-")[-1]=="hs6"]))
  out_dict={}
  out_dict["posted_data"]=posted_data
  out_dict["id"]=biz_id
  out_dict["today"]=today_str
  out_dict["countries"]=countries
  out_dict["cities"]=cities
  out_dict["provinces"]=provinces
  out_dict["hs2_list"]=hs2_list
  out_dict["hs4_list"]=hs4_list
  out_dict["hs6_list"]=hs6_list
  all_hs=hs2_list+hs4_list+hs6_list

  for country0 in countries:
    country_data_dir=os.path.join(country_dir,country0)
    create_dir(country_data_dir)
    sqld_fpath0=os.path.join(country_data_dir,"data.sqld")
    update_sqld_val(sqld_fpath0,biz_id,json.dumps(posted_data),overwrite=True)
    country_cities_companies_listing_fpath=os.path.join(country_data_dir,"listing.txt")
    country_cities=[v for v in cities if v.startswith(country0)]
    for city0 in country_cities:
      city_biz_id_line="%s\t%s"%(city0,biz_id)
      insert_sorted(city_biz_id_line,country_cities_companies_listing_fpath,line_size=100)
  for hs0 in all_hs:
    hs_data_dir=os.path.join(hs_dir,hs0) #hs_dir
    hs_listing_fpath=os.path.join(hs_dir,"%s.txt"%hs0)
    for city0 in cities:
      city_biz_id_line="%s\t%s"%(city0,biz_id)
      insert_sorted(city_biz_id_line,hs_listing_fpath,line_size=100)
  try: 
    country_stat_fpath=os.path.join(stat_dir,"country.txt")
    city_stat_fpath=os.path.join(stat_dir,"city.txt")
    province_stat_fpath=os.path.join(stat_dir,"province.txt")
    hs_stat_fpath=os.path.join(stat_dir,"hs.txt")
    services_stat_fpath=os.path.join(stat_dir,"services.txt")
    today_stat=os.path.join(historical_stat_dir,today_str)
    stat_countries=["total"]+countries
    inc_count_items(stat_countries,country_stat_fpath)
    inc_count_items(cities,city_stat_fpath)
    inc_count_items(provinces,province_stat_fpath)
    inc_count_items(all_hs,hs_stat_fpath)
    create_dir(today_stat)
    for fname in ["country.txt","city.txt","province.txt","hs.txt","services.txt"]:
      src_stat_file=os.path.join(stat_dir,fname)
      if not os.path.exists(src_stat_file): continue
      dst_stat_file=os.path.join(today_stat,fname)
      shutil.copy(src_stat_file,dst_stat_file)

  except Exception as e:
    error=str(e)
    trace=traceback.format_exc()
    success=False
    error_msg="%s - %s"%(error,trace) 
    out_dict["error"]= error_msg
  # inc_count_items(cities,city_stat_fpath)
  # inc_count_items(all_hs,hs_stat_fpath)
  # create_dir(today_stat)

  return json.dumps(out_dict)






##============= Mapping pages to content functions =========##
content_func_map_dict={} #linking the scriptname to the content generation function
content_func_map_dict["index"]=gen_index_page
content_func_map_dict["add-business"]=gen_add_business_page
content_func_map_dict["add-business-success"]=gen_add_business_success_page
content_func_map_dict["find-hs-code"]=gen_hs_code_page
content_func_map_dict["browse-products"]=gen_browse_products_page
content_func_map_dict["get-countries"]=get_countries
content_func_map_dict["get-provinces"]=get_provinces
content_func_map_dict["get-cities"]=get_cities
content_func_map_dict["get-hs-options"]=get_hs_options
content_func_map_dict["get-city-info"]=get_city_info
content_func_map_dict["get-business-info"]=get_business_info
content_func_map_dict["process-business-form"]=process_onboarding_form #process_business_form
content_func_map_dict["complete-business-profile"]=gen_complete_business_profile_page
content_func_map_dict["add-product"]=gen_add_product
content_func_map_dict["add-service"]=gen_add_service
content_func_map_dict["add-location"]=gen_add_location

#complete-business-profile
content_func_map_dict["test"]=test



def populate(environ):
  #page_content="<html><body><h1>Test Page</h1> Error: %s <br> Trace: %s </body></html>"%(error,trace)
  load_t0=time.time()
  
  qs_dict=get_wsgi_qs(environ) 
  posted_data_dict=get_wsgi_posted_data(environ)
  cookie_dict=get_wsgi_cookie(environ)
  userid=cookie_dict.get("userid","")
  is_admin=False
  env_load_elapsed=time.time()-load_t0

  #if userid in admin_emails: is_admin=True
  # #now creating a script name from the URL b2web/index = b2web/about ... etc
  script_url=environ["SCRIPT_URL"].strip("/")
  script_split=script_url.split("/")
  if len(script_split)==1: script_name="index"
  else: script_name=script_split[-1]

  data_dict={}
  data_dict["qs"]=qs_dict
  data_dict["posted_data"]=posted_data_dict
  data_dict["cookie_dict"]=cookie_dict
  data_dict["basic_load_elapsed"]=basic_load_elapsed
  data_dict["custom_load_elapsed"]=custom_load_elapsed
  data_dict["data_file_load_elapsed"]=data_file_load_elapsed
  data_dict["env_load_elapsed"]=env_load_elapsed
  cur_content_func=content_func_map_dict.get(script_name)
  if cur_content_func!=None: out_content=cur_content_func(data_dict)
  else: out_content=json.dumps(data_dict)
  # if script_name=="index":
  #   template_fpath=os.path.join(ui_dir,"template.html")
  #   content0=read_file(template_fpath)
  #   dom_obj=DOM(content0)
  #   repl_dict={}
  #   repl_dict["#main-div"]=("testing",{}) #content and attributes
  #   out_content=dom_obj.replace(repl_dict)
  # else:
  #   out_content=json.dumps(data_dict)


  #page_content="<html><body><h1>Unknown Page</h1> Not clear what this page is. <br> <a href='directory'>Go to B2WEB</a>  </body></html>"
  return out_content


def app(environ, start_response):
  start_time=time.time()
  start_response('200 OK', [('Content-Type', 'text/html')])

  #start_response('200 OK', [('Content-Type', 'text/plain')])
  # message = 'It works!\n'
  # #message = str(qs_dict)+str(cookie_dict)+str(posted_data_dict)+script_name
  # version = 'Python v' + sys.version.split()[0] + '\n'
  # response = '\n'.join([message, version])
  success=True
  try: response = populate(environ)
  except Exception as e:
    error=str(e)
    trace=traceback.format_exc()
    success=False
    response="%s - %s"%(error,trace)
  elpased=time.time()-start_time 
  return [response.encode()]


#dir structure
# main/ > where main is the main working directory, production or dev
# main/users  - main/logs - main/comm > user info, logs, and communications
# main/workflow > requests/approvals/verifications .. etc
# main/db_data  - main/db_data/fr -  main/db_data/fr/business.sqld , location.sqld, product.sqld, service.sqld - all.txt
# main/hs  > 09.txt 
# main/service  > accounting.txt (or with ISIC code)
# main/sectors  > agriculture.txt 
# main/stat main/stat/historical> ordered items, updated daily

#on business submit 
# gen id
# create location, gen location id, add to the location info the id of the business (parent id)
# add location id and country iso2/loc_id to locations in the business info object
#> use id as key, add business info object as value at: main/db_data/iso2/business.sqld 
#> use location id as key, add value/info to: main/db_data/iso2/location.sqld 
#> add iso2/id to: main/db_data/iso2/all.txt
#> add iso2/id to: main/db_data/all.txt > also to main/sectors/sector1.txt (for each sector)

#on location submit
# create location id, get parent business id
# update main/db_data/iso2/business.sqld
# update main/db_data/iso2/location.sqld 

#on product submit
# create product id, get parent business id, and parent iso2 
# update main/db_data/iso2/business.sqld with business_iso2/product_id (unless product has location, in this case product_iso2/product_id)
# update main/db_data/iso2/product.sqld 
#> add iso2/id to: main/hs/09.txt and all other hs codes
#> add iso2/id to: main/db_data/hs/09.txt and all other hs codes ?? maybe

#on service submit
# create service id, get parent business id, and parent iso2 
# update main/db_data/iso2/service.sqld with business_iso2/service_id (unless service has location, in this case service_iso2/product_id)
# update main/db_data/iso2/service.sqld 
#> add iso2/id to: main/service/accounting.txt and all other service/isic codes
#> add iso2/id to: main/db_data/service/accounting.txt and all other service/isic codes ? maybe 