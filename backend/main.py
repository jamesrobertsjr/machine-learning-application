from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import uvicorn

# Initialize the FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, including POST, GET, OPTIONS
    allow_headers=["*"],  # Allow all headers, including Content-Type
)

# Load the dataset and prepare it for modeling
def load_data():
    data_path = 'data_daily.csv'  # Path to the dataset
    data = pd.read_csv(data_path)
    data['Date'] = pd.to_datetime(data['# Date'], format='%Y-%m-%d')

    # Aggregate daily data into monthly totals
    monthly_data = data.resample('M', on='Date').sum()
    return monthly_data

# Manual min-max scaling function
def manual_min_max_scaling(data):
    min_val = np.min(data)
    max_val = np.max(data)

    # Scale data to [0, 1]
    scaled_data = (data - min_val) / (max_val - min_val)
    return scaled_data, min_val, max_val

# Manual inverse scaling function
def manual_inverse_scaling(scaled_data, min_val, max_val):
    # Reverse scale from [0, 1] back to original range
    return scaled_data * (max_val - min_val) + min_val

# Preprocessing and preparing the data for LSTM
def preprocess_data(monthly_data):
    # Manually scale the data
    scaled_data, min_val, max_val = manual_min_max_scaling(monthly_data['Receipt_Count'].values)

    # Create sequences of past data (3 past months to predict the next month)
    X_train = []
    y_train = []
    sequence_length = 3
    for i in range(sequence_length, len(scaled_data)):
        X_train.append(scaled_data[i-sequence_length:i])
        y_train.append(scaled_data[i])

    X_train, y_train = np.array(X_train), np.array(y_train)

    # Reshape X_train for LSTM (samples, time steps, features)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    return X_train, y_train, min_val, max_val

# Build and train the LSTM model
def build_train_lstm(X_train, y_train):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))  # Output layer

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(X_train, y_train, epochs=20, batch_size=1, verbose=2)

    return model

# Load and preprocess data
monthly_data = load_data()
X_train, y_train, min_val, max_val = preprocess_data(monthly_data)

# Train the LSTM model
model = build_train_lstm(X_train, y_train)

# Pydantic model for input validation
class PredictionRequest(BaseModel):
    month: int  # Month to predict for (1 to 12)

# Predict the next 12 months using the trained LSTM model
def predict_next_12_months(model, min_val, max_val, monthly_data):
    # Prepare the input data (last 3 months)
    input_data = monthly_data['Receipt_Count'].values[-3:]
    input_data_scaled = (input_data - min_val) / (max_val - min_val)  # Manually scale the input data
    input_data_scaled = np.reshape(input_data_scaled, (1, input_data_scaled.shape[0], 1))

    # Predict the next month
    predictions = []
    for i in range(12):
        # Predict receipt count for the next month
        predicted_receipt_count = model.predict(input_data_scaled)

        # Append the predicted value to the predictions list
        predictions.append(predicted_receipt_count[0][0])

        # Use the predicted value for the next prediction
        predicted_receipt_count_reshaped = np.reshape(predicted_receipt_count, (1, 1, 1))
        input_data_scaled = np.append(input_data_scaled[:, 1:, :], predicted_receipt_count_reshaped, axis=1)

    # Manually inverse scale the predictions
    predictions = manual_inverse_scaling(np.array(predictions), min_val, max_val)
    return predictions

# Predict future receipt counts
predicted_receipts = predict_next_12_months(model, min_val, max_val, monthly_data)

# Define API endpoint for receipt count predictions
@app.post("/predict")
def predict_receipts(request: PredictionRequest):
    # Validate the month value to be between 1 and 12
    if request.month < 1 or request.month > 12:
        raise HTTPException(status_code=400, detail="Month value must be between 1 and 12.")

    try:
        # Get the prediction for the requested month
        prediction_value = predicted_receipts[request.month - 1]
        return {"month": request.month, "predicted_receipts": int(prediction_value)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)