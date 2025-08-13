from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
import requests

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt_input = MDTextField(hint_text="Masukkan prompt", size_hint=(0.8, None), height=50, pos_hint={"center_x": 0.5, "center_y": 0.7})
        self.add_widget(self.prompt_input)

        self.generate_btn = MDRaisedButton(text="Buat Video", pos_hint={"center_x": 0.5, "center_y": 0.5}, on_release=self.generate_video)
        self.add_widget(self.generate_btn)

        self.status = MDLabel(text="", halign="center", pos_hint={"center_x": 0.5, "center_y": 0.3})
        self.add_widget(self.status)

    def generate_video(self, *args):
        prompt = self.prompt_input.text
        if not prompt.strip():
            self.status.text = "Prompt kosong!"
            return
        try:
            r = requests.post("http://192.168.1.3:7860/generate-video", json={"text": prompt})
            if r.status_code == 200:
                with open("output.mp4", "wb") as f:
                    f.write(r.content)
                self.status.text = "Video berhasil dibuat!"
            else:
                self.status.text = f"Error: {r.text}"
        except Exception as e:
            self.status.text = f"Gagal: {e}"

class MyApp(MDApp):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    MyApp().run()
