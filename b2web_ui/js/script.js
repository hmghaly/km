function $$(el_id){
    return document.getElementById(el_id)
}

function today(){
    date_str=new Date().toLocaleDateString('en-GB')
    return date_str
}

function img(src,onload=null,id=""){ //create img object
    new_img=new Image()
    
    if (id!="") new_img.id=id;
    if (onload!=null) new_img.onload=onload
    new_img.src=src;
    return new_img
}

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}


//utility functions, python style
function len(list1){
    return list1.length
}

function is_in(small,big){
    if (big.indexOf(small)>-1) return true
    else return false
}

function int(str_digits) {
    return parseInt(str_digits)
} 
function float(str_digits) {
    return parseFloat(str_digits)
} 

function str(myVar) {
    if (typeof myVar === 'string' || myVar instanceof String) return myVar
    return JSON.stringify(myVar)
} 
function make_str_array(array0) { // convert ["a",1,3,5] into ["a","1","3","5"] 
    new_array_of_strings=[]
    for (ar0 of array0) new_array_of_strings.push(str(ar0))
    return new_array_of_strings
} 


function get_percent(ratio){
    cur_int_percent=Math.round(100*ratio)
    return ""+cur_int_percent+"%"
}


function create_hyperlink(link_name,link_fn){
    // cur_link=document.createElement("a")
    // cur_link.href="javascript:void(0)"
    // cur_link.name=link_name
    // cur_link.onclick=link_fn //show_conj_modal
    // cur_link.innerHTML=link_name
    if (link_fn=="" || link_fn==null || link_fn==undefined) return link_name

    cur_link='<a href="javascript:void(0)" name="_name_" onclick="_function_(this)">'+link_name+"</a>"
    cur_link=cur_link.replace("_name_",link_name)    
    cur_link=cur_link.replace("_function_",link_fn)    
    return cur_link
}

function load_images(img_list,callback_fn=null){ //loading a group of images, adding them to images variable/namespace
    images.loaded_images=[] //we need to have a global variable called "images"
    for (im in img_list){
        cur_img_src=img_list[im]
        cur_img_src_split=cur_img_src.split("/")
        cur_img_id=cur_img_src_split[cur_img_src_split.length-1].split(".")[0]
        console.log(cur_img_id)
        new_img=new Image()
        new_img.src=cur_img_src
        new_img.id=cur_img_id
        images[cur_img_id]=new_img
        new_img.onload=function(){
            console.log(this)
            images.loaded_images.push(cur_img_id)
            if (images.loaded_images.length==img_list.length) callback_fn()
        }
        new_img.onerror=function(){
            console.log("error", this)
            images.loaded_images.push(cur_img_id)
            if (images.loaded_images.length==img_list.length) callback_fn()
        }        
    }
}

function load_sounds(sound_list,callback_fn=null){ //loading a group of sounds, adding them to images variable/namespace
    sounds.loaded_sounds=[] //we need to have a global variable called "sounds"
    for (snd in sound_list){
        cur_snd_src=sound_list[snd]
        cur_snd_src_split=cur_snd_src.split("/")
        cur_snd_id=cur_snd_src_split[cur_snd_src_split.length-1].split(".")[0]
        //console.log(cur_snd_id)
        new_snd=new Audio()
        new_snd.src=cur_snd_src
        new_snd.id=cur_snd_id
        //console.log(new_snd)
        sounds[cur_snd_id]=new_snd
        new_snd.addEventListener('canplaythrough', function() { 
           console.log(this)
            sounds.loaded_sounds.push(cur_snd_id)
            if (sounds.loaded_sounds.length==sound_list.length) callback_fn()
        }, false);
        new_snd.onerror=function(){
            console.log("error", this)
            sounds.loaded_sounds.push(cur_snd_id)
            if (sounds.loaded_sounds.length==sound_list.length) callback_fn()
        }        
    }
}

function aud(src,id="",onload=null,onended=null){ //create audio object
    new_aud=new Audio()
    new_aud.src=src;
    if (id!="") new_aud.id=id;
    if (onload!=null) new_aud.onload=onload
    if (onended!=null) new_aud.onended=onended
    return new_aud
}


function hide_class(class_name){
    all_class_items=document.getElementsByClassName(class_name)        
    for (am in all_class_items) all_class_items[am].hidden=true;        
}
function show_class(class_name){
    all_class_items=document.getElementsByClassName(class_name)        
    for (am in all_class_items) all_class_items[am].hidden=false;        
}
    
