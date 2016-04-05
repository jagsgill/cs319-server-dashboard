$(document).ready(function () {

  $("#startDate").datepicker();
  $("#endDate").datepicker();
  $(".chart").append("<svg id='lineChart' width="+ $(window).width()/1.5 +" height='600'></svg>");
  $("#liveUpdate").prop('checked',true);
  $("#dateError").hide();
  generateGraph();
  
  var interval;
  var sensorType;
  var yAxVal;
  var titleText;
  $('#generateGraph').on('click', function (ev) {
    generateGraph();
  });
  
  $('#liveUpdate').change(function() {
	$("#dateError").hide();
	generateGraph();
  });
  
  $('#sensorType').change(function() {
	generateGraph();
  });
  
  	function generateGraph() {
  		if($("#sensorType").val() == "Accelerometer") {
  			titleText = "Acceleration over Time";
  			yAxVal = "Acceleration (m/s^2)";
  	        sensorType = 1;
  	        getDataAccel();
  	    } else if ($("#sensorType").val() == "Battery Life"){
  	    	titleText = "Battery Life over Time";
  	    	yAxVal = "Battery Level";
  	        sensorType = 2;
  	        getDataBattery();
  	    } else {
  	    	titleText = "Acceleration over Time";
  			yAxVal = "Acceleration (m/s^2)";
  	        getDataAccel();
  	    }
  	    if($("#liveUpdate").is(':checked')) {
  	    	$("#sDate").hide();
  	    	$("#eDate").hide();
  	    	$("#generateGraph").hide();
  	        if(interval) {
  	            clearInterval(interval);
  	        }
  	        interval=setInterval(function() {update()}, 1000);
  	    } else {
  	    	$("#sDate").show();
  	    	$("#eDate").show();
  	    	$("#generateGraph").show();
  	        if(interval) {
  	            clearInterval(interval);
  	        }
  	    }
  	}

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
    var format = d3.time.format("%H:%M:%S"); 
    xScale = d3.time.scale().range([MARGINS.left, WIDTH - MARGINS.right]).domain([d3.min(data, function(d) {
        return d.accelDate;
    }), d3.max(data, function(d) {
        return d.accelDate;
    })]);
    
//    xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([d3.min(data, function(d) {
//                            return d.accelTime;
//                        }), d3.max(data, function(d) {
//                            return d.accelTime;
//                        })]);
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
                        })]);
    xAxis = d3.svg.axis().scale(xScale).ticks(5).tickFormat(format);
    yAxis = d3.svg.axis().scale(yScale).orient("left");
    vis.append("svg:g").attr("class","axis").attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")").call(xAxis);
    vis.append("svg:g").attr("class","axis").attr("transform", "translate(" + (MARGINS.left) + ",0)").call(yAxis);
    var lineGen = d3.svg.line()
    .x(function(d) {
        return xScale(d.accelDate);
    })
    .y(function(d) {
        return yScale(d.accel);
    })
    .interpolate("basis");
    vis.append("text")
