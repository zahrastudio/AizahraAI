
import curses
import subprocess
import json
import os

QURAN_JSON = 'data/quran_text.json'
AUDIO_DIR = 'audio'
BOOKMARK_FILE = 'bookmark.txt'

MUQRI_LIST = ['Abdul Basit', 'Mishary Rashid', 'Saad Al-Ghamdi']

def load_quran():
    with open(QURAN_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_bookmark(ayat_num):
    with open(BOOKMARK_FILE, 'w') as f:
        f.write(str(ayat_num))

def load_bookmark():
    if os.path.exists(BOOKMARK_FILE):
        with open(BOOKMARK_FILE, 'r') as f:
            try:
                return int(f.read())
            except:
                return 1
    return 1

def play_audio(ayat_num, muqri_index):
    muqri_name = MUQRI_LIST[muqri_index].lower().replace(' ', '_')
    filename = f'quran_1_{ayat_num}_{muqri_name}.mp3'
    path = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(path):
        # Mainkan audio tanpa blocking
        subprocess.Popen(['mpv', '--no-video', path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    else:
        return False

def main(stdscr):
    curses.curs_set(0)
    quran = load_quran()
    muqri_index = 0
    search_query = ''
    bookmark = load_bookmark()
    ayat_num = bookmark

    keys_sorted = sorted(quran.keys(), key=lambda x: int(x.split('_')[1]))

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(0, 0, "Pilih Ayat (Panah atas/bawah), 'c' Cari, 'm' Muqri, Enter mainkan, 'q' Keluar")
        stdscr.addstr(1, 0, f"Muqri: {MUQRI_LIST[muqri_index]} | Cari: {search_query}")

        # Filter ayat berdasarkan search query
        filtered_keys = []
        for key in keys_sorted:
            arab = quran[key]['arab']
            latin = quran[key]['latin']
            if search_query.lower() in arab.lower() or search_query.lower() in latin.lower():
                filtered_keys.append(key)
        if not filtered_keys:
            filtered_keys = keys_sorted

        # Pastikan ayat_num valid
        if ayat_num < 1 or ayat_num > len(filtered_keys):
            ayat_num = 1

        # Hitung area tampilan list agar tidak overflow layar
        list_area_height = h - 7  # sisakan baris utk info ayat dan instruksi

        start_index = 0
        if ayat_num > list_area_height:
            start_index = ayat_num - list_area_height

        for i, key in enumerate(filtered_keys[start_index:start_index+list_area_height]):
            nomor_ayat = int(key.split('_')[1])
            prefix = "-> " if (start_index + i + 1) == ayat_num else "   "
            text = f"{prefix}Ayat {nomor_ayat} - {quran[key]['latin'][:w-15]}"
            stdscr.addstr(i+3, 0, text)

        # Tampilkan detail ayat terpilih
        selected_key = filtered_keys[ayat_num - 1]
        ayat_arab = quran[selected_key]['arab']
        ayat_latin = quran[selected_key]['latin']
        ayat_id = quran[selected_key]['id']

        stdscr.addstr(h-3, 0, f"Arab  : {ayat_arab[:w-8]}")
        stdscr.addstr(h-2, 0, f"Latin : {ayat_latin[:w-8]}")
        stdscr.addstr(h-1, 0, f"Arti  : {ayat_id[:w-8]}")

        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            ayat_num = max(1, ayat_num - 1)
        elif key == curses.KEY_DOWN:
            ayat_num = min(len(filtered_keys), ayat_num + 1)
        elif key == ord('q'):
            break
        elif key == ord('m'):
            muqri_index = (muqri_index + 1) % len(MUQRI_LIST)
        elif key == ord('c'):
            curses.echo()
            stdscr.addstr(h-5, 0, "Masukkan kata kunci cari: ")
            stdscr.clrtoeol()
            search_query = stdscr.getstr(h-5, 23, 60).decode('utf-8').strip()
            curses.noecho()
            ayat_num = 1
        elif key == 10:  # Enter key
            # Mainkan audio dan simpan bookmark
            berhasil = play_audio(int(selected_key.split('_')[1]), muqri_index)
            if berhasil:
                save_bookmark(int(selected_key.split('_')[1]))
            else:
                stdscr.addstr(h-5, 0, "Audio tidak ditemukan untuk ayat tersebut. Tekan tombol apapun...")
                stdscr.getch()

if __name__ == '__main__':
    curses.wrapper(main)
