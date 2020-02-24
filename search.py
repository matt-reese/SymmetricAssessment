import pandas as pd

def get_descriptions(dataframe):
    catalog_number = dataframe['device_identifier'].head(1)
    device_description = dataframe['deviceDescription'].head(1)
    licence_name = dataframe['licence_name'].head(1)

    print('Catalog number: ' + str(catalog_number).replace((str(catalog_number.index[0]) + '    '), '').replace('Name: device_identifier, dtype: object',''))
    print('GUDID Description: ' + str(device_description).replace((str(device_description.index[0]) + '    '), '').replace('Name: deviceDescription, dtype: object',''))
    print('MDALL Description: ' + str(licence_name).replace((str(licence_name.index[0]) + '    '), '').replace('Name: licence_name, dtype: object',''))

catalog_number = input('Search for a catalog (blank for a random example, exit to exit): ')
if catalog_number == 'exit':
    exit()
else:
    aligned_df = pd.read_csv('aligned_data.csv', low_memory=False).astype(str)
    if catalog_number:
        series = aligned_df.loc[(aligned_df['device_identifier'] == catalog_number)]
        get_descriptions(series)
    else:
        aligned_df_sample = aligned_df.sample(n=1)
        get_descriptions(aligned_df_sample)
