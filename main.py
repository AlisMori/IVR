from kivy.lang import Builder
from kivymd.app import MDApp

navigation = '''
MDScreen:

    MDBottomNavigation:
        panel_color: "#eeeaea"
        selected_color_background: "#97ecf8"
        text_color_active: 0, 0, 0, 1

        MDBottomNavigationItem:
            name: 'Med info'
            text: 'Инфо'
            icon: 'information'
            
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_size: True
                pos_hint: {'center_x': .5, 'center_y': .75}
                spacing: 15
                            
                MDTextField:
                    id: drug
                    hint_text: "Введите название препарата"
                    # helper_text: "Название препара введено некорректно"
                    # helper_text_mode: "on_error"
                    size_hint_x: None
                    width: 300
                    
                MDRaisedButton:
                    id: research_info
                    text: "Поиск"
                    md_bg_color: 0, 0, 1, 1
                    halign: 'left'
                    on_press: app.info()
                     
                
                MDLabel:
                    text: "Описание"
                    halign: 'left'
                    
                MDLabel:
                    id: info
                    text: "#"
                    pos_hint: {'left': 1}
                
                MDLabel:
                    text: "Показания к применению"
                    halign: 'left'
                    
                MDLabel:
                    id: indications
                    text: "#"
                    halign: 'left'
                
                MDLabel:
                    text: "Противопоказания к применению"
                    halign: 'left'
                    
                MDLabel:
                    id: contraindications
                    text: "#"
                    halign: 'left'
                    
        MDBottomNavigationItem:
            name: 'Incompatibilities'
            text: 'Несовместимости'
            icon: 'close-circle-outline'
            
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_size: True
                pos_hint: {'center_x': .5, 'center_y': .75}
                spacing: 15

                MDTextField:
                    hint_text: "Введите название препарата"
                    # helper_text: "Название препара введено некорректно"
                    # helper_text_mode: "on_error"
                    size_hint_x: None
                    width: 300
                    
                MDRaisedButton:
                    id: research_incomp
                    text: "Поиск"
                    md_bg_color: 0, 0, 1, 1
                    halign: 'left'
                    on_press: app.incomp()
                     

                MDLabel:
                    id: list_med
                    text: "список препаратов"
                    pos_hint: {'left': 1}
                    
                    
        MDBottomNavigationItem:
            name: 'Compatibility'
            text: 'Совместимость'
            icon: 'file-search'

            MDBoxLayout:
                orientation: 'vertical'
                adaptive_size: True
                pos_hint: {'center_x': .5, 'center_y': .75}
                spacing: 15

                MDTextField:
                    id: drug_1
                    hint_text: "Введите название препарата"
                    # helper_text: "Название препара введено некорректно"
                    # helper_text_mode: "on_error"
                    size_hint_x: None
                    width: 300
                    
                MDTextField:
                    id: drug_2
                    hint_text: "Введите название препарата"
                    # helper_text: "Название препара введено некорректно"
                    # helper_text_mode: "on_error"
                    size_hint_x: None
                    width: 300
                    
                MDRaisedButton:
                    id: research_comp
                    text: "Поиск"
                    md_bg_color: 0, 0, 1, 1
                    halign: 'left'
                    on_press: app.comp()
                     

                MDLabel:
                    id: compatibility
                    text: "препараты совместимы/несовместимы"
                    pos_hint: {'left': 1}
        
        MDBottomNavigationItem:
            name: 'Calendar'
            text: 'Календарь'
            icon: 'calendar'

            MDLabel:
                text: 'Calendar'
                halign: 'center'
        
        MDBottomNavigationItem:
            name: 'Health statistic'
            text: 'Здоровье'
            icon: 'chart-areaspline'

            MDLabel:
                text: 'Health statistic'
                halign: 'center'
        
        MDBottomNavigationItem:
            name: 'Profile'
            text: 'Профиль'
            icon: 'account'

            MDLabel:
                text: 'Profile'
                halign: 'center'
'''


class Med(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(navigation)
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
