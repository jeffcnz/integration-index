#Flask application
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, make_response
import urllib
from datetime import datetime, timedelta

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


import settings
#Import database libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, AgencyTimeSeries, AgencyParameters, MonitoringSites, EnvDomains, Agency, AgencyWfs, TsServerTypes, Parameters, DomainParameters, WmlInterpolationType, TsServerTypeInterpolation, Procedures, TsServerProcedureCall, SiteDomains

from ts_helper import hilltopTsUrlRead, AgencyUrl, kistersSosTsUrlToDict

from json_helper import jsonSite, geoJsonSite, jsonTs

#setup app
app = Flask(__name__)
#setup database
engine = create_engine(settings.db_connection)

Base.metadata.bind = engine

#create comms link

DBSession = sessionmaker(bind = engine)
session = DBSession()


def AgencyTranslate(feature_of_interest, observed_property, procedure, time_period):
	"""Convert the provided key value pairs into an agency server request"""
	#query feature to get agency and agency site name
	if feature_of_interest:
		site_info = session.query(MonitoringSites).filter_by(national_id = feature_of_interest).first()
		if not site_info:
			return "Error", "No feature of interest with the name " + feature_of_interest
	else:
		return "Error", "A feature of interest must be provided."

	#query agency timeseries server type and url
		
	agency_ts_info = session.query(AgencyTimeSeries, TsServerTypes).join(TsServerTypes).filter(AgencyTimeSeries.agency_id == site_info.agency_id).first()
	#print agency_ts_info[1].server_type

	if observed_property:
		#identify the agency parameter
		temp_param = session.query(Parameters).filter_by(name = observed_property).first()
		if not temp_param:
			return "Error", "No observed property with the name " + observed_property
		agency_param_info = session.query(AgencyParameters).filter(AgencyParameters.agency_id == site_info.agency_id, AgencyParameters.parameter_id == temp_param.id).first()
		if not agency_param_info:
			return "Error", "No observed property available with the name " + observed_property 
	else:
		return "Error", "An observed property must be provided."

	if procedure:
		temp_proc = session.query(Procedures).filter_by(name = procedure).first()
		agency_proc_info = session.query(TsServerProcedureCall).filter(TsServerProcedureCall.ts_server_type_id == agency_ts_info[1].id, TsServerProcedureCall.procedure_id == temp_proc.id).first()
		if not agency_proc_info:
			return "Error", "No procedure with the name." + procedure
	else:
		return "Error", "A valid procedure must be provided."

	return AgencyUrl(agency_ts_info[1].server_type, agency_ts_info[0].timeseries_url, site_info.site_name, agency_param_info.agency_parameter_name, agency_proc_info.ts_server_procedure_call, time_period)
	
	

def InterpolationSet(observed_property, procedure):
	"""Identify the OGC interpolation type based on the requested procedure"""
	if "Total" in procedure:
		int_info = session.query(WmlInterpolationType).filter_by(interpolation_type = "Preceding Total").first()
	elif "Average" in procedure:
		int_info = session.query(WmlInterpolationType).filter_by(interpolation_type = "Average in Preceding Interval").first()
	else:
		#procedure is Raw
		temp_int = session.query(Parameters, WmlInterpolationType).join(WmlInterpolationType).filter(Parameters.name == observed_property).first()
		int_info = temp_int[1]
		
	return int_info



