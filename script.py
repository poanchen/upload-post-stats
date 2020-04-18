execfile('config.py')

# Get the XML
import requests, datetime
print 'Beginning to get the XML file...'
print 'Starting time: %s' % datetime.datetime.now()
r = requests.get(config['xml_url'])
print 'Finished to get the XML file'
print 'Ending time: %s' % datetime.datetime.now()

# Extract relative blog posts link from the XML
print 'Beginning to extract relative blog posts link from the XML file...'
print 'Starting time: %s' % datetime.datetime.now()
import xml.etree.ElementTree as ET, re
root = ET.fromstring(r.content)
links = []
for child in root:
  match = re.match('https://poanchen\.github\.io(/blog/[0-9]{4}/[0-9]{2}/[0-9]{2}/.+)', child[0].text)
  if match:
    links.append(match.group(1))
print 'Finished to extract relative blog posts link from the XML file'
print 'Ending time: %s' % datetime.datetime.now()

# Get the all time views for all the posts from Google's Core Reporting API
import helper
print 'Beginning to extract relative blog posts link from the XML file...'
print 'Starting time: %s' % datetime.datetime.now()
core_reporting_api_service = helper.get_core_reporting_api_service()
data = {}
for link in links:
  data[link] = core_reporting_api_service.data().ga().get(
                ids='ga:' + helper.get_the_first_profile_id(core_reporting_api_service),
                start_date=config['views_start_date'],
                end_date=config['views_end_date'] ,
                metrics='ga:pageviews',
                filters='ga:pagepath==%s' % (link)).execute().get('totalsForAllResults').get('ga:pageviews')
print 'Finished to extract relative blog posts link from the XML file...'
print 'Ending time: %s' % datetime.datetime.now()

# Convert dict to JSON file
import json
print 'Beginning to convert dict to JSON file...'
print 'Starting time: %s' % datetime.datetime.now()
open(config['json_file_name'], 'wb').write(json.dumps(data))
print 'Finished to convert dict to JSON file'
print 'Ending time: %s' % datetime.datetime.now()

# Upload it to the Azure Blob Storage
from azure.storage.blob import BlockBlobService
print 'Beginning to upload the JSON file...'
print 'Starting time: %s' % datetime.datetime.now()
blob_service = BlockBlobService(config['account_name'], config['account_key'])
full_path_to_file = config['absolute_path_to_this_project'] +\
  config['json_file_name']
blob_service.create_blob_from_path(
  config['container_name'],
  config['json_file_name'],
  full_path_to_file)
print 'Finished to upload the JSON file'
print 'Ending time: %s' % datetime.datetime.now()
