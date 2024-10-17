interface PredictionResultProps {
  prediction: number;
  monthName: string; // Added monthName to the props interface
}

export default function PredictionResult({ prediction, monthName }: PredictionResultProps) {
  return (
    <div className="text-center bg-gray-100 p-4 rounded-lg">
      <h2 className="text-2xl font-semibold">{monthName}&apos;s Projected Receipts</h2>
      <p className="text-lg mt-2">{prediction.toLocaleString()}</p>
    </div>
  );
}