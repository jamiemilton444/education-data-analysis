import pandas as pd
from scipy.stats import linregress

# Assume df is your merged, cleaned dataset
def analyze_relationship(df):
    result = {}

    # Example: funding vs test scores
    slope, intercept, r_value, p_value, std_err = linregress(df['funding'], df['test_scores'])
    result['funding_vs_scores'] = {
        'slope': slope,
        'r_squared': r_value**2,
        'p_value': p_value
    }

    # Example: funding vs % Black students
    slope, intercept, r_value, p_value, std_err = linregress(df['percent_black'], df['funding'])
    result['race_vs_funding'] = {
        'slope': slope,
        'r_squared': r_value**2,
        'p_value': p_value
    }

    return result
First code file for data analysis
