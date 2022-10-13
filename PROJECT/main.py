from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker


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

    def on_save(self, instance, value, date_range):
        self.screen.ids.date.text = f'{str(date_range[0])} - {str(date_range[-1])}'

    def on_cancel(self, instance, value):
        self.screen.ids.date.text = "You clicked Cancel"

    def calendar(self):
        date_dialog = MDDatePicker(mode='range')
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def build(self):
        return self.screen


if __name__ == "__main__":
    Med().run()
