'use client';

import { useState } from 'react';
import PredictionForm from './PredictionForm';
import PredictionResult from './PredictionResult';

export default function PredictionClient() {
  const [prediction, setPrediction] = useState<number | null>(null);
  const [month, setMonth] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  /* eslint-disable */
  const fetchPrediction = async (month: number) => {
    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ month }),
      });

      const data = await response.json();

      if (response.ok) {
        setPrediction(data.predicted_receipts);
        setMonth(month); // Set the selected month
        setError(null);
      } else {
        setError(data.detail || 'Prediction failed');
        setPrediction(null);
      }
    } catch (error) {
      setError('Failed to fetch prediction.');
      setPrediction(null);
    }
  };
  /* eslint-enable */

  return (
    <div className="w-full max-w-md">
      <PredictionForm onSubmit={fetchPrediction} />
      {error && <p className="mt-4 text-red-600">{error}</p>}
      {prediction !== null && month !== null && (
        <div className="mt-4">
          <PredictionResult
            prediction={prediction}
            monthName={monthNames[month - 1]} // Convert month number to month name
          />
        </div>
      )}
    </div>
  );
}