//    .attr("text-anchor", "start")  
//    .attr("transform", "translate("+ 0 +","+MARGINS.top/2+")")
    .attr("text-anchor", "middle")
    .attr("transform", "translate("+ 15 +","+(HEIGHT/2)+")rotate(-90)")
    .style("font-size", "20px")
    .text(yAxVal);
    vis.append("text")
    .attr("text-anchor", "end")
    .attr("transform", "translate("+ (WIDTH) +","+(HEIGHT-MARGINS.bottom-5)+")")
    .style("font-size", "20px")
    .text("Time");
    vis.append("text")
    .attr("text-anchor", "middle")
    .attr("transform", "translate("+ (WIDTH/2) +","+MARGINS.top+")")
    .style("font-size", "30px")
    .text(titleText);
    if(data.length===0) {
    	vis.append("text")
        .attr("text-anchor", "middle")
        .attr("transform", "translate("+ (WIDTH/2) +","+(HEIGHT/2)+")")
        .style("font-size", "30px")
        .text("No Data Available");
    }
    var color;
    dataGroup.forEach(function(d,i) {
                        vis.append('svg:path')
                        .attr('d', lineGen(d.values))
                        .attr('stroke', function(){
                        	color="hsl(" + i*(360/dataGroup.length) + ",100%,50%)";
                        	return color;
                        })
                        .attr('stroke-width', 1)
                        .attr('id', 'line_'+d.key)
                        .attr('fill', 'none')
                        .attr('opacity', 0.5);
                        vis.append("text")
                        	.attr("text-anchor", "middle")
                            .attr("x", (lSpace/2)+i*lSpace)
                            .attr("y", HEIGHT)
                            .style("font-size", "25px")
                            .style("stroke", "grey")
                            .style("fill", color)
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

  function getDataAccel() {
    console.log("getting data");
    //  Get URL, parse to get device ID
    var url = window.location.href;
    var regex =/[^/]*$/
    var id = url.match(regex);
    if(!$("#liveUpdate").is(':checked')) {
    	$("#dateError").hide();
    	var dateRegex = /^(0[1-9]|1[0-2])\/(0[1-9]|1\d|2\d|3[01])\/\d{4}$/
    	if(dateRegex.test($("#startDate").val()) && dateRegex.test($("#endDate").val()) && $("#endDate").val()>$("#startDate").val()){
	    	var start = (new Date($("#startDate").val()).getTime()).toFixed(0).toString();
	    	var end = (new Date($("#endDate").val()).getTime()).toFixed(0).toString();
	    	url = "http://localhost:8000/dashboard/live-accel-date/" + id + "/?start="+start+"&end="+end;
    	} else {
    		$("#dateError").show();
    		return;
    	}
    } else {
    	url = "http://localhost:8000/dashboard/live-accel/" + id;
    }
    console.log(url);
    d3.json(url, function(error, json){
    var newData=[];
    json.forEach(function(d){
    newData.push({"device_id":"X","accelTime":d.accelTime,"accel":d.xAccel,"accelDate":new Date(d.accelTime)});
    newData.push({"device_id":"Y","accelTime":d.accelTime,"accel":d.yAccel,"accelDate":new Date(d.accelTime)});
    newData.push({"device_id":"Z","accelTime":d.accelTime,"accel":d.zAccel,"accelDate":new Date(d.accelTime)});
    });
    updateGraph(newData);
    console.log(newData);});
  }
  
  function getDataBattery() {
    console.log("getting data");
    //  Get URL, parse to get device ID
    var url = window.location.href;
    var regex =/[^/]*$/
    var id = url.match(regex);
    if(!$("#liveUpdate").is(':checked')) {
    	$("#dateError").hide();
    	var dateRegex = /^(0[1-9]|1[0-2])\/(0[1-9]|1\d|2\d|3[01])\/\d{4}$/
    	if(dateRegex.test($("#startDate").val()) && dateRegex.test($("#endDate").val()) && $("#endDate").val()>$("#startDate").val()){
	    	var start = (new Date($("#startDate").val()).getTime()).toFixed(0).toString();
	    	var end = (new Date($("#endDate").val()).getTime()).toFixed(0).toString();
	    	url = "http://localhost:8000/dashboard/live-battery-date/" + id + "/?start="+start+"&end="+end;
    	} else {
    		$("#dateError").show();
    		return;
    	}
    } else {
    	url = "http://localhost:8000/dashboard/live-battery/" + id;
    }
    console.log(url);
    d3.json(url, function(error, json){
    var newData=[];
    json.forEach(function(d){
    newData.push({"device_id":"Battery_Life","accelTime":d.timestamp,"accel":d.battery_level,"accelDate":new Date(d.timestamp)});
    });
    updateGraph(newData);
    console.log(newData);});
  }
  
  function dateToUnix(){
	  
  }

});