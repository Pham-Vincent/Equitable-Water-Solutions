


//Function to update values when Short Term is Clicked 
function shortTermChanges(saltdata,xtitleName,barchartData1,barchartData2,barchartData3,Timespan,BarChartTimeSpan){
    saltdata = [
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
     xtitleName = '<b>Time(days)<b>',
     barchartData1=
     [
     ['Cl', 62.5],
     ['Na', 37.5],
     ['Ca', 50],
     ['K', 50],
     ['Br', 75],
     ['Mg', 25],
     ['SO', 25]
    ],
    barchartData2=[
        ['Cl', 65],
    ['Na', 30],
    ['Ca', 50],
    ['K', 40],
    ['Br', 70],
    ['Mg', 20],
    ['SO', 25]

    ],
    barchartData3=[
        ['Cl', 55],
        ['Na', 25],
        ['Ca', 40],
        ['K', 35],
        ['Br', 60],
        ['Mg', 15],
        ['SO', 20]
    ],
    Timespan = document.getElementById("myRange").value;
    BarChartTimeSpan = document.getElementById("myRange2").value;
    return [saltdata,xtitleName,barchartData1,barchartData2,barchartData3,Timespan,BarChartTimeSpan]
     

    
}

//Function to update values when LongTerm is Clicked 

function longTermChanges(saltdata,xtitleName,barchartData1,barchartData2,barchartData3,Timespan,BarChartTimeSpan){
    saltdata = [
        {x: 0, y: 80},
        {x: 5, y: 200},
        {x: 10, y: 200},
        {x: 20, y: 380},
        {x: 25, y: 250},
        {x: 30, y: 250},
        {x: 40, y: 300},
        {x: 50, y: 350},
        {x: 60, y: 330}
    ],
    xtitleName = '<b>Time(years)<b>',
    barchartData1 =
    [
        ['Cl', 90],
        ['Na', 65],
        ['Ca', 80],
        ['K', 75],
        ['Br', 95],
        ['Mg', 40],
        ['SO', 55]
    ],
    barchartData2=
    [
    ['Cl', 70],
    ['Na', 50],
    ['Ca', 60],
    ['K', 55],
    ['Br', 85],
    ['Mg', 35],
    ['SO', 45],
    ]
    barchartData3=
    [
    ['Cl', 80],
    ['Na', 40],
    ['Ca', 70],
    ['K', 60],
    ['Br', 90],
    ['Mg', 30],
    ['SO', 50]],
    Timespan = document.getElementById("myRange").value;
    BarChartTimeSpan=document.getElementById("myRange2").value;
    return [saltdata,xtitleName,barchartData1,barchartData2,barchartData3,Timespan,BarChartTimeSpan]


    
}


// Function to initiate graph creation and call functions to update the graph
function updateGraphs(currentChecked,saltdata,xtitleName,barchartData1,barchartData2,barchartData3,Timespan,BarChartTimeSpan){
    let radios = document.querySelectorAll('input[type="radio"][name="projection"]');
    radios.forEach(function(radio){
        //Checks if Long Term or Short Term is currently selected
        if(radio.checked){
            //Keeps track if Long term or Short Term is selected
            currentChecked=radio.value
        }
    })

    if(currentChecked == 'shortTerm')
    {
         [saltdata,xtitleName,barchartData1,barchartData2,barchartData3,Timespan,BarChartTimeSpan] = shortTermChanges();
    }
    else{
        [saltdata,xtitleName,barchartData1,barchartData2,barchartData3,Timespan,BarChartTimeSpan]= longTermChanges();
    }






    //                            Linechart 1 Code 
//<------------------------------------------------------------------------------------>
    Highcharts.chart('dashboard-saltchart', {
        chart: {
            type: 'line'
        },
  
        title: {
            text: '<b>Salinity levels over the next 60 days</b>'
        },
        xAxis: {
            title: {
                text: xtitleName
            },
            // Set type to linear for numeric x-axis
            type: 'linear',
            // Remove categories to use actual numerical values on x-axis
            min: 0,
            max:parseInt(Timespan, 10),
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
            data: saltdata,
          
            color: 'white',
        }],
        legend: {
          enabled: false // Disable the legend
      }
    });




    //                            Saltdial 1 Code 
//<------------------------------------------------------------------------------------>
    Highcharts.chart('dashboard-saltdial', {

    chart: {
        type: 'gauge',
        plotBackgroundColor: null,
        plotBackgroundImage: null,
        plotBorderWidth: 0,
        plotShadow: false,
        height: '70%'
    },

    title: {
        text:""
    },

    pane: {
        startAngle: -150,
        endAngle: 149.9,
        background: null,
        center: ['50%', '50%'],
        size: '100%'
    },

    // the value axis
    yAxis: {
        min: 0,
        max: 390,  // Adjust according to how many labels (words) you need
        tickLength: 0,
        minorTickInterval: null,

        labels: {
            distance: -20,
            style: {
                fontSize: '12px',
                color:'white',
                fontFamily:'Roboto',
                fontWeight:'bold',
            },
            formatter: function () {
                // Map the numerical values to specific words
                const words = {
                    50:'<span class="low">Low</span>',
                    150: '<span class="medium">Medium</span>',
                    250: '<span class="mid-high">Mid-High</span>',
                    350: '<span class="high">High</span>',
                };
                return words[this.value] || '';
            },
            useHTML: true
            
        },
        lineWidth: 0,
        plotBands: [
            createPlotBand(0, 90, '#50bcb9'),
            createPlotBand(100, 190, '#3d8c96'),
            createPlotBand(200, 290, '#265471'),
            createPlotBand(300, 390, '#173058','High')
        ]
    },
    
    series: [{
        name: 'Salinity',
        data: [200],
        tooltip: {
            valueSuffix: ' ppm'
        },
        dataLabels: {
            format: '{y} ppm',
            borderWidth: 0,
            color: (
                Highcharts.defaultOptions.title &&
                Highcharts.defaultOptions.title.style &&
                Highcharts.defaultOptions.title.style.color
            ) || '#333333',
            style: {
                fontSize: '16px'
            }
        },
        dial: {
            radius: '80%',
            backgroundColor: '#797EF6',
            baseWidth: 12,
            baseLength: '0%',
            rearLength: '0%'
        },
        pivot: {
            backgroundColor: 'white',
            radius: 10,
            borderColor: '#333333',
            borderWidth: .5,
            shadow: {
                color: 'rgba(0, 0, 0, 0.5)', // Shadow color
                offsetX: 2,                 // Horizontal shadow offset
                offsetY: 2,                 // Vertical shadow offset
                opacity: 0.5,               // Shadow opacity
                width: 5                    // Shadow spread
            }
            
        }

    }]
    

});

// Add some life
setInterval(() => {
    const chart = Highcharts.charts[0];
    if (chart && !chart.renderer.forExport) {
        const point = chart.series[0].points[0],
            inc = Math.round((Math.random() - 0.5) * 20);

        let newVal = point.y + inc;
        if (newVal < 0 || newVal > 200) {
            newVal = point.y - inc;
        }

        point.update(newVal);
    }

}, 3000);



function createPlotBand(from, to, color) {
    return {
        from: from,
        to: to,
        color: color,
        thickness: 100,
        outerRadius: '100%',  // Full outer radius
        innerRadius: '50%',
        borderRadius: '20%',
        label: {
            zIndex: 1,
            verticalAlign: 'middle',
            style: {
                color: 'black',
                textAlign: 'center',
                rotation:180
            }
            
        },
        
    };
}


//                            Barchart 1 Code 
//<------------------------------------------------------------------------------------>
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
            lineWidth: 2,
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
            max: parseInt(BarChartTimeSpan,10), // Set the maximum value for the Y-axis
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
            data: barchartData1,
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


//                            Barchart 2 Code 
//<------------------------------------------------------------------------------------>

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
            lineWidth: 2,
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
            max: parseInt(BarChartTimeSpan,10), // Set the maximum value for the Y-axis
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
            data: barchartData2,
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



//                            Barchart 3 Code 
//<------------------------------------------------------------------------------------>
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
            lineWidth: 2,
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
            max: parseInt(BarChartTimeSpan,10),  
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
            data: barchartData3,
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
}


