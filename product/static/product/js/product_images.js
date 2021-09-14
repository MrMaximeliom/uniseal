$( document ).ready(function() {
let deleted_pages = new Array()
let default_image = new Array()
// keeping an eye about default image changing or not
let is_default_image_changed = false
// update button
let update_button = $("#updating_images")
update_button.prop("disabled",true)
$('.input-default-js').each(function(){
let current_index = $( ".input-default-js" ).index($(this))
 if($('.input-delete-js').index($(this)) == current_index ){
 console.log("setting delete as not valid")
    $(this).prop("checked",false);
  $(this).prop( "disabled", true );
  }
if($(this).is(':checked')){
if(!default_image.includes($(this).prop("value"))){
default_image.push($(this).prop("value"))
}

}


})
$('#default_images').prop("value",default_image)
console.log("default image are: ",default_image)
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
$(".input-delete-js" ).click( function() {
let current_index = $( ".input-delete-js" ).index($(this));
$('.input-default-js').each(function(){

  if($('.input-default-js').index($(this)) == current_index ){
    $(this).prop("checked",false);
//  $(this).prop( "disabled", true );

  }
//  else{
//   $(this).prop( "disabled", false );
//  }
})
update_button.prop("disabled",false)
})
$( ".input-default-js" ).click(function() {
is_default_image_changed = true

let current_image = $(this).prop("value")

let current_index = $( ".input-default-js" ).index($(this));
$('.input-default-js').not(this).each(function(){
  $(this).prop("checked",false);
})
$('.input-delete-js').each(function(){

  if($('.input-delete-js').index($(this)) == current_index ){
    $(this).prop("checked",false);
  $(this).prop( "disabled", true );
if(deleted_pages.includes(current_image)){
removed_item = deleted_pages.indexOf($(this).prop("value"))
deleted_pages.splice(removed_item, 1);
}

  }
  else{
   $(this).prop( "disabled", false );
  }
  update_button.prop("disabled",false)
})
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
// collecting default image

$('.collect-default-image-js').on("click",function(){
if($(this).is(':checked')){
default_image = new Array()
default_image.push($(this).prop("value"))
}

$('#default_images').prop("value",default_image)
console.log("default image are: ",default_image)
});
// collecting deleted images

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
console.log("deleted images are: ",deleted_pages)
});

// event when update button is clicked
$('#updating_images').on('click',function(){
let images = deleted_pages;
if(images.length > 1){
console.log("adding images to modal now")
let parent_div = $('#confirm-delete-images');
$('#delete_images').css('display','block')
$('#delete_image').css('display','none')
//console.log($("#exampleFormControlInput1").prop('files'))
console.log("length of deleted images ",images.length)

$(".delete_img").each(function(){
$(this).remove();
})
for (var i = 0; i < images.length; i++){
console.log(images[i].name)
let new_img = $('<img src='+images[i]+' class="delete_img" alt='+images[i].name+'dd width=200px  height=200px />');
new_img.css('margin','5px')
$(parent_div).append(new_img)
}
}
else if (images.length == 1){
console.log("adding images to modal now")
let parent_div = $('#confirm-delete-image');
$('#delete_image').css('display','block')
$('#delete_images').css('display','none')
//console.log($("#exampleFormControlInput1").prop('files'))
console.log("length of deleted images ",images.length)

$(".delete_img").each(function(){
$(this).remove();
})
for (var i = 0; i < images.length; i++){
console.log(images[i].name)
let new_img = $('<img src='+images[i]+' class="delete_img" alt='+images[i].name+'dd width=200px  height=200px />');
new_img.css('margin','5px')
$(parent_div).append(new_img)
}
}
if(is_default_image_changed){
console.log("adding images to modal now")
let parent_div = $('#confirm-default-image');
let default_selected_image = default_image
$('#default_image').css('display','block')
//console.log($("#exampleFormControlInput1").prop('files'))
console.log("length of deleted images ",images.length)

$(".default_img").each(function(){
$(this).remove();
})
for (var i = 0; i < default_selected_image.length; i++){
console.log(default_selected_image[i].name)
let new_img = $('<img src='+default_selected_image[i]+' class="default_img" alt='+default_selected_image[i].name+'dd width=200px  height=200px />');
new_img.css('margin','5px')
$(parent_div).append(new_img)
}
$('#posted_default_image').prop("value",default_image)

}
$('#posted_deleted_images').prop("value",deleted_pages)





})




})