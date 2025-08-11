import datetime
import requests
# import feedparser  # FIXED: unknown import commented out
# from gtts import gTTS  # FIXED: unknown import commented out
# from pydub import AudioSegment  # FIXED: unknown import commented out
# from moviepy.editor import (  # FIXED: unknown import commented out
    TextClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
    CompositeAudioClip,
    afx,
)
# import tempfile  # FIXED: unknown import commented out
# import os  # FIXED: unknown import commented out

# --- Fungsi ambil berita dari NewsAPI ---
def ambil_berita_newsapi():
    API_KEY = "YOUR_NEWSAPI_KEY"
    hari_ini = datetime.datetime.now()
    tanggal_str = hari_ini.strftime("%Y-%m-%d")
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=Palestina OR Indonesia OR Israel&"
        f"from={tanggal_str}&"
        f"to={tanggal_str}&"
        f"sortBy=publishedAt&"
        f"language=id&"
        f"apiKey={API_KEY}"
    )
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("articles"):
            judul = data["articles"][0]["title"]
            sumber = data["articles"][0]["source"]["name"]
            return f"{judul} (Sumber: {sumber})"
        else:
            return "Berita terbaru NewsAPI tidak tersedia."
    except Exception as e:
        return f"Gagal ambil berita NewsAPI: {str(e)}"

# --- Fungsi ambil berita dari RSS feed ---
def ambil_berita_rss():
    rss_url = "https://www.antaranews.com/rss/terkini"  # Contoh RSS berita Indonesia
    try:
        feed = feedparser.parse(rss_url)
        if feed.entries:
            judul = feed.entries[0].title
            return f"{judul} (Sumber: ANTARA News)"
        else:
            return "Berita terbaru RSS tidak tersedia."
    except Exception as e:
        return f"Gagal ambil berita RSS: {str(e)}"

# --- Gabung berita dari dua sumber ---
def gabung_berita():
    berita1 = ambil_berita_newsapi()
    berita2 = ambil_berita_rss()
    return f"Berita Hari Ini:\n1. {berita1}\n2. {berita2}"

# --- Fungsi buat audio TTS dari teks ---
def buat_audio(teks, filename, lang='id'):
    tts = gTTS(teks, lang=lang, slow=False)
    tts.save(filename)
    return filename

# --- Fungsi gabungkan audio arab + terjemahan ---
def gabung_audio(arab_file, id_file, output_file):
    audio_arab = AudioSegment.from_file(arab_file)
    audio_id = AudioSegment.from_file(id_file)
    gabungan = audio_arab + AudioSegment.silent(duration=500) + audio_id
    gabungan.export(output_file, format="mp3")
    return output_file

# --- Fungsi buat clip teks dengan animasi fade in/out per paragraf ---
def buat_clip_animated(teks, durasi_total, ukuran=(1280,720), font='Arial', fontsize=28):
    paragraf = [p.strip() for p in teks.strip().split('\n') if p.strip()]
    durasi_per_paragraf = durasi_total / len(paragraf)
    clips = []

    for i, p in enumerate(paragraf):
        clip = TextClip(p, fontsize=fontsize, color='white', font=font, size=ukuran, method='caption', align='center')
        clip = clip.set_duration(durasi_per_paragraf)
        clip = clip.crossfadein(0.7).crossfadeout(0.7)
        clips.append(clip)

    return concatenate_videoclips(clips)