// Function to toggle visibility of content for long term and short radio buttons
document.addEventListener('DOMContentLoaded', function() {
    const shortTermRadio = document.getElementById('shortTerm');
    const longTermRadio = document.getElementById('longTerm');
    const vertical_bar = document.getElementById('long-term-vert-bar');
    const climate_buttons = document.querySelector('.long-term-radio-buttons')
  
    // Function to toggle content visibility based on the selected radio button
    function toggleContent() {
      if (longTermRadio.checked) {
        vertical_bar.style.display = 'block';
        climate_buttons.style.display = 'block'; 
      } else if (shortTermRadio.checked) {
        vertical_bar.style.display = 'none'; 
        climate_buttons.style.display = 'none';
      }
    }
  
    // Attach the function to the change event for both radio buttons
    shortTermRadio.addEventListener('change', toggleContent);
    longTermRadio.addEventListener('change', toggleContent);
  
    // Call the function initially to set the correct visibility
    toggleContent();
  });





$(function() {


    updateGraphs()
    $('input[type="radio"][name="projection"]').change(function(){ 
        updateGraphs()
    })
    $('input[type="range"][id="myRange"]').change(function(){
        updateGraphs()
    })
    $('input[type="range"][id="myRange2"]').change(function(){
        updateGraphs()
    })
    
    
});


document.addEventListener('DOMContentLoaded', () => {
    const headings = document.querySelectorAll('.bottom h5');

fetch('/session-data')
  .then(response => response.json())
  .then(data => {
    if(data.id == null){
    headings[0].textContent = 'Add Location 1';
    headings[1].textContent = 'Add Location 2';
    headings[2].textContent = 'Add Location 3';
    }
    var userid = data.id
    fetch('/locations-pinned',{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({userid: userid}),
    })
    .then(response1 => response1.json())
    .then(data => {
        if(data[0][0] != null){
        headings[0].textContent = data[0][0];
        }
        if(data[0][1] != null){
            headings[1].textContent = data[0][1];
            }
        if(data[0][2] != null){
            headings[2].textContent = data[0][2];
            }
        })

})

   
});
