#Initial data to load into the database, sites data is not included as that is loaded from the WFS

#System data
ts_servers = [{"server_type": "Hilltop", "website": "http://www.hilltop.co.nz/", "api_doc": ""},
    {"server_type": "KistersARC", "website": "https://www.kisters.net/NA/", "api_doc": ""},
    {"server_type": "KistersWRC", "website": "https://www.kisters.net/NA/", "api_doc": ""},
	{"server_type": "52North", "website": "http://52north.org/", "api_doc": ""}]

domains = [{"domain_name": "SW Quantity", "wfs_name": "SWQuantity"},
	{"domain_name": "Rainfall", "wfs_name": "Rainfall"},
	{"domain_name": "SW Quality", "wfs_name": "SWQuality"}]

params = [{"name": "Discharge", "domain": "SW Quantity", "interpolation_type":"Continuous", "uom": "m3/s", "parameter_url": ""},
	{"name": "Precipitation", "domain": "Rainfall", "interpolation_type":"Preceding Total", "uom": "mm", "parameter_url": ""},
	{"name": "Total Nitrogen", "domain": "SW Quality", "interpolation_type":"Discontinuous", "uom": "g/m3", "parameter_url": ""},
	{"name": "Total Phosphorus", "domain": "SW Quality", "interpolation_type":"Discontinuous", "uom": "g/m3", "parameter_url": ""}]

domain_params = [{"domain_name": "SW Quantity", "parameter": "Discharge"},
	{"domain_name": "Rainfall", "parameter": "Precipitation"},
	{"domain_name": "SW Quality", "parameter": "Total Nitrogen"},
	{"domain_name": "SW Quality", "parameter": "Total Phosphorus"}]

wml_interpolation_type = [{"interpolation_type": "Continuous", "interpolation_type_url": "http://www.opengis.net/def/waterml/2.0/interpolationType/Continuous"},
	{"interpolation_type": "Discontinuous", "interpolation_type_url": "http://www.opengis.net/def/waterml/2.0/interpolationType/Discontinuous"},
	{"interpolation_type": "Preceding Total", "interpolation_type_url": "http://www.opengis.net/def/waterml/2.0/interpolationType/TotalPrec"},
	{"interpolation_type": "Average in Preceding Interval", "interpolation_type_url": "http://www.opengis.net/def/waterml/2.0/interpolationType/AveragePrec"}]

procedures = [{"name": "Raw", "description": "No procedure applied, values are as measured."},
	{"name": "HourTotal", "description": "The total in the preceding hour."},
	{"name": "DayTotal", "description": "The total in the preceding day."},
	{"name": "MonthTotal", "description": "The total in the preceding calendar month."},
	{"name": "YearTotal", "description": "The total in the preceding calendar year."},
	{"name": "HourAverage", "description": "The average in the preceding hour."},
	{"name": "DayAverage", "description": "The average in the preceding day."},
	{"name": "MonthAverage", "description": "The average in the preceding calendar month."},
	{"name": "YearAverage", "description": "The average in the preceding calendar year."}]


#Server data
ts_server_interpolation = [{"ts_server_type": "Hilltop", "ts_server_interpolation": "Discrete", "interpolation_type": "Discontinuous"},
	{"ts_server_type": "Hilltop", "ts_server_interpolation": "Instant", "interpolation_type": "Continuous"},
	{"ts_server_type": "Hilltop", "ts_server_interpolation": "Histogram", "interpolation_type": "Preceding Total"},
	{"ts_server_type": "KistersWRC", "ts_server_interpolation": "Discontinuous", "interpolation_type": "Discontinuous"},
	{"ts_server_type": "KistersWRC", "ts_server_interpolation": "Continuous", "interpolation_type": "Continuous"},
	{"ts_server_type": "KistersWRC", "ts_server_interpolation": "Preceding Total", "interpolation_type": "Preceding Total"},
	{"ts_server_type": "KistersARC", "ts_server_interpolation": "Discontinuous", "interpolation_type": "Discontinuous"},
	{"ts_server_type": "KistersARC", "ts_server_interpolation": "Continuous", "interpolation_type": "Continuous"},
	{"ts_server_type": "KistersARC", "ts_server_interpolation": "Preceding Total", "interpolation_type": "Preceding Total"}]

ts_procedure_calls = [{"server_type":"Hilltop", "name": "Raw", "call": ""},
	{"server_type":"Hilltop", "name": "HourTotal", "call": "&Method=Total&Interval=1 Hour"},
	{"server_type":"Hilltop", "name": "DayTotal", "call": "&Method=Total&Interval=1 Day"},
	{"server_type":"Hilltop", "name": "MonthTotal", "call": "&Method=Total&Interval=1 Month"},
	{"server_type":"Hilltop", "name": "YearTotal", "call": "&Method=Total&Interval=1 Year"},
	{"server_type":"Hilltop", "name": "HourAverage", "call": "&Method=Average&Interval=1 Hour"},
	{"server_type":"Hilltop", "name": "DayAverage", "call": "&Method=Average&Interval=1 Day"},
	{"server_type":"Hilltop", "name": "MonthAverage", "call": "&Method=Average&Interval=1 Month"},
	{"server_type":"Hilltop", "name": "YearAverage", "call": "&Method=Average&Interval=1 Year"},
	{"server_type":"KistersWRC", "name": "Raw", "call": "&procedure=Cmd.P"},
	{"server_type":"KistersWRC", "name": "HourTotal", "call": "&procedure=Hour.Total"},
	{"server_type":"KistersWRC", "name": "HourTotal", "call": "&procedure=Day.Total"},
	{"server_type":"KistersWRC", "name": "MonthTotal", "call": "&procedure=Month.Total"},
	{"server_type":"KistersWRC", "name": "YearTotal", "call": "&procedure=Year.Total"},
	{"server_type":"KistersWRC", "name": "HourAverage", "call": "&procedure=Hour.Mean"},
	{"server_type":"KistersWRC", "name": "DayAverage", "call": "&procedure=Day.Mean"},
	{"server_type":"KistersWRC", "name": "MonthAverage", "call": "&procedure=Month.Mean"},
	{"server_type":"KistersWRC", "name": "YearAverage", "call": "&procedure=Year.Mean"},
	{"server_type":"KistersARC", "name": "Raw", "call": "&Procedure=RAW"},
	{"server_type":"KistersARC", "name": "HourTotal", "call": "&Procedure=HOURTOT"},
	{"server_type":"KistersARC", "name": "HourAverage", "call": "&Procedure=HOURMEAN"},
	{"server_type":"KistersARC", "name": "DayAverage", "call": "&Procedure=DAYMEAN"}]
	

