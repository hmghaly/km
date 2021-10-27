import re
class element_tag:
  def __init__(self):
    self.inner_html=""
    self.outer_html=""
    self.tag_name=""
    self.open_tag=""
    self.closing_tag=""
    self.class_name=""
    self.classes=[]
    self.children=[]
    self.attrs={}
    self.id=""

class html_page:
  def __init__(self,page_fpath):
    with open(page_fpath) as fopen:
      self.html_content=fopen.read()
    self.original_html_content=str(self.html_content)
    self.html_content=re.sub("(<!--.*?-->)", "", self.html_content, flags=re.DOTALL) #remove html comments
    self.html_content=re.sub("(<!.+?>)", "", self.html_content, flags=re.DOTALL) #remove html doc type
    self.html_content=re.sub('(?i)<script[\s\S]+?/script>', "", self.html_content) #remove script tags
    self.html_content=re.sub('(?i)<style[\s\S]+?/style>', "", self.html_content) #remove style tags

    open_tags=[] #keep track of which tags are open
    tag_counter_dict={}

    self.tag_dict={} #span (start loc, end loc) - key is the automatic tag id
    self.tag_obj_dict={}    #element obj 
    self.tag_id_list=[] # list of automatic tag ids
    self.tag_class_dict={} #list of automatic tag ids for each class
    self.tag_id_dict={} #the corresponding automatic tag id for each original id in the element <tag id="original">
    self.child_dict={} #which tag has which children - key is automatic tag id, children are list of automatic tag ids
    self.tag_txt_dict={} # just get the clean text of each tag/element
    self.title=""
    self.description=""

    tags=list(re.finditer('<([^<>]*?)>', self.html_content)) #then get each individual tag
    for t in tags:
      tag_str,tag_start,tag_end=t.group(0), t.start(), t.end()
      tag_name=re.findall(r'</?(.+?)[\s>]',tag_str)[0].lower()
      tag_count=tag_counter_dict.get(tag_name,0)
      tag_id="%s_%s"%(tag_name,tag_count) #automatically generated ID for each tag
      self.tag_dict[tag_id]=tag_start,tag_end
      
      last_tag=""
      if open_tags: last_tag=open_tags[-1]
      if tag_str.startswith('</'):
        tag_type="c"
        cur_span=self.html_content[self.tag_dict[last_tag][1]:tag_start]
        #if tag_str=="": print("??????????????", cur_span)
        #cur_span_clean=re.sub('<([^<>]*?)>',"", cur_span)
        self.tag_txt_dict[last_tag]=cur_span
        cur_inner_html=self.html_content[self.tag_dict[last_tag][1]:tag_start]
        cur_outer_html=self.html_content[self.tag_dict[last_tag][0]:tag_end]
        self.tag_obj_dict[last_tag].inner_html=cur_inner_html 
        self.tag_obj_dict[last_tag].outer_html=cur_outer_html
        
        self.tag_obj_dict[last_tag].closing_tag=tag_str
        #print("????? ",self.tag_obj_dict[last_tag].id, self.tag_obj_dict[last_tag].closing_tag)

        #full_span_dict[last_tag]=cur_span
        open_tags=open_tags[:-1]
        #cur_attrs={}
      elif tag_str.endswith('/>') or tag_str.lower().startswith('<meta') or tag_str.lower().startswith('<img') or tag_str.lower().startswith('<link'):
        tag_type='s' #stand alone tag
        #children_dict[last_tag]=self.children_dict.get(last_tag,[])+[tag_id]
        tag_counter_dict[tag_name]=tag_count+1
        #attrs_dict[tag_id]
        cur_attrs=dict(iter(re.findall('(\w+?)="(.+?)"',tag_str)))
        class_name=""
        original_id=""
        for key,val in cur_attrs.items():
          if key.lower()=="class": class_name=val
          if key.lower()=="id": original_id=val   
        class_list=class_name.split()     
        element_obj=element_tag()
        element_obj.id=original_id
        element_obj.class_name=class_name
        element_obj.class_list=class_list
        element_obj.tag_name=tag_name
        element_obj.open_tag=tag_str
        element_obj.attrs=cur_attrs
        self.tag_obj_dict[tag_id]=element_obj
                
        #actual_id=
      else:
        tag_type='o'
        #if tag_name==main_tag_name_criteria: self.main_keys.append(tag_id)
        open_tags.append(tag_id)
        #self.children_dict[last_tag]=self.children_dict.get(last_tag,[])+[tag_id]
        tag_counter_dict[tag_name]=tag_count+1
        cur_attrs=dict(iter(re.findall('(\w+?)="(.+?)"',tag_str)))
        class_name=""
        original_id=""
        for key,val in cur_attrs.items():
          if key.lower()=="class": class_name=val
          if key.lower()=="id": original_id=val
        class_list=class_name.split()
        element_obj=element_tag()
        element_obj.id=original_id
        element_obj.class_name=class_name
        element_obj.class_list=class_list
        element_obj.tag_name=tag_name
        element_obj.open_tag=tag_str
        element_obj.attrs=cur_attrs

        self.tag_obj_dict[tag_id]=element_obj
        if original_id!="": self.tag_id_dict[original_id]=tag_id
        for class_item in class_list:
          self.tag_class_dict[class_item]=self.tag_class_dict.get(class_item,[])+[tag_id]
        self.tag_id_list.append(tag_id)
    #cur_class=cur_attrs.get("class","")
    #self.attrs_dict[tag_id]=dict(iter(re.findall('(\w+?)="(.+?)"',tag_str))) 
    #print(tag_id, tag_type,cur_attrs, class_list, "id:", original_id)
    print(open_tags)
  def get_elements_by_class(self,class_name0):
    cur_element_auto_ids=self.tag_class_dict.get(class_name0,[])
    return [self.tag_obj_dict[v] for v in cur_element_auto_ids]
  def get_element_by_id(self,original_id0):
    cur_element_auto_id=self.tag_id_dict.get(original_id0,"")
    if cur_element_auto_id=="": return
    return self.tag_obj_dict[cur_element_auto_id]
  def replace_by_id(self,original_id0,new_inner_html):
    cur_el_obj=self.get_element_by_id(original_id0)
    if cur_el_obj==None: return
    original_outer_html=cur_el_obj.outer_html
    new_outer_html=cur_el_obj.open_tag+new_inner_html+cur_el_obj.closing_tag
    return [original_outer_html,new_outer_html]
  def replace_by_class(self,class_name0,new_inner_html):
    cur_element_auto_ids=self.tag_class_dict.get(class_name0,[])
    replacement_pairs=[]
    for auto_tag_id in cur_element_auto_ids:
      cur_el_obj1=self.tag_obj_dict[auto_tag_id]
      #print("??????", auto_tag_id,cur_el_obj1.open_tag,cur_el_obj1.closing_tag)
      original_outer_html=cur_el_obj1.outer_html
      #print("@@@@",cur_el_obj1.inner_html)
      new_outer_html=cur_el_obj1.open_tag+new_inner_html+cur_el_obj1.closing_tag
      replacement_pairs.append([original_outer_html,new_outer_html]) 
    return replacement_pairs
  def replace_by_dict(self,repl_dict0):
    original_html_copy=str(self.original_html_content)
    all_replacements=[]
    for key,val in repl_dict0.items():
      if key.startswith("#"): #we use jquery notation # to indicate element ID
        cur_id_pair=self.replace_by_id(key[1:],val)
        all_replacements.append(cur_id_pair)
      if key.startswith("."): #we use jquery notation . to indicate element classname
        cur_class_pairs=self.replace_by_class(key[1:],val)
        all_replacements.extend(cur_class_pairs) 
    for a,b in all_replacements:
      original_html_copy=original_html_copy.replace(a,b)
    return original_html_copy 
  def update_replace(self, repl_dict0, title, description="",keywords=""):
    out_html=self.replace_by_dict(repl_dict0)  
    new_title="<title>"+title+"</title>" 
    new_description='<meta name="description" content="%s">'%description #"<title>"+title+"</title>" 
    out_html=re.sub('(?i)<title.+?/title>',new_title,out_html)
    out_html=re.sub('(?i)<meta name="description".+?>',new_description,out_html)
    return out_html 


if __name__=="__main__":
  pass