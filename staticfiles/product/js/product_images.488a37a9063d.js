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

//imgInp.onchange = evt => {
//  const [file] = imgInp.files
//  if (file) {
//    blah.src = URL.createObjectURL(file)
//  }
//}


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
})