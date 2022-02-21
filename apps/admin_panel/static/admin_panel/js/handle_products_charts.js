import {drawChart} from './handle_charts.js';
document.addEventListener("DOMContentLoaded",()=>{
let myStorage = window.localStorage;
if ( myStorage.getItem("view") === null) {
// set view variable to tabular by default
      myStorage.setItem('view', 'tabular');
}
else {
if (myStorage.getItem("view") === 'charts'){
// hide the default tabular view
$("#defaultView").attr("hidden",true);
// show the charts view
$("#chartsView").attr("hidden",false);
$('#selectView').val('charts');
}
else{
// show the default tabular view
$("#defaultView").attr("hidden",false);
// hide the charts view
$("#chartsView").attr("hidden",true);
$('#selectView').val('default');
}

}
});
$( document ).ready(function() {
let data = JSON.parse($('#my-data').html())

let myLables = data.names;
let myData = data.num_users;
let labelString = '# of Users';
// define storage variable

drawChart(myLables,myData,labelString,'chartsView');
// check if their is a defined variable for view



$('#selectView').on('change',function(){
if($(this).val() === "charts"){
// hide the default tabular view
$("#defaultView").attr("hidden",true);
// show the charts view
$("#chartsView").attr("hidden",false);
// set view variable to charts
myStorage.setItem('view', 'charts');
$('#selectView').val('charts');



}
else{
// show the default tabular view
$("#defaultView").attr("hidden",false);
// hide the charts view
$("#chartsView").attr("hidden",true);
// set view variable to tabular
myStorage.setItem('view', 'tabular');
$('#selectView').val('default');
}
});

});