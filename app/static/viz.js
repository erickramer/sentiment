function create_updater(){

  function update(data){

    var bars = g.selectAll("rect")
      .data(data, function(d) { return d.emoji; });

    x.domain(data.map(function(d) { return d.emoji; }));
    y.domain([0, d3.max(data, function(d) { return d.num; })]);

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
    margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom

  var x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
      y = d3.scaleLinear().rangeRound([height, 0])

  var g = svg.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var t = d3.transition()
            .duration(750);

  return update
}


$('document').ready(function(){

  var update_barplot = create_updater()
  var data = {text: "hello"}

  $.post('/api/score', data, function(res){

    function randomizer(){
      var new_data = _.chain(res.emoji)
       .map(function(num, key){ return {'emoji': key, 'num': num + Math.random() - 0.5}})
       .sortBy(function(d){return -d.num})
       .first(20)
       .value();

      update_barplot(new_data)

    }

    var data = _.chain(res.emoji)
                .map(function(num, key){ return {'emoji': key, 'num': num} })
                .sortBy(function(x){ return -x.num})
                .first(20)
                .value();

    update_barplot(data);

    setInterval(randomizer, 5000)

  })




})
