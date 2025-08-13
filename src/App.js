import React, { useState, useEffect, useRef } from 'react';

// Fungsi untuk load Google Maps script dinamis
function loadScript(url) {
  return new Promise((resolve) => {
    const existingScript = document.querySelector(`script[src="${url}"]`);
    if (!existingScript) {
      const script = document.createElement('script');
      script.src = url;
      script.async = true;
      script.onload = () => resolve(true);
      document.body.appendChild(script);
    } else {
      resolve(true);
    }
  });
}

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

function App() {
  // State untuk chat history [{role:'user'|'bot', text: '...'}, ...]
  const [chatHistory, setChatHistory] = useState([]);
  const [chatInput, setChatInput] = useState('');

  // Ref untuk map & infoWindow agar tidak hilang saat re-render
  const mapRef = useRef(null);
  const infoWindowRef = useRef(null);
  // Ref untuk div chat container supaya bisa scroll otomatis
  const chatBoxRef = useRef(null);

  // Load Google Maps once
  useEffect(() => {
    const apiKey = process.env.REACT_APP_GOOGLE_MAPS_API_KEY; // Pastikan sudah diset di .env
    if (!apiKey) {
      console.error('Google Maps API key is missing in .env');
      return;
    }

    loadScript(`https://maps.googleapis.com/maps/api/js?key=${apiKey}`).then(() => {
      // Inisialisasi map
      mapRef.current = new window.google.maps.Map(document.getElementById('map'), {
        center: { lat: -6.200000, lng: 106.816666 }, // Jakarta
        zoom: 10,
      });

      // Buat info window
      infoWindowRef.current = new window.google.maps.InfoWindow();

      // Marker contoh
      const marker = new window.google.maps.Marker({
        position: { lat: -6.200000, lng: 106.816666 },
        map: mapRef.current,
        title: 'Marker di Jakarta',
      });

      // Event klik marker untuk buka info window
      marker.addListener('click', () => {
        infoWindowRef.current.setContent('<div><strong>Ini Jakarta</strong><br>Ini adalah info window.</div>');
        infoWindowRef.current.open(mapRef.current, marker);
      });
    });
  }, []);

  // Load chatHistory dari localStorage saat awal render
  useEffect(() => {
    const saved = localStorage.getItem('chatHistory');
    if (saved) setChatHistory(JSON.parse(saved));
  }, []);

  // Simpan chatHistory ke localStorage setiap kali berubah
  useEffect(() => {
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
  }, [chatHistory]);

  // Scroll chat container ke bawah setiap kali chatHistory berubah
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [chatHistory]);

  // Fungsi kirim chat ke backend
  const handleSendChat = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    // Tambah user message ke chat history
    setChatHistory((prev) => [...prev, { role: 'user', text: chatInput }]);
    setChatInput('');

    try {
      const res = await fetch(`${BACKEND_URL}/api/chatgpt`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: chatInput }),
      });
      const data = await res.json();

      // Tambah bot response ke chat history
      if (data.result) {
        setChatHistory((prev) => [...prev, { role: 'bot', text: data.result }]);
      } else {
        setChatHistory((prev) => [...prev, { role: 'bot', text: 'Gagal mendapatkan respons dari server' }]);
      }
    } catch (error) {
      setChatHistory((prev) => [...prev, { role: 'bot', text: 'Error: ' + error.message }]);
    }
  };

  return (
    <div style={{ padding: 20, maxWidth: 700, margin: 'auto' }}>
      <h1>Chat dengan Riwayat & Google Maps Info Window</h1>

      <section style={{ marginBottom: 30 }}>
        <h2>Chat</h2>
        <div
          ref={chatBoxRef}
          style={{
            border: '1px solid #ccc',
            padding: 10,
            height: 300,
            overflowY: 'auto',
            backgroundColor: '#fafafa',
          }}
        >
          {chatHistory.length === 0 && <p>Mulai chat dengan mengetik di bawah...</p>}
          {chatHistory.map((msg, idx) => (
            <div
              key={idx}
              style={{
                textAlign: msg.role === 'user' ? 'right' : 'left',
                marginBottom: 8,
              }}
            >
              <span
                style={{
                  display: 'inline-block',
                  padding: '8px 12px',
                  borderRadius: 16,
                  backgroundColor: msg.role === 'user' ? '#007bff' : '#e5e5ea',
                  color: msg.role === 'user' ? 'white' : 'black',
                  maxWidth: '80%',
                  wordWrap: 'break-word',
                }}
              >
                {msg.text}
              </span>
            </div>
          ))}
        </div>

        <form onSubmit={handleSendChat} style={{ marginTop: 10, display: 'flex' }}>
          <input
            type="text"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            placeholder="Tulis pesan..."
            style={{ flexGrow: 1, padding: 10, fontSize: 16 }}
            required
          />
          <button type="submit" style={{ padding: '10px 20px', marginLeft: 8 }}>
            Kirim
          </button>
        </form>
      </section>

      <section>
        <h2>Google Maps</h2>
        <div id="map" style={{ width: '100%', height: 400, border: '1px solid #ccc' }}></div>
      </section>
    </div>
  );
}

export default App;

