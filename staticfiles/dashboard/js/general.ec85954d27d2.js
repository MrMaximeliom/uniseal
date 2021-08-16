//$("form").each((args,er)=>{
////    $(this).find(':input') //<-- Should return all input elements in that specific form.
//console.log(er)
//});
$("#clear").on("click",()=>{
$('form')[0].reset();
})
