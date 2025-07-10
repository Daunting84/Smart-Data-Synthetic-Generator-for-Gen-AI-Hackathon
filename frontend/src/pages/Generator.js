import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Generator() {
  const navigate = useNavigate();
  const [status, setStatus] = useState("starting");

  useEffect(() => {
    const interval = setInterval(async () => {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/generation-status`);
      const data = await res.json();
          
      console.log("⏳ Generation status:", data.status);
      setStatus(data.status);

      if (data.status === "completed") {
        clearInterval(interval);
        navigate("/validate");
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [navigate]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen space-y-6">
      <h2 className="text-3xl font-bold">Generating Data...</h2>
      <p className="text-lg">Status: {status}</p>
      <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-#7B61FF"></div>
    </div>
  );
}