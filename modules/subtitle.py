def buat_subtitle(teks, filename="subtitle.srt"):
    lines = teks.split('. ')
    with open(filename, 'w') as f:
        for idx, sent in enumerate(lines, start=1):
            start = (idx-1)*3
            end = idx*3
            f.write(f"{idx}\n00:00:{start:02},000 --> 00:00:{end:02},000\n{sent.strip()}\n\n")
