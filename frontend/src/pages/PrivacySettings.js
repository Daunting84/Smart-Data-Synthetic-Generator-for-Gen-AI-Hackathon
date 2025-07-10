import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function PrivacySettings() {
  const [noise, setNoise] = useState(0);
  const [swap, setSwap] = useState(0);
  const [masking, setMasking] = useState(['']);
  const navigate = useNavigate();

  const generateData = async () => {
  const res = await fetch(`${process.env.REACT_APP_API_URL}/generate-data`, {
    method: 'POST',
  });
  const result = await res.json();
  console.log(result); // Optional: Display result/output path
  navigate('/generate'); // You can redirect only if result.status === "success"
};

  
  const updateMasking = (index, value) => {
    const newMasking = [...masking];
    newMasking[index] = value;
    if (value && index === masking.length - 1) {
      newMasking.push(''); // Add new input if last was filled
    }
    setMasking(newMasking);
  };

  const submitPrivacy = async () => {
    const filteredMasking = masking.filter(col => col.trim() !== '');
    await fetch(`${process.env.REACT_APP_API_URL}/set-privacy`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        noise_stddev: parseFloat(noise),
        category_swap_fraction: parseFloat(swap),
        masked_columns: filteredMasking
      }),
    });
  };

  return (
    <div className="p-10 max-w-4xl mx-auto space-y-6">
      <h2 className="text-3xl font-bold">Privacy Settings</h2>

      <div>
        <label className="block mb-1">Gaussian Noise (%): {noise}%</label>
        <input
          type="range"
          min="0"
          max="100"
          step="1"
          value={noise}
          onChange={(e) => setNoise(e.target.value)}
          className="w-full"
        />
        {noise > 0.2 && (
            <p className="text-yellow-600 text-sm mt-1">
            ⚠️ Warning: Noise above 20% may significantly reduce data quality.
            </p>
        )}
      </div>

      <div>
        <label className="block mb-1">Category Swap (%): {swap}%</label>
        <input
          type="range"
          min="0"
          max="100"
          step="1"
          value={swap}
          onChange={(e) => setSwap(e.target.value)}
          className="w-full"
        />
      </div>

      <div>
        <label className="block mb-2">Column Masking:</label>
        {masking.map((val, i) => (
          <input
            key={i}
            className="border p-2 mb-2 w-full"
            placeholder="Enter column name"
            value={val}
            onChange={(e) => updateMasking(i, e.target.value)}
          />
        ))}
      </div>

      <button onClick={() => {submitPrivacy(); navigate('/generate');generateData();}} className="bg-#7B61FF text-white px-6 py-2 rounded-xl">Generate Data</button>

    </div>
  );
}