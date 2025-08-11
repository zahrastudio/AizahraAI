<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>AizahraAI Map & Video</title>
</head>
<body>
  <h1>AizahraAI - Peta & Video Capture</h1>

  <h2>Peta Google Maps</h2>
  <iframe
    width="600"
    height="450"
    style="border:0"
    loading="lazy"
    allowfullscreen
    src="https://www.google.com/maps/embed/v1/view?key=YOUR_GOOGLE_MAPS_API_KEY&center=-6.2088,106.8456&zoom=12">
  </iframe>

  <h2>Live Video Capture</h2>
  <img src="{{ url_for('video_feed') }}" width="600" />
</body>
</html>
