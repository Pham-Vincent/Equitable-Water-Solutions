// Define an array of layers, where each layer is an object
// with the number of nodes and the activation function
const layers = [{
    nodes: 2,
    activation: 'tanh',
    label: 'Input Layer'
},  {
    nodes: 5,
    activation: 'ReLU',
    label: 'Weighted Layer'
}, {
    nodes: 4,
    activation: 'sigmoid',
    label: 'Output Layer'
}];

// Generates series for a neural network based on the defined layers.
function generateData() {
    // If there are no layers defined, we have no neural network to visualize
    if (layers.length === 0) {
        return [];
    }

    const data = [];

    // Recursive function to generate all possible connections of nodes
    // for each layer in then network
    function generate(currentIndices) {
        // Base case: If the current indices length matches the number of
        // layers, store the combination in the data array.
        if (currentIndices.length === layers.length) {
            data.push({
                data: [...currentIndices]
            });
            return;
        }

        // Get the current dimension index based on the length of
        // current indices.
        const dimensionIndex = currentIndices.length;

        // Iterate through all nodes in the current layer (dimensionIndex).
        for (let i = 0; i < layers[dimensionIndex].nodes; i++) {
            // Recursively call generate with the new node index added to
            // the current indices.
            generate([...currentIndices, i]);
        }
    }

    generate([]);
    return data;
}

function renderResponsiveChart() {
    const screenWidth = window.innerWidth;

    // Define width and height for different screen sizes
    let w, h;
    if (screenWidth > 1500) {
        w = 700;
        h = 550;
    } else {
        w = 500;
        h = 450;
    }

    Highcharts.chart('neural-model', {
        chart: {
            type: 'line',
            parallelCoordinates: true,
            inverted: false,
            width: w, // Set a smaller width lg-700, md-500
            height: h, // Reduces space around the chart lg-550, md-450
            spacing: [-10, -70, -10, -70],
        },
        title: false,
        accessibility: {
            typeDescription: 'Neural network chart',
            point: {
                descriptionFormat: 'node on {series.xAxis.options.custom.layers.(x).label}'
            }
        },
        tooltip: false,
        exporting:{
            enabled:false
        },
        plotOptions: {
            line: {
                lineWidth: 1,
                color: '#0A2B57',
                marker: {
                    symbol: 'circle',
                    enabled: true,
                    radius: 15,
                    fillColor: '#0A2B57',
                    lineWidth: 3,
                    lineColor: '#0A2B57',
                    states: {
                        hover: {
                            lineColor: '#0A2B57',
                        }
                    }
                },
                states: {
                    inactive: {
                        enabled: false
                    },
                    hover: {
                        lineColor: '#0A2B57',
                        lineWidthPlus: 0
                    }
                }
            }
        },
        xAxis: {
            visible: false, // Hide the xAxis completely
            labels: {
                enabled: false // Disable all labels on the xAxis
            },
            lineWidth: 0, // Remove axis line
            tickWidth: 0 // Remove ticks
        },
        yAxis: Array.from({ length: layers.length }, (_, i) => ({
            type: 'category',
            visible: false, // Hide the yAxis completely
            labels: {
                enabled: false // Disable all labels on the yAxis
            },
            gridLineWidth: 0, // Remove gridlines
            tickWidth: 0, // Remove ticks
            accessibility: {
                description: `Axis for the nodes contained the layer ${layers[i].label}.`
            }
        })),
        series: generateData(),
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    xAxis: {
                        categories: layers.map(layer => layer.activation)
                    }
                }
            }]
        }
    });

}


// Initial render
renderResponsiveChart();
// Re-render on window resize
window.addEventListener('resize', renderResponsiveChart);

