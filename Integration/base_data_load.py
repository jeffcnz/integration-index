from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings

#from database_setup import Restaurant, Base, MenuItem
from database_setup import Base, Agency, AgencyWfs, TsServerTypes, Parameters, EnvDomains, AgencyTimeSeries, AgencyParameters, MonitoringSites, DomainParameters, WmlInterpolationType, TsServerTypeInterpolation, Procedures, TsServerProcedureCall

from wfs_read import emarWfsRead
from base_data import agencies, agency_wfs, ts_servers, domains, params, agency_ts, agency_params, domain_params, wml_interpolation_type, ts_server_interpolation, procedures, ts_procedure_calls

#setup the sqlAlchemy link to the database and prepare it for use
engine = create_engine(settings.db_connection)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Each dataset in the base_data file relates to a table in the database.
#For each one, each element is checked, if it is in the database then the database is updated.
#If it isn't in the database then it is added.
#Site information is populated using a seperate routine once the base data has been loaded.

print "Loading agencies"
for agency in agencies:
	newAgency = session.query(Agency).filter_by(name = agency['name']).first()
	if newAgency:
		newAgency.details = agency['details']
		newAgency.website = agency['website']
	else:
		newAgency = Agency(name=agency['name'], details=agency['details'], website=agency['website'])
	session.add(newAgency)
	session.commit()

print "Loading site list url"
for wfs in agency_wfs:
	temp_agency = session.query(Agency).filter_by(name=wfs['agency']).first()
	newWfs = session.query(AgencyWfs).filter_by(agency_id = temp_agency.id).first()
	if newWfs:
		newWfs.sites_url = wfs['sites_url']
	else:
		newWfs = AgencyWfs(sites_url=wfs['sites_url'], agency=temp_agency)
	session.add(newWfs)
	session.commit()

print "Loading time series server types"
for ts in ts_servers:
	newTs = session.query(TsServerTypes).filter_by(server_type = ts['server_type']).first()
	if newTs:
		newTs.website = ts['website']
		newTs.api_doc = ts['api_doc']
	else:
		newTs = TsServerTypes(server_type=ts['server_type'], website=ts['website'], api_doc=ts['api_doc'])
	session.add(newTs)
	session.commit()

print "Loading domains"
for d in domains:
	newDomain = session.query(EnvDomains).filter_by(domain_name = d['domain_name']).first()
	if newDomain:
		newDomain.wfs_name = d['wfs_name']
	else:
		newDomain = EnvDomains(domain_name = d['domain_name'], wfs_name = d['wfs_name'])
	session.add(newDomain)
	session.commit()

print "Loading WaterML2 interpolation types."
for wml_int in wml_interpolation_type:
	newInterpolationType = session.query(WmlInterpolationType).filter_by(interpolation_type = wml_int['interpolation_type']).first()
	if newInterpolationType:
		newInterpolationType.interpolation_type_url = wml_int['interpolation_type_url']
	else:
		newInterpolationType = WmlInterpolationType(interpolation_type = wml_int['interpolation_type'], interpolation_type_url = wml_int['interpolation_type_url'])
	session.add(newInterpolationType)
	session.commit()

print "Loading parameters"
for p in params:
	tempInt = session.query(WmlInterpolationType).filter_by(interpolation_type = p['interpolation_type']).first()
	newParam = session.query(Parameters).filter_by(name = p['name']).first()
	if newParam:
		newParam.interpolation_type = tempInt
		newParam.uom = p['uom']
		newParam.parameter_url = p['parameter_url']
	else:
		newParam = Parameters(name = p['name'], interpolation_type = tempInt, uom = p['uom'], parameter_url = p['parameter_url'])
	session.add(newParam)
	session.commit()

