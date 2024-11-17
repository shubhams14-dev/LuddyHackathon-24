import React, { useState } from "react";
import ContactCard from "./components/ContactCard";
import "./styles/App.css";

function App() {
  const [productName, setProductName] = useState("");
  const [repositoryName, setRepositoryName] = useState("");
  const [contact, setContact] = useState(null);
  const [error, setError] = useState("");

  const fetchContact = async () => {
    setError("");
    setContact(null);
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/contacts?${
          productName ? `product_name=${productName}` : `repository_name=${repositoryName}`
        }`
      );
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error);
      }
      setContact(data);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900">Contact Lookup</h2>
          <p className="mt-2 text-gray-600">Search contacts by product or repository name</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md space-y-4">
          <div className="space-y-4">
            <input
              type="text"
              placeholder="Product Name"
              className="input-field"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
            />
            
            <div className="text-center text-gray-500">OR</div>
            
            <input
              type="text"
              placeholder="Repository Name"
              className="input-field"
              value={repositoryName}
              onChange={(e) => setRepositoryName(e.target.value)}
            />
          </div>

          <button
            onClick={fetchContact}
            className="button-primary w-full"
          >
            Search Contact
          </button>
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">
            {error}
          </div>
        )}

        {contact && <ContactCard contact={contact} />}
      </div>
    </div>
  );
}

export default App;