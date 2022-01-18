$( document ).ready(function() {
let deleted_top_projects = new Array()
let selected_top_projects = new Array()


$('.collect-top-project-js').on('click',function(){
if(!$(this).is(':checked')){
if(!deleted_top_projects.includes($(this).prop("value"))){
deleted_top_projects.push($(this).prop("value"))
}

}
else{
if(deleted_top_projects.includes($(this).prop("value"))){
removed_item = deleted_top_projects.indexOf($(this).prop("value"))
deleted_top_projects.splice(removed_item, 1);

}
}

$('#deleted_top_projects').prop("value",deleted_top_projects)
console.log("Values of deleted Top projects are: ",$('#deleted_top_projects').val())
})


// handling selected top products
$('.selected-top-project-js').on('click',function(){
if($(this).is(':checked')){
if(!selected_top_projects.includes($(this).prop("value"))){
selected_top_projects.push($(this).prop("value"))
}

}
else{
if(selected_top_projects.includes($(this).prop("value"))){
removed_item = selected_top_projects.indexOf($(this).prop("value"))
selected_top_projects.splice(removed_item, 1);

}
}
$('#selected_top_projects').prop("value",selected_top_projects)
console.log("Values selected of Top projects are: ",$('#selected_top_projects').val())
})


})