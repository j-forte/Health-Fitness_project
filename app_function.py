import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score


def load_and_preprocess(file_path):
    """Load dataset, preprocess data, and return cleaned DataFrame."""
    df = pd.read_csv(file_path).set_index('participant_id')

    # Convert date and extract features
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day

    # Drop non-essential columns
    df.drop(columns=['date'], inplace=True)

    # Encoding categorical variables
    mappings = {
        'intensity': {'Low': 1, 'Medium': 2, 'High': 3},
        'gender': {'Male': 0, 'Female': 1},
        'smoking_status': {'Non-Smoker': 0, 'Smoker': 1},
        'health_condition': {
                'Diabetes': 0,
                'Hypertension': 1,
                'Asthma': 2
            },
        'activity_type': {
            'Yoga': 1, 'Weight Training': 2, 'HIIT': 3, 'Dancing': 4, 'Cycling': 5,
            'Basketball': 6, 'Tennis': 7, 'Walking': 8, 'Swimming': 9, 'Running': 10
        }
    }

    #mappings 
    for col, mapping in mappings.items():
        if col in df.columns:
            df[col] = df[col].map(mapping).fillna(-1)

    # Feature engineering
    df['stressful_sleep_val'] = df['hours_sleep'] * df['stress_level']
    df['exercise_intensity_daily_step_val'] = df['intensity'] * df['daily_steps']

    # Fill missing values (exclude categorical variables)
    df.fillna(0, inplace=True)

    return df

def train_prediction_model(df, target_features):

    # List of selected features based on importance
    selected_features = ["age", "gender", "bmi", "daily_steps", "hydration_level", "stress_level", "hours_sleep"]

    # Drop unnecessary columns
    df = df.drop(columns=['date', 'participant_id'], errors='ignore')

    # Keep only relevant numeric columns
    df = df.select_dtypes(include=[np.number])

    # Drop rows with missing values (important for model stability)
    df = df.dropna()

    # Features (X) and target variables (Y)
    X = df[selected_features]
    Y = df[['health_condition', 'smoking_status']]

    # Train-test split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Standardize numerical features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, Y_train)

    return model, scaler, X_test, Y_test, selected_features

def main():
    file_path = 'data/health_fitness_dataset_primary.csv'
    
    df = load_and_preprocess(file_path)

    selected_features = ["age", "gender", "bmi", "daily_steps", "hydration_level", "stress_level", "hours_sleep"]

    target_features = ['health_condition', 'smoking_status']

    model, scaler, X_test, Y_test, selected_features = train_prediction_model(df, target_features)

   
    # for feature, acc in accuracy.items():
    #     if isinstance(acc, pd.Series):
    #         acc = acc.iloc[0]  # Extract first value if it's a Series
    #     print(f"{feature}: Accuracy = {acc:.4f}")   

    return df, model, scaler, X_test, Y_test, selected_features
