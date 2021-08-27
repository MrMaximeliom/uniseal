
$("#clear").on("click",()=>{
$('form')[0].reset();
})

// applying date picker to project forms
$( document ).ready(function() {
console.log("hi here in general")
$("#id_date").datepicker({
  format: "yyyy-mm",
    viewMode: "months",
    minViewMode: "months",
    autoclose:true,
    clearBtn:true,
    endDate:new Date().getFullYear().toString(),
    startDate:'2000-01'
});


})
