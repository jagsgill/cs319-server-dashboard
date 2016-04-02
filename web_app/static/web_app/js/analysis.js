$(document).ready(function () {

  $("#startDate").datepicker();
  $("#endDate").datepicker();
  $(".chart").append("<svg id='lineChart' width='1500' height='550'></svg>")
  
  var interval;
  var sensorType;
  $('#generateGraph').on('click', function (ev) {
    if($("#sensorType").val() == "Accelerometer") {
        sensorType = 1;
        getDataAccel();
    } else if ($("#sensorType").val() == "Battery Life"){
        sensorType = 2;
        getDataBattery();
    } else {
        getDataAccel();
    }
    if($("#liveUpdate").is(':checked')) {
        if(interval) {
            clearInterval(interval);
        }
        interval=setInterval(function() {update()}, 1000);
    } else {
        if(interval) {
            clearInterval(interval);
        }
    }
  });

    function updateGraph(data) {
    console.log("updating graph");
    $('#lineChart').empty();
    console.log(data);
    var dataGroup = d3.nest().key(function(d) {return d.device_id;}).entries(data);
    var color = d3.scale.category10();
    var vis = d3.select("#lineChart"),
    WIDTH = $(".chart").width(),
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
    						if(sensorType==2){
    							return 0;
    						} else {
                            return d.accel;
    						}
                        }), d3.max(data, function(d) {
                        	if(sensorType==2){
    							return 100;
    						} else {
                            return d.accel;
    						}
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
        if(sensorType==1){
            getDataAccel();
        } else if(sensorType==2) {
            getDataBattery();
        } else {
            getDataAccel();
        }
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

  function getDataAccel() {
    console.log("getting data");
    //  Get URL, parse to get device ID
    var url = window.location.href;
    var regex =/[^/]*$/g
    url = url.match(regex)
    console.log("url: http://localhost:8000/dashboard/live/" + url);

    d3.json("http://localhost:8000/dashboard/live/" + url, function(error, json){
    var newData=[];
    json.forEach(function(d){
    newData.push({"device_id":"X","accelTime":d.accelTime,"accel":d.xAccel});
    newData.push({"device_id":"Y","accelTime":d.accelTime,"accel":d.yAccel});
    newData.push({"device_id":"Z","accelTime":d.accelTime,"accel":d.zAccel});
    });
    updateGraph(newData);
    console.log(newData);});
  }
  
  function getDataBattery() {
    console.log("getting data");
    //  Get URL, parse to get device ID
    var url = window.location.href;
    var regex =/[^/]*$/g
    url = url.match(regex)
    console.log("url: http://localhost:8000/dashboard/live/" + url);
    d3.json("http://localhost:8000/dashboard/live/" + url, function(error, json){
    var newData=[];
    json.forEach(function(d){
    newData.push({"device_id":"Battery_Life","accelTime":d.accelTime,"accel":d.battery_level*100});
    });
    updateGraph(newData);
    console.log(newData);});
  }

});