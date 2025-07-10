export default function OutputPath() {
  const formats = ["csv", "json", "xlsx"];

  const setOutputFormat = async (format) => {
    await fetch(`${process.env.REACT_APP_API_URL}/set-output-format`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ output_ext: format }),
    });
  };

  return (
    <div className="p-10 max-w-4xl mx-auto space-y-4">
      <h2 className="text-2xl font-bold">Output Your Data As...</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {formats.map((format) => (
          <button
            key={format}
            onClick={() => setOutputFormat(format)}
            className="bg-#7B61FF p-4 rounded shadow hover:bg-purple-200"
          >
            {format.toUpperCase()}
          </button>
        ))}
      </div>
    </div>
  );
}