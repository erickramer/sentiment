function create_updater(){

  function update(data){

    var bars = g.selectAll("rect")
      .data(data, function(d) { return d.emoji; });

    var t = d3.transition()
              .duration(750);

    x.domain(data.map(function(d) { return d.emoji; }));
    y.domain([0, d3.max(data, function(d) { return d.num; })]);

    x_axis.style("fill-opacity", 1e-6)
      .transition(t)
      .call(d3.axisBottom(x))
      .style("fill-opacity", 1)

    bars.exit()
      .style("fill", "red")
      .transition(t)
      .style("fill-opacity", 1e-6)
      .remove();

    bars.transition(t)
      .attr("x", function(d) { return x(d.emoji); })
      .attr("y", function(d) { return y(d.num); })
      .attr("height", function(d){ return height - y(d.num)})

    bars.enter()
      .append("rect")
      .style('fill-opacity', 1e-6)
      .style('fill', "green")
      .transition(t)
      .attr("x", function(d) { return x(d.emoji); })
      .attr("y", function(d) { return y(d.num); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return height - y(d.num); })
      .style('fill', 'grey')
      .style('fill-opacity', 1)

  }

  var svg = d3.select("svg"),
    margin = {top: 20, right: 20, bottom: 50, left: 40},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom

  var x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
      y = d3.scaleLinear().rangeRound([height, 0])

  var g = svg.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var y_axis = g.append("g")
      .attr("class", "y axis")
      .call(d3.axisLeft(y).ticks(10, "%"))
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "0.71em")
      .attr("text-anchor", "end")

  var x_axis = g.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .style("font-size","30px")
      .call(d3.axisBottom(x));

  return update
}

function res_to_bar_data(res){
  var data = _.chain(res.emoji)
              .map(function(num, key){ return {'emoji': key, 'num': num} })
              .sortBy(function(x){ return -x.num})
              .first(30)
              .value();

  return data;
}


$('document').ready(function(){

  function barplot(res){
    var data = res_to_bar_data(res);
    update_barplot(data);
  }

  var update_barplot = create_updater()
  update_barplot = _.debounce(update_barplot, 1000)

  $('#target').keyup(function(){
    var post_data = {text: $(this).val()}
    console.log(post_data)
    $.post('/api/score', post_data, barplot);
  })

})
