import pandas as pd
import numpy as np
from scipy.stats import shapiro, kstest, norm

def codebook(df, column=None, advanced=False, decimal_places=3):
    def check_blanks(col_data):
        if col_data.dtype == 'object':
            embedded_blanks = col_data.apply(lambda x: ' ' in x.strip() if isinstance(x, str) else False).any()
            leading_blanks = col_data.apply(lambda x: x.startswith(' ') if isinstance(x, str) else False).any()
            trailing_blanks = col_data.apply(lambda x: x.endswith(' ') if isinstance(x, str) else False).any()

            warnings = []
            if embedded_blanks:
                warnings.append("Embedded blanks detected")
            if leading_blanks:
                warnings.append("Leading blanks detected")
            if trailing_blanks:
                warnings.append("Trailing blanks detected")

            return ', '.join(warnings) if warnings else "No blanks detected"
        return "Not applicable"

    def normality_test(col_data):
        n = col_data.dropna().count()
        if n <= 5000:
            stat, p_value = shapiro(col_data.dropna())
            test_name = "Shapiro-Wilk"
        else:
            stat, p_value = kstest((col_data.dropna() - col_data.mean()) / col_data.std(), 'norm')
            test_name = "Kolmogorov-Smirnov"
        return test_name, p_value

    def detect_mixed_types(col_data):
        inferred_type = pd.api.types.infer_dtype(col_data, skipna=True)
        return inferred_type in ['mixed', 'mixed-integer', 'mixed-integer-float', 'mixed-float']

    def round_numeric(value):
        if isinstance(value, (int, float)):
            return round(value, decimal_places)
        if isinstance(value, tuple) and len(value) == 2:
            return (round(value[0], decimal_places), round(value[1], decimal_places))
        return value

    def single_column_codebook(col_data, col_name, advanced=False):
        data = {}
        data['Variable'] = col_name
        data['Type'] = col_data.dtype

        if col_data.isnull().all():
            data['Unique values'] = 0
            data['Missing values'] = len(col_data)
            data['Blank issues'] = "Column is entirely missing"
            data['Range'] = "-"
            data['25th percentile'] = "-"
            data['50th percentile (Median)'] = "-"
            data['75th percentile'] = "-"
            data['Mean'] = "-"
            data['Examples'] = "-"
            data['Top categories'] = "-"
            data['SD'] = "-"
            data['95% CI'] = "-"
            data['Normality test'] = "-"
            data['p-value (normality)'] = "-"
            data['Top category proportion'] = "-"
            data['95% CI (top category)'] = "-"
            return data

        if detect_mixed_types(col_data):
            data['Warning'] = "Mixed data types detected, treating as object type"
            col_data = col_data.astype(str)

        data['Unique values'] = col_data.nunique(dropna=True)  
        data['Missing values'] = col_data.isnull().sum()
        data['Blank issues'] = check_blanks(col_data)

        if pd.api.types.is_bool_dtype(col_data):
            data['Range'] = (col_data.min(), col_data.max())
            data['25th percentile'] = "-"
            data['50th percentile (Median)'] = "-"
            data['75th percentile'] = "-"
            data['Mean'] = col_data.mean()
            data['Examples'] = list(col_data.sample(3, random_state=0))
            data['Top categories'] = dict(col_data.value_counts(dropna=True))
            data['SD'] = "-"
            data['95% CI'] = "-"
            data['Normality test'] = "-"
            data['p-value (normality)'] = "-"
        
        elif pd.api.types.is_numeric_dtype(col_data):
            mean_val = round_numeric(col_data.mean())
            sd_val = round_numeric(col_data.std())
            n = col_data.dropna().count()
            
            data['Range'] = round_numeric((col_data.min(), col_data.max()))
            data['25th percentile'] = round_numeric(col_data.quantile(0.25))
            data['50th percentile (Median)'] = round_numeric(col_data.median())
            data['75th percentile'] = round_numeric(col_data.quantile(0.75))
            data['Mean'] = mean_val
            data['Examples'] = list(col_data.sample(3, random_state=0))
            data['Top categories'] = "-"  

            if advanced:
                ci_low = mean_val - 1.96 * (sd_val / np.sqrt(n))
                ci_high = mean_val + 1.96 * (sd_val / np.sqrt(n))
                test_name, p_val = normality_test(col_data)
                
                data['SD'] = sd_val
                data['95% CI'] = round_numeric((ci_low, ci_high))
                data['Normality test'] = test_name
                data['p-value (normality)'] = round_numeric(p_val)
            else:
                data['SD'] = "-"
                data['95% CI'] = "-"
                data['Normality test'] = "-"
                data['p-value (normality)'] = "-"
        
        elif isinstance(col_data.dtype, pd.CategoricalDtype) or col_data.dtype == 'object':
            data['Examples'] = list(col_data.dropna().sample(3, random_state=0))
            top_categories = col_data.value_counts(dropna=True).head(5)  
            data['Top categories'] = dict(top_categories)
            data['Range'] = "-"  
            data['25th percentile'] = "-"
            data['50th percentile (Median)'] = "-"
            data['75th percentile'] = "-"
            data['Mean'] = "-"
            data['SD'] = "-"
            data['Normality test'] = "-"
            data['p-value (normality)'] = "-"

            if advanced and not col_data.empty:
                top_category = col_data.value_counts().idxmax()
                proportion = col_data.value_counts(normalize=True).loc[top_category]
                n = col_data.count()
                ci_low = proportion - 1.96 * np.sqrt((proportion * (1 - proportion)) / n)
                ci_high = proportion + 1.96 * np.sqrt((proportion * (1 - proportion)) / n)
                
                data['Top category proportion'] = round_numeric(proportion)
                data['95% CI (top category)'] = round_numeric((ci_low, ci_high))
            else:
                data['Top category proportion'] = "-"
                data['95% CI (top category)'] = "-"

        return data

    if column:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in the dataframe.")
        return pd.DataFrame([single_column_codebook(df[column], column, advanced)])
    else:
        return pd.DataFrame([single_column_codebook(df[col], col, advanced) for col in df.columns])



