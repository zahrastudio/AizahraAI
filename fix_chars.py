# import os  # FIXED: unknown import commented out

# Direktori kerja, sesuaikan jika perlu
DIR = "."

# Karakter bermasalah dan penggantinya
replacements = {
    "-": "-",   # em dash jadi minus
    "-": "-",   # en dash jadi minus
    """: '"',   # kutip buka jadi kutip biasa
    """: '"',   # kutip tutup jadi kutip biasa
    "'": "'",   # kutip tunggal buka jadi apostrof
    "'": "'",   # kutip tunggal tutup jadi apostrof
    # Tambahkan jika ada karakter lain yang mau diganti
}

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    for wrong, correct in replacements.items():
        content = content.replace(wrong, correct)

    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[FIXED] {filepath}")
    else:
        print(f"[OK] {filepath}")

def main():
    for root, _, files in os.walk(DIR):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                fix_file(full_path)

if __name__ == "__main__":
    main()