function shuffle(a) {
    var j, x, i;
    for (i = a.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        x = a[i];
        a[i] = a[j];
        a[j] = x;
    }
    return a;
}

function set_local_strorage(obj_name,obj_key,obj_val){
  retrieved_obj=localStorage.getItem(obj_name);
  parsed=JSON.parse(retrieved_obj)
  if (parsed==null) parsed={}
  parsed[obj_key]=obj_val
  localStorage.setItem(obj_name, JSON.stringify(parsed));
}


function get_local_strorage(obj_name,obj_key){
  retrieved_obj=localStorage.getItem(obj_name);
  parsed=JSON.parse(retrieved_obj)
  if (parsed==null) parsed={}
  val=parsed[obj_key]
  //parsed[obj_key]=obj_val
  //localStorage.setItem(obj_name, JSON.stringify(parsed));
  return val
}


function create_dict(dict_obj,nested_keys,default_val=null){
    tmp=dict_obj
    for (ki in nested_keys) {
        k0=nested_keys[ki]
        // console.log(k0)
        check0=tmp[k0]
        // console.log(check0)
        if (check0==null || check0==undefined) {
            if (ki==len(nested_keys)-1 && default_val!=null) tmp[k0]=default_val
            else tmp[k0]={}
        } 
        tmp=tmp[k0]
        // console.log(tmp)
    }
    // console.log(dict_obj)
    return dict_obj
}

//incrementing a dictionary with arbitrary subkeys dict["a"]["b"]["c"]["d"]
function increment_dict(dict_obj,nested_keys){
    tmp=dict_obj
    for (ki in nested_keys) {
        k0=nested_keys[ki]
        check0=tmp[k0]
        if (check0==null || check0==undefined) {
            if (ki==len(nested_keys)-1) {
                if (tmp[k0]==null) tmp[k0]=0
            } 
            else tmp[k0]={}
        }
        if (ki==len(nested_keys)-1){
            if (tmp[k0]==null) tmp[k0]=0
            tmp[k0]+=1
        }
        tmp=tmp[k0]
    }
    return dict_obj 
}

//get the value of a dict with certain subkeys, else return zero
function get_dict_OLD(dict_obj,nested_keys){
    tmp=dict_obj
    for (ki in nested_keys) {
        k0=nested_keys[ki]
        check0=tmp[k0]
        if (check0==null || check0==undefined) {
            if (ki==len(nested_keys)-1) {
                if (tmp[k0]==null) tmp[k0]=0
            } 
            else tmp[k0]={}
        }
        if (ki==len(nested_keys)-1){
            if (tmp[k0]==null) tmp[k0]=0
            //tmp[k0]+=1
        }
        tmp=tmp[k0]
    }
    return tmp 
}

function set_dict(dict_obj,nested_keys,val0){
    tmp=dict_obj
    for (ki in nested_keys) {
        k0=nested_keys[ki]
        if (ki==len(nested_keys)-1) tmp[k0]=val0
        else{
            check0=tmp[k0]
            if (check0==null || check0==undefined) tmp[k0]={}
        }

        tmp=tmp[k0]
    }
    return dict_obj 
}

function get_dict(dict_obj,nested_keys,val0){
    tmp=dict_obj
    for (ki in nested_keys) {
        k0=nested_keys[ki]
        check0=tmp[k0]
        if (ki==len(nested_keys)-1) {
            if (check0==null || check0==undefined) tmp[k0]=val0
        } 
        else{
            if (check0==null || check0==undefined) tmp[k0]={}
        }

        tmp=tmp[k0]
    }
    return tmp 
}


function create_el_basic(el_tag,el_parent){
    var el0=document.createElement(el_tag)
    el_parent.appendChild(el0)
    return el0
}

function create_el(el_tag,el_parent,el_id,el_name,el_html){
    var el0=document.createElement(el_tag)
    el_parent.appendChild(el0)
    if (el_id!="") el0.id=el_id
    if (el_name!="") el0.name=el_name
    if (el_html!="") el0.innerHTML=el_html
    return el0
}

function create_table(parent_el,array1){
    table_el=create_el_basic("table",parent_el)
    for (const item0 of array1){
        var row = table_el.insertRow(-1);
        for (const sub_item of item0){
            var cell0 = row.insertCell(-1);
            cell0.innerHTML=sub_item
        }
    }
    return table_el
}

