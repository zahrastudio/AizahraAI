#!/bin/bash
# Skrip ini untuk setup environment, buat React PWA dan backend Node.js minimal
# Jangan lupa ganti OPENAI_API_KEY di .env backend nanti dengan API kamu sendiri

echo "[1/10] Update & upgrade paket Termux..."
pkg update -y && pkg upgrade -y

echo "[2/10] Install nodejs, git, python, curl, wget..."
pkg install -y nodejs git python curl wget

echo "[3/10] Install yarn (optional tapi direkomendasikan)..."
npm install -g yarn

echo "[4/10] Buat folder kerja proyek ZahraApp dan masuk ke folder frontend..."
mkdir -p ~/ZahraApp && cd ~/ZahraApp
npx create-vite@latest zahra-frontend -- --template react
cd zahra-frontend

echo "[5/10] Install dependencies frontend..."
yarn install

echo "[6/10] Buat file service worker PWA sederhana (opsional, bisa dikembangkan)..."
cat > src/service-worker.js << 'EOF'
self.addEventListener('install', event => {
  self.skipWaiting();
});
self.addEventListener('activate', event => {
  clients.claim();
});
EOF

echo "[7/10] Tambahkan konfigurasi PWA di vite.config.js (optional minimal)..."
# Tambahkan konfigurasi PWA nanti manual jika ingin lanjut

echo "[8/10] Kembali ke folder proyek utama dan buat backend minimal..."
cd ~/ZahraApp
mkdir zahra-backend && cd zahra-backend

echo "[9/10] Inisialisasi npm, install express, dotenv, axios..."
npm init -y
npm install express dotenv axios cors

echo "[10/10] Buat file server.js untuk backend minimal..."
cat > server.js << 'EOF'
require('dotenv').config();
const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.post('/api/chat', async (req, res) => {
  const prompt = req.body.prompt;
  if (!prompt) return res.status(400).json({error: 'Prompt kosong'});

  try {
    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: "gpt-4o-mini",
        messages: [{role: "user", content: prompt}],
        max_tokens: 500,
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
          'Content-Type': 'application/json',
        }
      }
    );
    const message = response.data.choices[0].message.content;
    res.json({ reply: message });
  } catch (error) {
    console.error(error.response ? error.response.data : error.message);
    res.status(500).json({ error: 'Gagal memproses permintaan' });
  }
});

app.listen(port, () => {
  console.log(`Backend berjalan di http://localhost:${port}`);
});
EOF

echo "[11/10] Buat file .env untuk OpenAI API KEY (ganti YOUR_API_KEY_HERE dengan milikmu)..."
cat > .env << EOF
OPENAI_API_KEY=YOUR_API_KEY_HERE
EOF

echo "Setup selesai!"
echo "Cara menjalankan backend:"
echo "cd ~/ZahraApp/zahra-backend && node server.js"
echo "Cara menjalankan frontend:"
echo "cd ~/ZahraApp/zahra-frontend && yarn dev"
echo ""
echo "Frontend akan berjalan di http://localhost:5173"
echo "Backend API ada di http://localhost:3000/api/chat"
echo ""
echo "Pastikan kamu sudah isi .env di backend dengan API Key OpenAI-mu."

