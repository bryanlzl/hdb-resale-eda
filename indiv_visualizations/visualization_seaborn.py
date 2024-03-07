import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

hdb_resales = pd.read_csv('hdb_resales.csv')
new_resales = pd.read_csv('new_resales.csv')
old_resales = pd.read_csv('old_resales.csv')
hdb_rentals = pd.read_csv('hdb_rentals.csv')

year_cutoff = 2015      # Have to be in line with data.py

for df in [hdb_resales, new_resales, old_resales, hdb_rentals]:
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m')
    
    df['region'] = pd.Categorical(df['region'], 
        categories = ['Central', 'Northeast', 'East', 'West', 'North'])
    
    df['flat_type'] = pd.Categorical(df['flat_type'],
        categories = sorted(df['flat_type'].unique()))
    # Coincidentally flat type in alphabetical order is also in increasing size order
    
    df['flat_type_group'] = pd.Categorical(df['flat_type_group'],
        categories = ['Small', '3 ROOM', '4 ROOM', 'Big'])
    

#%%
'''Plotting price/sqm over the years'''
# sns.scatterplot(data=hdb_resales, x='year', y='price/sqm', hue='flat_type').set(
#     title='Inflation')
# plt.legend(loc='upper left')
# plt.show()

sns.displot(data=hdb_resales, x='date', y='price/sqm', row='flat_type_group', 
            hue='flat_type', aspect=3, 
            hue_order=hdb_resales['flat_type'].value_counts().index)
plt.show()

## Increasing price and price variance over the years for all flat types
## Some local highs at 1997 (Asian Financial Crisis) and 2013 (Cooling measures)
## A marked pickup in prices post 2020 (Covid)


#%%
''' Does Flat Type affect price/sqm? '''

# First checking distribution of area for each flat type
sns.boxplot(hdb_resales, x='flat_type', y='floor_area_sqm').set(
    title='Distribution of house area for each flat type')
plt.xticks(rotation=15)
plt.show()

## 3 room flats have large positive outliers due to luxury 3 room apartments
## Those are mostly ground floor or penthouse apartments with large balconies/patios


# Spltting by old and new resales
sns.boxplot(data=old_resales, x='flat_type', y='price/sqm').set(
    title=f'HDB Resales before {year_cutoff}')
plt.xticks(rotation=15)
plt.show()

sns.boxplot(data=new_resales, x='flat_type', y='price/sqm').set(
    title=f'HDB Resales after {year_cutoff}')
plt.xticks(rotation=15)
plt.show()

## Price/sqm largely invariant across flat types, although an interesting reversal of trend
## before and after 2015. Use a time slider to visualize this.


# Further breakdown by flat_model, not very insightful
category = 'flat_model'
sort_category = new_resales.groupby(by=category)['price/sqm'].mean()
sort_category.sort_values(inplace=True)
new_resales[category] = pd.Categorical(new_resales[category], categories=list(sort_category.index))

sns.displot(data=new_resales.sort_values(by=category), x='flat_model', y='price/sqm', row='flat_type_group', 
            aspect=3)
plt.xticks(rotation=90)
plt.show()


# Rentals
hdb_rentals.sort_values(by='flat_type', inplace=True)

sns.boxplot(data=hdb_rentals, x='flat_type', y='monthly_rent').set(
    title='HDB Rental Prices (2021-2023)')
plt.show()
## Generally increasing rental with size as expected



#%%
''' Plotting Price/sqm against Remaining Lease '''

# sns.scatterplot(data=new_resales, x='remaining_lease', y='price/sqm', hue='flat_type_group',
#     hue_order=new_resales['flat_type_group'].value_counts().index).set(
#     title=f'Price vs Remaining Lease after {year_cutoff}')
# plt.legend(loc='lower right')

sns.displot(data=new_resales, x='remaining_lease', y='price/sqm', row='flat_type_group', aspect=3)
plt.show()

## Generally increasing trend as expected, although seems to taper off when remaining lease reaches ~80 years
## Can use scatterplot for streamlit, for static graph displot seems better



#%%
''' Distribution of prices across different regions '''

new_resales.sort_values(by=['region', 'town'], inplace=True)

sns.boxplot(data=new_resales, x='town', y='price/sqm', hue='region', dodge=False).set(
    title=f'HDB Resales after {year_cutoff}')
plt.legend(bbox_to_anchor=(1.02, 0.65))
plt.xticks(rotation=90)
plt.show()

## Central areas are more expensive than the rest due to accessibility to work
## The remaining residential areas have less variance, slight differences might be 
## due to popularity/access to amenities, airport. 


hdb_rentals.sort_values(by=['region', 'town'], inplace=True)

sns.boxplot(data=hdb_rentals, x='town', y='monthly_rent', hue='region', dodge=False).set(
    title='HDB Rental Prices (2021-2023)')
plt.legend(bbox_to_anchor=(1.02, 0.65))
plt.xticks(rotation=90)
plt.show()

## Surprisingly, rentals are quite invariant across regions. Not sure why



#%%
''' Plotting price/sqm vs storey range '''

sns.scatterplot(data=new_resales, x='storey_range', y='price/sqm', hue='flat_type_group').set(
    title=f'Resales after {year_cutoff}')
plt.legend(loc='lower left')
plt.show()

## Quite interesting: price does increase with height generally but not by much if below 40


#%%
''' Distribution of flat types across towns '''

sns.displot(data=new_resales, y='town', x='flat_type', hue='region')
plt.xticks(rotation=45)
plt.show()

# Not super insightful but good to know 



#%%
''' Correlations and plots for regression '''

regression_columns = ['year', 'town', 'flat_type', 'storey_range', 'flat_model', 
                      'remaining_lease', 'flat_type_group', 'region', 'price/sqm']
sns.heatmap(new_resales[regression_columns].corr(numeric_only=True), vmin=-1, vmax=1, annot=True)
sns.pairplot(new_resales[regression_columns])

#%%
''' Regression '''

pd.options.display.max_columns = 20
new_resales_reg = new_resales.drop(columns=['date','block','town','street_name',
    'flat_model','floor_area_sqm','lease_commence_date','resale_price','flat_type_group'])
pd.get_dummies(new_resales_reg).columns