print "Loading agency time series server details"
for ats in agency_ts:
	temp_agency = session.query(Agency).filter_by(name=ats['agency']).first()
	temp_ts_server = session.query(TsServerTypes).filter_by(server_type = ats['tsType']).first()
	temp_domain = session.query(EnvDomains).filter_by(domain_name = ats['domain']).first()
	newAgencyTs = session.query(AgencyTimeSeries).join(Agency).join(EnvDomains).join(TsServerTypes).filter(EnvDomains.domain_name == ats['domain'], Agency.name == ats['agency']).first()
	if newAgencyTs:
		newAgencyTs.timeseries_url = ats['url']
		newAgencyTs.ts_type_id = temp_ts_server.id #need to check this works correctly
	else:
		newAgencyTs = AgencyTimeSeries(timeseries_url = ats['url'], agency = temp_agency, domain_name = temp_domain, ts_server_type = temp_ts_server)
	session.add(newAgencyTs)
	session.commit()

print "Loading agency parameter names."
for ap in agency_params:
	temp_agency = session.query(Agency).filter_by(name=ap['agency']).first()
	temp_param = session.query(Parameters).filter_by(name = ap['parameter']).first()
	newAgencyParam = session.query(AgencyParameters).join(Agency).join(Parameters).filter(Agency.name == ap['agency'], Parameters.name == ap['parameter']).first()
	if newAgencyParam:
		newAgencyParam.agency_parameter_name = ap['agencyParam']
	else:
		newAgencyParam = AgencyParameters(agency_parameter_name = ap['agencyParam'], agency = temp_agency, parameter = temp_param)
	session.add(newAgencyParam)
	session.commit()

print "Loading domain parameter relationships."
for dp in domain_params:
	temp_domain = session.query(EnvDomains).filter_by(domain_name = dp['domain_name']).first()
	temp_param = session.query(Parameters).filter_by(name = dp['parameter']).first()
	newDomainParam = session.query(DomainParameters).join(EnvDomains).join(Parameters).filter(EnvDomains.domain_name == dp['domain_name'], Parameters.name == dp['parameter']).first()
	if newDomainParam == None:
		newDomainParam = DomainParameters(domain_name = temp_domain, parameter = temp_param)
	session.add(newDomainParam)
	session.commit()



print "Loading time series server interpolation types."
for ts_server_int in ts_server_interpolation:
	temp_server_type = session.query(TsServerTypes).filter_by(server_type = ts_server_int['ts_server_type']).first()
	temp_interp_type = session.query(WmlInterpolationType).filter_by(interpolation_type = ts_server_int['interpolation_type']).first()
	newTsServerInterpolation = session.query(TsServerTypeInterpolation).join(TsServerTypes).join(WmlInterpolationType).filter(TsServerTypes.server_type == ts_server_int['ts_server_type'], WmlInterpolationType.interpolation_type == ts_server_int['ts_server_interpolation']).first()
	if newTsServerInterpolation:
		newTsServerInterpolation.ts_server_interpolation = ts_server_int['ts_server_interpolation']
	else:
		newTsServerInterpolation = TsServerTypeInterpolation(ts_server_type = temp_server_type, ts_server_interpolation = ts_server_int['ts_server_interpolation'], interpolation_type = temp_interp_type)
	session.add(newTsServerInterpolation)
	session.commit()


print "Loading procedures."
for proc in procedures:
	newProcedure = session.query(Procedures).filter_by(name = proc['name']).first()
	if newProcedure:
		newProcedure.description = proc['description']
	else:
		newProcedure = Procedures(name=proc['name'], description=proc['description'])
	session.add(newProcedure)
	session.commit()

print "Loading Time Series Procedure Calls."
for ts_proc_call in ts_procedure_calls:
	temp_server_type = session.query(TsServerTypes).filter_by(server_type = ts_proc_call['server_type']).first()
	temp_proc_type = session.query(Procedures).filter_by(name = ts_proc_call['name']).first()
	newTsServerProcedureCall = session.query(TsServerProcedureCall).join(TsServerTypes).join(Procedures).filter(TsServerTypes.server_type == ts_proc_call['server_type'], Procedures.name == ts_proc_call['name']).first()
	if newTsServerProcedureCall:
		newTsServerProcedureCall.ts_server_procedure_call = ts_proc_call['call']
	else:
		newTsServerProcedureCall = TsServerProcedureCall(ts_server_type = temp_server_type, ts_server_procedure_call = ts_proc_call['call'], procedure_name = temp_proc_type)
	session.add(newTsServerProcedureCall)
	session.commit()