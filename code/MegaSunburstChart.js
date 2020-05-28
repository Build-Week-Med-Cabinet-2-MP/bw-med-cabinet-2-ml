//https://shop.greenhouseseeds.nl/flavor-wheel/

url = 'https://raw.githubusercontent.com/alex-pakalniskis/visualizations/master/assets/csv/sunburst_data_trimmed.csv'

Plotly.d3.csv(url, function(err, rows){
  function unpack(rows, key) {
  return rows.map(function(row) {return row[key]})
}

  var data = [{
        type: "sunburst",
        maxdepth: 4,
        ids: unpack(rows, 'ids'),
        labels: unpack(rows, 'ids'),
        parents: unpack(rows, 'parent'),
        marker: {
          //"colors": unpack(rows, "color")
        },
        textposition: 'inside',
        insidetextorientation: 'radial'
  }]

  var layout = {margin: {l: 0, r: 0, b: 0, t:0}}

  Plotly.newPlot('myDiv', data, layout)
})