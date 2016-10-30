from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings

from database_setup import Base, Agency, AgencyWfs, MonitoringSites, SiteDomains, EnvDomains

from wfs_read import emarWfsRead

engine = create_engine(settings.db_connection)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()




def missingCheck(key, dict):
	if key in dict:
		return dict[key]
	else:
		return None

wfsUrl = session.query(AgencyWfs).all()
error = 0

for w in wfsUrl:
	url = w.sites_url#w['sites_url'] 
	print "Reading " + url
	sitesinfo = emarWfsRead(url)
	print str(len(sitesinfo)) + " Sites in WFS"
	for site in sitesinfo:
		#print site['CouncilSiteID']
		domains = session.query(EnvDomains).all()
		tempagency = session.query(Agency).filter_by(name=site['agency']).first()
		newSite = session.query(MonitoringSites).filter_by(national_id = site['lawasiteid']).first()
		site_id = missingCheck('councilsiteid', site)
		if site_id:
			#site_id = missingCheck('SiteID', site)
			if newSite != None:
				#update
				
				newSite.site_name = site_id
				newSite.agency = tempagency
				newSite.latlng = missingCheck('latlong', site)
				newSite.latitude = missingCheck('latitude', site)
				newSite.longitude = missingCheck('longitude', site)
				newSite.sw_zone = missingCheck('swmanagementzone', site)
				newSite.gw_zone = missingCheck('gwmanagementzone', site)
				newSite.catchment = missingCheck('catchment', site)
				newSite.region = missingCheck('region', site)
				newSite.description = missingCheck('description', site)
				newSite.photo_url = missingCheck('photo', site)
				newSite.lfenzid = missingCheck('lfenzid', site)
				newSite.lake_type = missingCheck('ltype', site)
				newSite.surface_wq_altitude_class = missingCheck('swqaltitude', site)
				newSite.surface_wq_freq = missingCheck('swqfrequencyall', site)
				newSite.surface_wq_freq_5y = missingCheck('swqfrequencylast5', site)
				newSite.surface_wq_landuse = missingCheck('swqlanduse', site)
				
				session.add(newSite)
				session.commit()
				for domain in domains:
					tempSite = session.query(MonitoringSites).filter_by(national_id='lawasiteid').first()
					#check site domains for a record
					tempsitedomain = session.query(SiteDomains).join(EnvDomains).join(MonitoringSites).filter((MonitoringSites.national_id == site['lawasiteid']), (EnvDomains.domain_name == domain.domain_name)).first()
					if tempsitedomain != None:
						#there is a record
						if site[domain.wfs_name.lower()].lower() == "no":
							#there is a record and there shouldn't be so delete
							session.delete(tempsitedomain)
							session.commit
					else:
						#no record, check if there should be
						if site[domain.wfs_name.lower()].lower() == "yes":
							newSiteDomain = SiteDomains(
								site_nat_id = tempSite, 
								domain_id = domain.id)
							session.add(newSiteDomain)
							session.commit()
					

			else:
				newSite = MonitoringSites(
					national_id = missingCheck('lawasiteid', site),
					site_name = site_id,
					agency = tempagency,
					latlng = missingCheck('latlong', site),
					latitude = missingCheck('latitude', site),
					longitude = missingCheck('longitude', site),
					sw_zone = missingCheck('swmanagementzone', site),
					gw_zone = missingCheck('gwmanagementzone', site),
					catchment = missingCheck('catchment', site),
					region = missingCheck('region', site),
					description = missingCheck('description', site),
					photo_url = missingCheck('photo', site),
					lfenzid = missingCheck('lfenzid', site),
					lake_type = missingCheck('ltype', site),
					surface_wq_altitude_class = missingCheck('swqaltitude', site),
					surface_wq_freq = missingCheck('swqfrequencyall', site),
					surface_wq_freq_5y = missingCheck('swqfrequencylast5', site),
					surface_wq_landuse = missingCheck('swqlanduse', site))
					
				session.add(newSite)
				session.commit()
				for domain in domains:
					#check if there should be a record
					if site[domain.wfs_name.lower()].lower() == "yes":
						tempSite = session.query(MonitoringSites).filter_by(national_id = site['lawasiteid']).first()
						newSiteDomain = SiteDomains(
							site_id = tempSite.id,
							domain_id = domain.id)
						session.add(newSiteDomain)
						session.commit()
		else:
			error += 1

	print str(error) + " Sites not imported"
		

			