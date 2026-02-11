import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine
} from 'recharts';
import './App.css';

function App() {
  const [data, setData] = useState([]);
  const [stats, setStats] = useState({});

  useEffect(() => {
    // Fetch Data from Flask
    axios.get('http://127.0.0.1:5000/api/oil-prices')
      .then(response => setData(response.data))
      .catch(error => console.error("Error fetching data:", error));

    axios.get('http://127.0.0.1:5000/api/stats')
      .then(response => setStats(response.data))
      .catch(error => console.error("Error fetching stats:", error));
  }, []);

  return (
    <div className="App" style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🛢️ Birhan Energies: Market Intelligence Dashboard</h1>

      <div style={{ display: "flex", gap: "20px", marginBottom: "20px" }}>
        <div className="card">Current Price: ${stats.current_price}</div>
        <div className="card">Regimes Detected: {stats.regimes_detected}</div>
        <div className="card">Range: {stats.start_date} to {stats.end_date}</div>
      </div>

      <div style={{ height: "500px", width: "100%", background: "#fff", padding: "20px", borderRadius: "10px", boxShadow: "0 0 10px rgba(0,0,0,0.1)" }}>
        <h3>Brent Oil Prices & Structural Breaks (2010-2022)</h3>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="Date" tick={{ fontSize: 12 }} minTickGap={50} />
            <YAxis domain={['auto', 'auto']} />
            <Tooltip />
            <Legend />
            {/* Actual Price */}
            <Line type="monotone" dataKey="Price" stroke="#8884d8" dot={false} strokeWidth={1} name="Daily Price" />
            {/* Regime Mean (The red line) */}
            <Line type="step" dataKey="Regime_Mean" stroke="#ff0000" dot={false} strokeWidth={2} name="Regime Mean" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default App;
