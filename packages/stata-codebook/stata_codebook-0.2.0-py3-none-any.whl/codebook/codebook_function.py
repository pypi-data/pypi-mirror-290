import pandas as pd
import numpy as np
from scipy.stats import shapiro, t

def codebook(df, column=None):
    def single_column_codebook(col_data, col_name):
        data = {}
        data['Variable'] = col_name
        data['Type'] = col_data.dtype
        data['Unique values'] = col_data.nunique(dropna=True)  
        data['Missing values'] = col_data.isnull().sum()

        # If the column is numeric, get range, percentiles, and mean values
        if pd.api.types.is_numeric_dtype(col_data):
            data['Range'] = (col_data.min(), col_data.max())
            data['25th percentile'] = col_data.quantile(0.25)
            data['50th percentile (Median)'] = col_data.median()
            data['75th percentile'] = col_data.quantile(0.75)
            data['Mean'] = col_data.mean()
            data['Examples'] = list(col_data.sample(3, random_state=0))
            data['Top categories'] = "-"  
        # If the column is categorical or object type, get examples and the most frequent categories (excluding NaNs)
        elif pd.api.types.is_categorical_dtype(col_data) or col_data.dtype == 'object':
            data['Examples'] = list(col_data.dropna().sample(3, random_state=0))
            top_categories = col_data.value_counts(dropna=True).head(5)  
            data['Top categories'] = dict(top_categories)
            data['Range'] = "-"  
            data['25th percentile'] = "-"
            data['50th percentile (Median)'] = "-"
            data['75th percentile'] = "-"
            data['Mean'] = "-"

        return data

    if column:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in the dataframe.")
        return pd.DataFrame([single_column_codebook(df[column], column)])
    else:
        return pd.DataFrame([single_column_codebook(df[col], col) for col in df.columns])
    

def academic_codebook(df, column=None):
    def single_column_integrated_codebook(col_data, col_name):
        data = {}
        data['Variable'] = col_name
        data['Type'] = col_data.dtype
        data['Unique values'] = col_data.nunique(dropna=True) 
        
        # If the column is numeric, get range, percentiles, mean, SD, 95% CI, and p-value (normality test)
        if pd.api.types.is_numeric_dtype(col_data):
            mean_val = col_data.mean()
            sd_val = col_data.std()
            n = col_data.dropna().count()
            ci_low = mean_val - 1.96 * (sd_val / np.sqrt(n))
            ci_high = mean_val + 1.96 * (sd_val / np.sqrt(n))
            
            data['Range'] = (col_data.min(), col_data.max())
            data['25th percentile'] = col_data.quantile(0.25)
            data['50th percentile (Median)'] = col_data.median()
            data['75th percentile'] = col_data.quantile(0.75)
            data['Mean'] = mean_val
            data['SD'] = sd_val
            data['95% CI'] = (ci_low, ci_high)
            # Testing for normality using the Shapiro-Wilk test
            _, p_val = shapiro(col_data.dropna())
            data['p-value (normality)'] = p_val
            data['Top categories'] = "-"  
            
        # If the column is categorical or object type, get examples, top categories, and proportion 95% CI for the top category
        elif pd.api.types.is_categorical_dtype(col_data) or col_data.dtype == 'object':
            data['Examples'] = list(col_data.dropna().sample(3, random_state=0))
            top_categories = col_data.value_counts(dropna=True).head(5)  
            data['Top categories'] = ', '.join([f"{key}: {value}" for key, value in top_categories.items()])
            top_category = col_data.value_counts().idxmax()
            proportion = col_data.value_counts(normalize=True).loc[top_category]
            n = col_data.count()
            ci_low = proportion - 1.96 * np.sqrt((proportion * (1 - proportion)) / n)
            ci_high = proportion + 1.96 * np.sqrt((proportion * (1 - proportion)) / n)
            
            data['Top category proportion'] = proportion
            data['95% CI (top category)'] = (ci_low, ci_high)
            data['Range'] = "-"  
            data['25th percentile'] = "-"
            data['50th percentile (Median)'] = "-"
            data['75th percentile'] = "-"
            data['Mean'] = "-"
            data['SD'] = "-"
            data['p-value (normality)'] = "-"

        return data

    if column:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in the dataframe.")
        return pd.DataFrame([single_column_integrated_codebook(df[column], column)])
    else:
        return pd.DataFrame([single_column_integrated_codebook(df[col], col) for col in df.columns])


