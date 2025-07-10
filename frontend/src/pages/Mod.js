import { useNavigate } from 'react-router-dom';
import FileUpload from '../components/FileUpload';
import PromptSender from '../components/PromptSender';

export default function ModGEN() {
const navigate = useNavigate();
return (
<div className="p-10 max-w-4xl mx-auto space-y-6">
<h2 className="text-3xl font-bold">Mod Mode</h2>
<FileUpload />
<PromptSender />
<button onClick={() => navigate(-1)} className="bg-#7B61FF text-white px-6 py-2 rounded-xl">Back</button>
<button onClick={() => navigate('/settings-mod')} className="bg-#7B61FF text-white px-6 py-2 rounded-xl">Next</button>
</div>
);
}