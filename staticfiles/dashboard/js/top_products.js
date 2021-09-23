$( document ).ready(function() {
let deleted_top_products = new Array()
let selected_top_products = new Array()


$('.collect-top-product-js').on('click',function(){
if(!$(this).is(':checked')){
if(!deleted_top_products.includes($(this).prop("value"))){
deleted_top_products.push($(this).prop("value"))
}

}
else{
if(deleted_top_products.includes($(this).prop("value"))){
removed_item = deleted_top_products.indexOf($(this).prop("value"))
deleted_top_products.splice(removed_item, 1);

}
}

$('#deleted_top_products').prop("value",deleted_top_products)
console.log("Values of deleted Top products are: ",$('#deleted_top_products').val())
})


// handling selected top products
$('.selected-top-product-js').on('click',function(){
if($(this).is(':checked')){
if(!selected_top_products.includes($(this).prop("value"))){
selected_top_products.push($(this).prop("value"))
}

}
else{
if(selected_top_products.includes($(this).prop("value"))){
removed_item = selected_top_products.indexOf($(this).prop("value"))
selected_top_products.splice(removed_item, 1);

}
}
$('#selected_top_products').prop("value",selected_top_products)
console.log("Values selected of Top products are: ",$('#selected_top_products').val())
})


})