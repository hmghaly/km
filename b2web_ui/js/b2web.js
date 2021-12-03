function init(){
	userid=getCookie("userid")
	if (userid!=""){
		$('.logged-in').show()
		$('.logged-out').hide()
	}
	else {
		$('.logged-in').hide()
		$('.logged-out').show()		
	}

//submitting result click
	$(".results_link").on('click', function(event){
		//event.preventDefault();
		//alert("Hello!")
		trg=event.currentTarget
		console.log(trg)
		tmp_dict=parse_qs()
		tmp_dict["href"]=trg.href
		tmp_dict["id"]=trg.id
		console.log(tmp_dict)
		post_data("send_click",tmp_dict,function(obj1){
			console.log(obj1)
		})

	    // event.current;
	    // event.stopImmediatePropagation();
	    //(... rest of your JS code)
	});	
}

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
function signup_user(){
	//get info from signup form, and upload it to server, and save the email in local storage
	cur_qs_dict=parse_qs()
	form_vals_dict=get_vals("signup")
	form_vals_dict["country"]=cur_qs_dict["country"]
	form_vals_dict["method"]="email"
	//form_vals_dict["user_email"]="test@test.com"//get from local storage - can be different from contact email
	console.log(form_vals_dict)
	if (form_vals_dict.name==null || form_vals_dict.name==undefined || form_vals_dict.name==""){alert("Please enter name");return}
	if (form_vals_dict.email==null || form_vals_dict.email==undefined || form_vals_dict.email==""){alert("Please enter email");return}
	email_is_valid=check_email_str(form_vals_dict.email)
	if (email_is_valid==false){alert("Please enter a valid email");return}	
	if (form_vals_dict.password==null || form_vals_dict.password==undefined || form_vals_dict.password==""){alert("Please enter password");return}
	if (form_vals_dict.password!=form_vals_dict.password2) {alert("Passwords must match");return}

	post_data("signup_user",form_vals_dict,function(obj1){
		console.log(obj1)
		console.log(str(obj1))
		if (obj1.success==true) {
			alert("You successfully signed up")
			$('.modal').modal('hide');
			if (obj1.email!=null) setCookie("userid", obj1.email, 1)
			$('.logged-in').show()
			$('.logged-out').hide()					
		} 
		else alert(obj1.message)
		
		
		
	})

}

function login_user(){
	//get info from login form, and upload it to server, and save the email in local storage
	cur_qs_dict=parse_qs()
	form_vals_dict=get_vals("login_form")	
	console.log(form_vals_dict)
	if (form_vals_dict.email==null || form_vals_dict.email==undefined || form_vals_dict.email==""){alert("Please enter email");return}
	email_is_valid=check_email_str(form_vals_dict.email)
	if (email_is_valid==false){alert("Please enter a valid email");return}	
	if (form_vals_dict.password==null || form_vals_dict.password==undefined || form_vals_dict.password==""){alert("Please enter password");return}
	post_data("login_user",form_vals_dict,function(obj1){
		console.log(obj1)
		console.log(str(obj1))
		if (obj1.success==true) {
			alert("You successfully logged in")
			$('.modal').modal('hide');
			if (obj1.email!=null) setCookie("userid", obj1.email, 1)
			$('.logged-in').show()
			$('.logged-out').hide()				
		} 
		else alert(obj1.message)
		
		
		
	})
}

function logout(){
	delCookie("userid")
	$('.logged-in').hide()
	$('.logged-out').show()
	alert("Logged out successfully")
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
	
	cur_qs_dict=parse_qs()
	form_vals_dict=get_vals("feedback_form")
	form_vals_dict["country"]=cur_qs_dict["country"]
	console.log(form_vals_dict)
	if (form_vals_dict.email==null || form_vals_dict.email==undefined || form_vals_dict.email==""){alert("Please enter email");return}
	email_is_valid=check_email_str(form_vals_dict.email)
	if (email_is_valid==false){alert("Please enter a valid email");return}	

	post_data("send_feedback",form_vals_dict,function(obj1){
		console.log(obj1)
		console.log(str(obj1))
		if (obj1.success==true) {
			alert("Thanks for your feedback!\nWe will email you shortly at the email provided: "+obj1.email)
			$('.modal').modal('hide');
			//if (obj1.email!=null) setCookie("userid", obj1.email, 1)
		} 
		else alert(obj1.message)
		
		
		
	})

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


