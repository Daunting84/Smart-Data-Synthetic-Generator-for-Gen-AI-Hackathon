import { useNavigate } from 'react-router-dom';

export default function DualMode() {
const navigate = useNavigate();

const setDualMode = async (user_intent) => {
    await fetch(`${process.env.REACT_APP_API_URL}/set-dual-mode`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_intent }),
    });
  };
return (
<div className="p-10 max-w-4xl mx-auto space-y-6">
<div>
<h2 className="text-3xl font-bold">ModGEN Mode</h2>
<ul className="list-disc list-inside text-lg">
<li>Great for producing synthetic data that mirrors compliant, cleaned input.</li>
<li>Modify your database first with a prompt, then generate synthetic data based on the new database. Ensures that synthetic data is generated from already-cleaned, privacy-compliant input, preserving structural integrity and compliance from the source.</li>
</ul>
<button onClick={() => {setDualMode("modgen"); navigate('/mod-gen');}} className="bg-#7B61FF text-white px-6 py-2 rounded-xl">Select</button>
</div>
<div>
<h2 className="text-3xl font-bold">GenEN Mode</h2>
<ul className="list-disc list-inside text-lg">
<li>Great for fine tuning your synthetic data</li>
<li>Generate synthetic data first, the modify it with a prompt. Enables rapid scaling by generating large amounts of base data first, then customizing or augmenting it for specific domains, personas, or formats.</li>
</ul>
<button onClick={() => {setDualMode("genen"); navigate('/gen-en');}} className="bg-#7B61FF text-white px-6 py-2 rounded-xl">Select</button>
</div>
<div>
<h2 className="text-3xl font-bold">Mod Mode</h2>
<ul className="list-disc list-inside text-lg">
<li>Great for quick and easy fine tuning of your pre-existing data</li>
<li>Modify your data however you see fit, with just a prompt. Allows precise control over existing datasets by applying targeted transformations without altering overall data distribution.</li>
</ul>
<button onClick={() => {setDualMode("mod"); navigate('/mod');}} className="bg-#7B61FF text-white px-6 py-2 rounded-xl">Select</button>
</div>
</div>

);
}