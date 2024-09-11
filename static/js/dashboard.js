document.addEventListener('DOMContentLoaded', function () {
  Highcharts.chart('dashboard-saltchart', {
      chart: {
          type: 'line'
      },

      title: {
          text: '<b>Salinity levels over the next 60 days</b>'
      },
      xAxis: {
          title: {
              text: '<b>Time(days)</b>'
          },
          // Set type to linear for numeric x-axis
          type: 'linear',
          // Remove categories to use actual numerical values on x-axis
          min: 0,
          max:60,
          gridLineWidth: .5,
          tickInterval: 5,
      },
      yAxis: {
          title: {
              text: '<b>Salinity Levels (ppm)</b>'
          },
          plotBands: [
              {
                  from: 0,
                  to: 100,
                  color: '#51bcb9'
              }, 
              {
                  from: 100,
                  to: 200,
                  color: '#3d8c96'
              },
              {
                  from: 200,
                  to: 300,
                  color: '#265471'
              }, 
              {
                  from: 300,
                  to: 400,
                  color: '#173058'
              }
          ],
          gridLineWidth: .5,
          min: 0
      },

      series: [{
          name: 'Tokyo',
          marker: {
              enabled: false
          },
          
          // Use object format for full control over x and y values
          data: [
              {x: 0, y: 40},
              {x: 5, y: 29.9},
              {x: 10, y: 71.5},
              {x: 15, y: 106.4},
              {x: 20, y: 129.2},
              {x: 25, y: 144.0},
              {x: 30, y: 176.0},
              {x: 35, y: 380},
              {x: 40, y: 148.5},
              {x: 45, y: 216.4},
              {x: 50, y: 194.1},
              {x: 55, y: 95.6},
              {x: 60, y: 54.4}
          ],
        
          color: 'white',
      }],
      legend: {
        enabled: false // Disable the legend
    }
  });
});
