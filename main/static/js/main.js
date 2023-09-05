document.getElementById("su-re_password").disabled = true;
document.getElementById("su-re_password").placeholder = 'Confirm Password';
document.getElementsByClassName("btn-primary").disabled = true;

function validate_password(passcode){
    const condition = /^[a-zA-Z\d!@#$%^&*]{8,}$/;
    if(condition.test(passcode)){
        return true;
    }else{
        return false;
    }
}

document.getElementById("su-password").addEventListener("input", function(){
    var password = document.getElementById("su-password").value;
    var re_password = document.getElementById("su-re_password");
    var password_validate = document.getElementById("password_validate");

    if(password===""){
        password_validate.innerHTML = "";
        re_password.placeholder = "Confirm Password";
        re_password.disabled = true;
    }else if (validate_password(password)) {
        password_validate.style.color = "#0bd45c";
        password_validate.innerHTML = "Valid Password";
        re_password.disabled = false;
    }else {
        password_validate.style.color = "red";
        password_validate.innerHTML = "Minimum 8 Characters<br>Special Characters must be !@#$%^&*";
        re_password.disabled = true;
    }
});

document.getElementById("su-re_password").addEventListener("input", function(){
    var password = document.getElementById("su-password").value;
    var re_password = document.getElementById("su-re_password").value;
    var re_password_alert = document.getElementById("re_password_alert");

    if(re_password===""){
        re_password_alert.innerHTML = "";
    }else if(password!=re_password){
        re_password_alert.style.color = "red";
        re_password_alert.innerHTML = "Password Didn't Match";
    }else if(password===re_password){
        re_password_alert.style.color = "#0bd45c";
        re_password_alert.innerHTML = "Password Confirmed";
    }

    var name = document.getElementById("su-name").value;
    var contact = document.getElementById("su-contact").value;
    var email = document.getElementById("su-email").value;
    var password = document.getElementById("su-password").value;
    var re_password = document.getElementById("su-re_password").value;

    if(name!="" && contact!="" && email!="" && validate_password(password)){
        if(password===re_password){
            document.getElementsByClassName("btn-primary0").disabled = false;
        }
    }else{
        alert("Fill all the Required Details");
    }
});

