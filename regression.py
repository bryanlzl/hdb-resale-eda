import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
# import matplotlib.pyplot as plt

current_year = 2024

new_resales = pd.read_csv('new_resales.csv')
hdb_rentals = pd.read_csv('hdb_rentals.csv')

regression_columns = ['year', 'flat_type', 'storey_range', 'town',
                      'remaining_lease', 'resale_price', 'floor_area_sqm']

#%%
''' Checking for hints of multicollinearity '''

new_resales_reg = new_resales[regression_columns]

sns.heatmap(new_resales_reg.corr(numeric_only=True), vmin=-1, vmax=1, annot=True)
sns.pairplot(new_resales_reg)

## There is slight positive correlation between storey range and remaining lease actually.
## Probably due to newer flats having higher floors. 
## Probably not big enough to cause multicollinearity issues.


#%%
''' Pre-Regression Cleaning '''

# Rename some columns to get smf.ols to read x variables properly
original_col = pd.get_dummies(new_resales_reg).columns
new_resales_reg = pd.get_dummies(new_resales_reg, drop_first=True)
dummy_var = set(original_col) - set(new_resales_reg.columns)

new_resales_reg.columns = new_resales_reg.columns.str.replace(' ','_')
new_resales_reg.rename(columns={'price/sqm':'Price_per_sqm',
                                'town_KALLANG/WHAMPOA':'town_KALLANG_WHAMPOA',
                                'flat_type_MULTI-GENERATION':'flat_type_MULTI_GENERATION'},
                       inplace=True)

# Subtract year by 2024 to simplify analysis of coefficients
new_resales_reg['year'] = new_resales_reg['year'] - 2024


''' Regression '''

x_variables = list(new_resales_reg.columns)
y_variable = 'resale_price'

try: x_variables.remove(y_variable)
except ValueError: pass

# Exporting the correlation matrix, too large to visualize
new_resales_reg[x_variables].corr().to_csv('correl.csv')

linear_model = smf.ols(data=new_resales_reg, formula=f'np.log({y_variable}) ~ {"+".join(x_variables)}').fit()
print(linear_model.summary())
print(f'Dummy Variables: {dummy_var}')

#%%

#%%

#%%

#%%

#%%