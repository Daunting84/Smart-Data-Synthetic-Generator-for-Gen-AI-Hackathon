import { useState } from 'react';

export default function RowSelector() {
  const [numRows, setNumRows] = useState('');
  const [error, setError] = useState('');

  const submitNumRows = async () => {
    const value = parseInt(numRows);
    if (isNaN(value) || value <= 0) {
      setError('Please enter a valid positive number.');
      return;
    }

    setError('');
    await fetch(`${process.env.REACT_APP_API_URL}/set-rows`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ num_rows: value }),
    });
  };

  return (
    <div className="p-10 max-w-4xl mx-auto space-y-4">
      <h2 className="text-2xl font-bold">How many rows of synthetic data?</h2>
      <input
        type="number"
        min="1"
        className="w-full border rounded p-4 text-lg"
        placeholder="Enter a number"
        value={numRows}
        onChange={(e) => setNumRows(e.target.value)}
      />
      {error && <p className="text-red-600 font-medium">{error}</p>}
      <button
        onClick={submitNumRows}
        className="bg-purple-500 text-white px-6 py-2 rounded-xl"
        disabled={isNaN(parseInt(numRows)) || parseInt(numRows) <= 0}
      >
        Submit
      </button>
    </div>
  );
}
