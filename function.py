import pandas as pd
import numpy as np


'''
Write a function that will take in a datafram and a participant_id and return a datafram with only the participant data
'''
def set_up_participants_df(df, participant_id):
    # if isinstance(df, pd.DataFrame):
    #     if 'participant_id' in df.columns:
    #         participant_data = df[df['participant_id'] == participant_id]
    #         return participant_data
    # else:
    #     raise ValueError("The input is not a valid DataFrame.")
    df_reset = df.reset_index()

    # Filter the DataFrame based on the participants_id column
    filtered_df = df_reset[df_reset['participant_id'] == participant_id]
    
    return filtered_df
    

# '''
# Writa a funciton that will get the z-score of a column in a dataframe
# '''
# def outlier_cleaner(feature):
#     df_q1 = new_df_data[feature].quantile(.25)
#     df_q3 = new_df_data[feature].quantile(.75)
#     df_med = new_df_data[feature].quantile(.50)
#     iqr = df_q3 - df_q1
#     lower = df_q1 - iqr * 1.5
#     upper = df_q3 + iqr * 1.5
#     no_outliers_df = new_df_data[(new_df_data[feature] >= lower) & (new_df_data[feature] <= upper)]
#     return no_outliers_df