function fill_table(table_id,array1){
    table_el=$$(table_id)
    table_el.innerHTML=""
    for (const item0 of array1){
        var row = table_el.insertRow(-1);
        for (const sub_item of item0){
            var cell0 = row.insertCell(-1);
            cell0.innerHTML=sub_item
        }
    }
    return table_el    
}
function post_data(link,obj2upload,callback_fn){
    //we expect both uploaded data and received data to be of json format
    fetch(link,
      {
          method: "POST",
          body: JSON.stringify(obj2upload)
      })
      .then(function(res){ return res.json(); })
      .then(function(data){
        //console.log(data)
        callback_fn(data)
      })  
      // .catch(error => {
      //     console.error('Error:', error);
      //   });  
}

function read_file(file_path,callback_fn){
    fetch(file_path)
      .then(function(res){ return res.json(); })
      .then(function(data){
        callback_fn(data)
      })      
}

function check_email_str(email_str){
    split=email_str.split("@")
    if (split.length!=2) return false
    domain_split=split[1].split(".")
    if (domain_split.length<2) return false
    return true
}

function show_screen(screen_id){
    $(".screen").hide()
    $("#"+screen_id).show()
    $$(screen_id).hidden=false;
    return $$(screen_id)
}
function gen_options(correct_option,option_pool,n_options=4){
    option_pool_copy=option_pool.slice()
    shuffle(option_pool_copy)
    cur_i=option_pool_copy.indexOf(correct_option)
    option_pool_copy.splice(cur_i, 1);
    cur_options=[correct_option]
    for (var i=0;i<n_options-1;i++) cur_options.push(option_pool_copy[i])
    return cur_options
    
}

function get_1st_random(items){
    shuffle(items)
    return items[0]
}

////add line break to split text across multiple lines, specifying maximum width in characters
function multiline1(txt,max_size){
    words=txt.split(" ")
    new_words=[]  
    offset=0
    for (wd in words){
        cur_word=words[wd]
        offset+=cur_word.length
        if (offset>max_size){
            new_words.push("\n"+cur_word)
            offset=0
        }
        else new_words.push(cur_word)
    }
    out= $.trim(new_words.join(" "))
    return out
    
}



////add line break to split text across multiple lines, specifying maximum width in characters, 
//respecting the original breaks, and also respecting the <br> breaks if any
function multiline(txt,max_size){
    final_segs=[]
    txt=txt.split("\n").join("<br>")
    segs=txt.split("<br>")
    for (const sg of segs){
        words=sg.split(" ")
        new_words=[]  
        offset=0
        for (wd in words){
            cur_word=words[wd]
            offset+=cur_word.length
            if (offset>max_size){
                new_words.push("\n"+cur_word)
                offset=0
            }
            else new_words.push(cur_word)
        }
        out= $.trim(new_words.join(" ")) //need to have jquery
        final_segs.push(out)
        
    }
    final_str=final_segs.join("\n")
    return $.trim(final_str)
    
}

//turn a list of items into a list of lists
function nesting(list1,max_sublist_size){
    sublist_items=[]
    list_of_lists=[]
    for (it in list1){
        cur_item=list1[it]
        sublist_items.push(cur_item)
        if (sublist_items.length==max_sublist_size){
            list_of_lists.push(sublist_items)
            sublist_items=[]
        }
    }    
    if (sublist_items.length>0) list_of_lists.push(sublist_items)
    return list_of_lists
}

function split(txt){
    if (txt=="") return []
    txt=$.trim(txt)
    items=[]
    txt_split=txt.split(" ")
    for (ts in txt_split) items.push($.trim(txt_split[ts]))
    return items
}

function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

function push(list,item){ //push an item to an array that may have not been defined before
    if (list==undefined || list==null) list=[]
    list.push(item)
    return list
}

function filter_list(list,key,val){ //array of objects- get only items with certain value for a key
    new_list=[]
    for (it in list){
        cur_item=list[it]
        if (cur_item[key]==val) new_list.push(cur_item)
    }
    return new_list
}

function get_vals(class_name){ //get the vals from inputs of a form
    val_dict={}
    elements=document.getElementsByClassName(class_name)
    used_names=[] //to address radio buttons, where inputs have the same names
    for (el in elements){
        cur_el=elements[el]
        el_name=cur_el.name
        el_value=cur_el.value
        if (el_name==null || el_name==undefined) continue
        if (el_value==null || el_value==undefined) continue
        if (used_names.indexOf(el_name)>-1) continue
        
        if (cur_el.type=="radio"){
            used_names.push(el_name)
            var radios = document.getElementsByName(el_name);
            for (rd in radios){
                //check if the radio button is of the same class
                cur_rd=radios[rd]
                if (cur_rd.checked) val_dict[el_name]=cur_rd.value
            }
        }
        else if (cur_el.type=="checkbox") val_dict[el_name]=cur_el.checked
        else val_dict[el_name]=el_value
    }
    return val_dict
}

