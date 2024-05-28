import random 
import numpy as np
import json
import pandas as pd
from funkcije import test_async,test_writerows,test_writerow, test_thread
from plott import plot_uni,bar_plot

#### ROWS vs. ROW ##############################################################
def testing_rows_row(interval, num_rep):
    """
    Testira učinkovitost funkcij test_writerows in test_writerow za različne intervale in število ponovitev.
    
    :param interval: Seznam intervalov, za katere se testira.
    :param num_rep: Število ponovitev testiranja za vsak interval.
    :return: Seznam povprečnih časov izvajanja funkcij test_writerows in test_writerow za vsak interval.
    """
    times_posebej = []  # Povprečni časi izvajanja za test_writerow
    times_skupaj = []   # Povprečni časi izvajanja za test_writerows
    
    for i in interval:
        temp1 = []  # Časi izvajanja za test_writerows za trenuten interval
        temp2 = []  # Časi izvajanja za test_writerow za trenuten interval
        
        for i in range(num_rep):
            # Generiranje naključnih vrstic
            test_lines = [[random.random() for i in range(5)] for j in range(i)]
            
            temp1.append(test_writerows(test_lines))  # Testiranje funkcije test_writerows
            temp2.append(test_writerow(test_lines))   # Testiranje funkcije test_writerow
        
        times_skupaj.append(np.mean(temp1))  # Povprečni čas izvajanja za test_writerows
        times_posebej.append(np.mean(temp2))  # Povprečni čas izvajanja za test_writerow
         
    # Create a DataFrame
    data = {'Interval': list(interval), 'Skupaj': times_skupaj, 'Posebej': times_posebej}
    df = pd.DataFrame(data)

    # Save DataFrame to a CSV file
    csv_filename = 'podatki/Prenos/data_rows_vs_row.csv'
    df.to_csv(csv_filename, index=False)
    return df


def plot_rows_row():
        
    csv_filename = 'podatki/Prenos/data_rows_vs_row.csv'
    df = pd.read_csv(csv_filename)

    plot_uni(
            x_values_int=df['Interval'].values.tolist(),
            y1_values=df['Skupaj'].values.tolist(),
            y1_label='Skupaj',
            y2_values=df['Posebej'].values.tolist(),
            y2_label='Vsako posebej',
            ax_name='Število vrstic',
            ay_name='Čas (sekunde)',
            title='Primerjava časov pisanja v datoteko csv',
            denominator=100000)
    
#### šTEVILO NITI ##############################################################

def testing_num_threads(num_rep,count,interval):
    """
    Testira različno število niti za dano število ponovitev in interval.

    :param num_rep: Število ponovitev testiranja za vsak posamezen interval niti.
    :param count: Število za testiranje v funkciji test_thread.
    :param interval: Seznam števil niti (intervalov), za katere se izvaja testiranje.
    :return: None
    """
    all_times={}
    
    for num_th in interval:
        temp_times=[]
        for i in range(num_rep):
            time=test_thread(range(1,count),num_th)
            temp_times.append(time)
        all_times[str(num_th)]=np.mean(temp_times)
     
    with open("podatki/Prenos/all_threads_2_58.txt", "a") as fp:
        json.dump(all_times, fp)

    return None


def plot_num_threads():
    with open("podatki/Prenos/all_threads_2_58.txt") as fp:
        data = json.load(fp)
    bar_plot(data)

#### NITI vs. ASINHRONO ##############################################################

def testing_thread_vs_async_average(num_rep,interval,st_niti=16):
    """
    Testira povprečne čase izvajanja med uporabo niti (threads) in asinhronim pristopom za dani interval.

    :param num_rep: Število ponovitev testiranja za vsak interval.
    :param interval: Seznam intervalov za testiranje.
    :param st_niti: Število niti za testiranje izvajanja z nitmi (privzeto 16).
    :return: None
    """

    t_val = []  # Povprečni časi za niti
    a_val = []  # Povprečni časi za asinhrono

    for count in interval:
        t_val_temp = []  # Časi za niti
        a_val_temp = []  # Časi za asinhrono
        for i in range(num_rep):
            print(i)
            # Testiramo asinhrono izvajanje
            time_a = test_async(range(1, count))
            # Testiranje izvajanja z niti (threads) s podanim številom niti (st_niti)
            time_t = test_thread(range(1, count), st_niti)
            # Shranimo čase v seznam
            t_val_temp.append(time_t)
            a_val_temp.append(time_a)
        t_val.append(np.mean(t_val_temp))
        a_val.append(np.mean(a_val_temp))
        print(count)

    # Create a DataFrame
    data = {'Interval': list(interval), 'Niti': t_val, 'Asinhrono': a_val}
    df = pd.DataFrame(data)

    # Save DataFrame to a CSV file
    csv_filename = 'podatki/Prenos/data_niti_vs_asinhrono_dva.csv'
    df.to_csv(csv_filename, index=False)


def plot_niti_vs_asinhrono():
        
    csv_filename = 'podatki/Prenos/data_niti_vs_asinhrono_dva.csv'
    df = pd.read_csv(csv_filename)
    
    plot_uni(
            x_values_int=df['Interval'].values.tolist(),
            y1_values=df['Niti'].values.tolist(),
            y1_label='Concurrent.futures',
            y2_values=df['Asinhrono'].values.tolist(),
            y2_label='Asyncio',
            diff=True,
            denominator=1000,
            ax_name='Število oglasov',
            ay_name='Čas (sekunde)',
            title='Primerjeva učinkovitosti knjižnjic concurrent.futures in asyncio',
            )
