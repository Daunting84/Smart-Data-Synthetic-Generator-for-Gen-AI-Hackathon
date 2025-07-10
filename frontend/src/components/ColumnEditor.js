import { useState } from 'react';

export default function ColumnEditor() {
  const [headers, setHeaders] = useState(Array(6).fill(""));

  const handleChange = (i, value) => {
    const newHeaders = [...headers];
    newHeaders[i] = value;
    setHeaders(newHeaders);
  };

  const submitHeaders = async () => {
    const cleaned = headers.filter(h => h.trim() !== "");
    await fetch(`${process.env.REACT_APP_API_URL}/set-fields`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ fields: cleaned }),
    });
  };

  return (
    <div className="p-10 max-w-4xl mx-auto space-y-4">
      <h2 className="text-2xl font-bold">Enter Column Headers</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
        {headers.map((header, i) => (
          <input
            key={i}
            className="border rounded p-2"
            placeholder={`Column header ${i + 1}`}
            value={header}
            onChange={(e) => handleChange(i, e.target.value)}
          />
        ))}
      </div>
      <button
        onClick={submitHeaders}
        className="mt-6 bg-#7B61FF text-white px-6 py-2 rounded-xl"
      >
        Submit
      </button>
    </div>
  );
}
