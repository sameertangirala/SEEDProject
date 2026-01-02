import { useEffect, useState } from "react";
import Dashboard from "./pages/Dashboard";
import "./App.css";

function App() {
  const [apps, setApps] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/apps/")
      .then((res) => res.json())
      .then((data) => setApps(data))
      .catch((err) => console.error("Error fetching apps:", err));
  }, []);

  return (
    <div className="app-container">
      <h1>Redwood SEED Scholar Portal</h1>
      <Dashboard apps={apps} />
    </div>
  );
}

export default App;
