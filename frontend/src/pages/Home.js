import { useNavigate } from 'react-router-dom';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 to-black text-white">
      <h1 className="text-5xl font-bold mb-4">Let’s get started...</h1>
      <button
        onClick={() => navigate('/data-selector')}
        className="px-6 py-3 bg-#7B61FF hover:bg-blue-700 rounded-xl text-xl"
      >
        Start
      </button>
    </div>
  );
}

