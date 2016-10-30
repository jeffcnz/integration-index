import urllib
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def AgencyUrl(server_type, agency_ts_url, agency_site, agency_parameter, procedure, time_period):
    #return a request url and the server type (for later processing the returned xml)
    if server_type == "Hilltop":
        proc = ""
        if time_period:

            tFilt = "&TimeInterval=" + time_period.split(",")[1]
        else:
            tFilt = ""
        agency_url = agency_ts_url + "?Service=Hilltop&Request=GetData&Site=" + agency_site + "&Measurement=" + agency_parameter + procedure + tFilt
        return agency_url, server_type

    elif "Kisters" in server_type:
        if time_period:
            tFilt = "&TemporalFilter=" + time_period
        else:
            tFilt = ""
        agency_url = agency_ts_url + "?service=SOS&version=2.0&request=GetObservation&featureOfInterest=" + agency_site + "&observedProperty=" + agency_parameter + procedure + tFilt
        return agency_url, server_type
    else:
        return "Unmapped server type", "Unknown"




def hilltopTsUrlRead(url):
    tsxml = urllib.urlopen(url)				
    data = ET.parse(tsxml)
    root = data.getroot()
    meta = {}
    series =[]
    m = root.find('Measurement')
    if m:
        ds = m.find('DataSource')
        meta['Interpolation'] = ds.find('Interpolation').text
        meta['DataType'] = ds.find('DataType').text
        meta['uom'] = ds.find('ItemInfo').find('Units').text
        d = m.find('Data')
        
        if meta['DataType'] in ["SimpleTimeSeries", "Rain6"]:
            #Simple time series have a different structure to water quality data
            for tvp in d.findall('E'):
                item = {}
                item['time'] = tvp.find('T').text
                item['value'] = tvp.find('I1').text
                #print item
                series.append(item)
        
        elif meta['DataType'] == "WQData":
            #Parses limited water quality data
            for tvp in d.findall('E'):
                item = {}
                item['time'] = tvp.find('T').text
                item['value'] = tvp.find('Value').text
                try:
                    item['quality'] = tvp.find('QualityCode').text
                except:
                    item['quality'] = None
                #print item
                series.append(item)
        
    return [meta, series]

    
def kistersSosTsUrlToDict(tsurl):
    """Parses a Kisters Server SOS response to a dictionary.
    
    Takes a url and returns a list containing a metadata object and a list of timeseries objects"""
    
    ns = {'sos': 'http://www.opengis.net/sos/2.0',
      'om': 'http://www.opengis.net/om/2.0',
      'wml2': 'http://www.opengis.net/waterml/2.0'}    
    
    tsxml = urllib.urlopen(tsurl)               
    data = ET.parse(tsxml)
    root = data.getroot()

    meta = {}
    series =[]
    m = root.find('sos:observationData', ns)
    if m:
        ds = m.find('om:OM_Observation', ns)
        r = ds.find('om:result', ns).find('wml2:MeasurementTimeseries', ns)
        md = r.find('wml2:defaultPointMetadata', ns).find('wml2:DefaultTVPMeasurementMetadata', ns)
        meta['Interpolation'] = md.find('wml2:interpolationType', ns).attrib['{http://www.w3.org/1999/xlink}title']
        meta['DataType'] = None
        meta['uom'] = md.find('wml2:uom', ns).attrib['code']
              
        
        for tvp in r.findall('wml2:point', ns):
            item = {}
            #May need to check that the time is consistent across servers
            item['time'] = tvp.find('wml2:MeasurementTVP', ns).find('wml2:time', ns).text
            item['value'] = tvp.find('wml2:MeasurementTVP', ns).find('wml2:value', ns).text
            #print item
            series.append(item)
        
    return [meta, series]