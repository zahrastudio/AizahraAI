import subprocess
import sys
import requests
import csv
import os
import time
from packaging import version
from dotenv import load_dotenv

load_dotenv()

# Ambil token dan chat ID dari .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Paket yang akan dicek/upgrage
PAKET = [
    "moviepy",
    "gTTS",
    "pydub",
    "requests",
    "feedparser",
    "pyvis",
    "matplotlib",
    "networkx",
]

LOG_FILE = "upgrade_log.csv"
MAX_RETRY = 3

def get_installed_version(pkg):
    try:
        import pkg_resources
        return pkg_resources.get_distribution(pkg).version
    except Exception:
        return None

def get_pypi_version(pkg):
    try:
        url = f"https://pypi.org/pypi/{pkg}/json"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()["info"]["version"]
        else:
            return None
    except Exception:
        return None

def upgrade_package(pkg):
    """Upgrade paket dengan retry jika gagal."""
    for attempt in range(1, MAX_RETRY + 1):
        print(f"Upgrading {pkg} (Attempt {attempt}/{MAX_RETRY})...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", pkg],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{pkg} upgraded successfully.")
            return True
        else:
            print(f"Attempt {attempt} failed: {result.stderr.strip()}")
            time.sleep(3)  # delay sebelum retry
    return False

def compare_versions(local_ver, pypi_ver):
    if local_ver is None:
        return "upgrade"
    try:
        lv = version.parse(local_ver)
        pv = version.parse(pypi_ver)
        if lv < pv:
            return "upgrade"
        elif lv > pv:
            return "downgrade"
        else:
            return "same"
    except Exception:
        return "compare_fail"

def save_log_versions(log_versions):
    with open(LOG_FILE, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Package", "Version"])
        for pkg, ver in log_versions.items():
            writer.writerow([pkg, ver or "N/A"])

def kirim_notifikasi_telegram(pesan: str) -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: TELEGRAM_BOT_TOKEN atau TELEGRAM_CHAT_ID belum diatur di .env")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            return True
        else:
            print(f"Gagal mengirim notifikasi. Response: {response.text}")
            return False
    except Exception as e:
        print(f"Exception kirim notifikasi Telegram: {e}")
        return False

def main():
    log_versions = {}
    upgrade_results = []
    ada_upgrade = False

    print(f"{'Package':15} | {'Local Version':15} | {'PyPI Version':15} | Status")
    print("-" * 70)

    for pkg in PAKET:
        local_ver = get_installed_version(pkg)
        pypi_ver = get_pypi_version(pkg)

        if pypi_ver is None:
            status = "PyPI unavailable"
        else:
            cmp_result = compare_versions(local_ver, pypi_ver)
            if cmp_result == "upgrade":
                sukses_upgrade = upgrade_package(pkg)
                if sukses_upgrade:
                    local_ver = get_installed_version(pkg)
                    status = "Upgraded"
                    ada_upgrade = True
                else:
                    status = "Failed upgrade"
            elif cmp_result == "downgrade":
                status = "Local newer"
            elif cmp_result == "same":
                status = "Up to date"
            else:
                status = "Compare fail"

        log_versions[pkg] = local_ver or "N/A"
        upgrade_results.append(f"{pkg}: {status}")
        print(f"{pkg:15} | {local_ver or 'N/A':15} | {pypi_ver or 'N/A':15} | {status}")

    save_log_versions(log_versions)
    print(f"Log saved to {LOG_FILE}")

    # Kirim notifikasi Telegram
    pesan = "<b>Hasil Upgrade Paket Python</b>\n"
    pesan += "\n".join(upgrade_results)
    notif_sukses = kirim_notifikasi_telegram(pesan)

    if notif_sukses:
        print("Notifikasi Telegram terkirim.")
    else:
        print("Gagal mengirim notifikasi Telegram.")

if __name__ == "__main__":
    main()

