import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.metrics import accuracy_score
import app_function as af  


@st.cache_data
def load_main():
    return af.main()

# Load data and model
df, model, scaler, X_test, Y_test, selected_features = af.main()

st.title("Health Prediction Dashboard")

# Sidebar Navigation
st.sidebar.header("Select Tab")
page = st.sidebar.radio("Go to", ["Data Visualizations", "Model Predictions"])

if page == "Data Visualizations":
    st.header("Data Visualizations")

    # Show raw data
    st.subheader("Raw Data")
    st.write(df.head())

    st.subheader("Activity Type vs. Calories Burned")
    st.write({'Yoga': 1, 'Weight Training': 2, 'HIIT': 3, 'Dancing': 4, 'Cycling': 5,
            'Basketball': 6, 'Tennis': 7, 'Walking': 8, 'Swimming': 9, 'Running': 10})
    fig, ax = plt.subplots(figsize=(8, 4))
    activity_calories = df.groupby("activity_type")["calories_burned"].mean().sort_values()
    sns.barplot(x=activity_calories.index, y=activity_calories.values, ax=ax, palette="coolwarm")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_xlabel("Activity Type")
    ax.set_ylabel("Avg. Calories Burned")
    st.pyplot(fig)

    st.subheader("Sleep Hours vs. Stress Level")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(x=df["hours_sleep"], y=df["stress_level"], alpha=0.6, ax=ax)
    ax.set_xlabel("Hours of Sleep")
    ax.set_ylabel("Stress Level")
    st.pyplot(fig)

    # Age Distribution
    st.subheader("Age Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df["age"], bins=15, kde=True, color="blue", ax=ax)  
    ax.set_xlabel("Age")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # Correlation Heatmap
    st.subheader("Correlation Heatmap (Top Features)")
    top_features = df.corr()["health_condition"].abs().sort_values(ascending=False).head(10).index
    fig, ax = plt.subplots()
    sns.heatmap(df[top_features].corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

elif page == "Model Predictions":
    st.header("Model Predictions")


    important_features = ["age", "gender", "bmi", "daily_steps", "hydration_level", "stress_level", "hours_sleep"]

    st.subheader("Enter Your Parameters for your Health predictions")

    user_data = {}
    for feature in important_features:
        if feature == "gender":
            user_data[feature] = 0 if st.radio("Gender", ["Male", "Female"]) == "Male" else 1
        else:
            min_val = float(df[feature].min())
            max_val = float(df[feature].max())
            avg_val = float(df[feature].mean())

            user_data[feature] = st.slider(
                f"{feature.replace('_', ' ').title()}",
                min_value=min_val,
                max_value=max_val,
                value=avg_val,
                step=(max_val - min_val) / 100) 

    
    user_df = pd.DataFrame([user_data])[selected_features]

    # Scale input using the trained scaler
    scaled_input = scaler.transform(user_df)

    # Predict health condition 
    prediction = model.predict(scaled_input)

    st.subheader("Prediction Result")
    health_condition_map = {
        0: "Diabetes",
        1: "Hypertension",
        2: "Asthma",
        -1: "None" 
    }

    predicted_health_condition = health_condition_map.get(int(prediction[0][0]), "None")  
    predicted_smoking_status = "Smoker" if prediction[0][1] == 1 else "Non-Smoker"

    st.write(f"Predicted Health Condition: {predicted_health_condition}")
    st.write(f"Predicted Smoking Status: {predicted_smoking_status}")

    # Model Performance 
    st.subheader("Model Performance")
    y_pred = model.predict(X_test)

    accuracy_scores = {}
    for i, feature in enumerate(['health_condition', 'smoking_status']):
        accuracy_scores[feature] = accuracy_score(Y_test[feature], y_pred[:, i])

    for feature, acc in accuracy_scores.items():
        if isinstance(acc, pd.Series):
            acc = acc.iloc[0]  
        st.write(f"{feature} Accuracy: {acc:.2f}") 
