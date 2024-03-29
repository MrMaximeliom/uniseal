let error_messages
$( document ).ready(function() {
error_messages = JSON.parse($('#my-data').html())
console.log(new Date().getFullYear())
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
console.log("selected pages are: ",selected_pages)
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
else if(selected_value == 'project'){
$('#searchPhrase').prop("placeholder","search by project name ..")
}
else if(selected_value == 'beneficiary'){
$('#searchPhrase').prop("placeholder","search by beneficiary name ..")
}
else if(selected_value == 'main_material'){
$('#searchPhrase').prop("placeholder","search by main material name ..")
}
else if(selected_value == 'type'){
$('#searchPhrase').prop("placeholder","search by project type name ..")
}
else if(selected_value == 'city'){
$('#searchPhrase').prop("placeholder","search by city name ..")
}
else if(selected_value == 'state'){
$('#searchPhrase').prop("placeholder","search by state name ..")
}
else if(selected_value == 'area'){
$('#searchPhrase').prop("placeholder","search by area name ..")
}
else if(selected_value == 'country'){
$('#searchPhrase').prop("placeholder","search by country name ..")
}
else if(selected_value == 'selling_point_name'){
$('#searchPhrase').prop("placeholder","search by selling point name ..")
}
else if(selected_value == 'selling_point_name'){
$('#searchPhrase').prop("placeholder","search by selling point name ..")
}
else if(selected_value == 'title'){
$('#searchPhrase').prop("placeholder","search by notification title ..")
}
else if(selected_value == 'body'){
$('#searchPhrase').prop("placeholder","search by notification body ..")
}
else if(selected_value == 'os_type'){
$('#searchPhrase').prop("placeholder","search by OS type..")
}
else if(selected_value == 'top_products'){
$('#searchPhrase').prop("placeholder","search by product name in top products")
}


if(selected_value == "execution_year"){
$('#search_phrase_holder').css('display','none')
$('#search_phrase_date_holder').css('display','block')
}
else{
$('#search_phrase_holder').css('display','block')
$('#search_phrase_date_holder').css('display','none')
}

})
function validate_string_search_phrase(search_phrase,search_option){
let error_message
console.log("search option is: ",search_option)
if(search_option == 'username'){

error_message =  error_messages.username_error
}
else if(search_option == 'full_name'){

error_message =  error_messages.full_name_error
}
else if(search_option == 'organization'){

error_message =  error_messages.organization_error
}
else if(search_option == 'product'){

error_message =  error_messages.product_error
}
else if(search_option == 'category'){

error_message =  error_messages.category_error
}
else if(search_option == 'supplier'){
error_message =  error_messages.supplier_error
}
else if(search_option == 'project'){
error_message =  error_messages.project_error
}
else if(search_option == 'beneficiary'){
error_message =  error_messages.beneficiary_error
}
else if(search_option == 'main_material'){
error_message =  error_messages.main_material_error
}
else if(search_option == 'type'){
error_message =  error_messages.type_error
}
else if(search_option == 'application'){
error_message =  error_messages.application_error
}
else if(search_option == 'country'){
console.log("here nowww!!")
error_message =  error_messages.country_error
}
else if(search_option == 'state'){
error_message =  error_messages.state_error
}
else if(search_option == 'city'){
error_message =  error_messages.city_error
}
else if(search_option == 'area'){
error_message =  error_messages.area_error
}
else if(search_option == 'selling_point_name'){
error_message =  error_messages.point_error
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
else if(search_option == 'category'){
dash_regex = /([A-Z])*\s*\W*(a-z)*\s*\w+/g

console.log(tempHolder)
if(dash_regex.test(tempHolder)){
return true
}
else{
console.log("search_option is: ", search_option)
console.log(special_chars_array)
console.log("showing error message ",error_message)
$('#search_phrase_error').html(error_message)
$('#search_phrase_error').css('display','block')
return false
}
}
else if(search_option == 'country' || search_option == 'state' || search_option == 'city' || search_option == 'selling_point_name'){
dash_regex = /([A-Z])*\s*\W*(a-z)*\s*\w+/g
names_with_dashes = /\w+[-]*\s*/g
console.log(tempHolder)
if(dash_regex.test(tempHolder) || names_with_dashes.test(tempHolder) ){
return true
}
else{
console.log("search_option is: ", search_option)
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
}}
$('#searchButton').on('click',function(event){
$('#selection_error').html('')
$('#search_phrase_error').html('')
$('#search_phrase_date_error').html('')
console.log("in this function")
if($('#search_phrase_holder').css('display') == 'block'){
console.log("search phrase holder not hidden")
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
if($('#searchBy').find(":selected").prop("value")  == null){

if($('#searchPhrase').prop("value") == ''){
$('#search_phrase_error').html(error_messages.empty_search_phrase)
$('#search_phrase_error').css('display','block')
return false
}
else{
return validate_string_search_phrase($('#searchPhrase').prop("value"),$('#searchButton').prop("value"))

}
}
return validate_string_search_phrase($('#searchPhrase').prop("value"),$('#searchBy').find(":selected").prop("value"))
}}
else{
console.log($('#searchPhraseDate').prop("value") )
if($('#searchBy').find(":selected").prop("value") == "none"){
$('#selection_error').html(error_messages.empty_search_phrase)
$('#selection_error').css('display','block')
console.log("please select value first")
return false
}
else{
if($('#searchPhraseDate').prop("value") != "" ){
return true
}
else{
console.log("please enter execution date first")
$('#search_phrase_date_error').html(error_messages.execution_date_error)
$('#search_phrase_date_error').css('display','block')
return false
}
}
}
})