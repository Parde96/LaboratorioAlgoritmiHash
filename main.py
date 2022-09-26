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


def draw_plot(x_lf, y1_c, y2_o, name_file_image, name_plot, y_name):
    plt.figure(dpi=1200)
    exp_x = []
    exp_y1 = []
    exp_y2 = []
    # scrivo i tempi in notazione scientifica da mettere poi nelle tabelle
    for i in range(len(x_lf)):
        exp_x.append("{:.2e}".format(x_lf[i]))
        exp_y1.append("{:.2e}".format(y1_c[i]))
        exp_y2.append("{:.2e}".format(y2_o[i]))

    plt.title(name_plot + "    Numero di test " + str(num_test))
    plt.plot(x_lf, y2_o, label="Indirizzamento aperto")
    plt.plot(x_lf, y1_c, label="Concatenamento")
    plt.xlabel('Fattore di caricamento')
    plt.ylabel(y_name)
    plt.legend()

    tab_tempi = go.Figure(data=[go.Table(header=dict(
        values=['Fattore di caricamento', 'Concatenamento', 'Indirizzamento aperto']),
        cells=dict(values=[exp_x, exp_y1, exp_y2]))])
    tab_tempi.write_html("Tabelle test/Tabella " + name_file_image + ".html")
    plt.savefig("Grafici test/Grafico " + name_file_image)


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


def testing_insert():
    all_insert_times_chained = []  # lista contenente liste di tempi per ogni test per il concatenamento
    all_insert_times_open = []  # come sopra con indirizzamento aperto
    all_collisions_chained = []  # come sopra con le collisioni per concatenamento
    all_collisions_open = []  # come sopra per indirizzamento aperto
    loading_factor = []  # fattore di caricamento che fungerà da asse x nel grafico

    # facciamo in modo che sia più grande di 1 per testarne i tempi del concatenamento in particolare
    for i in range(num_cells + 100):
        loading_factor.append(i / num_cells)

    # inizio test inserimento
    for i in range(num_test):

        # creo ogni volta una nuova tabella hash per ripartire da zero
        chained = Chained(num_cells)
        open_add = OpenAddress(num_cells)

        # liste di tempi per questa iterazione del test
        insert_time_chained = []
        insert_time_open = []

        # liste di collisioni per questa iterazione del test
        collisions_chained = []
        collisions_open = []

        # lista coi valori da inserire in entrambe le liste, creata casualmente ad ogni iterazione della stessa
        # grandezza del fattore di caricamento
        val_to_insert = []
        for j in range(num_cells + 100):
            val_to_insert.append(random.randint(-10000, 100000))

        # inizio inserimenti e misurazione dei tempi
        for j in range(len(val_to_insert)):
            start = timer()
            chained.insert(Node(val_to_insert[j]))
            end = timer()
            insert_time_chained.append(end - start)
            collisions_chained.append(chained.get_collision())

            start = timer()
            open_add.insert(val_to_insert[j])
            end = timer()
            insert_time_open.append(end - start)
            collisions_open.append(open_add.get_collision())

        all_insert_times_chained.append(insert_time_chained)
        all_insert_times_open.append(insert_time_open)
        all_collisions_chained.append(collisions_chained)
        all_collisions_open.append(collisions_open)

    # liste in cui salvare le medie dei tempi e collisioni di tutti i test dopo averli completati tutti
    mean_times_chained = []
    mean_times_open = []
    mean_collisions_chained = []
    mean_collisions_open = []
    for i in range(len(loading_factor)):
        mean_times_chained.append([])
        mean_times_open.append([])
        mean_collisions_chained.append([])
        mean_collisions_open.append([])
        for j in range(num_test):
            mean_times_chained[i].append(all_insert_times_chained[j][i])
            mean_times_open[i].append(all_insert_times_open[j][i])
            mean_collisions_chained[i].append(all_collisions_chained[j][i])
            mean_collisions_open[i].append(all_collisions_open[j][i])
        mean_times_chained[i] = mean(mean_times_chained[i])
        mean_times_open[i] = mean(mean_times_open[i])
        mean_collisions_chained[i] = mean(mean_collisions_chained[i])
        mean_collisions_open[i] = mean(mean_collisions_open[i])

    # chiamo le funzioni per andare a disegnare i grafici e le tabelle, per le collisioni andiamo ad usare meno valori
    # del fattore di caricamento
    draw_plot(loading_factor[0:num_cells + 10], mean_collisions_chained[0:num_cells + 10],
              mean_collisions_open[0:num_cells + 10], "collisioni", "Collisioni", "Collisioni")
    draw_plot(loading_factor, mean_times_chained, mean_times_open, "test inserimento", "Test inserimento",
              "Inserimento")