# --- Fungsi buat subtitle SRT sederhana ---
def buat_subtitle_srt(teks, durasi_total, filename="subtitle.srt"):
    paragraf = [p.strip() for p in teks.strip().split('\n') if p.strip()]
    durasi_per_paragraf = durasi_total / len(paragraf)

    def format_waktu(secs):
        millis = int((secs - int(secs)) * 1000)
        h = int(secs // 3600)
        m = int((secs % 3600) // 60)
        s = int(secs % 60)
        return f"{h:02}:{m:02}:{s:02},{millis:03}"

    with open(filename, "w", encoding="utf-8") as f:
        for i, p in enumerate(paragraf):
            start = i * durasi_per_paragraf
            end = start + durasi_per_paragraf
            f.write(f"{i+1}\n")
            f.write(f"{format_waktu(start)} --> {format_waktu(end)}\n")
            f.write(f"{p}\n\n")
    return filename

# --- Fungsi main buat video lengkap ---
def buat_video_lengkap():
    utc_now = datetime.datetime.utcnow()
    wib_now = utc_now + datetime.timedelta(hours=7)
    tanggal_wib = wib_now.strftime("%A, %d %B %Y, %H:%M WIB")
    tanggal_utc = utc_now.strftime("%A, %d %B %Y, %H:%M UTC")

    berita = gabung_berita()

    teks_arab = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ\nوَاللَّهُ أَعْلَمُ بِالصَّوَابِ"
    teks_terjemah = f"""
Bismillahirrahmanirrahim
"Dengan nama Allah Yang Maha Pengasih dan Penyayang"

---

Al-Qur'an (QS. Ali Imran: 139):
"Janganlah kamu lemah dan jangan bersedih hati, padahal kamulah orang-orang yang paling tinggi (derajatnya), jika kamu orang-orang yang beriman."

Hadits Shahih (HR. Muslim):
"Sesungguhnya bersama kesulitan itu ada kemudahan."

Ahli Kitab (QS. Al-Baqarah: 143):
"Dan Kami jadikan kamu umat yang adil dan pilihan supaya kamu menjadi saksi atas manusia."

---

{berita}
(Tanggal WIB: {tanggal_wib} / UTC: {tanggal_utc})

---

Keberagaman adalah kekuatan,
Negara Kesatuan Republik Indonesia adalah rumah kita bersama,
Berpegang teguh pada persatuan dalam keberagaman.

---

Terima kasih telah menonton.
Jangan lupa subscribe dan share untuk dukung karya ini!
"""

    # Buat audio terpisah
    arab_audio_file = "arab.mp3"
    terjemah_audio_file = "terjemah.mp3"
    output_audio_file = "gabungan_audio.mp3"

    buat_audio(teks_arab, arab_audio_file, lang='ar')
    buat_audio(teks_terjemah, terjemah_audio_file, lang='id')
    gabung_audio(arab_audio_file, terjemah_audio_file, output_audio_file)

    # Load audio gabungan
    audio_clip = AudioFileClip(output_audio_file)
    durasi_audio = audio_clip.duration

    # Buat video animasi teks
    video_teks = buat_clip_animated(teks_terjemah, durasi_audio)

    # Buat subtitle file SRT
    subtitle_file = buat_subtitle_srt(teks_terjemah, durasi_audio)

    # Tambahkan subtitle sebagai TextClip yang muncul di bagian bawah
    # Subtitle muncul sesuai waktu tiap paragraf
    paragraf = [p.strip() for p in teks_terjemah.strip().split('\n') if p.strip()]
    durasi_per_paragraf = durasi_audio / len(paragraf)
    subtitle_clips = []
    for i, p in enumerate(paragraf):
        start = i * durasi_per_paragraf
        sub_clip = (
            TextClip(p, fontsize=22, color='yellow', font='Arial', size=(1280, 60), method='caption', align='center')
            .set_start(start)
            .set_duration(durasi_per_paragraf)
            .set_position(("center", "bottom"))
            .crossfadein(0.3)
            .crossfadeout(0.3)
        )
        subtitle_clips.append(sub_clip)

    # Gabungkan subtitle ke video teks
    video_dengan_subtitle = CompositeVideoClip([video_teks] + subtitle_clips)

    # Watermark kecil transparan pojok kanan bawah supaya tidak mengganggu
    watermark = (
        TextClip(
            "Subscribe untuk dukung channel ini!",
            fontsize=20,
            color='white',
            font='Arial-Bold',
            method='label'
        )
        .set_opacity(0.3)
        .set_duration(durasi_audio)
        .set_position(("right", "bottom"))
    )

    video_final = CompositeVideoClip([video_dengan_subtitle, watermark])

    # Load background musik loop (pastikan ada 'background.mp3')
    try:
        bg_music = AudioFileClip("background.mp3").volumex(0.1)
        loop_count = int(durasi_audio // bg_music.duration) + 1
        bg_music_loop = concatenate_videoclips([bg_music] * loop_count).subclip(0, durasi_audio)
        final_audio = CompositeAudioClip([audio_clip, bg_music_loop])
    except Exception as e:
        print("Gagal muat background musik, tanpa musik:", e)
        final_audio = audio_clip

    # Pasang audio ke video
    video_final = video_final.set_audio(final_audio)

    # Render video
    video_final.write_videofile("video_final_subtitle_watermark.mp4", fps=24, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    buat_video_lengkap()
