import {drawChart} from './handle_charts.js';
$( document ).ready(function() {
let data = JSON.parse($('#my-data').html())
console.log(data.num_users)
let myLables = data.products_names;
let myData = data.num_users;
let labelString = '# of Users';
drawChart(myLables,myData,labelString,'tabularView');
$('#selectView').on('change',function(){
if($(this).val() === "charts"){
$("#defaultView").attr("hidden",false);
$("#tabularView").attr("hidden",true);


}
else{
$("#defaultView").attr("hidden",true);
$("#tabularView").attr("hidden",false);

}
});

});