def testing_search_success():
    all_search_times_chained = []  # lista contenente liste di tempi per ogni test per il concatenamento
    all_search_times_open = []  # come sopra con indirizzamento aperto
    loading_factor = []  # fattore di caricamento che fungerà da asse x nel grafico

    # fermarsi prima nella ricerca rispetto ad inserimento che poi diventa senza successo non essendoci più spazio
    # nell'open
    for i in range(num_cells + 1):  # +1 per avere il loading factor anche uguale ad 1
        loading_factor.append(i / num_cells)

    # inizio test ricerca
    for i in range(num_test):

        # creo ogni volta una nuova tabella hash per ripartire da zero
        chained = Chained(num_cells)
        open_add = OpenAddress(num_cells)

        # liste di tempi per questa iterazione del test
        search_time_chained = []
        search_time_open = []

        # lista coi valori da inserire in entrambe le liste, creata casualmente ad ogni iterazione della stessa
        # grandezza del fattore di caricamento, la stessa lista sarà usata per fare anche la ricerca
        val_to_insert = []
        for j in range(num_cells + 1):
            val_to_insert.append(random.randint(-10000, 100000))
            chained.insert(Node(val_to_insert[j]))
            open_add.insert(val_to_insert[j])

        # inizio ricerche e misurazione dei tempi
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

    # liste in cui salvare le medie dei tempi e collisioni di tutti i test dopo averli completati tutti
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

    # chiamo la funzione per andare a disegnare i grafici e le tabelle
    draw_plot(loading_factor, mean_chained, mean_open, "test ricerca", "Test ricerca", "Tempi ricerca")


def testing_search_no_success():
    all_search_times_chained = []  # lista contenente liste di tempi per ogni test per il concatenamento
    all_search_times_open = []  # come sopra con indirizzamento aperto
    loading_factor = []  # fattore di caricamento che fungerà da asse x nel grafico

    # fermarsi prima nella ricerca rispetto ad inserimento che poi diventa senza successo non essendoci più spazio
    # nell'open
    for i in range(num_cells + 1):  # +1 per avere il loading factor anche uguale ad 1
        loading_factor.append(i / num_cells)

    # inizio test ricerca
    for i in range(num_test):

        # creo ogni volta una nuova tabella hash per ripartire da zero
        chained = Chained(num_cells)
        open_add = OpenAddress(num_cells)

        # liste di tempi per questa iterazione del test
        search_time_chained = []
        search_time_open = []

        # lista coi valori da inserire in entrambe le liste, creata casualmente ad ogni iterazione della stessa
        # grandezza del fattore di caricamento
        val_to_insert = []

        # lista coi valori non presenti da cercare creata ogni colta casualmente in funzione dei valori inseriti
        val_to_search = []

        for j in range(num_cells + 1):
            val_to_insert.append(random.randint(-10000, 100000))
            val_to_search.append(val_to_insert[j] + 1)
            chained.insert(Node(val_to_insert[j]))
            open_add.insert(val_to_insert[j])

        # inizio ricerche e misurazione dei tempi
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

    # liste in cui salvare le medie dei tempi e collisioni di tutti i test dopo averli completati tutti
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

    # chiamo la funzione per andare a disegnare i grafici e le tabelle
    draw_plot(loading_factor, mean_chained, mean_open, "test ricerca senza successo", "Test ricerca senza successo",
              "Tempi ricerca senza successo")


if __name__ == '__main__':
    print(sys.version)

    print()
    print("......")
    print()

    num_test = 10
    num_cells = 109  # 1009, 503, 109
    testing_insert()
    # testing_search_success()
    # testing_search_no_success()
