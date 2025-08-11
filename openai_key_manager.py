# import os  # FIXED: unknown import commented out
# from dotenv import load_dotenv, set_key, unset_key, find_dotenv  # FIXED: unknown import commented out
# from openai import OpenAI  # FIXED: unknown import commented out

load_dotenv()
ENV_PATH = find_dotenv()

def list_api_keys():
    print("Daftar API key di .env:")
    keys = [k for k in os.environ if k.startswith("OPENAI_KEY_")]
    if not keys:
        print("  Tidak ada API key tersimpan.")
        return []
    for k in keys:
        active_mark = "(aktif)" if os.getenv("OPENAI_API_KEY") == os.getenv(k) else ""
        print(f"  {k} {active_mark}")
    return keys

def add_api_key():
    nama = input("Masukkan nama key baru (contoh: OPENAI_KEY_1): ").strip().upper()
    if not nama.startswith("OPENAI_KEY_"):
        print("Nama key harus diawali dengan 'OPENAI_KEY_'")
        return
    if nama in os.environ:
        print("Key sudah ada.")
        return
    value = input("Masukkan nilai API key: ").strip()
    set_key(ENV_PATH, nama, value)
    print(f"API key '{nama}' berhasil disimpan ke .env")

def delete_api_key():
    keys = list_api_keys()
    if not keys:
        return
    nama = input("Masukkan nama key yang ingin dihapus: ").strip().upper()
    if nama not in keys:
        print("Key tidak ditemukan.")
        return
    unset_key(ENV_PATH, nama)
    print(f"API key '{nama}' berhasil dihapus.")

def select_active_key():
    keys = list_api_keys()
    if not keys:
        return
    nama = input("Masukkan nama key yang ingin dijadikan aktif: ").strip().upper()
    if nama not in keys:
        print("Key tidak ditemukan.")
        return
    value = os.getenv(nama)
    set_key(ENV_PATH, "OPENAI_API_KEY", value)
    print(f"API key '{nama}' sudah dijadikan aktif sebagai OPENAI_API_KEY")

def test_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Tidak ada API key aktif. Silakan pilih API key aktif terlebih dahulu.")
        return
    client = OpenAI(api_key=api_key)
    prompt = input("Masukkan prompt untuk tes API: ").strip()
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        print("\nResponse dari OpenAI:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error OpenAI API:\n{str(e)}")

def main():
    while True:
        print("\nMenu OpenAI API Key Manager:")
        print("1. Tambah API key")
        print("2. Hapus API key")
        print("3. Lihat API key tersimpan")
        print("4. Pilih API key aktif")
        print("5. Tes API dengan prompt")
        print("6. Keluar")
        pilih = input("Pilih (1-6): ").strip()
        if pilih == "1":
            add_api_key()
        elif pilih == "2":
            delete_api_key()
        elif pilih == "3":
            list_api_keys()
        elif pilih == "4":
            select_active_key()
        elif pilih == "5":
            test_api_key()
        elif pilih == "6":
            print("Keluar.")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    main()