#Agency data
agencies = [{"name": "HBRC", "details": "Hawkes Bay Regional Council", "website": "http://www.hbrc.govt.nz"},
	{"name": "HRC", "details": "Horizons Regional Council", "website": ""},
	{"name": "WRC", "details": "Waikato Regional Council", "website": ""},
	{"name": "Auckland Council", "details": "Auckland Council", "website": ""}]

agency_wfs = [{"sites_url": "https://hbrcwebmap.hbrc.govt.nz/arcgis/services/emar/MonitoringSiteReferenceData/MapServer/WFSServer?request=GetFeature&service=WFS&typename=MonitoringSiteReferenceData&srsName=urn:ogc:def:crs:EPSG:6.9:4326&Version=1.1.0",
 	"agency": "HBRC"},
 	{"sites_url": "http://gis.horizons.govt.nz/arcgis/services/emar/ACMonitoringSiteReferenceData/MapServer/WFSServer?request=GetFeature&service=WFS&typeName=MonitoringSiteReferenceData", 
 	"agency": "Auckland Council"},
 	{"sites_url": "http://wrcgis.waikatoregion.govt.nz/wrcgis/services/emar/MonitoringSiteReferenceData/MapServer/WFSServer?request=Getfeature&service=WFS&VERSION=1.1.0&typename=monitoringsitereferencedata&srsname=epsg:4326", 
 	"agency": "WRC"},
 	{"sites_url": "http://gis.horizons.govt.nz/arcgis/services/emar/MonitoringSiteReferenceData/MapServer/WFSServer?request=getfeature&service=WFS&typename=MonitoringSiteReferenceData", 
 	"agency": "HRC"}]

agency_ts = [{"url": "http://data.hbrc.govt.nz/Envirodata/Emar.hts", "agency": "HBRC", "domain": "SW Quantity", "tsType": "Hilltop"},
	{"url": "http://data.hbrc.govt.nz/Envirodata/Emar.hts", "agency": "HBRC", "domain": "Rainfall", "tsType": "Hilltop"},
	{"url": "http://data.hbrc.govt.nz/Envirodata/Emar.hts", "agency": "HBRC", "domain": "SW Quality", "tsType": "Hilltop"},
	{"url": "http://aklc.hydrotel.co.nz:8080/KiWIS/KiWIS", "agency": "Auckland Council", "domain": "SW Quantity", "tsType": "KistersARC"},
	{"url": "http://aklc.hydrotel.co.nz:8080/KiWIS/KiWIS", "agency": "Auckland Council", "domain": "Rainfall", "tsType": "KistersARC"},
	{"url": "http://envdata.waikatoregion.govt.nz:8080/KiWIS/KiWIS", "agency": "WRC", "domain": "SW Quantity", "tsType": "KistersWRC"},
	{"url": "http://envdata.waikatoregion.govt.nz:8080/KiWIS/KiWIS", "agency": "WRC", "domain": "Rainfall", "tsType": "KistersWRC"},
	{"url": "http://envdata.waikatoregion.govt.nz:8080/KiWIS/KiWIS", "agency": "WRC", "domain": "SW Quality", "tsType": "KistersWRC"},
	{"url": "http://tsdata.horizons.govt.nz/boo.hts", "agency": "HRC", "domain": "SW Quantity", "tsType": "Hilltop"},
	{"url": "http://tsdata.horizons.govt.nz/boo.hts", "agency": "HRC", "domain": "Rainfall", "tsType": "Hilltop"}]

agency_params = [{"agency": "HBRC", "parameter": "Discharge", "agencyParam": "FlowM3S"},
	{"agency": "HBRC", "parameter": "Precipitation", "agencyParam": "Rainfall"},
	{"agency": "HBRC", "parameter": "Total Nitrogen", "agencyParam": "Total Nitrogen"},
	{"agency": "HBRC", "parameter": "Total Phosphorus", "agencyParam": "Total Phosphorus[Total Phosphorus]"},
	{"agency": "Auckland Council", "parameter": "Discharge", "agencyParam": "Stream Flow Rate"},
	{"agency": "Auckland Council", "parameter": "Precipitation", "agencyParam": "Rainfall"},
	{"agency": "WRC", "parameter": "Discharge", "agencyParam": "Discharge"},
	{"agency": "WRC", "parameter": "Precipitation", "agencyParam": "Precipitation"},
	{"agency": "WRC", "parameter": "Total Nitrogen", "agencyParam": "TotalNitrogen"},
	{"agency": "WRC", "parameter": "Total Phosphorus", "agencyParam": "Total Phosphorus"},
	{"agency": "HRC", "parameter": "Discharge", "agencyParam": "Flow [Water Level]"},
	{"agency": "HRC", "parameter": "Precipitation", "agencyParam": "Rainfall [SCADA Rainfall]"}]








