import sys
from openai import OpenAI
from api_key_manager import get_openai_api_key


def main():
    try:
        api_key = get_openai_api_key()
    except ValueError as e:
        print("ERROR:", e)
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    print("===== AizahraAI Chat =====")
    print("---")
    print("بسم الله الرحمن الرحيم")
    print("Dengan nama Allah Yang Maha Pengasih, Maha Penyayang.")
    print("---\n")
    print("Assalamu'alaikum, ada yang bisa saya bantu?")
    print("\n---")
    print("والله أعلم")
    print("Dan hanya Allah yang Maha Mengetahui")
    print("---")
    print("Ketik pesan untuk chat dengan AI.")
    print("Perintah khusus:")
    print("  /help  - Bantuan")
    print("  /reset - Reset sesi chat")
    print("  /exit  - Keluar program\n")

    chat_history = []

    while True:
        try:
            user_input = input("Anda: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nKeluar dari program.")
            break

        if user_input.lower() in ["/exit", "exit"]:
            print("Keluar dari program.")
            break
        elif user_input.lower() == "/help":
            print("Perintah khusus yang bisa digunakan:")
            print("  /help  : Tampilkan bantuan ini")
            print("  /reset : Hapus riwayat chat, mulai ulang sesi")
            print("  /exit  : Keluar dari aplikasi")
            continue
        elif user_input.lower() == "/reset":
            chat_history = []
            print("Riwayat chat telah direset.")
            continue
        elif user_input == "":
            continue

        chat_history.append({"role": "user", "content": user_input})

        try:
            api_key = get_openai_api_key()
            client.api_key = api_key

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=chat_history,
                max_tokens=1000,
                temperature=0.7,
            )
            assistant_message = response.choices[0].message.content
            print("AizahraAI:", assistant_message)
            chat_history.append({"role": "assistant", "content": assistant_message})

        except Exception as e:
            print(f"Error OpenAI API: {e}")
            break

if __name__ == "__main__":
    main()



