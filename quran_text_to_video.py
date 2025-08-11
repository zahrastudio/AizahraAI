from moviepy.editor import TextClip, concatenate_videoclips, CompositeVideoClip, ColorClip

# Data contoh ayat, bisa kamu ganti dari JSON
ayat_list = [
    {
        "arab": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "latin": "Bismillāhir-Raḥmānir-Raḥīm",
        "arti": "Dengan nama Allah Yang Maha Pengasih, Maha Penyayang."
    },
    {
        "arab": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
        "latin": "Al-ḥamdu lillāhi rabbi al-‘ālamīn",
        "arti": "Segala puji bagi Allah, Tuhan seluruh alam."
    },
    {
        "arab": "الرَّحْمَٰنِ الرَّحِيمِ",
        "latin": "Ar-Raḥmānir-Raḥīm",
        "arti": "Yang Maha Pengasih, Maha Penyayang."
    }
]

VIDEO_SIZE = (1280, 720)
DURASI_AYAT = 10  # detik per ayat
BACKGROUND_COLOR = (20, 30, 60)  # contoh biru gelap, sesuaikan

def make_ayat_clip(ayat, duration=DURASI_AYAT):
    # Background polos warna
    bg_clip = ColorClip(size=VIDEO_SIZE, color=BACKGROUND_COLOR, duration=duration)

    # Text gabungan, tiga baris (Arab, Latin, Arti)
    teks = f"{ayat['arab']}\n\n{ayat['latin']}\n\n{ayat['arti']}"

    # TextClip dengan style
    txt_clip = (TextClip(teks, fontsize=48, font='Arial', color='white', method='caption', size=(VIDEO_SIZE[0]-100, None), align='center')
                .set_position('center')
                .set_duration(duration))

    # Gabungkan background dan teks
    video = CompositeVideoClip([bg_clip, txt_clip])
    return video

def main():
    clips = [make_ayat_clip(ayat) for ayat in ayat_list]
    final_video = concatenate_videoclips(clips, method="compose")

    output_file = "quran_video.mp4"
    final_video.write_videofile(output_file, fps=24)

    print(f"Video selesai dibuat: {output_file}")
    print("Kamu bisa putar dengan mpv atau pemutar video lainnya.")

if __name__ == "__main__":
    main()

