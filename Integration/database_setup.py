#Setting up database for Integration engine
#Starting with sqlAlchemy
#Jeff Cooke September 2016



import sys
from sqlalchemy import Column, Table, ForeignKey, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import settings

Base = declarative_base()

#Add classes for each table in the database 

class Agency(Base):
    __tablename__ = "agency"
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    details = Column(String(500), nullable = True)
    website = Column(String(200))



class AgencyWfs(Base):
    __tablename__ = "agency_wfs"
    sites_url = Column(String(500), nullable = False)
    id = Column(Integer, primary_key = True)
    agency_id = Column(Integer, ForeignKey("agency.id"))
    agency = relationship(Agency)


class TsServerTypes(Base):
    __tablename__ = "ts_server_types"
    server_type = Column(String(15), nullable = False)
    id = Column(Integer, primary_key = True)
    website = Column(String(100))
    api_doc = Column(String(200))


class WmlInterpolationType(Base):
    __tablename__ = "wml_interpolation_type"
    id = Column(Integer, primary_key = True)
    interpolation_type = Column(String(50), nullable = False)
    interpolation_type_url = Column(String(200), nullable = False)
    

class Parameters(Base):
    __tablename__ = "parameters"
    name = Column(String(40), nullable = False)
    id = Column(Integer, primary_key = True)
    uom = Column(String(20))
    parameter_url = Column(String(200))
    interpolation_id = Column(Integer, ForeignKey("wml_interpolation_type.id"))
    interpolation_type = relationship(WmlInterpolationType)


class EnvDomains(Base):
    __tablename__ = "env_domains"
    domain_name = Column(String(20), nullable = False)
    id = Column(Integer, primary_key = True)
    wfs_name = Column(String(20))
    

class DomainParameters(Base):
    __tablename__ = "domain_parameters"
    id = Column(Integer, primary_key = True)
    env_domains_id = Column(Integer, ForeignKey("env_domains.id"))
    domain_name = relationship(EnvDomains)
    parameters_id = Column(Integer, ForeignKey("parameters.id"))
    parameter = relationship(Parameters)


class AgencyTimeSeries(Base):
    __tablename__ = "agency_time_series"
    timeseries_url = Column(String(100), nullable = False)
    timeseries_id = Column(Integer, primary_key = True)
    agency_id = Column(Integer, ForeignKey("agency.id"))
    agency = relationship(Agency)
    domain_id = Column(Integer, ForeignKey("env_domains.id"))
    domain_name = relationship(EnvDomains)
    ts_type_id = Column(Integer, ForeignKey("ts_server_types.id"))
    ts_server_type = relationship(TsServerTypes)





class AgencyParameters(Base):
    __tablename__ = "agency_parameters"
    agency_parameter_name = Column(String(50), nullable = False)
    id = Column(Integer, primary_key = True)
    parameter_id = Column(Integer, ForeignKey("parameters.id"))
    parameter = relationship(Parameters)
    agency_id = Column(Integer, ForeignKey("agency.id"))
    agency = relationship(Agency)







class MonitoringSites(Base):
    __tablename__ = "monitoring_sites"
    national_id = Column(String(20), nullable = False)
    id = Column(Integer, primary_key = True)
    site_name = Column(String(80), nullable = False)
    agency_id = Column(Integer, ForeignKey("agency.id"))
    agency = relationship(Agency)
    latlng = Column(String(50), nullable = False)
    latitude = Column(Numeric, nullable = False)
    longitude = Column(Numeric, nullable = False)
    sw_zone = Column(String(50))
    gw_zone = Column(String(50))
    catchment = Column(String(50))
    region = Column(String(50))
    description = Column(String(500))
    photo_url = Column(String(200))

    lfenzid = Column(Integer)
    lake_type = Column(String(50))
    surface_wq_altitude_class = Column(String(15))
    surface_wq_freq = Column(String(15))
    surface_wq_freq_5y = Column(String(15))
    surface_wq_landuse = Column(String(15))



    @property
    def serialize(self):
        #returns object data in easy serialisable format

        return {
            'National ID' : self.national_id,
            'Site Name' : self.site_name,
            'Agency ID' : self.agency_id,
            'latitude' : self.latitude,
            'longitude' : self.longitude
        }

class SiteDomains(Base):
    __tablename__ = "site_domains"
    id = Column(Integer, primary_key = True)
    site_id = Column(Integer, ForeignKey("monitoring_sites.id"))
    site_nat_id = relationship(MonitoringSites)
    domain_id = Column(Integer, ForeignKey("env_domains.id"))
    domain_name = relationship(EnvDomains)




class TsServerTypeInterpolation(Base):
    __tablename__ = "ts_server_type_interpolation"
    id = Column(Integer, primary_key = True)
    ts_server_type_id = Column(Integer, ForeignKey("ts_server_types.id"))
    ts_server_type = relationship(TsServerTypes)
    ts_server_interpolation = Column(String(50))
    interpolation_type_id = Column(Integer, ForeignKey("wml_interpolation_type.id"))
    interpolation_type = relationship(WmlInterpolationType)


class Procedures(Base):
    __tablename__ = "procedures"
    id = Column(Integer, primary_key = True)
    name = Column(String(20), nullable = False)
    description = Column(String(200))

class TsServerProcedureCall(Base):
    __tablename__ = "ts_server_procedure_calls"
    id = Column(Integer, primary_key = True)
    ts_server_type_id = Column(Integer, ForeignKey("ts_server_types.id"))
    ts_server_type = relationship(TsServerTypes)
    ts_server_procedure_call = Column(String(100))
    procedure_id = Column(Integer, ForeignKey("procedures.id"))
    procedure_name= relationship(Procedures)


engine = create_engine(settings.db_connection)
if not database_exists(engine.url):
    create_database(engine.url)



Base.metadata.create_all(engine)