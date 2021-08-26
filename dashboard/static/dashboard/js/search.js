let error_messages
$( document ).ready(function() {
error_messages = JSON.parse($('#my-data').html())
console.log(error_messages.sd)

})

// if user chooses to select all pages , then select all pages also in export data functionality

$('#allData-report').on("click",function(){
// check if it's checked or not
if($(this).is(':checked')){
// make all input fields for pages checked also
$('.page-js').each(function(){
  $(this).prop("checked",true);
})
}
else{
// else make them unchecked
$('.page-js').each(function(){
  $(this).prop("checked",false);
})
}
});

// get all selected pages into hidden field
let collector_value = $('#pages_collector').prop("value")
let selected_pages = new Array()
$('.page-js').on("click",function(){
if($(this).is(':checked')){
if(!selected_pages.includes($(this).prop("value"))){
selected_pages.push($(this).prop("value"))
}

}
else{
console.log("it unchecked now")
if(selected_pages.includes($(this).prop("value"))){
console.log("yeah it contains it")
removed_item = selected_pages.indexOf($(this).prop("value"))
selected_pages.splice(removed_item, 1);
}
}
$('#pages_collector').prop("value",selected_pages)
});

$('#searchBy').on('change',function(){
// get selected option text
let selected_value = $('#searchBy').find(":selected").prop("value");
// search in product pages
if(selected_value == 'none'){
$('#searchPhrase').prop("placeholder","Search ..")
}
else if(selected_value == 'product'){
$('#searchPhrase').prop("placeholder","search by product name ..")
}
else if(selected_value == 'category'){
$('#searchPhrase').prop("placeholder","search by category name ..")
}
else if(selected_value == 'supplier'){
$('#searchPhrase').prop("placeholder","search by supplier name ..")
}
// search in users pages
else if(selected_value == 'full_name'){
$('#searchPhrase').prop("placeholder","search by full name ..")
}
else if(selected_value == 'username'){
$('#searchPhrase').prop("placeholder","search by username ..")
}
else if(selected_value == 'organization'){
$('#searchPhrase').prop("placeholder","search by organization name ..")
}
else if(selected_value == 'phone_number'){
$('#searchPhrase').prop("placeholder","search by phone number ..")
}
})
function validate_string_search_phrase(search_phrase,search_option){
let error_message
console.log("search option is: ",search_option)
if(search_option == 'username'){
console.log("username error man")
error_message =  error_messages.username_error
}
else if(search_option == 'full_name'){
console.log("full name error man")
error_message =  error_messages.full_name_error
}
else if(search_option == 'organization'){
console.log("organization error man")
error_message =  error_messages.organization_error
}
else if(search_option == 'product'){
console.log("organization error man")
error_message =  error_messages.product_error
}
else if(search_option == 'category'){
console.log("organization error man")
error_message =  error_messages.category_error
}
else if(search_option == 'supplier'){
console.log("organization error man")
error_message =  error_messages.supplier_error
}

const special_chars_regex = /\W+/g;
//let search_phrase = $('#searchPhrase').prop("value")
// test for any errors before submitting
let tempHolder = search_phrase.trim()
// remove start and end spaces
modified_search_phrase =  tempHolder
//  extract words only from search phrase
extracted_words = modified_search_phrase.split(' ')
special_chars_array = new Array()
if(search_option == 'product'){
dash_regex = /\w+[-]+\w+$/g
extracted_words.forEach((word) => {
if (special_chars_regex.test(word) && !dash_regex.test(word)){
special_chars_array.push(word)
}
})
if(special_chars_array.length == 0){
return true
}
else{
console.log(special_chars_array)
console.log("showing error message ",error_message)
$('#search_phrase_error').html(error_message)
$('#search_phrase_error').css('display','block')
return false
}
}
else{
extracted_words.forEach((word) => {
if (special_chars_regex.test(word)){
//dash_regex = /[-]+/g
//if(dash_regex.test(word)){
//console.log("word is: ",word)
//console.log("word can pass")
//}
special_chars_array.push(word)
}
})
if(special_chars_array.length == 0){
return true
}
else{
console.log(special_chars_array)
console.log("showing error message ",error_message)
$('#search_phrase_error').html(error_message)
$('#search_phrase_error').css('display','block')
return false
}

}


}
function validate_phone_number(search_phrase){
const default_phone_regex = /^9\d{8}$|^1\d{8}$/
const phone_regex = /^09\d{8}$|^01\d{8}$/
if(default_phone_regex.test(search_phrase) || phone_regex.test(search_phrase)){
return true
}
else{
$('#search_phrase_error').html(error_messages.phone_number_error)
$('#search_phrase_error').css('display','block')

return false
}


}
$('#searchButton').on('click',function(event){
$('#selection_error').html('')
$('#search_phrase_error').html('')

if($('#searchBy').find(":selected").prop("value") == "none"){
$('#selection_error').html(error_messages.empty_search_phrase)
$('#selection_error').css('display','block')
console.log("please select value first")

return false
}
else if($('#searchBy').find(":selected").prop("value") == "phone_number"){
return validate_phone_number($('#searchPhrase').prop("value"))
}
else{
console.log("here now")
return validate_string_search_phrase($('#searchPhrase').prop("value"),$('#searchBy').find(":selected").prop("value"))
}


})