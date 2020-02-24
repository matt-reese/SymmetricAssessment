import io
import os
import pandas as pd
import requests
import ssl
import zipfile

# Delete datasets if previously generated
if os.path.exists('gudid_data.csv'):
    os.remove('gudid_data.csv')
if os.path.exists('mdall_data.csv'):
    os.remove('mdall_data.csv')
if os.path.exists('aligned_data.csv'):
    os.remove('aligned_data.csv')

# Get latest full release of GUDID data
request = requests.get("https://accessgudid.nlm.nih.gov/download/delimited")
string = request.text
index = string.find('AccessGUDID_Delimited_Full_Release_')
latest_release = string[index+35:index+43]
latest_gudid_full_release_url = f'https://accessgudid.nlm.nih.gov/release_files/download/AccessGUDID_Delimited_Full_Release_{latest_release}.zip'

# Extract GUDID zipfile's device.txt to current directory
req = requests.get(latest_gudid_full_release_url)
z = zipfile.ZipFile(io.BytesIO(req.content))
z.extract('device.txt')

# Pull catalogNumber, versionModelNumber, and deviceDescription from device.txt into dataframe
gudid_df = pd.read_csv('device.txt', sep='|', usecols=['companyName', 'catalogNumber', 'versionModelNumber', 'deviceDescription'], low_memory=False).astype(str)

# Strip matching columns, and then drop duplicate records
gudid_df['catalogNumber'] = gudid_df['catalogNumber'].str.strip()
gudid_df['versionModelNumber'] = gudid_df['versionModelNumber'].str.strip()
gudid_df = gudid_df.drop_duplicates()

# Create CSV of GUDID data for consumption by other project Python files or a Jupyter notebook
gudid_df.to_csv('gudid_data.csv', index=False)

# Delete device.txt for cleanliness
os.remove('device.txt')

# Create dataframes of relevant MDALL data, and select only relevant columns
device_identifier_columns = ['device_identifier', 'original_licence_no']
licence_columns = ['licence_name', 'original_licence_no', 'company_id']
company_columns = ['company_name', 'company_id']

ssl._create_default_https_context = ssl._create_unverified_context

active_device_identifier_df = pd.read_json('https://health-products.canada.ca/api/medical-devices/deviceidentifier/?state=active&type=json', orient='columns').astype(str)
active_device_identifier_df = active_device_identifier_df[device_identifier_columns]
active_licence_df = pd.read_json('https://health-products.canada.ca/api/medical-devices/licence/?state=active&type=json&lang=en', orient='columns').astype(str)
active_licence_df = active_licence_df[licence_columns]
archived_device_identifier_df = pd.read_json('https://health-products.canada.ca/api/medical-devices/deviceidentifier/?state=archived&type=json', orient='columns').astype(str)
archived_device_identifier_df = archived_device_identifier_df[device_identifier_columns]
archived_licence_df = pd.read_json('https://health-products.canada.ca/api/medical-devices/licence/?state=archived&type=json&lang=en', orient='columns').astype(str)
archived_licence_df = archived_licence_df[licence_columns]
company_df = pd.read_json('https://health-products.canada.ca/api/medical-devices/company/?type=json', orient='columns').astype(str)
company_df = company_df[company_columns]

devices_columns = ['company_id', 'device_identifier', 'licence_name']
active_devices_df = pd.merge(active_device_identifier_df, active_licence_df, left_on='original_licence_no', right_on='original_licence_no', how='inner').astype(str)
active_devices_df = active_devices_df[devices_columns]
archived_devices_df = pd.merge(archived_device_identifier_df, archived_licence_df, left_on='original_licence_no', right_on='original_licence_no', how='inner').astype(str)
archived_devices_df = archived_devices_df[devices_columns]

mdall_final_columns = ['company_name', 'device_identifier', 'licence_name']
mdall_without_company_df = pd.concat([active_devices_df, archived_devices_df], ignore_index=True)
mdall_df = pd.merge(mdall_without_company_df, company_df, left_on='company_id', right_on='company_id', how='left').astype(str)
mdall_df = mdall_df[mdall_final_columns]

# Strip matching column, and then drop duplicate records
mdall_df['device_identifier'] = mdall_df['device_identifier'].str.strip()
mdall_df = mdall_df.drop_duplicates()

# Create CSV of MDALL data for consumption by other project Python files or a Jupyter notebook
mdall_df.to_csv('mdall_data.csv', index=False)

# Join GUDID data with MDALL data
aligned_on_catalog_df = pd.merge(gudid_df, mdall_df, left_on='catalogNumber', right_on='device_identifier', how='inner').astype(str)
aligned_on_version_model_df = pd.merge(gudid_df, mdall_df, left_on='versionModelNumber', right_on='device_identifier', how='inner').astype(str)
aligned_df = pd.concat([aligned_on_catalog_df, aligned_on_version_model_df], ignore_index=True).drop_duplicates().astype(str)

# Create CSV of aligned GUDID and MDALL data for consumption by other project Python files or a Jupyter notebook
aligned_df.to_csv('aligned_data.csv', index=False)
