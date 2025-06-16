import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

# Sample dataset with square footage and number of bedrooms
data = {
    'SquareFeet': [1000, 1500, 2000, 2500, 3000, 1800, 2200, 2700, 1600, 2100],
    'Bedrooms': [2, 3, 3, 4, 4, 3, 4, 5, 2, 3],
    'Price': [200000, 250000, 300000, 360000, 400000, 275000, 330000, 390000, 240000, 310000]
}
df = pd.DataFrame(data)

# Train model
X = df[['SquareFeet', 'Bedrooms']]
y = df['Price']
model = LinearRegression()
model.fit(X, y)

# Streamlit UI
st.title("🏡 House Price Predictor (with Bedrooms)")
st.write("Predict the house price based on square footage and number of bedrooms.")

# User inputs
sqft = st.slider("Select square footage", 500, 4000, 1500, step=100)
bedrooms = st.slider("Select number of bedrooms", 1, 6, 3)

# Prediction
features = np.array([[sqft, bedrooms]])
predicted_price = model.predict(features)[0]
st.subheader(f"📈 Predicted Price: ${predicted_price:,.2f}")

# Show dataset
#st.write("### Sample Training Data")
#st.dataframe(df)

# Optional: 2D scatter plot showing only sqft vs price (color-coded by bedrooms)
fig, ax = plt.subplots()
scatter = ax.scatter(df['SquareFeet'], df['Price'], c=df['Bedrooms'], cmap='viridis', label='Training Data')
ax.scatter(sqft, predicted_price, color='red', s=100, label='Your Prediction')
ax.set_xlabel("Square Feet")
ax.set_ylabel("Price")
ax.set_title("Square Feet vs Price (color = Bedrooms)")
legend1 = ax.legend()
st.pyplot(fig)
