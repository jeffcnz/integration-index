
def oldjsonSite(site):

	return {
            'National ID' : site[0].national_id,
            'Site Name' : site[0].site_name,
            'Agency ID' : site[0].agency_id,
            'latitude' : site[0].latitude,
            'longitude' : site[0].longitude,
            'Agency Name': site[1].name,
            'Offering': site[2].domain_name
        }


def jsonSite(sites):
	out = []
	for s in sites:
		index = [i for i,o in enumerate(out) if o["National ID"] == s[0].national_id]
		#temp = first(o for o in out if o["National ID"] == s[0].national_id)
		if index:
			if [s[2].domain_name] not in out[index[0]]["Offering"]:
				out[index[0]]["Offering"].append(s[2].domain_name)
				#print out[index[0]]["Offering"]
				#print s[2].domain_name
			#o[index[0]]["Offering"].append(s[2]["domain_name"])
		else:
			out.append({
            'National ID' : s[0].national_id,
            'Site Name' : s[0].site_name,
            'Agency ID' : s[0].agency_id,
            'latitude' : s[0].latitude,
            'longitude' : s[0].longitude,
            'Agency Name': s[1].name,
            'Offering': [s[2].domain_name]
        })
	
	return out


def geoJsonSite(sites):
	out = []
	for s in sites:
		if out:
			index = [i for i,o in enumerate(out) if o["properties"]["National_ID"] == s[0].national_id]
			#temp = first(o for o in out if o["National ID"] == s[0].national_id)
		else:
			index=[]
		if index:
			if [s[2].domain_name] not in out[index[0]]["properties"]["Offering"]:
				out[index[0]]["properties"]["Offering"].append(s[2].domain_name)
				#print out[index[0]]["Offering"]
				#print s[2].domain_name
				#o[index[0]]["Offering"].append(s[2]["domain_name"])
		else:
			out.append({
  				"type": "Feature",
  				"geometry": {
    				"type": "Point",
    				"coordinates": [s[0].longitude, s[0].latitude]
  					},
  				"properties": {
    				"National_ID" : s[0].national_id,
            		"Site_Name" : s[0].site_name,
            		"Agency_ID" : s[0].agency_id,
            		"Agency_Name": s[1].name,
            		"Offering": [s[2].domain_name]
  				}
			})
	
	return {"type": "FeatureCollection",
    		"features": out}

	

def jsonTs(data, foi, parameter, procedure, time):
	"""Converts the supplied data into a JSON string according to the OGC O&M draft encoding standard.

	Output attempts to conform with the Requirements Class for Observation data"""
	outJson = []
	points = []
	#print data[1]
	for tvp in data[1]:
		#print tvp
		points.append({
			"time":{
				"instant": tvp["time"]
			},
			"value": tvp["value"]
			})

	outJson.append({
		"id": foi + " " + parameter + " " + procedure,
		"type": "TimeSeriesObservation",
		"phenomenonTime": {
			"interval": {
				"begin": data[1][0]["time"], 
				"end": data[1][-1]["time"]
				}
		},
		"observedProperty": {"href": "http://localhost:5000/parameters/" + parameter},
		"procedure": {"href": "http://localhost:5000/procedures/" + procedure},
		"featureOfInterest": {"href": "http://localhost:5000/sites/" + foi},
		"resultTime": {"instant": time},
		"defaultPointMetadata":{
			"interpolationType":{
				"term": data[2].interpolation_type,
				"vocabulary": data[2].interpolation_type_url
			},
			"uom": data[0]["uom"]
		},
		"result": points
		})
	#print outJson
	return outJson


