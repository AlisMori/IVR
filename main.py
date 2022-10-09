from kivy.lang import Builder
from kivymd.app import MDApp


class Med(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('main.kv')
        self.theme_cls.material_style = "M3"

    def info(self):
        name = self.screen.ids.drug.text
        self.screen.ids.indications.text = 'New text'

    def incomp(self):
        self.screen.ids.list_med.text = 'List of drugs'

    def comp(self):
        self.screen.ids.compatibility.text = 'УРААА'

    def build(self):
        return self.screen


if __name__ == "__main__":
    Med().run()
