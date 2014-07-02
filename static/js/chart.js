var w = 1200;
var h = 500;
var width;
var height;
var margin = {top: 30, right: 10, bottom: 50, left: 40};
var x;
var y;
var xAxis;
var yAxis;
var svg;

var number = 0;
var one_bar = 10;

function calculate_w_h(w, h)
{


  // width = w + extra - margin.left - margin.right;
  width = w - margin.left - margin.right;
  height = h - margin.top - margin.bottom;

  x = d3.scale.ordinal()
      .rangeRoundBands([0, width], .1, 1);

  y = d3.scale.linear()
      .range([height, 0]);

  xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  yAxis = d3.svg.axis()
      .scale(y)
      .orient("left");  
}

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

function draw(data)
{
  $('#chart-container').find('svg').remove();

  calculate_w_h(w, h, data.length);

  var c_Width = $(document.body)[0].clientWidth;
  var left_offset = c_Width-width < 0 ? 0 : (c_Width-width)/2
  var position = {left: left_offset, top: 30};

  $('#chart-container').css({ 'left': position.left, 'top':position.top })

  

  svg = d3.select("#chart-container").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
      .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

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
      .text("frequency");

    svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.key); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.val); })
      .attr("height", function(d) { return height - y(d.val); });

  align();


}
