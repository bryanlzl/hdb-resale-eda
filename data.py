#%%
import os
import pandas as pd
pd.options.display.max_columns = 10
pd.options.display.width = 200

#%%

''' Reading Resale Data and Cleaning '''

resale_filenames = ['ResaleFlatPricesBasedonApprovalDate19901999.csv',
                    'ResaleFlatPricesBasedonApprovalDate2000Feb2012.csv',
                    'ResaleFlatPricesBasedonRegistrationDateFromMar2012toDec2014.csv',
                    'ResaleFlatPricesBasedonRegistrationDateFromJan2015toDec2016.csv',
                    'ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv']

hdb_resales = pd.DataFrame()

# Concatenating all time periods
for file in resale_filenames:
    df = pd.read_csv(file)
    hdb_resales = pd.concat([hdb_resales, df], ignore_index=True)

# Cleaning functions
def clean_remaining_lease(row):
    return row['lease_commence_date'] + 99 - row['year']

def clean_storey_range(x):
    # input is from hdb_resales['storey_range']
    a,b,c = x.split()
    return (int(a)+int(c))//2

def add_flat_type_group(x):
    # input is from hdb_resales['flat_type']
    if x in ['1 ROOM', '2 ROOM']:
        group = 'Small' 
    elif x in ['5 ROOM', 'EXECUTIVE', 'MULTI-GENERATION']:
        group = 'Big'
    else:
        group = x
    return group

def add_region(x):
    # input is from hdb_resales['town']
    if x in ['BISHAN', 'BUKIT MERAH', 'BUKIT TIMAH', 'CENTRAL AREA', 'GEYLANG',
             'KALLANG/WHAMPOA', 'MARINE PARADE', 'QUEENSTOWN', 'TOA PAYOH']:
        region = 'Central'
    elif x in ['BUKIT BATOK', 'BUKIT PANJANG', 'CHOA CHU KANG', 'JURONG EAST', 
               'JURONG WEST']:
        region = 'West'
    elif x in ['LIM CHU KANG', 'SEMBAWANG', 'WOODLANDS', 'YISHUN']:
        region = 'North'
    elif x in ['ANG MO KIO', 'HOUGANG', 'PUNGGOL', 'SENGKANG', 'SERANGOON']:
        region = 'Northeast'
    elif x in ['BEDOK', 'CLEMENTI', 'PASIR RIS', 'TAMPINES']:
        region = 'East'
    else: 
        region = ''
    return region


# Adding year and date
hdb_resales = hdb_resales.rename(columns={'month': 'date'})
hdb_resales.insert(0, 'year', hdb_resales['date'].apply(lambda x: int(x[:4])))

# Cleaning existing columns
hdb_resales['flat_type'] = hdb_resales['flat_type'].str.replace('MULTI GENERATION', 'MULTI-GENERATION')
hdb_resales['flat_model'] = hdb_resales['flat_model'].str.upper()
hdb_resales['remaining_lease'] = hdb_resales.apply(clean_remaining_lease, axis=1)
hdb_resales['storey_range'] = hdb_resales['storey_range'].apply(clean_storey_range)

# Adding new columns
hdb_resales['flat_type_group'] = hdb_resales['flat_type'].apply(add_flat_type_group)
hdb_resales['region'] = hdb_resales['town'].apply(add_region)
hdb_resales['price/sqm'] = hdb_resales['resale_price'] / hdb_resales['floor_area_sqm']

# Sorting (can change category)
hdb_resales = hdb_resales.sort_values(by='flat_type')
# hdb_resales

#%%
''' Reading Rental Data and Cleaning '''

hdb_rentals = pd.read_csv('RentingOutofFlats.csv')
hdb_rentals['flat_type_group'] = hdb_rentals['flat_type'].apply(add_flat_type_group)
hdb_rentals['region'] = hdb_rentals['town'].apply(add_region)
hdb_rentals = hdb_rentals.rename(columns={'rent_approval_date':'date'})
# hdb_rentals


#%%
''' Descriptive Stats '''
# Set to True to print this section
print1 = False

if print1:
    for i, df in enumerate([hdb_resales, hdb_rentals]):
        print(f'DATA FOR {"RESALES" if i==0 else "RENTALS"}-----------')
        print('Missing Data')
        print(df.isna().sum())      # No NAs in data o.o
        print()
        
        print('Numerical Values')
        print(df.describe())
        print()
        
        print('Categorical Values')
        for col in ['town', 'flat_type', 'flat_model', 'flat_type_group', 'region']:
            print()
            try:
                print(df[col].value_counts())
            except:
                pass
        print()

# print(hdb_resales.dtypes)


#%%
## Have to set a year cutoff to separate recent data from old data
## to try to adjust for inflation.

year_cutoff = 2015

old_resales = hdb_resales[hdb_resales['year'] <= year_cutoff]
new_resales = hdb_resales[hdb_resales['year'] > year_cutoff]

hdb_resales.to_csv('hdb_resales.csv', index=False)
old_resales.to_csv('old_resales.csv', index=False)
new_resales.to_csv('new_resales.csv', index=False)

hdb_rentals.to_csv('hdb_rentals.csv', index=False)


#%% For location mapping data

hdb_locations = pd.read_csv("sg_zipcode_mapper_updated.csv")
hdb_resales = pd.read_csv('hdb_resales.csv')
# hdb_mapping = pd.read_csv('hdb_mapping.csv').dropna()

hdb_mapping = pd.merge(hdb_resales, hdb_locations, how='left', left_on=['block', 'street_name'], right_on=['block', 'street_name'])

# hdb_mapping = hdb_mapping.pivot_table(index=['block', 'street_name'], columns='year', values='price/sqm', aggfunc='mean')

# # Flatten the MultiIndex columns
# hdb_mapping.columns = [f'{col[0]}_{col[1]}' for col in hdb_mapping.columns]

# # Reset index to make 'block' and 'street_name' regular columns
# hdb_mapping.reset_index(inplace=True)


# # hdb_resales['region'] = hdb_resales['town'].apply(add_region)
# hdb_mapping = hdb_mapping[hdb_mapping['price/sqm'].notna()]
# hdb_mapping.drop(['town'], axis=1)
# hdb_mapping.to_csv('hdb_mapping2.csv', index=True)
hdb_mapping.to_csv('hdb_mapping.csv', index=False)
# # hdb_locations.to_csv("sg_zipcode_mapper_updated.csv", index=False)

#%%
