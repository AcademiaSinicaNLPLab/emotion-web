var margin = {top: 30, right: 10, bottom: 50, left: 30},
    width = 840 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// var formatPercent = d3.format(".0%");

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1, 1);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    // .tickFormat(formatPercent);

var svg = d3.select("#chart-container").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// d3.tsv("/static/data.tsv", function(error, data) {

$.getJSON('/api/pat/i%20am%20pissed', function(data){
  // console.log(data);

  data.forEach(function(d) {
    d.val = +d.val;
  });

  x.domain(data.map(function(d) { return d.key; }));
  y.domain([0, d3.max(data, function(d) { return d.val; })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Frequency");

  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.key); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.val); })
      .attr("height", function(d) { return height - y(d.val); });

  d3.select("input").on("change", change);

  // var sortTimeout = setTimeout(function() {
  //   d3.select("input").property("checked", true).each(change);
  // }, 2000);

  function align() {
    $('.x').find('.tick').each(function(index, value){
      var transform = $(this).attr('transform');
      var ordinate = transform.split('(')[1].split(')')[0].split(',');

      ordinate = $.map(ordinate, function(n){ return parseInt(n); });

      var sink_offset = index%2*15;

      ordinate[1] = ordinate[1] + sink_offset;

      var ordinate_str = $.map(ordinate, function(n){ return n.toString(); }).join(',');

      // console.log(ordinate_str);

      $(this).find('text').attr('transform', 'translate(0,'+sink_offset.toString()+')');
      var y2 = $(this).find('line').attr('y2');
      $(this).find('line').attr('y2', parseInt(y2)+index%2*10);
    });    
  }

  align();

  function change() {
    // clearTimeout(sortTimeout);

    // Copy-on-write since tweens are evaluated after a delay.
    var x0 = x.domain(data.sort(this.checked
        ? function(a, b) { return b.val - a.val; }
        : function(a, b) { return d3.ascending(a.key, b.key); })
        .map(function(d) { return d.key; }))
        .copy();

    var transition = svg.transition().duration(200),
        delay = function(d, i) { return i * 0; };

    transition.selectAll(".bar")
        .delay(delay)
        .attr("x", function(d) { return x0(d.key); });

    transition.select(".x.axis")
        .call(xAxis)
      .selectAll("g")
        .delay(delay);

    align();
  } 
});