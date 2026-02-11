import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine
} from 'recharts';

function App() {
  const [data, setData] = useState([]);
  const [events, setEvents] = useState([]);
  const [stats, setStats] = useState({});

  // Date Filter State
  const [startDate, setStartDate] = useState('2010-01-01');
  const [endDate, setEndDate] = useState('2022-12-31');

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/oil-prices').then(res => setData(res.data));
    axios.get('http://127.0.0.1:5000/api/stats').then(res => setStats(res.data));
    axios.get('http://127.0.0.1:5000/api/events').then(res => setEvents(res.data));
  }, []);

  // Filter Logic
  const filteredData = data.filter(item => item.Date >= startDate && item.Date <= endDate);

  return (
    <div className="App" style={{ padding: "20px", fontFamily: "Arial", backgroundColor: "#f5f5f5", minHeight: "100vh" }}>
      <h1 style={{ color: "#333" }}>🛢️ Birhan Energies: Strategic Market Dashboard</h1>

      {/* Control Panel */}
      <div style={{ background: "white", padding: "15px", borderRadius: "8px", marginBottom: "20px", display: "flex", gap: "20px", alignItems: "center" }}>
        <div>
          <label><strong>Start Date: </strong></label>
          <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
        </div>
        <div>
          <label><strong>End Date: </strong></label>
          <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} />
        </div>
        <div style={{ marginLeft: "auto" }}>
          <strong>Current Price:</strong> ${stats.current_price} | <strong>Regimes:</strong> {stats.regimes_detected}
        </div>
      </div>

      <div style={{ height: "600px", width: "100%", background: "#fff", padding: "20px", borderRadius: "10px", boxShadow: "0 4px 6px rgba(0,0,0,0.1)" }}>
        <h3>Brent Oil Price Regimes & Geopolitical Events</h3>
        <ResponsiveContainer width="100%" height="90%">
          <LineChart data={filteredData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
            <XAxis dataKey="Date" minTickGap={50} />
            <YAxis domain={[0, 140]} />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="Price" stroke="#8884d8" dot={false} strokeWidth={1} name="Market Price" />
            <Line type="step" dataKey="Regime_Mean" stroke="#ff4d4d" dot={false} strokeWidth={2} name="Regime Mean" />

            {/* Render Events (Only if they are within range) */}
            {events.filter(e => e.date >= startDate && e.date <= endDate).map((event, index) => (
              <ReferenceLine
                key={index}
                x={event.date}
                stroke="orange"
                strokeDasharray="3 3"
                label={{ position: 'top', value: '📍', fontSize: 16 }}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default App;
