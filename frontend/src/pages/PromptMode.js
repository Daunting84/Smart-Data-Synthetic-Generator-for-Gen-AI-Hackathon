import { useNavigate } from 'react-router-dom';
import PromptSender from '../components/PromptSender';

export default function PromptMode() {
const navigate = useNavigate();

return (
<div className="p-10 max-w-4xl mx-auto space-y-4">
<h2 className="text-3xl font-bold">Prompt Mode</h2>
<PromptSender />
<button onClick={() => navigate(-1)} className="bg-#7B61FF text-white px-6 py-2 rounded-xl">Back</button>
<button onClick={() => navigate('/settings')} className="bg-#7B61FF text-white px-6 py-2 rounded-xl">Next</button>
</div>
);
}