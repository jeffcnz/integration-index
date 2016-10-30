//Javascript for the sites page to provide interactive map and table.


//setup variables for later use
var dt;
var monSites;
var markers; 
var geojsonMarkerOptions = {
    radius: 8,
    fillColor: "#2b8cbe",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
};

//Define the columns for the table.
var sitesColDef = [
                    { "data": function (data, type, row, meta) {
                        return '<a href="http://localhost:5000/sites/' + data.properties.National_ID +'">' + data.properties.National_ID + '</a>'; 
                    }},
                    { "data": "properties.Site_Name" },
                    { "data": "properties.Agency_Name"},
                    { "data": "properties.Offering"}
                                            ];



function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties) {
        layer.bindPopup(feature.properties.National_ID);
    }
}


var getFeaturesUrl = function(offering){
    var url = "http://localhost:5000/SOS?Service=SOS&Request=GetFeatureOfInterest&Format=JSON"
    if (offering != "All"){
        url = url.concat("&Offering=",offering)
    }
    var bb = map.getBounds();
    //console.log(bb);
    var c1 = bb._southWest;
    var c2 = bb._northEast;
    //console.log(c1);
    var outurl = url.concat("&BBox=",c1.lat,",",c1.lng,",",c2.lat,",",c2.lng)
    //console.log(outurl)
    return outurl

}

var refreshMapTable = function(){
    //check what offering is selected from the dropdown
    var off = $("#offering_select :selected").text();
    //request sites based on that offering
    $.get(getFeaturesUrl(off), function (data) {
    dt = data;
    //If there is already data on the map clear it
    if (monSites) {monSites.clearLayers()};
    if (markers) {markers.clearLayers()};

    //Create the monitoring sites layer, with circles for points and popup info.
    monSites = L.geoJson(dt, {
        pointToLayer: function (feature, latlng) {
            return L.circleMarker(latlng, geojsonMarkerOptions);
            },
        onEachFeature: function (feature, layer) {
            return layer.bindPopup('<a href="http://localhost:5000/sites/' + feature.properties.National_ID +'">' + feature.properties.National_ID + '</a><p>' + feature.properties.Site_Name + '</p>' );
        }
        });

    //Setup the clustering layer, add the monitoring sites and then add to the map.
    markers = L.markerClusterGroup();
    markers.addLayer(monSites);
    map.addLayer(markers);

    //Populate the datatable
    $('#sites_table').DataTable({
        destroy: true,
        data: dt.features,
        columns: sitesColDef
    });
    });
}

//var refreshSitesTable = function(){
//    var off = $("#offering_select :selected").text();
//    $.get(getFeaturesUrl(off), function (data) {

 //       dt = data;
//        $('.table').DataTable({
//        destroy: true,
 //       data: dt.features,
//        columns: sitesColDef
 //   });
        
//    });
//}

//Initialise the map with a base map and showing all of New Zealand
var map = L.map('map');

map.on({load :function() {//console.log("map loaded");
    var off = $("#offering_select :selected").text();
    $.get(getFeaturesUrl(off), function(data) {refreshMapTable(data)});
}
});

map.setView([-39, 177], 6);
  
  // {s}, {z}, {x} and {y} are placeholders for map tiles
  // {x} and {y} are the x/y of where you are on the map
  // {z} is the zoom level
  // {s} is the subdomain of cartodb
var layer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
  });
  
  // Now add the layer onto the map
map.addLayer(layer);



//Define callbacks so that when the map is zoomed or dragged the sites are updated (uses BBox on map extent)
map.on({zoomend: refreshMapTable,
        dragend: refreshMapTable,
        moveend: refreshMapTable});


//Update the map and table when the offering selection changes
$("#offering_select").change(refreshMapTable);


