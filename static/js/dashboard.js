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
          name: 'Salinity',
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


document.addEventListener('DOMContentLoaded', function () {
    Highcharts.chart('dashboard-barchart-1', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Number of days below the LO Threshold in the next 60 days.',
            style: {
                fontSize: '16px',
                fontFamily: 'Roboto'
            }
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            type: 'category',
            labels: {
                autoRotation: [-45, -90],
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        },
        yAxis: {
            min: 0,
            max: 100, // Set the maximum value for the Y-axis
            lineWidth: 1.5,
            tickInterval: 25, 
            minorTickInterval: 25, 
            minorTickLength: 15, 
            minorTickWidth: 1.5,
            tickColor: '#000000',
            minorTickColor: ' #000000',
            title: {
                text: 'Number of Days',
                style: {
                    fontSize: '12px',
                    fontFamily: 'Roboto',
                    fontWeight: 'bold',
                }
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            pointFormat: 'Number of Days: <b>{point.y:.1f}</b>'
        },
        series: [{
            name: 'Population',
            colors: [
                '#7CB935'
            ],
            colorByPoint: true,
            groupPadding: 0,
            data: [
                ['Cl', 62.5],
                ['Na', 37.5],
                ['Ca', 50],
                ['K', 50],
                ['Br', 75],
                ['Mg', 25],
                ['SO', 25]
            ],
            dataLabels: {
                enabled: false,
                rotation: -90,
                color: '#FFFFFF',
                inside: true,
                verticalAlign: 'top',
                format: '{point.y:.1f}', // one decimal
                y: 10, // 10 pixels down from the top
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        }]
    });
});


document.addEventListener('DOMContentLoaded', function () {
    Highcharts.chart('dashboard-barchart-2', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Number of days above the HI Threshold in the next 60 days.',
            style: {
                fontSize: '16px',
                fontFamily: 'Roboto'
            }
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            type: 'category',
            labels: {
                autoRotation: [-45, -90],
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        },
        yAxis: {
            min: 0,
            max: 100, // Set the maximum value for the Y-axis
            lineWidth: 1.5,
            tickInterval: 25, 
            minorTickInterval: 25, 
            minorTickLength: 15, 
            minorTickWidth: 1.5, 
            tickColor: '#000000',
            minorTickColor: ' #000000',
            title: {
                text: 'Number of Days',
                style: {
                    fontSize: '12px',
                    fontFamily: 'Roboto',
                    fontWeight: 'bold',
                }
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            pointFormat: 'PNumber of Days: <b>{point.y:.1f}</b>'
        },
        series: [{
            name: 'Population',
            colors: [
                '#797EF6'
            ],
            colorByPoint: true,
            groupPadding: 0,
            data: [
                ['Cl', 62.5],
                ['Na', 37.5],
                ['Ca', 50],
                ['K', 50],
                ['Br', 75],
                ['Mg', 25],
                ['SO', 25]
            ],
            dataLabels: {
                enabled: false,
                rotation: -90,
                color: '#FFFFFF',
                inside: true,
                verticalAlign: 'top',
                format: '{point.y:.1f}', // one decimal
                y: 10, // 10 pixels down from the top
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        }]
    });
});


document.addEventListener('DOMContentLoaded', function () {
    Highcharts.chart('dashboard-barchart-3', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Number of days between the LO & HI Thresholds in the next 60 days.',
            style: {
                fontSize: '16px',
                fontFamily: 'Roboto'
            }
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            type: 'category',
            labels: {
                autoRotation: [-45, -90],
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        },
        yAxis: {
            min: 0,
            max: 100,  
            lineWidth: 1.5,
            tickInterval: 25, 
            minorTickInterval: 25, 
            minorTickLength: 15, 
            minorTickWidth: 1.5, 
            tickColor: '#000000',
            minorTickColor: ' #000000',
            title: {
                text: 'Number of Days',
                style: {
                    fontSize: '12px',
                    fontFamily: 'Roboto',
                    fontWeight: 'bold',
                }
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            pointFormat: 'Number of Days: <b>{point.y:.1f}</b>'
        },
        series: [{
            name: 'Population',
            colors: [
                '#0A2B57'
            ],
            colorByPoint: true,
            groupPadding: 0,
            data: [
                ['Cl', 62.5],
                ['Na', 37.5],
                ['Ca', 50],
                ['K', 50],
                ['Br', 75],
                ['Mg', 25],
                ['SO', 25],
            ],
            dataLabels: {
                enabled: false,
                rotation: -90,
                color: '#FFFFFF',
                inside: true,
                verticalAlign: 'top',
                format: '{point.y:.1f}', // one decimal
                y: 10, // 10 pixels down from the top
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        }]
    });
});