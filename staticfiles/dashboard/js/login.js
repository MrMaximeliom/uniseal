$( document ).ready(function() {
console.log("Hi")
let error_messages = JSON.parse($('#my-data').html())

  const togglePassword = $('#eye_password');
  const password = $('#id_password');
  const show = $('#show');
  const hide = $('#hide');

  togglePassword.on('click', function (e) {
    // toggle the type attribute
    let type = password.attr('type')
    if(type === 'password'){
    type = 'text'
    show.css('display','none')
    hide.css('display','block')
    }
    else{
      type = 'password'
      hide.css('display','none');
    show.css('display','block');
    }

    password.attr('type', type);
    // toggle the eye slash icon
});
let form_errors = ''
let no_errors = true
let phone_number_regex_no_zero = /^9\d{8}$|^1\d{8}$/g
let phone_number_regex_with_zero = /^09\d{8}$|^01\d{8}$/g
// check username field as the user types it down
$("#id_username").keyup(function(){
let current_username_error_msg = ''
let current_password_error_msg = ''
let username_errors = "phone number contains only numbers with 10 digits"
let username_errors_space = $('#username_errors')
//let password_errors_space = $('#password_errors')
if($("#id_username").val() === ''){
//username_errors_space.html("it should not be empty")
current_username_error_msg = error_messages.username_empty_error
no_errors = false
}
else{
//username_errors_space.html(username_errors)
if (!phone_number_regex_no_zero.test($("#id_username").val()) && !phone_number_regex_with_zero.test($("#id_username").val())){
current_username_error_msg = error_messages.username_bad_format
no_errors = false
}
else{
no_errors = true
}

}
//console.log($("#id_username").val())
if(no_errors){
current_username_error_msg=''
}
username_errors_space.html(current_username_error_msg)
console.log("has errors value: ",no_errors)


})

// check password field as the user types it down
$("#id_password").keyup(function(){
//let current_username_error_msg = ''
let current_password_error_msg = ''
//let username_errors = "phone number contains only numbers with 10 digits"
let password_errors_space = $('#password_errors')
if($("#id_password").val() === ''){
//username_errors_space.html("it should not be empty")
current_password_error_msg = error_messages.password_empty_error
has_errors = true
}
else{
has_errors = true
}
//else{
////username_errors_space.html(username_errors)
//if (!phone_number_regex_no_zero.test(word) && !phone_number_regex_with_zero.test(word)){
//current_password_error_msg = error_messages.username_bad_format
//has_errors = true
//}
//else{
//has_errors = false
//}
//
//}
//console.log($("#id_username").val())
if(no_errors){
current_username_error_msg=''
}
password_errors_space.html(current_password_error_msg)
console.log("has errors value: ",no_errors)

})
console.log("has errors value: ",no_errors)

// when the user tries to submit check that there is no errors in his data
$('#login_btn').on('click',function(event){
// check if form has no errors then it will submit

return no_errors

})


})