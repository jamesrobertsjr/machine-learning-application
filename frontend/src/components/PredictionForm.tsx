'use client';

import { useState, FormEvent } from 'react';

interface PredictionFormProps {
  onSubmit: (month: number) => void;
}

export default function PredictionForm({ onSubmit }: PredictionFormProps) {
  const [month, setMonth] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();

    const monthNumber = parseInt(month, 10);
    if (isNaN(monthNumber) || monthNumber < 1 || monthNumber > 12) {
      setError('Please enter a month between 1 and 12.');
    } else {
      setError(null);
      onSubmit(monthNumber);  // Pass the entered month as a number
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
      <label htmlFor="month" className="text-lg text-center">
        Choose a month (1-12) to see the projected scanned receipts for that month in 2022.
      </label>
      <input
        type="number"
        id="month"
        value={month}
        onChange={(e) => setMonth(e.target.value)}
        className="border border-gray-400 p-2 rounded-md"
        required
      />
      <button type="submit" className="py-2 px-4 bg-blue-500 text-white rounded-md">
        Get Results
      </button>
      {error && <p className="text-red-600">{error}</p>}
    </form>
  );
}