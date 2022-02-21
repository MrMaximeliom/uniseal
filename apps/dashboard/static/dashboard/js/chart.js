$( document ).ready(function() {
$(function () {
      var $populationChart = $("#population-chart");
      $.ajax({
        url: $populationChart.data("url"),
        success: function (data) {

          var ctx = $populationChart[0].getContext("2d");

          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: data.labels,
              datasets: [{
                label: 'Products Count',
                backgroundColor: 'skyblue',
                data: data.data
              }]
            },
            options: {
              responsive: true,
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: 'Products Count Per Categories'
              }
            }
          });

        }
      });

    });
$(function () {
      var $populationChart = $("#users-chart");
      $.ajax({
        url: $populationChart.data("url"),
        success: function (data) {

          var ctx = $populationChart[0].getContext("2d");

          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: data.labels,
              datasets: [{
                label: 'Users Count',
                backgroundColor: 'pink',
                data: data.data
              }]
            },
            options: {
              responsive: true,
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: 'Users Registration Count Per Month'
              }
            }
          });

        }
      });

    });
 });