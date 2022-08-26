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
                    hint_text: "Введите название препарата"
                    # helper_text: "Название препара введено некорректно"
                    # helper_text_mode: "on_error"
                    size_hint_x: None
                    width: 300
                    
                MDRaisedButton:
                    text: "Поиск"
                    md_bg_color: 0, 0, 1, 1
                    halign: 'left'
                     
                
                MDLabel:
                    text: "Описание"
                    halign: 'left'
                    
                MDLabel:
                    id: info
                    text: "#"
                    size_hint_x: None
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

            MDLabel:
                text: 'Incompatibilities'
                halign: 'center'

        MDBottomNavigationItem:
            name: 'Compatibility'
            text: 'Совместимость'
            icon: 'file-search'

            MDLabel:
                text: 'Compatibility'
                halign: 'center'
        
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

    def build(self):
        self.theme_cls.material_style = "M3"
        return Builder.load_string(navigation)


Med().run()
