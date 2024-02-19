import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

os.chdir('C:\\Users\\user\\Desktop\\IT5006 Project')

hdb_resales = pd.read_csv('hdb_resales.csv')
new_resales = pd.read_csv('new_resales.csv')
old_resales = pd.read_csv('old_resales.csv')
hdb_rentals = pd.read_csv('hdb_rentals.csv')

year_cutoff = 2015      # Have to be in line with data.py

for df in [hdb_resales, new_resales, old_resales, hdb_rentals]:
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m')
    df['region'] = pd.Categorical(df['region'], 
        categories=['Central', 'Northeast', 'East', 'West', 'North'])



#%%
'''Plotting price/sqm over the years'''
# sns.scatterplot(data=hdb_resales, x='year', y='price/sqm', hue='flat_type').set(
#     title='Inflation')
# plt.legend(loc='upper left')
# plt.show()

sns.displot(data=hdb_resales, x='date', y='price/sqm', row='flat_type_group', 
            hue='flat_type', aspect=3, 
            hue_order=hdb_resales['flat_type'].value_counts().index)



#%%
''' Does Flat Type affect price/sqm? '''

# First checking distribution of area for each flat type
sns.boxplot(hdb_resales, x='flat_type', y='floor_area_sqm').set(
    title='Distribution of house area for each flat type')
plt.xticks(rotation=15)
plt.show()

# Spltting by old and new resales
sns.boxplot(data=old_resales, x='flat_type', y='price/sqm').set(
    title=f'HDB Resales before {year_cutoff}')
plt.xticks(rotation=15)
plt.show()

sns.boxplot(data=new_resales, x='flat_type', y='price/sqm').set(
    title=f'HDB Resales after {year_cutoff}')
plt.xticks(rotation=15)
plt.show()

## Very interesting reversal of trend in recent years. Before 2010 there is increasing premium 
## to a bigger house, nowadays there is a slight premium to small houses.


#%%
''' Plotting Price/sqm against Remaining Lease '''

sns.scatterplot(data=new_resales, x='remaining_lease', y='price/sqm', hue='flat_type_group',
                hue_order=new_resales['flat_type_group'].value_counts().index).set(
    title=f'Price vs Remaining Lease after {year_cutoff}')
plt.legend(loc='lower right')
plt.show()


#%%
''' Distribution of prices across different regions '''
sns.boxplot(data=new_resales.sort_values(by=['region', 'town']), x='town', 
                 y='price/sqm', hue='region', dodge=False).set(
    title=f'HDB Resales after {year_cutoff}')
plt.legend(bbox_to_anchor=(1.02, 0.65))
plt.xticks(rotation=90)
plt.show()

sns.boxplot(data=hdb_rentals.sort_values(by=['region', 'town']), x='town', 
                 y='monthly_rent', hue='region', dodge=False).set(
    title='HDB Rental Prices (2021-2023)')
plt.legend(bbox_to_anchor=(1.02, 0.65))
plt.xticks(rotation=90)
plt.show()



#%%
''' Plotting price/sqm vs storey range '''

sns.scatterplot(data=new_resales, x='storey_range', y='price/sqm', hue='flat_type_group').set(
    title=f'Resales after {year_cutoff}')
plt.legend(loc='lower left')
plt.show()

## Quite interesting: price does increase with height generally but not by much if below 40

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




