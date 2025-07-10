
export default function DomainSelect() {
  const domains = ["AI Assistant", "Education", "Healthcare", "Retail", "Marketing", "Public Policy", "Finance", "Manufacturing", "Biotech", "AI Training"];

  const setUseCase = async (domain) => {
    await fetch(`${process.env.REACT_APP_API_URL}/set-use-case`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ use_case: domain })
    });
  };

  return (
    <div className="p-10 max-w-4xl mx-auto space-y-4">
      <h2 className="text-2xl font-bold">Please pick a domain...</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {domains.map((d) => (
          <button
            key={d}
            onClick={() => setUseCase(d)}
            className="bg-#7B61FF p-4 rounded shadow hover:bg-blue-200"
          >
            {d}
          </button>
        ))}
      </div>
    </div>
  );
}