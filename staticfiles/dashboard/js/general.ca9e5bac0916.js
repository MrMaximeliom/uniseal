
$("#clear").on("click",()=>{
$('form')[0].reset();
})
let currentDate = new Date();
var date = new Date();
var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
// applying date picker to project forms
$( document ).ready(function() {
console.log("hi here in general")
console.log('page id is: ',$('#page-id-js').html())
if($('#page-id-js').text() == "Industry Updates"){

$("#id_date").datepicker({
  format: "yyyy-mm-dd",
    viewMode: "days",
    minViewMode: "days",
    autoclose:true,
    clearBtn:true,

    startDate:today
});

}
else if($('#page-id-js').text() == "Offer"){
$("#id_offer_start_date").datepicker({
  format: "yyyy-mm-dd",
    viewMode: "days",
    minViewMode: "days",
    autoclose:true,
    clearBtn:true,
    startDate:today
});
$("#id_offer_end_date").datepicker({
  format: "yyyy-mm-dd",
    viewMode: "days",
    minViewMode: "days",
    autoclose:true,
    clearBtn:true,
    startDate:today
});

}
else{
$("#id_date").datepicker({
  format: "yyyy-mm",
    viewMode: "months",
    minViewMode: "months",
    autoclose:true,
    clearBtn:true,
    endDate:new Date().getFullYear().toString(),
    startDate:'2000-01'
});
}



})
