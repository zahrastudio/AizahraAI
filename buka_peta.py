# import webbrowser  # FIXED: unknown import commented out

def buka_peta(latitude, longitude):
    url = f"https://www.google.com/maps/@{latitude},{longitude},15z"
    webbrowser.open(url)

if __name__ == "__main__":
    buka_peta(-6.2088, 106.8456)  # Contoh koordinat Jakarta

