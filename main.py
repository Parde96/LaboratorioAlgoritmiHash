import sys
import random
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from HashTables.Chained import Chained
from HashTables.OpenAddress import OpenAddress
from LinkedList.Node import Node
from timeit import default_timer as timer
from statistics import mean


"""
Testare con cancellazioni e senza, il senza per vedere le potenzialità dell'open address che dovrebbe essere meglio, 
con per vedere che effettivamente l'open address perde di prestazioni rispetto al chained
"""


def draw_plot(x, y1, y2, name_image, name_plot, y_name):

    plt.figure(dpi=1200)
    plt.plot(x, y2, label="Open")
    plt.plot(x, y1, label="Chained")
    plt.xlabel('Fattore di caricamento')
    plt.ylabel('Tempi di ' + y_name)
    plt.title(name_plot + "    Numero di test " + str(num_test))
    plt.legend()
    plt.savefig("Grafici test/Grafico " + name_image)
    # plt.show()

    exp_x = []
    exp_y1 = []
    exp_y2 = []
    for i in range(len(x)):
        exp_x.append("{:.2e}".format(x[i]))
        exp_y1.append("{:.2e}".format(y1[i]))
        exp_y2.append("{:.2e}".format(y2[i]))

    fig = go.Figure(data=[go.Table(header=dict(
        values=['Fattore di caricamento', 'Concatenamento', 'Indirizzamento aperto']),
        cells=dict(values=[exp_x, exp_y1, exp_y2]))])
    # fig.write_image("Test" + str(index) + ".pdf")
    fig.write_html("Tabelle test/Tabella " + name_image + ".html")
    # fig.show()


def test():

    print(sys.version)

    print()
    print("......")
    print()

    chained = Chained(101)
    chained.insert(Node(10))
    chained.insert(Node(1))
    chained.insert(Node(2))
    chained.insert(Node(3))
    chained.insert(Node(30))
    chained.insert(Node(45))
    chained.insert(Node(120))
    chained.insert(Node(312))
    chained.insert(Node(5432))
    chained.print_table()

    print()
    print("......")
    print()

    open_address = OpenAddress(101)
    open_address.insert(10)
    open_address.insert(1)
    open_address.insert(2)
    open_address.insert(3)
    open_address.insert(30)
    open_address.insert(45)
    open_address.insert(120)
    open_address.insert(312)
    open_address.insert(5432)
    open_address.print()


def testing_insert(num_test):

    num_cells = 101
    all_insert_times_chained = []
    all_insert_times_open = []
    loading_factor = []
    for i in range(num_cells + 100):
        loading_factor.append(i / num_cells)
    for i in range(num_test):
        chained = Chained(num_cells)
        open_add = OpenAddress(num_cells)
        insert_time_chained = []
        insert_time_open = []
        val_to_insert = []
        for j in range(num_cells + 100):
            val_to_insert.append(random.randint(-10000, 100000))

        for j in range(len(val_to_insert)):
            start = timer()
            chained.insert(Node(val_to_insert[j]))
            end = timer()
            insert_time_chained.append(end - start)

            start = timer()
            open_add.insert(val_to_insert[j])
            end = timer()
            insert_time_open.append(end - start)

        all_insert_times_chained.append(insert_time_chained)
        all_insert_times_open.append(insert_time_open)

    mean_chained = []
    mean_open = []
    for i in range(len(loading_factor)):
        mean_chained.append([])
        mean_open.append([])
        for j in range(num_test):
            mean_chained[i].append(all_insert_times_chained[j][i])
            mean_open[i].append(all_insert_times_open[j][i])
        mean_chained[i] = mean(mean_chained[i])
        mean_open[i] = mean(mean_open[i])
    #draw_plot(loading_factor, mean_chained, mean_open, "test inserimento" + str(i+1),
     #         "Test inserimento", "inserimento")
    draw_plot(loading_factor, mean_chained, mean_open, "test inserimento", "Test inserimento", "inserimento")


def testing_search_success(num_test):
    num_cells = 101
    all_search_times_chained = []
    all_search_times_open = []
    loading_factor = []
    for i in range(num_cells + 1): # +1 per avere il loading factor anche uguale ad 1
        loading_factor.append(i / num_cells)
    for i in range(num_test):
        chained = Chained(num_cells)
        open_add = OpenAddress(num_cells)
        search_time_chained = []
        search_time_open = []
        val_to_insert = []

        # fermarsi prima nella ricerca che poi diventa senza successo non essendoci più spazio nell'open
        for j in range(num_cells + 1):
            val_to_insert.append(random.randint(-10000, 100000))
            chained.insert(Node(val_to_insert[j]))
            open_add.insert(val_to_insert[j])

        for j in range(len(val_to_insert)):
            start = timer()
            chained.search(val_to_insert[j])
            end = timer()
            search_time_chained.append(end - start)

            start = timer()
            open_add.search(val_to_insert[j])
            end = timer()
            search_time_open.append(end - start)

        all_search_times_chained.append(search_time_chained)
        all_search_times_open.append(search_time_open)

    mean_chained = []
    mean_open = []
    for i in range(len(loading_factor)):
        mean_chained.append([])
        mean_open.append([])
        for j in range(num_test):
            mean_chained[i].append(all_search_times_chained[j][i])
            mean_open[i].append(all_search_times_open[j][i])
        mean_chained[i] = mean(mean_chained[i])
        mean_open[i] = mean(mean_open[i])

    draw_plot(loading_factor, mean_chained, mean_open, "test ricerca", "Test ricerca", "ricerca")


def testing_search_no_success(num_test):
    num_cells = 101
    all_search_times_chained = []
    all_search_times_open = []
    loading_factor = []
    for i in range(num_cells + 1):
        loading_factor.append(i / num_cells)
    for i in range(num_test):
        chained = Chained(num_cells)
        open_add = OpenAddress(num_cells)
        search_time_chained = []
        search_time_open = []
        val_to_insert = []
        val_to_search = []
        for j in range(num_cells + 1):
            val_to_insert.append(random.randint(-10000, 100000))
            val_to_search.append(val_to_insert[j] + 1)
            chained.insert(Node(val_to_insert[j]))
            open_add.insert(val_to_insert[j])

        for j in range(len(val_to_search)):
            start = timer()
            chained.search(val_to_search[j])
            end = timer()
            search_time_chained.append(end - start)

            start = timer()
            open_add.search(val_to_search[j])
            end = timer()
            search_time_open.append(end - start)

        all_search_times_chained.append(search_time_chained)
        all_search_times_open.append(search_time_open)

    mean_chained = []
    mean_open = []
    for i in range(len(loading_factor)):
        mean_chained.append([])
        mean_open.append([])
        for j in range(num_test):
            mean_chained[i].append(all_search_times_chained[j][i])
            mean_open[i].append(all_search_times_open[j][i])
        mean_chained[i] = mean(mean_chained[i])
        mean_open[i] = mean(mean_open[i])

    draw_plot(loading_factor, mean_chained, mean_open, "test ricerca senza successo", "Test ricerca senza successo",
              "ricerca senza successo")


if __name__ == '__main__':
    print(sys.version)

    print()
    print("......")
    print()

    num_test = 4
    testing_insert(num_test)
    testing_search_success(num_test)
    testing_search_no_success(num_test)