@app.route("/SOS")
def service():
	
	if request.args.get("Service"):
		if request.args.get("Service") == "SOS":
			if request.args.get("Request"):
				if request.args.get("Request") == "GetObservation":
					feature = request.args.get("FeatureOfInterest")
					measured_param = request.args.get("ObservedProperty")
					time_period = request.args.get("TemporalFilter")
					procedure = request.args.get("Procedure")
					tsurl, tsserver = AgencyTranslate(feature, measured_param, procedure, time_period)
					#print tsserver, tsurl
					if tsurl == "Error":
						code = "MissingParameterValue"
						locator = "Request"
						text = tsserver
						response = make_response(render_template("xml/error.xml", code = code, text = text, locator = locator))
					else:
						if "Hilltop" == tsserver:
							data = hilltopTsUrlRead(tsurl)
						elif "Kisters" in tsserver:
							data = kistersSosTsUrlToDict(tsurl)
							
						
						data.append(InterpolationSet(measured_param, procedure))
						
						time_now = datetime.utcnow()
						nz_time = time_now + timedelta(hours=12)
						if data[0] and data[1]:
							if request.args.get("Format") == "JSON":
								return jsonify(Observation = jsonTs(data, feature, measured_param, procedure, datetime.strftime(nz_time, "%Y-%m-%dT%H:%M:%S")))
							else:
								template = render_template("xml/getobservation.xml", data = data, foi = feature, param = measured_param, proc = procedure, time = datetime.strftime(nz_time, "%Y-%m-%dT%H:%M:%S"))
								response = make_response(template)
								response.headers["Content-Type"] = "application/xml"
								return response
						else:
							response = make_response(render_template("xml/error.xml", code = "ResourceNotFound", text = "No data available for the requested Feature of Interest and Observed Parameter.", locator = ""))
							response.headers["Content-Type"] = "application/xml"
							return response

				elif request.args.get("Request") == "GetFeatureOfInterest":
					features = session.query(MonitoringSites, Agency, EnvDomains).join(Agency).join(SiteDomains).join(EnvDomains)
					if request.args.get("Offering"):
						features = features.filter(EnvDomains.domain_name == request.args.get("Offering"))
					if request.args.get("BBox"):
						coords = request.args.get("BBox").split(",")
						lats = sorted([float(coords[0]), float(coords[2])])
						longs = sorted([float(coords[1]), float(coords[3])])
						features = features.filter(MonitoringSites.latitude >= lats[0], MonitoringSites.latitude <= lats[1], MonitoringSites.longitude >= longs[0], MonitoringSites.longitude <= longs[1])
					time_now = datetime.utcnow()
					nz_time = time_now + timedelta(hours=12)
					if request.args.get("Format") == "JSON":
						return jsonify(geoJsonSite(features))
					else:	
						template = render_template("xml/getfeatures.xml", features = features, time = datetime.strftime(nz_time, "%Y-%m-%dT%H:%M:%S"))
						response = make_response(template)
						response.headers["Content-Type"] = "application/xml"
						return response
					
				elif request.args.get("Request") == "GetCapabilities":
					params = session.query(Parameters).all()
					procedures = session.query(Procedures).all()
					domains = session.query(EnvDomains).all()
					#code = "OperationNotSupported"
					#locator = "Request"
					#text = "GetCapabilities isn't implemented yet"
					#response = make_response(render_template("xml/error.xml", code = code, text = text, locator = locator))
					response = make_response(render_template("xml/getCapabilities.xml", params = params, procedures = procedures, domains = domains))
					response.headers["Content-Type"] = "application/xml"
					return response

				else:
					code = "OperationNotSupported"
					locator = "Request"
					text = "Valid requests are GetCapabilities, GetFeatureOfInterest, GetObservation"
					response = make_response(render_template("xml/error.xml", code = code, text = text, locator = locator))
					response.headers["Content-Type"] = "application/xml"
					return response
			else:
				code = "MissingParameterValue"
				locator = "Request"
				text = "A Request statement must be provided"
				response = make_response(render_template("xml/error.xml", code = code, text = text, locator = locator))
				response.headers["Content-Type"] = "application/xml"
				return response
		else:
			code = "OperationNotSupported"
			locator = "Request"
			text = "Valid services are SOS"
			response = make_response(render_template("xml/error.xml", code = code, text = text, locator = locator))
			response.headers["Content-Type"] = "application/xml"
			return response 
	else:
		code = "MissingParameterValue"
		locator = "Request"
		text = "Requests must start with Service="
		response = make_response(render_template("xml/error.xml", code = code, text = text, locator = locator))
		response.headers["Content-Type"] = "application/xml"
		return response

	
@app.route("/")
@app.route("/home/")
def home():
	return render_template("home.html")

@app.route("/sites/")
def sites():
	sites = session.query(MonitoringSites).all()
	offerings = session.query(EnvDomains).all()
	return render_template("sites.html", sites = sites, offerings=offerings)

@app.route("/sites/<string:site_id>")
def oneSite(site_id):
	procedures = session.query(Procedures).all()
	siteAgency = session.query(MonitoringSites, Agency).join(Agency).filter(MonitoringSites.national_id == site_id).first()
	siteParams = session.query(MonitoringSites, EnvDomains, Parameters).join(SiteDomains).join(EnvDomains).join(DomainParameters).join(Parameters).filter(MonitoringSites.national_id == site_id)
	return render_template("single_site.html", siteAgency = siteAgency, siteParams = siteParams, procedures = procedures)


@app.route("/agencies/")
def agencies():
	agencies = session.query(Agency).all()
	return render_template("agencies.html", agencies = agencies)

@app.route("/wfs/")
def wfs():
	wfs = session.query(AgencyWfs, Agency).join(Agency).all()
	return render_template("wfs.html", wfs = wfs)

@app.route("/domains/")
def domains():
	domains = session.query(EnvDomains).all()
	return render_template("domains.html", domains = domains)

@app.route("/parameters/")
def parameters():
	params = session.query(Parameters).all()
	return render_template("parameters.html", params = params)

@app.route("/parameters/<string:parameter_name>")
def oneParameter(parameter_name):
	param = session.query(Parameters).filter_by(name = parameter_name).first()
	return render_template("single_parameter.html", param = param)


@app.route("/ts/")
def ts():
	ts = session.query(TsServerTypes).all()
	return render_template("ts.html", ts = ts)	

@app.route("/procedures/")
def procedures():
	procedures = session.query(Procedures).all()
	return render_template("procedures.html", procedures = procedures)

@app.route("/procedures/<string:procedure_name>")
def oneProcedure(procedure_name):
	proc = session.query(Procedures).filter_by(name = procedure_name).first()
	return render_template("single_procedure.html", procedure = proc)


@app.route("/sites/Json/")
def sitesJson():
	sites = session.query(MonitoringSites, Agency, EnvDomains).join(Agency).join(SiteDomains).join(EnvDomains).all()
	return jsonify(Sites=jsonSite(sites))

@app.route("/api/")
def api():
	procedures = session.query(Procedures).all()
	return render_template("api.html", procedures = procedures)

@app.route("/debug/")
def debug():
	return render_template("debug.html")

if __name__ == "__main__":
	app.secret_key = "super_secret_key"
	app.debug = True #automatically restarts when code changes
	app.run(host = "0.0.0.0", port = 5000) #listens on specified IP address and port