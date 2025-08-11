from moviepy.editor import TextClip

clip = TextClip("Test MoviePy", fontsize=70, color='white', size=(640, 480), bg_color='black')
clip = clip.set_duration(3)
clip.write_videofile("test_output.mp4", fps=24)

