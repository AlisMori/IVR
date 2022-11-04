from matplotlib import pyplot as plt
import requests


def graph(user_id):
    response = requests.get("http://127.0.0.1:5000/users/get_stats", json={'id': user_id})
    weight = []
    pressure_s = []
    pressure_d = []
    glucose = []
    date = []
    ls = response.json()
    for i in ls:
        weight.append(i[0])
        pressure_s.append(i[1])
        pressure_d.append(i[2])
        glucose.append(i[3])
        date.append(i[4])

    fig, axs = plt.subplots(4, figsize=(10, 10))
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

    fig.savefig('graph.png')
