def kenali_karakter_sahabat(nama):
    nama = nama.strip().lower()
    
    alias = {
        "muhammad": "nabi muhammad",
        "rasulullah": "nabi muhammad",
        "isa": "nabi isa",
        "yesus": "nabi isa",
        "ibrahim": "nabi ibrahim",
        "abraham": "nabi ibrahim",
        "musa": "nabi musa",
        "daud": "nabi daud",
        "sulaiman": "nabi sulaiman",
        "adam": "nabi adam",
        "nuh": "nabi nuh",
        "yunus": "nabi yunus",
        "ayyub": "nabi ayyub",
        "yusuf": "nabi yusuf",
        "jibril": "malaikat jibril",
    }

    daftar = {
        "nabi muhammad": {
            "nama": "Nabi Muhammad ﷺ",
            "arab": "النبي محمد ﷺ",
            "latin": "Nabiyy Muhammad ﷺ",
            "peran": "Penutup para nabi, pembawa Al-Qur'an",
            "kutipan": "Sampaikan dariku walau satu ayat."
        },
        "nabi musa": {
            "nama": "Nabi Musa عليه السلام",
            "arab": "النبي موسى عليه السلام",
            "latin": "Nabiyy Mūsā ‘alayhis-salām",
            "peran": "Penerima Taurat, penyelamat Bani Israil",
            "kutipan": "Wahai Tuhanku, lapangkanlah dadaku."
        },
        "nabi isa": {
            "nama": "Nabi Isa عليه السلام",
            "arab": "النبي عيسى عليه السلام",
            "latin": "Nabiyy ‘Īsā ‘alayhis-salām",
            "peran": "Pembawa Injil, diangkat ke langit",
            "kutipan": "Aku adalah hamba Allah."
        },
        "nabi ibrahim": {
            "nama": "Nabi Ibrahim عليه السلام",
            "arab": "النبي إبراهيم عليه السلام",
            "latin": "Nabiyy Ibrāhīm ‘alayhis-salām",
            "peran": "Bapak para nabi, membangun Ka'bah",
            "kutipan": "Tuhanku yang menghidupkan dan mematikan."
        },
        "nabi adam": {
            "nama": "Nabi Adam عليه السلام",
            "arab": "النبي آدم عليه السلام",
            "latin": "Nabiyy Ādam ‘alayhis-salām",
            "peran": "Manusia pertama dan nabi pertama",
            "kutipan": "Kami telah menzalimi diri kami sendiri."
        }
    }

    nama = alias.get(nama, nama)
    return daftar.get(nama, False)

