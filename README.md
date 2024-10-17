# Receipt Scan Quantity Forecaster

## Project Overview
The **Receipt Scan Quantity Forecaster** uses historical data from 2021 to predict the number of scanned receipts for each month of 2022. The system employs a machine learning model built using TensorFlow, which is exposed via a FastAPI backend. A Next.js frontend enables users to interact with the system by selecting a month and receiving a prediction of scanned receipts for that month.

## Key Features
- Predict the number of receipts scanned for each month of 2022.
- Machine learning model based on historical data from 2021.
- Interactive frontend built using **Next.js** and **React**.
- Backend API powered by **FastAPI** and **TensorFlow** for serving predictions.
- Fully containerized using Docker for ease of deployment.

---

## Installation

### Prerequisites
- **Docker Desktop** and **Docker Compose** installed.
- **Node.js** (v18.12 or higher) with **pnpm** installed globally.

### Backend Requirements
- **Python 3.9+**
- **FastAPI**
- **TensorFlow**
- **Uvicorn** (for running the FastAPI server)
- **pandas** (for data handling)

### Frontend Requirements
- **Next.js**

---

## Project Structure

The project is divided into two main parts: the backend (FastAPI) and the frontend (Next.js).

### Backend (FastAPI)

```
backend/
├── main.py                # FastAPI application entry point, including models
├── requirements.txt       # Python dependencies
├── data_daily.csv         # Historical data for 2021
└── Dockerfile             # Dockerfile for containerizing the backend
```

- **main.py**: Defines the FastAPI endpoints and implements the receipt prediction logic using TensorFlow.
- **data_daily.csv**: Contains the historical data from 2021.
- **Dockerfile**: Dockerfile to containerize the backend.

### Frontend (Next.js)

```
frontend/
├── src/
│   ├── app/                        # Next.js app-related files (e.g., layouts, pages)
│   ├── components/                 # React components for the UI
│       ├── PredictionClient.tsx    # Handles form submission and API interaction
│       ├── PredictionForm.tsx      # Form for inputting month number
│       └── PredictionResult.tsx    # Displays prediction result
├── Dockerfile                      # Dockerfile for containerizing the frontend
├── package.json                    # Project dependencies
├── pnpm-lock.yaml                  # pnpm lockfile for dependencies
├── [config files]                  # Additional config files like .eslintrc, .prettierrc, etc.
```

- **PredictionClient.tsx**: Manages form submission and prediction API calls.
- **PredictionForm.tsx**: Handles user input for month selection.
- **PredictionResult.tsx**: Displays the predicted receipt count for the selected month.
- **Dockerfile**: Dockerfile to containerize the frontend.

---

## Setup Instructions

1. **Clone the repository**
    
   ```bash
   git clone https://github.com/jamesrobertsjr/receipt-scan-quantity-forecaster
   cd receipt-scan-quantity-forecaster
   ```

2. **Install dependencies**

   You can install the dependencies using Docker.

    ```bash
    docker compose up --build
    ```

   *Optional*: Manual Setup
    
    - Backend:
      - Move your pointer into the backend directory: `cd backend`
      - Create a virtual environment: 
        - `pip3 -m venv .venv`
        - `source .venv/bin/activate`
      - Install dependencies: `uv pip install -r requirements.txt` 
      
    - Frontend:
      - Move your pointer into the frontend directory:
        - From the monorepository's root, run `cd frontend`
      - Install dependencies: `pnpm install`
      - Build and run the frontend:
      ```
      pnpm build
      pnpm dev
      ```

---

## Docker Compose

A **Docker Compose** setup has been provided to simplify the installation and running process. The backend and frontend services are fully containerized.

1. **Build and Run the entire system**:
   In the root directory of the project, simply run:

    ```bash
    docker compose up --build
    ```

2. The services will be accessible at:
    - **Frontend**: `http://localhost:3000`
    - **Backend API**: `http://localhost:8000`

---

## Usage Instructions

### Frontend: Interacting with the System

1. **Open the frontend** at `http://localhost:3000`.
2. **Enter a month number (1 for January, 12 for December)** into the input field.
3. **Submit the form** to receive a prediction of the number of receipts scanned for the selected month.
4. The system will display the predicted value for that month.

### Backend API Endpoints

#### `POST /predict`
- **Description**: Returns the predicted number of receipts for a specified month.
- **Request Body**:
    - `month`: integer between 1 and 12 (representing the month for which prediction is required).


---

## How the System Works

1. **Backend**:
    - The FastAPI backend loads historical receipt scan data from 2021.
    - A machine learning model (TensorFlow-based) is trained on this data to predict the number of receipts scanned in future months (2022).
    - The `/predict` endpoint receives a month number and returns the predicted number of receipts scanned for that month.

2. **Frontend**:
    - The user enters a month number (between 1 and 12) and submits the form.
    - The frontend calls the `/predict` API, retrieves the prediction, and displays it to the user.

---

## Troubleshooting

### 1. Frontend Changes Not Reflected After Modification

If you modify the frontend code but changes do not reflect when running `docker compose up`, force Docker to rebuild the frontend container:

```bash
docker compose up --build
```

### 2. CORS Issues

If you face CORS-related errors while trying to access the backend API from the frontend, ensure that the FastAPI application has proper CORS middleware set up.

### 3. TensorFlow Errors

If you encounter errors related to TensorFlow installation, ensure you’re using a compatible Python version (Python 3.9) and that all dependencies are installed properly.

# Author

James E. Roberts, Jr.