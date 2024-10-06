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


Highcharts.chart('gauge', {

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
            icon: 'static/images/Antonia_water.png',
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
            icon: 'static/images/Antonia_water.png',    
            iconColor: '#ffffff'
        }
    }]
});

