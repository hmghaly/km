#!/usr/bin/python
#A script to preprocess the output of AI classification
#first unzip the results in the respective country/directory
#and update the info_dict sqlite dict for key-value pairs accordingly
import shutil, shelve, os, sys, time, json
import zipfile
from zipfile import ZipFile
from sqlitedict import SqliteDict

if __name__=="__main__":
	print sys.argv
	country="au"
	country_dir=os.path.join("main",country)
	if len(sys.argv)>1: country=sys.argv[1]
	#for fname in os.listdir(country):
	for fname in os.listdir(country_dir):
		if not fname.endswith(".zip"): continue
		#zip_fpath=os.path.join(country,fname)
		zip_fpath=os.path.join(country_dir,fname)
		unzip_dir=zip_fpath.replace(".zip","")
		print zip_fpath	
		t0=time.time()
		zip_ref=zipfile.ZipFile(zip_fpath, 'r')
		zip_ref.extractall(unzip_dir)
		zip_ref.close()
		t1=time.time()
		elapsed=t1-t0
		print("finished unzipping in %s seconds"%elapsed)
		print("now processing the info_dict")
		info_dict_fpath=os.path.join(unzip_dir,"info_dict.txt")
		#shelve_fopen=shelve.open("info_dict.shelve")
		sqlite_path=os.path.join(country_dir,"info_dict.sqlite")
		mydict = SqliteDict(sqlite_path, autocommit=True)
		#mydict = SqliteDict('./info_dict.sqlite', autocommit=True)

		info_fopen=open(info_dict_fpath)
		processed_counter=0
		t0=time.time()
		for i,line in enumerate(info_fopen):
			if i%1000==0: print(i)
			#if i>10: break
			line_split=line.strip().split("\t")
			if len(line_split)!=2: continue
			key,val=line_split
			
			found=mydict.get(key)
			if found==None: 
				tmp_val_dict=json.loads(val)
				tmp_meta_dict=tmp_val_dict.get("meta",{})
				title=tmp_meta_dict.get("title","")
				description=tmp_meta_dict.get("description","")
				tmp_val_dict["title"]=title
				tmp_val_dict["description"]=description
				tmp_val_dict.pop('meta', None)

				mydict[key] =json.dumps(tmp_val_dict)  #val
				#shelve_fopen[key]=val #update the info_dict shelve only for new items
				processed_counter+=1
		info_fopen.close()
		#shelve_fopen.close()
		mydict.close()	
		t1=time.time()
		elapsed=t1-t0		
		print("finished processing info dict - %s items added in %s seconds"%(processed_counter,elapsed))
