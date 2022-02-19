
$( document ).ready(function() {
error_messages = JSON.parse($('#my-data').html());

// for projects pages
$("#searchPhraseDate").datepicker({
  format: "yyyy",
    viewMode: "years",
    minViewMode: "years",
    autoclose:true,
    clearBtn:true,
    endDate:new Date().getFullYear().toString(),
    startDate:'2000'
});
// for products' page
$("#searchPhraseDateProductsPage").datepicker({
    format: "yyyy-mm-dd",
    autoclose:true,
    clearBtn:true,
    startDate:'2020-1-1'
});

// for offers pages
let currentDate = new Date();
var date = new Date();
var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
$("#searchPhraseDateOffer").datepicker({
    format: "d-m-yyyy",
    autoclose:true,
    clearBtn:true,
    startDate:today
});

$('searchPhraseDate').on('input',function(){
$(this).prop('value',$(this).datepicker ('getDate'))
});
$('searchPhraseDateOffer').on('input',function(){
$(this).prop('value',$(this).datepicker ('getDate'))
});


})
