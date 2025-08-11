# hadits.py - offline hadits tematik untuk ZahraVerseAI

hadits_data = [
    {
        "tema": "niat",
        "arab": "إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ",
        "latin": "Innamal a'mālu bin‑niyyāt",
        "terjemahan": "Setiap amal tergantung pada niatnya",
        "sumber": "HR. Bukhari & Muslim"
    },
    {
        "tema": "cinta sesama",
        "arab": "لَا يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لِأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ",
        "latin": "Lā yu'minu aḥadukum ḥattā yuḥibba li‑akhīhi mā yuḥibbu linafsih",
        "terjemahan": "Iman sempurna saat mencintai saudara seperti mencintai diri sendiri",
        "sumber": "HR. Bukhari & Muslim"
    },
    {
        "tema": "penyampaian pesan",
        "arab": "بَلِّغُوا عَنِّي وَلَوْ آيَةً",
        "latin": "Ballighū 'annī walau āyah",
        "terjemahan": "Sampaikan dariku walau hanya satu ayat",
        "sumber": "HR. Bukhari"
    },
    {
        "tema": "silaturahmi",
        "arab": "مَنْ أَحَبَّ أَنْ يُبْسَطَ لَهُ فِي رِزْقِهِ وَبُسِطَ لَهُ فِي عُمُرِهِ",
        "latin": "Man aḥabba an yubsaṭa lahu fī rizqihi wa yunsa'a lahu fī umrihi",
        "terjemahan": "Sambung silaturahmi agar rezeki dan umur diperluas",
        "sumber": "HR. Bukhari & Muslim"
    },
    {
        "tema": "kesabaran",
        "arab": "وَاعْلَمْ أَنَّ فِي الصَّبْرِ عَلَى مَا تَكْرَهُ خَيْرًا كَثِيرًا",
        "latin": "Wa'lam anna fī ṣ‑ṣabri 'alā mā takrahu khayran kathīran",
        "terjemahan": "Dalam kesabaran terdapat banyak kebaikan",
        "sumber": "HR. Ahmad"
    },
    {
        "tema": "lisan",
        "arab": "مَنْ كَانَ يُؤْمِنُ بِاللَّهِ وَالْيَوْمِ الْآخِرِ فَلْيَقُلْ خَيْرًا أَوْ لِيَصْمُتْ",
        "latin": "Man kāna yu'minu billāhi wal‑yawmil‑ākhir falyaqul khayran aw liyasmut",
        "terjemahan": "Beriman berarti berkata baik atau diam",
        "sumber": "HR. Bukhari & Muslim"
    },
    {
        "tema": "pemaaf",
        "arab": "مَا نَقَصَتْ صَدَقَةٌ مِنْ مَالٍ",
        "latin": "Mā naqāṣat ṣadaqah min māl",
        "terjemahan": "Sedekah tidak mengurangi harta",
        "sumber": "HR. Muslim"
    },
    {
        "tema": "amanah",
        "arab": "كُلُّكُمْ رَاعٍ وَكُلُّكُمْ مَسْئُولٌ",
        "latin": "Kullukum rā'in wa kullukum mas'ūlun",
        "terjemahan": "Setiap pemimpin akan dimintai pertanggungjawaban",
        "sumber": "HR. Bukhari & Muslim"
    },
    {
        "tema": "doa kesulitan",
        "arab": "اللَّهُمَّ لاَ سَهْلَ إِلاَّ مَا جَعَلْتَهُ سَهْلاً",
        "latin": "Allāhumma lā sahlā illā mā ja'altahu sahlā",
        "terjemahan": "Ya Allah, tidak ada kemudahan kecuali yang Engkau mudahkan",
        "sumber": "HR. Ibnu Hibban"
    },
    {
        "tema": "kejujuran",
        "arab": "عَلَيْكُمْ بِالصِّدْقِ",
        "latin": "'Alaykum biṣ-ṣidq",
        "terjemahan": "Peganglah kejujuran karena membawa berkah",
        "sumber": "HR. Muslim"
    }
]

def cari_hadits(keyword):
    """
    Cari hadits berdasarkan keyword tema,
    mengembalikan list hadits yang mengandung kata tersebut.
    """
    kw = keyword.lower().strip()
    found = [h for h in hadits_data if kw in h["tema"]]
    return found if found else []

