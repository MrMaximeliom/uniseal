$( document ).ready(function() {
// event for adding new image block
$(".hover").mouseleave(
  function() {
    $(this).removeClass("hover");
  }
);
//////////////////////////////////

$( ".input-default-js" ).click(function() {
 console.log('setting image as default')
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