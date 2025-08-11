import subprocess
import json

def get_location():
    try:
        result = subprocess.run(["termux-location", "-p", "gps"], capture_output=True, text=True)
        output = result.stdout.strip()
        if not output:
            raise ValueError("Output dari GPS kosong")
        location = json.loads(output)
        return location
    except Exception as e:
        print(f"Error getting location: {e}")
        return None


