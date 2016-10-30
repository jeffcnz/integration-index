
var resultChart;
var tsdata;
var monSite;
var geojsonMarkerOptions = {
    radius: 8,
    fillColor: "#2b8cbe",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
};

var emptyTs = {"time": {"instant":""},
                "value": ""};

var siteLoc = L.map('siteLoc');

var long = ($('#site_long').data()).long;
var lat = ($('#site_lat').data()).lat;

var ctx = document.getElementById("resultChart");

//var tsColDef = [{"title": "Time",
//                "data": "time.instant"},
//                {"title": "Value",
 //               "data": "value"}];



siteLoc.setView([lat, long], 11);

//siteLoc.setView([-39, 177], 6);
  
  // {s}, {z}, {x} and {y} are placeholders for map tiles
  // {x} and {y} are the x/y of where you are on the map
  // {z} is the zoom level
  // {s} is the subdomain of cartodb
var layer = L.tileLayer("http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
  });
  
  // Now add the layer onto the map
siteLoc.addLayer(layer);

monSites = L.circleMarker([lat, long], geojsonMarkerOptions).addTo(siteLoc);

var checkDate = function(rawdate) {
    if(rawdate != "Invalid date"){
        return rawdate;
    }else{
        return null;
    }
}

var getObservationsUrl = function(feature, parameter, procedure, tstart = null, tend = null){
    var url = "http://localhost:5000/SOS?Service=SOS&Request=GetObservation&Format=JSON&FeatureOfInterest=" + feature + "&ObservedProperty=" + parameter + "&Procedure=" + procedure;
    //append time interval depending on data providied
    //console.log(tstart);
    //console.log(tend);
    if(tstart && tend){
        
        //console.log(start);
        var outurl = url + "&TemporalFilter=om:phenomenonTime," + tstart + "/" + tend;
    }else{
        //console.log("No times")
        var outurl = url;
    };
    //var outurl = url;
    return outurl

}

var refreshTsChartTable = function(){
    //First remove any previous data in the table, then if the request doesn't work old data doesn't stay in the table
    $("#result_table").DataTable({
        scrollY: 300,
        paging: false,
        ordering: false,
        searching: false,
        destroy: true,
        data: emptyTs,
        columns: [{"title": "Time",
                "data": "time.instant"},
                {"title": "",
                "data": "value"}]
    });

    if(resultChart!=null){
        resultChart.destroy();
    }

    //Set up the variables required for passing to the url builder
    var feature = $("#site_id").text();
    var param = $("#observedProperty_Select :selected").text();
    var proc = $("#procedure_Select :selected").text();
    //var tzoffset = moment().utcOffset();
    //var tstart = moment($('#startdatetimepicker').data().date, "DD/MM/YYYY hh:mm").local().add(tzoffset, "m").format("YYYY-MM-DDTHH:mm");
    //var tend = moment($('#enddatetimepicker').data().date, "DD/MM/YYYY hh:mm").local().add(tzoffset, "m").format("YYYY-MM-DDTHH:mm");
    var tstart = checkDate(moment($("#startdatetimepicker").data().date, "DD/MM/YYYY hh:mm").local().format("YYYY-MM-DDTHH:mm"));
    var tend = checkDate(moment($("#enddatetimepicker").data().date, "DD/MM/YYYY hh:mm").local().format("YYYY-MM-DDTHH:mm"));
    
    

    //var tzoffset = tstart.utcOffset();
    //console.log(tstart);
    //console.log(tend);

    //Build the url, and display it
    var url = getObservationsUrl(feature, param, proc, tstart, tend);
    
    $("#url_display").html("<p>"+url+"</p>");
    //var data = $.get(url, function(data){
       // return data});

    //Send the ajax request and populate the data table with the result
    $.get(url, function (data) {
    var dt = data;
    //console.log(tsColDef[1]);

    //console.log(dt["responseJSON"]);
    //tsColDef[1]["title"] = "mm";
    //console.log(tsColDef[1]);
    var points = function(){
               var arr = [];
               var results = dt.Observation[0].result;
               //console.log(results);
               for(var i=0; i<results.length; i++){
                   
                       arr.push({x:new Date(results[i].time.instant), y:results[i].value});
                   
               }
               return arr;
           }

        
    resultChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                fill: false,
                borderColor: "#2b8cbe",
                pointBorderColor: "#2b8cbe",
                data: points()
            }]
        },
        options: {
            legend:{
                display: false
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    position: 'bottom'
                }]
            }
        }
    });

    $("#result_table").DataTable({
        scrollY: 300,
        paging: false,
        ordering: false,
        searching: false,
        destroy: true,
        data: dt.Observation[0].result,
        columns: [{"title": "Time",
                "data": "time.instant"},
                {"title": dt.Observation[0].defaultPointMetadata.uom,
                "data": "value"}]
    });
    });
}

//$(function () {
//                $('#startdatetimepicker').datetimepicker();
//            });
//$(function () {
//                $('#enddatetimepicker').datetimepicker();
//            });


//Initialisation of elements on page load

$(function () {
    $("#startdatetimepicker").datetimepicker({locale: "en-nz"});
    $("#enddatetimepicker").datetimepicker({locale: "en-nz", useCurrent: false});
    $("#startdatetimepicker").on("dp.change", function(e){
        $('#enddatetimepicker').data("DateTimePicker").minDate(e.date);
        $('#startdatetimepicker').data("DateTimePicker").date(e.date);
        refreshTsChartTable();
        });
    $("#enddatetimepicker").on("dp.change", function(e){
        $('#startdatetimepicker').data("DateTimePicker").maxDate(e.date);
        $('#enddatetimepicker').data("DateTimePicker").date(e.date);
        refreshTsChartTable();
        });
})

//$("document").ready(function () {
//                $("#startdatetimepicker").datetimepicker({locale: "en-nz"});
//            });

//$("document").ready(function () {
//                $("#enddatetimepicker").datetimepicker({locale: "en-nz", useCurrent: false});
//            });

$("document").ready(refreshTsChartTable);

//update the table and chart when an input variable changes
$("#observedProperty_Select").change(refreshTsChartTable);
$("#procedure_Select").change(refreshTsChartTable);
//$("#startdatetimepicker").on("dp.change", function(e){
//    $('#enddatetimepicker').data("DateTimePicker").minDate(e.date);
//});
//$("#enddatetimepicker").on("dp.change", function(e){
//    $('#startdatetimepicker').data("DateTimePicker").maxDate(e.date);
//});
//$("#startdatetimepicker").change(refreshTsChartTable);
//$("#enddatetimepicker").change(refreshTsChartTable);