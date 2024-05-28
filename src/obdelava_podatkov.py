import pandas as pd
import re
import json
import seaborn as sns
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
## UREDITEV TABELE ###################################################################
def uredi_podatke():
    # Naloži CSV datoteko v DataFrame
    csv_file = 'all_data/all_data.csv'
    df = pd.read_csv(csv_file,on_bad_lines='skip')
    df.drop('Spol', inplace=True, axis=1)
    df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y', errors='coerce')
    df = df.dropna(subset=['Datum'])
    df['Leto'] = df['Datum'].dt.year
    df.drop_duplicates()
    df.to_csv('podatki/Oglasi/processed_data.csv', index=False,date_format='%d.%m.%Y')
    

## ŠTEVILO LETNO #####################################################################
def plot_letno():
    """
    Izriše stolpični graf števila oglasov glede na leto.
    :return: None
    """
    df = pd.read_csv('podatki/Oglasi/processed_data.csv')
    df_grouped_leto = df.groupby(['Leto']).size().reset_index(name='Sum')

    plt.bar(df_grouped_leto['Leto'], df_grouped_leto['Sum'])
    plt.xlabel('Leto')
    plt.ylabel('Število ponudb')
    plt.title('Število oglasov po letih')
    plt.xticks(df_grouped_leto['Leto'], rotation='vertical')

    plt.show()

## ŠTEVILO MESEČNO ###################################################################
def plot_mesec(leto=2020):
    """
    Izriše stolpični graf mesečnega števila oglasov glede na izbrano leto.
    :param year: Leto za prikaz mesečnega števila oglasov (privzeto 2020).
    :return: None
    """
    df = pd.read_csv('podatki/Oglasi/processed_data.csv')
    df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y')
    df['LetoMesec'] = df['Datum'].dt.to_period('M')
    df_grouped_leto_mesec = df.groupby(['LetoMesec']).size().reset_index(name='Sum')
    df_grouped_leto_mesec = df_grouped_leto_mesec[df_grouped_leto_mesec['LetoMesec'].dt.year == leto]

    plt.bar(df_grouped_leto_mesec['LetoMesec'].dt.month, df_grouped_leto_mesec['Sum'])
    plt.xlabel('Mesec')
    plt.ylabel('Število ponudb')
    plt.title(f'Mesečno število ponudb glede na leto {leto}')
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun', 'Jul', 'Avg', 'Sep', 'Okt', 'Nov', 'Dec'])
    
    plt.show()

## ŠTEVILO POVPREČNO MESEČNO #########################################################
def plot_mesec_povp():
    """
    Izriše stolpični graf povprečnega mesečnega števila oglasov glede na obdobje od leta 2004 do 2022.
    :return: None
    """
    df = pd.read_csv('podatki/Oglasi/processed_data.csv')
    df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y')
    df['LetoMesec'] = df['Datum'].dt.to_period('M')
    df = df.groupby(['LetoMesec']).size().reset_index(name='Sum')
    filtered_df = df[df['LetoMesec'].dt.year != 2023]
    average_by_month = filtered_df.groupby(filtered_df['LetoMesec'].dt.month)['Sum'].mean().reset_index()
    average_by_month['Sum'] = average_by_month['Sum'].round()

    average_by_month.columns = ['Month', 'Povprecje']

    plt.bar(average_by_month['Month'], average_by_month['Povprecje'])
    plt.xlabel('Mesec')
    plt.ylabel('Poprečno število ponudb')
    plt.title(f'Povprečno mesečno število ponudb glede na leta 2005-2022')
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun', 'Jul', 'Avg', 'Sep', 'Okt', 'Nov', 'Dec'])
    plt.show()

## ŠTEVILO PONUDB DELO OD DOMA ########################################################
def plot_st_od_doma():
    """
    Izriše stolpični graf števila ponudb za delo na daljavo glede na leto.

    :return: None
    """
    df = pd.read_csv('podatki/Oglasi/processed_data.csv')
    df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y')
    
    # Filtrira vrstice, kjer je v stolpcu 'Ponudba' prisoten niz 'na daljavo' ali 'od doma'
    df = df[df['Ponudba'].str.contains('na daljavo|od doma', case=False, na=False)]
    df_grouped_leto = df.groupby(['Leto']).size().reset_index(name='Sum')
    
    plt.figure(figsize=(6.4, 6))
    plt.bar(df_grouped_leto['Leto'], df_grouped_leto['Sum'])
    plt.xlabel('Leto')
    plt.ylabel('Število ponudb')
    plt.title('Število ponudb za delo na daljavo')
    plt.xticks(df_grouped_leto['Leto'], rotation='vertical')

    plt.show()

