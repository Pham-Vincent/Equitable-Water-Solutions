var slider = document.getElementById("myRange");
var selectedWeather = "Sunny";  // Default weather condition
var currentTime = "12:00";

var timeAdjustment = {
  '0-4' : 0.8,
  '4-8' : 0.9,
  '8-12' : 1.1,
  '12-16' : 1,
  '16-20' : .9,
  '20-24' : .8
};

// Function to render icons
function renderIcons() {
    this.series.forEach(series => {
        if (!series.icon) {
            series.icon = this.renderer
                .image(
                    series.options.custom.icon, // Custom PNG for each series
                    0, 0,                       // Initial position
                    23, 23                      // Icon size
                )
                .attr({
                    zIndex: 10
                })
                .add(this.series[3].group);     // Add to the 4th group (adjust for 4th track)
        }

        series.icon.attr({
            x: this.chartWidth / 2 - 15,        // Horizontal adjustment
            y: this.plotHeight / 2 -            // Vertical adjustment
                series.points[0].shapeArgs.innerR - 
                (series.points[0].shapeArgs.r -
                    series.points[0].shapeArgs.innerR) / 2 + 8 - 20
        });
    });
}

// Initialize the chart and store it in a variable
var chart = Highcharts.chart('gauge', {
    chart: {
        type: 'solidgauge',
        height: '110%',
        events: {
            render: renderIcons
        }
    },

    title: {
        text: 'Water Plant Release',
        style: {
            fontSize: '24px',
            color: '#0A2B57'
        }
    },

    tooltip: {
        borderWidth: 0,
        backgroundColor: 'none',
        shadow: false,
        style: {
            fontSize: '16px'
        },
        valueSuffix: '(ppg)',
        pointFormat: '{series.name}<br>' +
            '<span style="font-size: 1.5em; color: {point.color}; ' +
            'font-weight: bold">{point.y}</span>',
        positioner: function (labelWidth) {
            return {
                x: (this.chart.chartWidth - labelWidth) / 2,
                y: (this.chart.plotHeight / 2) + 15
            };
        }
    },

    pane: {
        startAngle: 0,
        endAngle: 360,
        background: [{ // Track for Conversion
            outerRadius: '112%',
            innerRadius: '91%',
            backgroundColor: '#587db8',
            borderWidth: 0
        }, { // Track for Engagement
            outerRadius: '90%',
            innerRadius: '70%',
            backgroundColor: '#75a7c7',
            borderWidth: 0
        }, { // Track for Feedback
            outerRadius: '69%',
            innerRadius: '49%',
            backgroundColor: '#8fd3db',
            borderWidth: 0
        }, { // New Track for the fourth series
            outerRadius: '48%',
            innerRadius: '30%',
            backgroundColor: '#a0f2f0', 
            borderWidth: 0
        }]
    },

    yAxis: {
        min: 0,
        max: 100,
        lineWidth: 0,
        tickPositions: []
    },

    plotOptions: {
        solidgauge: {
            dataLabels: {
                enabled: false
            },
            linecap: 'round',
            stickyTracking: false,
            rounded: true
        }
    },

    series: [{
        name: 'Baltimore',
        data: [{
            color: '#173058',
            radius: '112%',
            innerRadius: '91%',
            y: 80
        }],
        custom: {
            icon: 'static/images/Antonia_water.png',
            iconColor: '#ffffff'
        }
    }, {
        name: 'Chester',
        data: [{
            color: '#265471',
            radius: '90%',
            innerRadius: '70%',
            y: 65
        }],
        custom: {
            icon: 'static/images/Antonia_water.png',
            iconColor: '#ffffff'
        }
    }, {
        name: 'Power Plant',
        data: [{
            color: '#3d8c96',
            radius: '69%',
            innerRadius: '49%',
            y: 50
        }],
        custom: {
            icon: 'static/images/Antonia_power.png',
            iconColor: '#ffffff'
        }
    }, {
        name: 'Downstream',   
        data: [{
            color: '#51bcb9',  
            radius: '48%',
            innerRadius: '30%',
            y: 30           
        }],
        custom: {
            icon: 'static/images/Antonia_downstream.png',    
            iconColor: '#ffffff'
        }
    }]
});

// Listen for changes in weather input
document.querySelectorAll('input[name="weather"]').forEach((input) => {
    input.addEventListener('change', function() {
        selectedWeather = this.value;  // Update selected weather
        updateGaugeValues();            // Recalculate the values based on weather and slider
    });
});

//Listen for changes to time input
document.getElementById("time").addEventListener("input", function() {
    currentTime = this.value;  // Update the currentTime variable
    updateGaugeValues();       // Recalculate the values based on weather, slider, and time
});

// Slider event listener to dynamically change y-values
function updateGaugeValues() {
    var sliderValue = parseInt(slider.value);
    
    // Adjustments based on weather
    var adjustments = {
        'Sunny': { 'Baltimore': 1, 'Chester': 1, 'Power Plant': 1, 'Downstream': 1 },
        'Rain': { 'Baltimore': 1.3, 'Chester': 1.1, 'Power Plant': 0.75, 'Downstream': 1 },
        'Windy': { 'Baltimore': 0.9, 'Chester': 1.2, 'Power Plant': 1.1, 'Downstream': 0.85 },
        'Snow': { 'Baltimore': 0.8, 'Chester': 0.9, 'Power Plant': 0.9, 'Downstream': 1.2 }
    };
    
    var timeAdjustment = getTimeAdjustment(currentTime);

    var adjustment = adjustments[selectedWeather];

    // Update y value based on weather and slider input
    chart.series[0].setData([{ y: sliderValue * adjustment.Baltimore * timeAdjustment, color: '#173058', radius: '112%', innerRadius: '91%' }], true);
    chart.series[1].setData([{ y: (sliderValue - 10) * adjustment.Chester * timeAdjustment, color: '#265471', radius: '90%', innerRadius: '70%' }], true);
    chart.series[2].setData([{ y: (sliderValue - 20) * adjustment['Power Plant'] * timeAdjustment, color: '#3d8c96', radius: '69%', innerRadius: '49%' }], true);
    chart.series[3].setData([{ y: (sliderValue - 30) * adjustment.Downstream * timeAdjustment, color: '#51bcb9', radius: '48%', innerRadius: '30%' }], true);
}

// Slider event listener to update the chart when the slider changes
slider.oninput = updateGaugeValues;

function getTimeAdjustment(time){
    var hours = parseInt(time.split(":")[0])

    if(hours <= 4)
        return timeAdjustment['0-4']
    else if(hours <= 8)
        return timeAdjustment['4-8']
    else if(hours <= 12)
        return timeAdjustment['8-12']
    else if(hours <= 16)
        return timeAdjustment['12-16']
    else if(hours <= 20)
        return timeAdjustment['16-20']
    else 
        return timeAdjustment['20-24']
}
