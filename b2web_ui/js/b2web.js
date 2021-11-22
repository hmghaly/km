//managing websites
function submit_website(){
	//ading a business website - with its url- category - country, and corresponding info: description, location(s)
	//get_vals
	cur_qs_dict=parse_qs()
	form_vals_dict=get_vals("add_business_frm")
	form_vals_dict["country"]=cur_qs_dict["country"]
	form_vals_dict["user_email"]="test@test.com"//get from local storage - can be different from contact email
	console.log(form_vals_dict)
	post_data("add_business",form_vals_dict,function(obj1){
		console.log(obj1)
		console.log(str(obj1))
		alert("Your website is successfully added! Check your profile for all the websites you submitted.")
		$('.modal').modal('hide');
	})
}

function remove_website(){
	//removing a website from a category-country
}

function update_website(){
	//updating name/description/location info of a website
}

function sponsor_website(){
	//updating sponsored data for a manually submitted website, to indicate which categories it is sponsored in, and timeframes
}


//login-signup functions
function email_signup_user(){
	//get info from signup form, and upload it to server, and save the email in local storage
}

function email_login_user(){
	//get info from login form, and upload it to server, and save the email in local storage
}

function continue_with_google(){
	//both login/signup through google, and upload the email/info to server, and save the email in local storage
}

function get_user_profile(){
	//get the profile of the user, name/update password options, list of submitted/sponsored website
	//premium - subscribed account - download results without paying for each download
}

//send message/feedback
function send_feedback(){
	//get info from send feedback form and upload it to server to send email to b2web
}

//share results by email
function email_share_results(){
	//get info from share results by email form and upload it to server to send email to both sharer and the one shared with
}

//Download results
function email_download_results(){
	//options - download all results (57) $5 ==> if less than 100 - download first 100 results ($10), first 200 ($15) - contact us for downloading larger number of results
	//get the download data - check if user is logged in - provide payment options, with successful payment, success message
	//receive the data by email - make sure to check spam folders - also provide a link to download the data
}


function search_for_category(){
	//from a search query, identify the corresponding categories
	//resultModal
	//document.getElementById("resultModal").showModal();
	cur_qs_dict=parse_qs()
	search_val=$$("input_category_search").value.toLowerCase()
	country=cur_qs_dict["country"]
	console.log([search_val,country])
	form_vals_dict={"query":search_val}
	post_data("cat_vec",form_vals_dict,function(obj1){
		console.log(obj1)
		console.log(str(obj1))
		$$("search_category_content").innerHTML="<ul>"
		for (item of obj1){
			//<li><i class="fal fa-tag"></i>Category name</li>
			cat0=item[0]
			cat_name0=item[1]
			href="category?country=_country_&cat=_cat_".replace("_country_",country).replace("_cat_",cat0)
			link='<a href="_href_">_cat_name_</a>'.replace("_href_",href).replace("_cat_name_",cat_name0)
			full_str='<li><i class="fal fa-tag"></i> _link_</li><br>'.replace("_link_",link)
			$$("search_category_content").innerHTML+=full_str
			console.log(full_str)
		}
		$$("search_category_content").innerHTML+="</ul>"
		//alert("Your website is successfully added! Check your profile for all the websites you submitted.")
		//$('.modal').modal('hide');
	})

	// form_vals_dict=get_vals("add_business_frm")
	// form_vals_dict["country"]=cur_qs_dict["country"]

	$("#resultModal").modal()
	//alert("Hello!")
}