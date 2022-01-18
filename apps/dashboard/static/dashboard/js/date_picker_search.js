
$( document ).ready(function() {
error_messages = JSON.parse($('#my-data').html())
console.log(new Date().getFullYear())
$("#searchPhraseDate").datepicker({
  format: "yyyy",
    viewMode: "years",
    minViewMode: "years",
    autoclose:true,
    clearBtn:true,
    endDate:new Date().getFullYear().toString(),
    startDate:'2000'
});


})
$('searchPhraseDate').on('input',function(){
$(this).prop('value',$(this).datepicker ('getDate'))
})