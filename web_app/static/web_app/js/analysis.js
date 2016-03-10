$(document).ready(function () {

  $("#startDate").datepicker();
  $("#endDate").datepicker();

  var interval;
  $('#generateGraph').on('click', function (ev) {
    updateGraph();
    if(interval) {
        clearInterval(interval);
    }
    interval=setInterval(function() {update()}, 3000);
  });

    function updateGraph() {
    console.log("updating graph");
    $('#lineChart').empty();
    var data = getData(data);
    var dataGroup = d3.nest().key(function(d) {return d.deviceID;}).entries(data);
    var color = d3.scale.category10();
    var vis = d3.select("#lineChart"),
    WIDTH = 1000,
    HEIGHT = 500,
    MARGINS = {
        top: 50,
        right: 20,
        bottom: 50,
        left: 50
    },

    lSpace = WIDTH/dataGroup.length;

    xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([d3.min(data, function(d) {
                            return d.timestamp;
                        }), d3.max(data, function(d) {
                            return d.timestamp;
                        })]),
    yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([d3.min(data, function(d) {
                            return d.acceleration;
                        }), d3.max(data, function(d) {
                            return d.acceleration;
                        })]),
    xAxis = d3.svg.axis().scale(xScale),
    yAxis = d3.svg.axis().scale(yScale).orient("left");
    vis.append("svg:g").attr("class","axis").attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")").call(xAxis);
    vis.append("svg:g").attr("class","axis").attr("transform", "translate(" + (MARGINS.left) + ",0)").call(yAxis);
    var lineGen = d3.svg.line()
    .x(function(d) {
        return xScale(d.timestamp);
    })
    .y(function(d) {
        return yScale(d.acceleration);
    })
    .interpolate("basis");
    dataGroup.forEach(function(d,i) {
                        vis.append('svg:path')
                        .attr('d', lineGen(d.values))
                        .attr('stroke', function(d,j) { 
                                return "hsl(" + Math.random() * 360 + ",100%,50%)";
                        })
                        .attr('stroke-width', 2)
                        .attr('id', 'line_'+d.key)
                        .attr('fill', 'none');
                        vis.append("text")
                            .attr("x", (lSpace/2)+i*lSpace)
                            .attr("y", HEIGHT)
                            .style("fill", "black")
                            .attr("class","legend")
                            .on('click',function(){
                                var active   = d.active ? false : true;
                                var opacity = active ? 0 : 1;
                                d3.select("#line_" + d.key).style("opacity", opacity);
                                d.active = active;
                            })
                            .text(d.key);
                    });
    }

    function update() {
        updateGraph();
    }

    function toDate(unix_tm) {
        var a = new Date(unix_tm * 1000);
        var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
        var year = a.getFullYear();
        var month = months[a.getMonth()];
        var day = a.getDate();
        var hour = a.getHours();
        var min = a.getMinutes();
        var sec = a.getSeconds();
        var time = month + ' ' + day + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
        return time;
    }

  function getData(data) {
    var data = [
    {"deviceID": "watch999","timestamp":1000098160,"x":1,"y":2,"z":14,"latitude":169,"longitude":105,"acceleration":14.177446878757825},
    {"deviceID": "watch999","timestamp":1000107500,"x":2,"y":2,"z":6,"latitude":154,"longitude":101,"acceleration":6.6332495807108},
    {"deviceID": "watch999","timestamp":1000123460,"x":8,"y":2,"z":9,"latitude":152,"longitude":103,"acceleration":12.206555615733702},
    {"deviceID": "watch999","timestamp":1000246750,"x":3,"y":2,"z":9,"latitude":151,"longitude":103,"acceleration":9.695359714832659},
    {"deviceID": "watch999","timestamp":1000264100,"x":4,"y":2,"z":13,"latitude":164,"longitude":92,"acceleration":13.74772708486752},
    {"deviceID": "watch999","timestamp":1000284000,"x":0,"y":2,"z":14,"latitude":170,"longitude":93,"acceleration":14.142135623730951},
    {"deviceID": "watch999","timestamp":1000319630,"x":3,"y":2,"z":6,"latitude":178,"longitude":107,"acceleration":7.0}
    ];

    return data;
  }

});