import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

"""
Python file that will hold all the functions that will be used in the main notebook
"""

#Write a function that will take in a datafram and a participant_id and return a dataframe with only the participant data
def set_up_participants_df(df, participant_id):
    
    df_reset = df.reset_index()

    filtered_df = df_reset[df_reset['participant_id'] == participant_id]
    
    return filtered_df
    
# function to generate three lineplots for 'avg_heart_rate', 'fitness_level', 'stress_level' grouped by input perameter
def plot_grouped_metrics(grouped_df, metrics=['avg_heart_rate', 'fitness_level', 'stress_level'], 
                         x_column='age_group', group_by_column='age_group'):
    
    grouped_df.columns = grouped_df.columns.str.strip()
    grouped_df.columns = grouped_df.columns.str.lower()

    grouped_df = grouped_df.dropna(subset=metrics + [x_column, group_by_column])
    
    grouped_df = grouped_df.groupby(group_by_column)[metrics].mean().reset_index()

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    axes = axes.flatten()
    
    for i, metric in enumerate(metrics):
        ax = axes[i]  
        
        sns.lineplot(x=x_column, y=metric, data=grouped_df, ax=ax, marker='o', color='blue')
        
        #ax.set_ylim(0,100)
        ax.set_xlabel(x_column)
        ax.set_ylabel(metric)
        ax.set_title(f'{metric} by {x_column}')
    
    plt.tight_layout()
    plt.show()

# function to generate three histogram for 'avg_heart_rate', 'fitness_level', 'stress_level' grouped by input perameter
def plot_grouped_metrics_hist(grouped_df, metrics=['avg_heart_rate', 'fitness_level', 'stress_level'], 
                         x_column='age_group', group_by_column='age_group'):
    
    grouped_df.columns = grouped_df.columns.str.strip()
    grouped_df.columns = grouped_df.columns.str.lower()

    grouped_df = grouped_df.dropna(subset=metrics + [x_column, group_by_column])
    grouped_df = grouped_df.groupby(group_by_column)[metrics].mean().reset_index()

    fig, axes = plt.subplots(1, 3, figsize=(12, 4)) 

    axes = axes.flatten()  

    for i, metric in enumerate(metrics):
        ax = axes[i]  
        
        sns.histplot(grouped_df, x=metric, hue=x_column, kde=True, ax=ax, bins=15, color='blue', element="step", stat="density")

        ax.set_xlabel(metric)
        ax.set_ylabel("Density")
        ax.set_title(f'Distribution of {metric} by {x_column}')

    plt.tight_layout()
    plt.show()

# function to generate three boxplots for 'avg_heart_rate', 'fitness_level', 'stress_level' grouped by input perameter
def plot_grouped_metrics_boxplot(grouped_df, metrics=['avg_heart_rate', 'fitness_level', 'stress_level'], 
                         x_column='age_group', group_by_column='age_group'):
    
    grouped_df.columns = grouped_df.columns.str.strip()
    grouped_df.columns = grouped_df.columns.str.lower()

    grouped_df = grouped_df.dropna(subset=metrics + [x_column, group_by_column])

    grouped_df = grouped_df.groupby(group_by_column)[metrics].mean().reset_index()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))  
    
    axes = axes.flatten()  

    for i, metric in enumerate(metrics):
        ax = axes[i]  

        sns.boxplot(x=x_column, y=metric, data=grouped_df, ax=ax, palette="Set2")
        
        #ax.set_ylim(0,100)
        ax.set_xlabel(x_column)
        ax.set_ylabel(metric)
        ax.set_title(f'{metric} by {x_column}')
   

    plt.tight_layout()
    plt.show()

