
$("#clear").on("click",()=>{
$('form')[0].reset();
})

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
    endDate:new Date().getFullYear().toString(),
    startDate:'2000-01-01'
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
