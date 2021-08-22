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
