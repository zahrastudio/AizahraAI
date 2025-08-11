import requests
from datetime import datetime

# Lokasi kamu (contoh: Jakarta)
LATITUDE = -6.2
LONGITUDE = 106.816666
TIMEZONE = 7  # WIB (UTC+7)

# 1. Dapatkan waktu sholat dari Aladhan API
pray_url = f"https://api.aladhan.com/v1/timings?latitude={LATITUDE}&longitude={LONGITUDE}&method=2&timezonestring=Asia/Jakarta"
pray_res = requests.get(pray_url).json()

# 2. Dapatkan tanggal Hijriah dari Aladhan juga
hijri_date = pray_res['data']['date']['hijri']['date']
gregorian_date = pray_res['data']['date']['gregorian']['date']
weekday = pray_res['data']['date']['gregorian']['weekday']['en']

# 3. Ambil waktu-waktu
timings = pray_res['data']['timings']

# 4. Tampilkan semua
print(f"Hari ini: {weekday}, {gregorian_date} M / {hijri_date} H\n")
print("🕌 Waktu Sholat:")
print(f"  Subuh    : {timings['Fajr']}")
print(f"  Terbit   : {timings['Sunrise']}")
print(f"  Dzuhur   : {timings['Dhuhr']}")
print(f"  Ashar    : {timings['Asr']}")
print(f"  Maghrib  : {timings['Maghrib']}")
print(f"  Isya     : {timings['Isha']}")
print(f"  Terbenam : {timings['Sunset']}")
print(f"\nZona Waktu: UTC+{TIMEZONE} (Asia/Jakarta)")