function apply_form_vals(val_dict,form_class_name){
    elements=document.getElementsByClassName(form_class_name)
    used_names=[] //to address radio buttons, where inputs have the same names
    for (el in elements){
        cur_el=elements[el]
        el_name=cur_el.name
        dict_val=val_dict[el_name]
        console.log(dict_val,el_name)
        if (dict_val==null || dict_val==undefined) continue 
        
        // el_value=cur_el.value
        if (el_name==null || el_name==undefined) continue
        //if (el_value==null || el_value==undefined) continue
        if (used_names.indexOf(el_name)>-1) continue
        
        if (cur_el.type=="radio"){
            used_names.push(el_name)
            var radios = document.getElementsByName(el_name);
            for (rd in radios){
                //check if the radio button is of the same class
                cur_rd=radios[rd]
                //if (cur_rd.checked) val_dict[el_name]=cur_rd.value
                if (val_dict[el_name]=cur_rd.value) cur_rd.checked=true   
            }
        }
        else if (cur_el.type=="checkbox") cur_el.checked=val_dict[el_name]
        else cur_el.value=dict_val //val_dict[el_name]=el_value
    }
    return val_dict    
}

function listToMatrix(list, elementsPerSubArray) {
    var matrix = [], i, k;

    for (i = 0, k = -1; i < list.length; i++) {
        if (i % elementsPerSubArray === 0) {
            k++;
            matrix[k] = [];
        }

        matrix[k].push(list[i]);
    }

    return matrix;
}  


//Query string functions - get the parameters from the query string
function parse_qs(){
    qs_dict={}
    qs=window.location.search.slice(1)
    amp_split=qs.split("&")
    for (const am of amp_split){
        eq_split=am.split("=")
        if (eq_split.length==2)  qs_dict[eq_split[0]]=eq_split[1] //we should strip/trim spaces if any
    }
    return qs_dict
}

//create a query string from a parameters dict
function join_qs(data_dict){
    items=[]
    for (key in data_dict){
        val=data_dict[key]
        cur_item=key+"="+val
        items.push(cur_item)
    }
    return items.join("&")
}

function seconds2str(seconds){
    n_seconds=seconds%60
    n_minutes=(seconds-n_seconds)/60
    n_minutes_str=""+n_minutes
    n_seconds_str=""+n_seconds
    if (n_seconds_str.length==1) n_seconds_str="0"+n_seconds_str
    timer_str=n_minutes_str+":"+n_seconds_str   
    return timer_str
}

function start_timer(timer_id,callback_fn,interval=1000){ //
    timer_str=seconds2str(timer.remianing_time)
    $$(timer_id).innerHTML=timer_str
    timer.starter = setInterval(function(){
        //console.log(timer.remianing_time)
        if (timer.remianing_time==null) { //there is a bug causing timer to continue counting even after clearinterval
            //timer={}
            clearInterval(timer.starter)
            return
        } 
        timer.remianing_time-=interval/1000 //milliseconds
        //console.log(timer.remianing_time)
        timer_str=seconds2str(timer.remianing_time)
        $$(timer_id).innerHTML=timer_str
        if (timer.remianing_time<=0) {
            console.log("timer ended",timer.remianing_time)
            timer.remianing_time=null

            callback_fn()
            //clearInterval(timer.starter)
            //timer.remianing_time=null
            // console.log("timer finished")
            // console.log(this)
            
        } 
        //if (timer.remianing_time==null) return
    }, interval);

    //console.log(timer_str)
}

function pause_timer(){
    clearInterval(timer.starter)
}


function sort_array(array0,element_i,ascending=true){
    if (element_i<0) element_i=len(array0[0])+element_i //to account for situations with negative index e.g. last element -1
    array_copy=copy_obj(array0)
    array_copy = array_copy.sort(function(a,b) {
        if (ascending) return a[element_i] - b[element_i];
        else return b[element_i] - a[element_i];
    });  
    return  array_copy
}

function copy_obj(obj1){
    return JSON.parse(JSON.stringify(obj1))
}
// arr = arr.sort(function(a,b) {
//     return a[1] - b[1];
// });
