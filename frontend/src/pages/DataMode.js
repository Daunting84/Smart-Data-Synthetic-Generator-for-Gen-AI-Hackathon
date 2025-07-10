import { useNavigate } from 'react-router-dom';
import FileUpload from '../components/FileUpload';

export default function DataMode() {
const navigate = useNavigate();
return (
<div className="p-10 max-w-4xl mx-auto space-y-6">
<h2 className="text-3xl font-bold">Data Mode</h2>
<ul className="list-disc list-inside text-lg">
<li>Upload CSV, JSON or XLSX</li>
<li>Receive key data insights</li>
<li>Choose the amount of data produced</li>
<li>Analyzed and replicated by CTGAN</li>
<li>Adjust privacy features</li>
<li>Receive data validation results</li>
<li>Download data</li>
</ul>
<FileUpload />
<button onClick={() => navigate(-1)} className="bg-#7B61FF text-white px-6 py-2 rounded-xl">Back</button>
<button onClick={() => navigate('/settings-data')} className="bg-#7B61FF text-white px-6 py-2 rounded-xl">Next</button>
</div>
);
}