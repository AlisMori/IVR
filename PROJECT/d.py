import kivy
from kivy.lang import Builder

kivy.require('1.9.0')

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

Builder.load_string('''
<BoxLayout>:

''')


data = {'apple': 10, 'orange': 15, 'lemon': 5, 'lime': 20}
names = list(data.keys())
values = list(data.values())

fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
axs[0].bar(names, values)
axs[1].scatter(names, values)
axs[2].plot(names, values)
fig.suptitle('Categorical Plotting')

class BoxLayoutApp(App):

    def build(self):
        box = BoxLayout()
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        return box


blApp = BoxLayoutApp()
blApp.run()
