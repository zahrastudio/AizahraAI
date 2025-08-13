const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.send('Backend API for ChatGPT Multifunction Web');
});

// TODO: add routes for ChatGPT, Google Maps, Al-Qur'an, etc.

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

