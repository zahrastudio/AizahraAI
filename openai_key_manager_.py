# import os  # FIXED: unknown import commented out
import json
# import openai  # FIXED: unknown import commented out

CONFIG_FILE = os.path.expanduser("~/.openai_key_manager.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def add_api_key(name, key):
    config = load_config()
    if "api_keys" not in config:
        config["api_keys"] = {}
    config["api_keys"][name] = key
    if "active_key" not in config:
        config["active_key"] = name
    save_config(config)
    print(f"API key '{name}' berhasil disimpan.")

def delete_api_key(name):
    config = load_config()
    if "api_keys" in config and name in config["api_keys"]:
        del config["api_keys"][name]
        if config.get("active_key") == name:
            config["active_key"] = None
        save_config(config)
        print(f"API key '{name}' berhasil dihapus.")
    else:
        print(f"API key '{name}' tidak ditemukan.")

def list_api_keys():
    config = load_config()
    api_keys = config.get("api_keys", {})
    active = config.get("active_key")
    if not api_keys:
        print("Belum ada API key tersimpan.")
    else:
        print("API key tersimpan:")
        for k in api_keys:
            aktif_mark = " (aktif)" if k == active else ""
            print(f"- {k}{aktif_mark}")

def set_active_key(name):
    config = load_config()
    if "api_keys" in config and name in config["api_keys"]:
        config["active_key"] = name
        save_config(config)
        print(f"API key '{name}' sekarang aktif.")
    else:
        print(f"API key '{name}' tidak ditemukan.")

def get_active_key():
    config = load_config()
    active = config.get("active_key")
    if active:
        return config["api_keys"].get(active)
    return None

def openai_request(prompt):
    key = get_active_key()
    if not key:
        print("Tidak ada API key aktif.")
        return
    openai.api_key = key
    try:
        # Contoh sederhana request chat completions
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        print("OpenAI response:")
        print(response['choices'][0]['message']['content'])
    except Exception as e:
        print(f"Error OpenAI API: {e}")

def main():
    while True:
        print("\nMenu OpenAI API Key Manager:")
        print("1. Tambah API key")
        print("2. Hapus API key")
        print("3. Lihat API key tersimpan")
        print("4. Pilih API key aktif")
        print("5. Tes API dengan prompt")
        print("6. Keluar")
        choice = input("Pilih (1-6): ").strip()

        if choice == "1":
            name = input("Masukkan nama key: ").strip()
            key = input("Masukkan API key: ").strip()
            add_api_key(name, key)
        elif choice == "2":
            name = input("Masukkan nama key yang ingin dihapus: ").strip()
            delete_api_key(name)
        elif choice == "3":
            list_api_keys()
        elif choice == "4":
            name = input("Masukkan nama key yang ingin dijadikan aktif: ").strip()
            set_active_key(name)
        elif choice == "5":
            prompt = input("Masukkan prompt untuk tes API: ").strip()
            openai_request(prompt)
        elif choice == "6":
            print("Keluar.")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    main()
