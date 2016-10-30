import urllib
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

ns = {
    'emar': 'http://www.lawa.org.nz/emar',
    'gml': 'http://www.opengis.net/gml'
}

#siteattrib = {}

wfsurl = 'https://hbrcwebmap.hbrc.govt.nz/arcgis/services/emar/MonitoringSiteReferenceData/MapServer/WFSServer?request=GetFeature&service=WFS&typename=MonitoringSiteReferenceData&srsName=urn:ogc:def:crs:EPSG:6.9:4326&Version=1.1.0'

def emarWfsRead(wfsurl):
    """Parse an EMAR MonitoringSItesReferenceData WFS and return a dictionary """

    xmldata = urllib.urlopen(wfsurl)

    sites = ET.parse(xmldata)
    #tree = ET.ElementTree(xmldata)

    root = sites.getroot()

    sitelist = []

    for child in root:
        for elem in child:
            if elem.tag == '{http://www.lawa.org.nz/emar}MonitoringSiteReferenceData':
                siteattrib = {}
                for e in elem:
                    tagname = e.tag.replace('{http://www.lawa.org.nz/emar}', '')
                    if tagname.upper() == 'SHAPE':
                        for a in e:
                            siteattrib['Shape'] = a.tag.replace('{http://www.opengis.net/gml}', '')
                            for s in a:
                                siteattrib['latlong'] = s.text
                                latlng = s.text.split()
                                siteattrib['latitude'] = latlng[0]
                                siteattrib['longitude'] = latlng[1]
                                
                    else:
                        siteattrib[tagname.lower()] = e.text
                sitelist.append(siteattrib)
            else:
                siteattrib = {}
            

    return sitelist  