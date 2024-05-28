import matplotlib.pyplot as plt

def plot_uni(y1_values, x_values_int, y1_label='None', denominator=None, diff=False, y2_values=None,
             y2_label='None', ax_name=None, ay_name=None, title=None):
    """
    Ustvari graf z eno ali dvema krivulkama in morebitno razliko ter ga prikaže ter shrani v datoteko.

    :param y1_values: Seznam vrednosti za y-koordinate prve krivulje.
    :param x_values_int: Seznam celoštevilskih vrednosti za x-koordinate.
    :param y1_label: Oznaka za prvo krivuljo na legendi.
    :param denominator: Imenovalec za izbiro prikaza x-oznak (če je podan).
    :param diff: True, če želite prikazati razliko med y1_values in y2_values.
    :param y2_values: Seznam vrednosti za y-koordinate druge krivulje (če je podan).
    :param y2_label: Oznaka za drugo krivuljo na legendi.
    :param ax_name: Ime x-osi.
    :param ay_name: Ime y-osi.
    :param title: Naslov grafa.
    :param file_name: Ime datoteke za shranjevanje grafa (brez pripon).
    """

    x_values = [str(x) for x in x_values_int]

    # Ustvari sliko in os
    fig, ax = plt.subplots()

    # Nariši podatke
    ax.plot(x_values, y1_values, label=y1_label)
    if y2_values:
        ax.plot(x_values, y2_values, label=y2_label)
    if diff and y2_values:
        razlika = [max(t, a) - min(t, a) for t, a in zip(y1_values, y2_values)]
        ax.plot(x_values, razlika, label='Razlika', linestyle='--', color='red')
    if denominator is not None:
        plt.xticks([str(i) for i in x_values_int if (i % denominator) == 0])

    # Dodaj naslov in oznake
    if ax_name:
        ax.set_xlabel(ax_name)
    if ay_name:
        ax.set_ylabel(ay_name)
    if title:
        ax.set_title(title)

    # Dodaj legendo
    ax.legend()

    # Prikaz in shranjevanje
    plt.show()


def bar_plot(data):
    # Get keys and values from the dictionary
    keys = list(data.keys())
    values = list(data.values())
    clrs = ['blue' if (x > min(values)) else 'red' for x in values ]
    # Create a bar chart
    plt.figure(figsize=(15, 8))  # width:20, height:3
    plt.bar(keys, values, align='center', width=0.2,color=clrs)
    
    # Find the minimum value and its index
    min_value = min(values)
    min_index = values.index(min_value)

    # Add values as text labels above the minimum bar
    for i, v in enumerate(values):
        if i == min_index:
            plt.text(i, v + min_value * 0.09+2, str(v), ha='center', va='top', fontsize=10, color='black', rotation='vertical')

    # Add labels and title
    plt.xlabel('Število niti')
    plt.ylabel('Čas')
    plt.title('Povprečni časi izvajanja glede na število niti')

    # Display the plot
    plt.show()