# function to generate three boxplots for 'avg_heart_rate', 'fitness_level', 'stress_level' grouped by input perameter
def plot_grouped_metrics_barplot(grouped_df, metrics=['avg_heart_rate', 'fitness_level', 'stress_level'], 
                         x_column='age_group', group_by_column='age_group'):
    
    grouped_df.columns = grouped_df.columns.str.strip()
    grouped_df.columns = grouped_df.columns.str.lower()

    grouped_df = grouped_df.dropna(subset=metrics + [x_column, group_by_column])

    grouped_df = grouped_df.groupby(group_by_column)[metrics].mean().reset_index()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))  
    
    axes = axes.flatten()  

    for i, metric in enumerate(metrics):
        ax = axes[i]  

        sns.barplot(x=x_column, y=metric, data=grouped_df, ax=ax, palette="Set2")
        
        #ax.set_ylim(0,100)
        ax.set_xlabel(x_column)
        ax.set_ylabel(metric)
        ax.set_title(f'{metric} by {x_column}')
   

    plt.tight_layout()
    plt.show()

# function to generate three scatter plots for 'avg_heart_rate', 'fitness_level', 'stress_level' grouped by input perameter
def plot_grouped_metrics_scatter(grouped_df, metrics=['avg_heart_rate', 'fitness_level', 'stress_level'], 
                                 x_column='age_group', group_by_column='age_group'):
    
    grouped_df.columns = grouped_df.columns.str.strip()
    grouped_df.columns = grouped_df.columns.str.lower()

    grouped_df = grouped_df.dropna(subset=metrics + [x_column, group_by_column])

    grouped_df = grouped_df.groupby(group_by_column)[metrics].mean().reset_index()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))  

    axes = axes.flatten()  

    for i, metric in enumerate(metrics):
        ax = axes[i]  

        sns.scatterplot(x=x_column, y=metric, data=grouped_df, ax=ax, color='blue', marker='o')

        ax.set_xlabel(x_column)
        ax.set_ylabel(metric)
        ax.set_title(f'{metric} by {x_column}')

    plt.tight_layout()
    plt.show()

# function to normalize the data
def normalize_data(df, columns):
    for column in columns:
        min_val = df[columns].min()
        max_val = df[columns].max()
        df[columns] = (df[columns] - min_val) / (max_val - min_val)
    return df   

# function to standardize the data
def standardize_data(df, columns):
    for column in columns:
        mean = df[column].mean()
        std_dev = df[column].std()
        df[column] = (df[column] - mean) / std_dev
    return df

# function to convert scaled value to raw value
def convert_scaled_to_raw(scaled_value, min_raw_score, max_raw_score):
    raw_value = (scaled_value * (max_raw_score - min_raw_score)) / 10 + min_raw_score
    return raw_value

def plot_participant_id_over_time(participant):

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.lineplot(x='month', y='stress_level', data=participant, ci=None, marker='o', ax=ax, color='green', label='Stress Level')
    sns.lineplot(x='month', y='hours_sleep', data=participant, ci=None, marker='o', ax=ax, color='blue', label='Hours Sleep')
    sns.lineplot(x='month', y='fitness_level', data=participant, ci=None, marker='o', ax=ax, color='orange', label='Fitness Level')
    sns.lineplot(x='month', y='duration_minutes', data=participant, ci=None, marker='o', ax=ax, color='black', label='Duration Minutes')
    sns.lineplot(x='month', y='intensity_lvl_value', data=participant, ci=None, marker='o', ax=ax, color='yellow', label='Intensity Level')
    sns.lineplot(x='month', y='stressful_sleep_val', data=participant, ci=None, marker='o', ax=ax, color='purple', label='stressful Sleep')
    sns.lineplot(x='month', y='calories_burned', data=participant, ci=None, marker='o', ax=ax, color='red', label='Calories Burned')
    sns.lineplot(x='month', y='bmi', data=participant, ci=None, marker='o', ax=ax, color='black', label='BMI')

    ax.set_title(f'Participant {participant.index} Metrics Over Time')
    ax.set_xlabel('Date')

    plt.xticks(rotation=45)
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()