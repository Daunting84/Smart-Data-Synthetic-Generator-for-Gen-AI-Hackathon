import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import DataSelector from './pages/DataSelector';
import DataMode from './pages/DataMode';
import PromptMode from './pages/PromptMode';
import DualMode from './pages/DualMode';
import PrivacySettings from './pages/PrivacySettings';
import Generator from './pages/Generator';
import Validation from './pages/Validation';
import ModGEN from './pages/ModGEN';
import GenEN from './pages/GenEN';
import Mod from './pages/Mod';
import Settings from './pages/Settings';
import SettingsData from './pages/SettingsData';
import SettingsMod from './pages/SettingsMod';

/*
import DomainSelect from './pages/DomainSelect';
import ColumnEditor from './pages/ColumnEditor';4
*/
export default function App() {
return (
<Router>
<Routes>
<Route path="/" element={<Home />} />
<Route path="/data-selector" element={<DataSelector />} />
<Route path="/data-mode" element={<DataMode />} />
<Route path="/prompt-mode" element={<PromptMode />} />
<Route path="/dual-mode" element={<DualMode />} />
<Route path="/privacy" element={<PrivacySettings />} />
<Route path="/generate" element={<Generator />} />
<Route path="/validate" element={<Validation />} />
<Route path="/mod-gen" element={<ModGEN />} />
<Route path="/gen-en" element={<GenEN />} />
<Route path="/mod" element={<Mod />} />
<Route path="/settings" element={<Settings />} />
<Route path="/settings-data" element={<SettingsData />} />
<Route path="/settings-mod" element={<SettingsMod />} />

</Routes>
</Router>
);
}
/*
<Route path="/domain" element={<DomainSelect />} />
<Route path="/columns" element={<ColumnEditor />} />
*/