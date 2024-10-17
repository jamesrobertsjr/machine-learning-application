import PredictionClient from '../components/PredictionClient';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-4xl mb-8 text-center">Receipt Scan Quantity Forecaster</h1>
      <PredictionClient/>
    </div>
  );
}