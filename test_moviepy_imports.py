# test_moviepy_imports.py

def test_imports():
    results = {}

    try:
        import moviepy
        results['moviepy'] = "OK"
    except Exception as e:
        results['moviepy'] = f"ERROR: {e}"

    try:
        from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
        results['moviepy.editor'] = "OK"
    except Exception as e:
        results['moviepy.editor'] = f"ERROR: {e}"

    try:
        from moviepy.video.VideoClip import TextClip, ColorClip
        results['moviepy.video.VideoClip'] = "OK"
    except Exception as e:
        results['moviepy.video.VideoClip'] = f"ERROR: {e}"

    try:
        from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
        results['moviepy.video.compositing.CompositeVideoClip'] = "OK"
    except Exception as e:
        results['moviepy.video.compositing.CompositeVideoClip'] = f"ERROR: {e}"

    # Tambah cek modul lain yang kamu pakai kalau perlu

    return results


if __name__ == "__main__":
    import json
    res = test_imports()
    print(json.dumps(res, indent=4))

