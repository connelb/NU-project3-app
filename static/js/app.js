
function buildMetadata(sample) {
  var url = "/metadata/" + sample;
  var selector = d3.select('#sample-metadata');
  selector.html('');
  d3.json(url).then((response) => {
    Object.entries(response).forEach(([key, value]) => {
      selector
        .append('div')
        .html(`${key}: ${value}</br>`)
    });
  });

  // BONUS: Build the Gauge Chart
  // buildGauge(data.WFREQ);
}

function buildCharts(sample) {

  // @TODO: Use `d3.json` to fetch the sample data for the plots

  var results = [];
  var labels = [];
  var values = [];
  var hovertext = [];
  var bubbleChart = d3.select('#bubble');

  var url = "/samples/" + sample;

  // otu_ids x
  // otu_labels
  // sample_values y?

  d3.json(url).then((response) => {
    Object.entries(response).forEach(([key, value]) => {
      console.log(key)
      results.push(value);
    })

    labels = results[0].slice(0, 10);
    values = results[1].slice(0, 10);
    hovertext = results[2].slice(0, 10);

    // @TODO: Build a Bubble Chart using the sample data
    var trace_bubble = {
      x: labels,
      y: hovertext,
      mode: "markers",
      type: "scatter",
      name: "discus throw",
      text: values.map(datum => datum),
      marker: {
        color: "orange",
        //symbol: "diamond-x",
        size: 22,
        opacity: 0.5
      }
    };

    var data_bubble = [trace_bubble];

    var layout = {
      title: "Bubble Title here",

    };

    Plotly.newPlot("bubble", data_bubble, layout);


    // @TODO: Build a Pie Chart
    var trace_pie = {
      labels: values,
      values: labels,
      type: 'pie'
    };

    var data_pie = [trace_pie];

    var layout = {
      title: "Pie Title here",
      height: 800,
      width: 700,
      domain: {
        x: [0, .48],
        y: [0, .49]
      },
    };

    Plotly.newPlot("pie", data_pie, layout);
  })
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();

