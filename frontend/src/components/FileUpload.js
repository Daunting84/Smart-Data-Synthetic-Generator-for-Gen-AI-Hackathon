import { useState } from "react";

export default function FileUpload() {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first.");
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${process.env.REACT_APP_API_URL}/upload-file/`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    console.log("Uploaded file info:", data);
    // You can now send the file path (data.filepath) to other backend endpoints if needed
  };

  return (
    <div className="border-2 border-dashed border-gray-400 rounded-xl p-6 w-full max-w-xl text-center">
      <p className="mb-2">Select a file or drag and drop your dataset here</p>
      <p className="text-sm text-gray-400">CSV, JSON or XLSX</p>
      <input type="file" className="mt-4" onChange={handleFileChange} />
      <button onClick={handleUpload} className="mt-4 bg-#7B61FF text-white px-6 py-2 rounded-xl">
        Upload File
      </button>
    </div>
  );
}
