import { useNavigate } from 'react-router-dom';
import DomainSelect from '../components/DomainSelect';
import ColumnEditor from '../components/ColumnEditor';
import RowSelector from '../components/RowSelector';
import OutputPath from '../components/OutputPath';

export default function Settings() {
const navigate = useNavigate();
return (
<div className="p-10 max-w-4xl mx-auto space-y-4">
<h2 className="text-2xl font-bold">Settings</h2>
<DomainSelect />
<OutputPath />
<ColumnEditor />
<button onClick={() => navigate('/privacy')} className="bg-#7B61FF text-white px-6 py-2 rounded-xl">Next</button>
</div>
);
}