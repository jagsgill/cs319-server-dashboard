$(document).ready(function () {

	$('#signInForm').on('submit', function (ev) {
	ev.preventDefault();
    console.log("clicked");
    var validLogin = validate();
    if(validLogin) {
    	window.location = "dashboard.html";
    } 
    this.reset();
  	})

  	function validate() {
    	var inputEmail = document.getElementById("inputEmail").value;
  		var inputPassword = document.getElementById("inputPassword").value;
  		if ( inputEmail == "asdf@asdf.com" && inputPassword == "asdf"){
  			return true;
  		} else {
        window.alert("Invalid login information");
  			return false;
  		}
  	}

});