## ŠTEVILO PONUDB NA PONUDNIKA ########################################################
def plot_st_ponudnik(leta=[2005, 2004], st_podjetji=10):
    # Branje podatkov iz CSV datoteke v DataFrame
    df = pd.read_csv('podatki/Oglasi/processed_data.csv')
    
    # Pretvorba stolpca 'Datum' v obliko datuma
    df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y')
    
    # Predprocesiranje stolpca 'Ponudnik': odstranitev vzorcev besed in pretvorba v male črke
    df['Ponudnik'] = df['Ponudnik'].str.replace(r's\.p\.*|d\.d\.*|d\.o\.o\.*|,', '', regex=True).apply(str.lower)
    
    # Filtriranje podatkov glede na dana leta
    df = df[df['Leto'].isin(leta)]
    
    # Agregacija podatkov glede na 'Ponudnika' in leto ter preštevanje ponudb
    df = df.groupby([df['Ponudnik'], df['Datum'].dt.year])['Ponudba'].count().reset_index()
    
    # Nadaljnja agregacija podatkov glede na 'Ponudnika' in seštevanje števila ponudb
    df = df.groupby(['Ponudnik'])['Ponudba'].sum().reset_index()
    
    # Izbor prvih 'st_podjetji' največjih ponudnikov
    top_n = df.nlargest(st_podjetji, 'Ponudba')
    
    # Definicija števila in postavitve podgrafov
    
    if st_podjetji % 10 == 0:
        num_subplots = round(st_podjetji / 10) 
    else:
        num_subplots= round(st_podjetji / 10)+1
    fig, axs = plt.subplots(num_subplots, 1, figsize=(10, 6*num_subplots))
    
    # Izris podgrafov
    for i in range(num_subplots):
        start_idx = i * (len(top_n) // num_subplots)
        end_idx = (i + 1) * (len(top_n) // num_subplots)
        subset_data = top_n[start_idx:end_idx]
     
        ax = axs[i]
        ax.bar(subset_data['Ponudnik'], subset_data['Ponudba'])
        ax.set_ylabel('Število ponudb')
        ax.set_title(f'Graf {i+1}')
        ax.tick_params(axis='x', rotation=45)

        if i == 0:
            y_min, y_max = ax.get_ylim()
        else:
            ax.set_ylim(y_min, y_max)

    # Prilagoditev postavitve in prikaz grafov
    plt.tight_layout()
    plt.show()

## NAJVEČJI PONUDNIK PO LETIH ########################################################
def plot_best_ponudnik():
    # Branje podatkov iz CSV datoteke v DataFrame
    df = pd.read_csv('podatki/Oglasi/processed_data.csv')
    
    # Pretvorba stolpca 'Datum' v obliko datuma
    df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y')
    
    # Predprocesiranje stolpca 'Ponudnik': odstranitev vzorcev besed in pretvorba v male črke
    df['Ponudnik'] = df['Ponudnik'].str.replace(r's\.p\.*|d\.d\.*|d\.o\.o\.*|,','', regex=True).apply(str.lower)
    
    # Agregacija podatkov glede na 'Ponudnika' in leto ter preštevanje ponudb
    df = df.groupby([df['Ponudnik'], df['Datum'].dt.year])['Ponudba'].count().reset_index()
    
    # Nadaljnja agregacija podatkov glede na 'Datum' in seštevanje števila ponudb
    df = df.groupby('Datum').apply(lambda x: x.nlargest(1, 'Ponudba')).reset_index(drop=True)

    # Vsakemu podjetju dodelimo barvo
    barve = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'cyan', 'magenta', 'lime', 'teal', 'indigo']
    uni_podjetja= list(set(list(df['Ponudnik'])))
    barva_ponudnik=zip(uni_podjetja,barve)
    # Izris stolpičnega grafa
    
    for ponudnik, barva in barva_ponudnik:
        top = df[df['Ponudnik'] == ponudnik]
        plt.bar(top['Datum'], top['Ponudba'], color=barva, label=ponudnik)

    plt.xlabel('Leto')
    plt.ylabel('Število ponudb')
    plt.title('Največji ponudniki del po letih')
    plt.xticks(df['Datum'], rotation='vertical')
    plt.legend()
    plt.tight_layout()
    plt.show()

## ANALIZA PO LOKACIJAH ########################################################

def get_drzave():
    wikiurl="https://sl.wikipedia.org/wiki/Seznam_suverenih_dr%C5%BEav"
    response=requests.get(wikiurl)

    soup = BeautifulSoup(response.text, 'html.parser')
    indiatable=soup.find('table',{'class':"wikitable"})

    df=pd.read_html(str(indiatable))
    df=pd.DataFrame(df[0])
    df.rename(columns={'Kratko ime države': "Drzava" }, inplace = True)
    vse=df.Drzava.values.tolist()
    regex = re.compile(r'.+\[[a-z]+\s\|\s[a-z|\s]+\]')
    filtered = [i[0] for i in vse if not regex.match(i[0])]
   
    return filtered

def get_regije():
    
    wikiurl="https://sl.wikipedia.org/wiki/Statisti%C4%8Dne_regije_Slovenije"
    response=requests.get(wikiurl)

    soup = BeautifulSoup(response.text, 'html.parser')
    indiatable=soup.find('table',{'class':"wikitable"})

    df=pd.read_html(str(indiatable))
    df=pd.DataFrame(df[0])

    return [x.replace('-',' ') for x in list(df['Statistična regija'])]

def get_naselja():
    abe=['A','B','C','Č','D','E','F','G','H','I','J','K','L','M','N','O','P','R','S','Š','T','U','V','Z','Ž']
    vsi=[]
    for i in abe:
        link=f'https://sl.wikipedia.org/wiki/Seznam_naselij_v_Sloveniji_({i})'
        response=requests.get(link)

        soup = BeautifulSoup(response.text, 'html.parser')
        indiatable=soup.find('table',{'class':"wikitable"})

        df=pd.read_html(str(indiatable))
        df=pd.DataFrame(df[0])
        vsi=vsi+[x for x in list(df[df.columns[0]])]
        
    return vsi

def get_locations():
    vse=get_drzave()+get_regije()+get_naselja()
    with open("podatki/Oglasi/lokacije.json", "w",encoding='utf-8') as file:
        json.dump(vse, file)
    return vse


def get_top_lokacije():
    # Preberi podatke iz CSV datoteke v DataFrame
    df = pd.read_csv('podatki/Oglasi/processed_data.csv')
    # Združi po stolpcu 'Lokacija' in preštej pojavitev vsake skupine, nato ponastavi indeks
    df = df.groupby('Lokacija')['Ponudba'].count().reset_index()

    # Naloži seznam lokacij iz JSON datoteke in dodaj dodatne lokacije
    with open('podatki/Oglasi/lokacije.json', "r") as file:
        lokacije_vse = json.load(file) + ['EU', 'Dolenjska regija', 'Gorenjska regija', 'Notranjska regija']
  
    # Odstrani posebne znake iz vrednosti stolpca 'Lokacija'
    df["Lokacija"] = df["Lokacija"].apply(lambda x: re.sub(r'[^\w\sčšž]', '', x, flags=re.UNICODE))

    # Razdeli vrednosti stolpca 'Lokacija' glede na različne ločila
    new_rows = []
    for index, row in df.iterrows():
        if 'in' in row['Lokacija'].lower():
            lokacije = [loc.strip() for loc in row['Lokacija'].split('in')]
            for loc in lokacije:
                new_rows.append([ loc, row['Ponudba']])
        elif ',' in row['Lokacija'].lower():
            lokacije = [loc.strip() for loc in row['Lokacija'].split(',')]
            for loc in lokacije:
                new_rows.append([ loc, row['Ponudba']])
        elif '-' in row['Lokacija'].lower():
            lokacije = [loc.strip() for loc in row['Lokacija'].split('-')]
            for loc in lokacije:
                new_rows.append([ loc, row['Ponudba']])
        else:
            new_rows.append([row['Lokacija'], row['Ponudba']])

    # Ustvari nov DataFrame z obdelanimi vrednostmi stolpca 'Lokacija' in stolpcem 'St_Ponudb'
    new_df = pd.DataFrame(new_rows, columns=["Lokacija", "St_Ponudb"])

    # Preveri ujemanje vrednosti 'Lokacija' z vrednostmi iz 'lokacije_vse' in zamenjaj z ujemajočimi vrednostmi
    filtered_df = new_df[new_df["Lokacija"].str.lower().isin([loc.lower() for loc in lokacije_vse])]

    # Združi po 'Lokacija' in seštej 'St_Ponudb', nato ponastavi indeks in shrani v novo CSV datoteko
    filtered_df=filtered_df.groupby(filtered_df["Lokacija"].str.lower())['St_Ponudb'].sum().reset_index()

    # Velike začetnice v vsakem zapisu 'Lokacija'
    filtered_df['Lokacija'] = filtered_df['Lokacija'].str.capitalize()

    filtered_df.to_csv('podatki/Oglasi/get_top_lokacije_data.csv', index=False)


def plot_top_lokacije():
    df = pd.read_csv('podatki/Oglasi/get_top_lokacije_data.csv').nlargest(15, 'St_Ponudb')

    plt.bar(df['Lokacija'], df['St_Ponudb'])
    plt.xlabel('Leto')
    plt.ylabel('Število ponudb')
    plt.title('Število oglasov po lokacijah')
    plt.xticks(df['Lokacija'], rotation='vertical')

    plt.show()


def get_top_lokacije_all():
    # Preberi podatke iz CSV datoteke
    df = pd.read_csv('podatki/Oglasi/processed_data.csv')
    # Preberi seznam lokacij iz JSON datoteke in dodaj dodatne lokacije
    with open('podatki/Oglasi/lokacije.json', "r") as file:
        lokacije_vse = json.load(file) +  ['EU','Dolenjska regija','Gorenjska regija','Notranjska regija']

    # Očisti vsebino stolpca "Lokacija"
    df["Lokacija"] = df["Lokacija"].apply(lambda x: re.sub(r'[^\w\sčšž]', '', str(x), flags=re.UNICODE))

    new_rows = []
    # Loops through rows and splits multiple locations and formats them
    for index, row in df.iterrows():
        if 'in' in row['Lokacija'].lower():
            lokacije = [loc.strip() for loc in row['Lokacija'].split('in')]
            for loc in lokacije:
                new_rows.append([row['Ponudba'],row['Datum'],row['Ponudnik'], loc])
        elif ',' in row['Lokacija'].lower():
            lokacije = [loc.strip() for loc in row['Lokacija'].split(',')]
            for loc in lokacije:
                new_rows.append([row['Ponudba'],row['Datum'],row['Ponudnik'], loc])
        elif '-' in row['Lokacija'].lower():
            lokacije = [loc.strip() for loc in row['Lokacija'].split('-')]
            for loc in lokacije:
                new_rows.append([row['Ponudba'],row['Datum'],row['Ponudnik'], loc])
        else:
            new_rows.append([row['Ponudba'],row['Datum'],row['Ponudnik'], row['Lokacija']])

    # Ustvari nov DataFrame z urejenimi podatki
    new_df = pd.DataFrame(new_rows, columns=['Ponudba',"Datum", "Ponudnik",'Lokacija'])

    # Preveri ujemanje vrednosti 'Lokacija' z vrednostmi iz 'lokacije_vse' in zamenjaj z ujemajočimi vrednostmi
    filtered_df = new_df[new_df["Lokacija"].str.lower().isin([loc.lower() for loc in lokacije_vse])]
    
    # Velike začetnice v vsakem zapisu 'Lokacija'
    filtered_df.loc[:, 'Lokacija'] = filtered_df['Lokacija'].str.capitalize()

    filtered_df.to_csv('podatki/Oglasi/get_top_lokacije_all_data.csv', index=False)


def plot_heatmap(st_ponudnikov=3,st_lokacij=10):
    # Naloži CSV datoteko v DataFrame
    df = pd.read_csv('podatki/Oglasi/get_top_lokacije_all_data.csv')
    
    # Pretvori 'Ponudnik' v male črke
    df['Ponudnik2'] = df['Ponudnik'].str.lower()

    # Seznam nizov za odstranitev iz 'Ponudnik2'
    strings_to_remove = ['d.o.o', 'd.d', 's.p','d.o.o.', 'd.d.', 's.p.']

    # Odstrnani nize 'string_to_remove' in združi po Lokaciji in Ponudnik2
    df['Ponudnik2'] = df['Ponudnik2'].apply(lambda x: ' '.join([word for word in x.split() if word not in strings_to_remove]))
    df=df.groupby(['Lokacija','Ponudnik2'])['Ponudba'].count().reset_index()

    # Naloži CSV datoteko za filtrirane lokacije
    df_top = pd.read_csv('podatki/Oglasi/get_top_lokacije_data.csv').nlargest(st_lokacij, 'St_Ponudb')

    # Združi DataFrame-je na podlagi 'Lokacija'
    merged_df = pd.merge(df_top, df, on='Lokacija')

    # Najdi najboljši st_ponudnikov 'Ponudba' v vsaki 'Lokacija' po združevanju
    top_podjetja = merged_df.groupby('Lokacija').apply(lambda x: x.nlargest(st_ponudnikov, 'Ponudba')).reset_index(drop=True)
    
    # Prikaz heatmap-a
    heatmap_data = top_podjetja.pivot_table(index='Lokacija', columns='Ponudnik2', values='Ponudba', aggfunc='sum', fill_value=0)
    
    plt.figure(figsize=(10, 10))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='g')
    plt.xlabel('Podjetja')
    plt.ylabel('Lokacija')
    plt.xticks(rotation='vertical')
    plt.tight_layout()
    plt.show()


