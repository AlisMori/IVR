from matplotlib import pyplot as plt
import numpy as np
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.app import App
from kivy.lang import Builder


# from data.users import User
# from data.stats import Stats


class Graph(App):

    def build(self):
        self.str = Builder.load_string(""" 

BoxLayout:
    layout:layout

    BoxLayout:

        id:layout

                                """)

        # weight = Stats.query.filter_by(user_id=User.query.filter_by(id=1).first().weight).all()
        # pressure_s = Stats.query.filter_by(user_id=User.query.filter_by(id=1).first().pressure_s).all()
        # pressure_d = Stats.query.filter_by(user_id=User.query.filter_by(id=1).first().pressure_s).all()
        # glucose = Stats.query.filter_by(user_id=User.query.filter_by(id=1).first().glucose).all()
        # date = Stats.query..filter_by(user_id=User.query.filter_by(id=1).first().created_date).all()

        weight = [50, 49, 51, 52]
        pressure_s = [100, 125, 127, 119]
        pressure_d = [70, 85, 81, 83]
        glucose = [4.5, 5.6, 5.2, 5.0]
        date = [1, 2, 3, 4]

        fig, axs = plt.subplots(4)
        axs[0].plot(date, weight)
        axs[0].set_ylabel('вес')
        axs[1].plot(date, pressure_s)
        axs[1].set_ylabel('САД')
        axs[2].plot(date, pressure_d)
        axs[2].set_ylabel('ДАД')
        axs[3].plot(date, glucose)
        axs[3].set_ylabel('Глюкоза')
        fig.suptitle('Статистика')
        axs[3].set_xlabel('Date')

        self.str.layout.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return self.str


Graph().run()
