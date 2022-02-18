import {drawChart} from './handle_charts.js';
$( document ).ready(function() {
let data = JSON.parse($('#my-data').html())
console.log(data.num_users)
let myLables = data.products_names;
let myData = data.num_users;
let labelString = '# of Users';
drawChart(myLables,myData,labelString,'chartsView');
$('#selectView').on('change',function(){
if($(this).val() === "charts"){
$("#defaultView").attr("hidden",true);
$("#chartsView").attr("hidden",false);


}
else{
$("#defaultView").attr("hidden",false);
$("#chartsView").attr("hidden",true);

}
});

});