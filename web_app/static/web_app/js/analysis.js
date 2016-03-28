$(document).ready(function () {

  $("#startDate").datepicker();
  $("#endDate").datepicker();

  var interval;
  $('#generateGraph').on('click', function (ev) {
    getData();
    console.log("hello");
    if(interval) {
        clearInterval(interval);
    }
    interval=setInterval(function() {update()}, 1000);
  });

    function updateGraph(data) {
    console.log("updating graph");
    $('#lineChart').empty();
    //var data = globaldata;
    console.log("i got here");
    console.log(data);
    var dataGroup = d3.nest().key(function(d) {return d.deviceId;}).entries(data);
    console.log("can i get here");
    var color = d3.scale.category10();
    var vis = d3.select("#lineChart"),
    WIDTH = 800,
    HEIGHT = 500,
    MARGINS = {
        top: 50,
        right: 20,
        bottom: 50,
        left: 50
    },

    lSpace = WIDTH/dataGroup.length;

    xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([d3.min(data, function(d) {
                            return d.accelTime;
                        }), d3.max(data, function(d) {
                            return d.accelTime;
                        })]),
    yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([d3.min(data, function(d) {
                            return d.accel;
                        }), d3.max(data, function(d) {
                            return d.accel;
                        })]),
    xAxis = d3.svg.axis().scale(xScale),
    yAxis = d3.svg.axis().scale(yScale).orient("left");
    vis.append("svg:g").attr("class","axis").attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")").call(xAxis);
    vis.append("svg:g").attr("class","axis").attr("transform", "translate(" + (MARGINS.left) + ",0)").call(yAxis);
    var lineGen = d3.svg.line()
    .x(function(d) {
        return xScale(d.accelTime);
    })
    .y(function(d) {
        return yScale(d.accel);
    })
    .interpolate("basis");
    dataGroup.forEach(function(d,i) {
                        vis.append('svg:path')
                        .attr('d', lineGen(d.values))
                        .attr('stroke', function(){
                        return "hsl(" + i*(360/dataGroup.length) + ",100%,50%)";
                        })
                        .attr('stroke-width', 1)
                        .attr('id', 'line_'+d.key)
                        .attr('fill', 'none')
                        .attr('opacity', 0.5);
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
        getData();
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

  function getData() {
    console.log("getting data");
    //  Get URL, parse to get device ID
    var url = window.location.href;
    var regex =/[^/]*$/g
    url = url.match(regex)
    console.log("url: http://localhost:8000/dashboard/live/" + url);

    d3.json("http://localhost:8000/dashboard/live/" + url, function(error, json){
    var newData=[];
    json.forEach(function(d){
    newData.push({"deviceId":d.deviceId+"x","accelTime":d.accelTime,"accel":d.xAccel});
    newData.push({"deviceId":d.deviceId+"y","accelTime":d.accelTime,"accel":d.yAccel});
    newData.push({"deviceId":d.deviceId+"z","accelTime":d.accelTime,"accel":d.zAccel});
    });
    updateGraph(newData);
    console.log(newData);});
  }

});