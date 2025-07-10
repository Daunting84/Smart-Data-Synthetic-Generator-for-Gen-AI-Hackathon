import { useNavigate } from 'react-router-dom';

export default function DataSelector() {
const navigate = useNavigate();

const setMode = async (mode) => {
    await fetch(`${process.env.REACT_APP_API_URL}/set-mode`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode }),
    });
  };
return (
<div className="p-10 max-w-4xl mx-auto space-y-6">
<div>
<h2 className="text-3xl font-bold">Data Mode</h2>
<h4 className="text-1xl font-italics">Generate synthetic data based on a pre-existing database</h4>

<ul className="list-disc list-inside text-lg">
<li>Upload CSV, JSON or XLSX</li>
<li>Receive key data insights</li>
<li>Choose the amount of data produced</li>
<li>Analyzed and replicated by CTGAN</li>
<li>Adjust privacy features</li>
<li>Receive data validation results</li>
<li>Download data</li>
</ul>
<button onClick={() => {setMode("data"); navigate('/data-mode');}} className="bg-#7B61FF text-white px-6 py-2 rounded-xl">Upload Data</button>
</div>
<div>
<h2 className="text-3xl font-bold">Dual Mode</h2>
<h4 className="text-1xl font-italics">Generate and customize synthetic data, using both AI and CTGAN features</h4>
<ul className="list-disc list-inside text-lg">
<li>Upload CSV, JSON or XLSX</li>
<li>Enter a prompt</li>
<li>Receive key data insights</li>
<li>Choose amount of data</li>
<li>Choose 3 production pathways</li>
<li>Modify data</li>
<li>Adjust privacy</li>
<li>Get validation results</li>
</ul>
<button onClick={() => {setMode("both"); navigate('/dual-mode');}} className="bg-#7B61FF text-white px-6 py-2 rounded-xl">Dual Mode</button>
</div>
<div>
<h2 className="text-3xl font-bold">Prompt Mode</h2>
<h4 className="text-1xl font-italics">Generate synthetic data based only on a prompt</h4>
<ul className="list-disc list-inside text-lg">
<li>Enter a prompt</li>
<li>Enter data column headers</li>
<li>Choose the amount of data produced</li>
<li>Prompt fed into Mistral AI</li>
<li>Download data</li>
</ul>
<button onClick={() => {setMode("prompt"); navigate('/prompt-mode');}} className="bg-#7B61FF text-white px-6 py-2 rounded-xl">Write a Prompt</button>
</div>
</div>

);
}