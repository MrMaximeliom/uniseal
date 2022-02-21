
$( document ).ready(function() {
error_messages = JSON.parse($('#my-data').html());
let currentDate = new Date();
var date = new Date();
var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
// for projects pages
$("#searchPhraseDate").datepicker({
  format: "yyyy",
    viewMode: "years",
    minViewMode: "years",
    autoclose:true,
    clearBtn:true,
    endDate:new Date().getFullYear().toString(),
    startDate:'2000',

});
// for products' pages
$("#searchPhraseDateProductsPageMonth").datepicker({
    format: "mm",
    viewMode: "months",
    minViewMode: "months",
    autoclose:true,
    clearBtn:true,
    startView:'months'
})
$("#searchPhraseDateProductsPageYear").datepicker({
    format: "yyyy",
    viewMode: "years",
    minViewMode: "years",
    autoclose:true,
    clearBtn:true,
    startDate:'2020',
    endDate:new Date().getFullYear().toString(),
    startView:'years'
});
$("#searchPhraseDateProductsPage").datepicker({
    format: "yyyy-mm-dd",
    autoclose:true,
    clearBtn:true,
    startDate:'2020-1-1',
    endDate:today
});
$('#searchBy').on('change',()=>{
selected_value = $('#searchBy').find(":selected").prop("value");
$('#searchPhraseDateProductsPage').val('')
$('#searchPhraseDateProductsPageYear').val('')
$('#searchPhraseDateProductsPageMonth').val('')
if(selected_value == 'month'){
console.log('now in month');
$('#searchPhraseDateProductsPage').attr('hidden',true);
$('#searchPhraseDateProductsPageYear').attr('hidden',true);
$('#searchPhraseDateProductsPageMonth').attr('hidden',false);


}
else if(selected_value == 'year'){
console.log('now in year');
$('#searchPhraseDateProductsPage').attr('hidden',true);
$('#searchPhraseDateProductsPageYear').attr('hidden',false);
$('#searchPhraseDateProductsPageMonth').attr('hidden',true);


}
else{
console.log('now in none');
console.log(selected_value);
$('#searchPhraseDateProductsPage').attr('hidden',false);
$('#searchPhraseDateProductsPageYear').attr('hidden',true);
$('#searchPhraseDateProductsPageMonth').attr('hidden',true);


}
});



// for offers pages
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
