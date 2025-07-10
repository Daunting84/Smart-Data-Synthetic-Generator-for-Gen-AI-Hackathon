import { useState } from 'react';

export default function PromptSender() {
const [prompt, setPrompt] = useState('');
const submitPrompt = async () => {
  await fetch(`${process.env.REACT_APP_API_URL}/set-prompt`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ custom_prompt: prompt }),
  });
};
return (
<div className="p-10 max-w-4xl mx-auto space-y-4">
<textarea
className="w-full border rounded p-4 text-lg"
rows={4}
placeholder="Enter a prompt"
value={prompt}
onChange={(e) => setPrompt(e.target.value)}
/>
<button onClick={() => submitPrompt()} className="bg-purple-500 text-white px-6 py-2 rounded-xl">Submit</button>
</div>
);
}