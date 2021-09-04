$( document ).ready(function() {
// event for adding new image block
$(".hover").mouseleave(
  function() {
    $(this).removeClass("hover");
  }
);
//////////////////////////////////
//let default_checked;
$("#exampleFormControlInput1").on('change',function(){
let parent_div = $('#new-images-js');
//console.log($("#exampleFormControlInput1").prop('files'))
let images = $("#exampleFormControlInput1").prop('files')

$(".new_img").each(function(){
$(this).remove();
})
for (var i = 0; i < images.length; i++){
console.log(images[i].name)
let new_img = $('<img src='+URL.createObjectURL(images[i])+' class="new_img" alt='+images[i].name+'dd width=200px  height=200px />');
new_img.css('margin','5px')
$(parent_div).append(new_img)



}

})
$( ".input-default-js" ).click( function() {
let current_index = $( ".input-default-js" ).index($(this));
$('.input-default-js').not(this).each(function(){
  $(this).prop("checked",false);
})
$('.input-delete-js').each(function(){

  if($('.input-delete-js').index($(this)) == current_index ){
    $(this).prop("checked",false);
  $(this).prop( "disabled", true );

  }
  else{
   $(this).prop( "disabled", false );
  }
})
});

$( ".input-delete-js" ).click(function() {
 if($(this).is(':checked')){
 console.log("its checked")
 }
 else{
 console.log("not checked")
 }
});
// displaying images after selecting them
$("#id_image").on('change',function(){
let parent_div = $('#new-images-js');
//console.log($("#exampleFormControlInput1").prop('files'))
let images = $("#id_image").prop('files')

$(".new_img").each(function(){
$(this).remove();
})
for (var i = 0; i < images.length; i++){
console.log(images[i].name)
let new_img = $('<img src='+URL.createObjectURL(images[i])+' class="new_img" alt='+images[i].name+'dd width=200px  height=200px />');
new_img.css('margin','5px')
$(parent_div).append(new_img)
}
})
// collecting default images
let selected_pages = new Array()
$('.collect-default-image-js').on("click",function(){
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
$('#default_images').prop("value",selected_pages)
console.log("selected pages are: ",selected_pages)
});
// collecting deleted images
let deleted_pages = new Array()
$('.collect-deleted-images-js').on("click",function(){
if($(this).is(':checked')){
if(!deleted_pages.includes($(this).prop("value"))){
deleted_pages.push($(this).prop("value"))
}

}
else{
console.log("it unchecked now")
if(deleted_pages.includes($(this).prop("value"))){
console.log("yeah it contains it")
removed_item = deleted_pages.indexOf($(this).prop("value"))
deleted_pages.splice(removed_item, 1);
}
}
$('#deleted_images').prop("value",deleted_pages)
console.log("selected pages are: ",deleted_pages)
});


})