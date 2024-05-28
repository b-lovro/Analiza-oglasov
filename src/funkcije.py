import requests
from bs4 import BeautifulSoup as bs
import csv
import time as time_2

import timeit
from concurrent.futures import ThreadPoolExecutor
import aiohttp
import asyncio
link='https://www.mojedelo.com/studentsko-delo/d-'


def write_rows(data, file_name='test_ena'):
    f = open(file_name+'.csv', 'w',newline='', encoding='utf-8')
    writer = csv.writer(f)
    writer.writerows(data)
    f.close()

def write_row(data, file_name='test_ena'):
    f = open(file_name+'.csv', 'w',newline='', encoding='utf-8')
    writer = csv.writer(f)
    for line in data:
        writer.writerow(line)
    f.close()

def test_writerows(all_data):
    start_time = timeit.default_timer()
    write_rows(all_data,file_name='test_rows_3')
    time = timeit.default_timer() - start_time
    return time

def test_writerow(all_data):
    start_time = timeit.default_timer()
    write_row(all_data,file_name='test_row_3')
    time= timeit.default_timer() - start_time
    return time

def fetch_data(interval):
    """
    Pridobivanje podatkov iz spletne strani za dani interval.

    :param interval: Interval za pridobivanje podatkov s spleta.
    :return: Seznam podatkov za dani interval ali None, če zahteva ne uspe.
    """
    html = requests.get(link + str(interval))
    if html.status_code in [410, 200]:
        soup = bs(html.text, 'html5lib')
        okence = soup.find("div", {"class": "page-title"})
        data_temp = [item.get_text(strip=True) for item in okence.find_all("div", {"class": "boxItemGroup"})[0:4]]
        data_temp = [okence.findChildren()[1].get_text(strip=True)] + data_temp
        return data_temp
    return None


def test_thread(interval,num_niti=16):
    """
    Testiranje časa izvajanja pridobivanja podatkov z niti (threads) za dani interval.

    :param interval: Interval za testiranje pridobivanja podatkov.
    :param num_niti: Število niti za uporabo v ThreadPoolExecutor (privzeto 16).
    :return: Čas, porabljen za izvedbo testiranja.
    """
    start_time = timeit.default_timer()

    with ThreadPoolExecutor(max_workers=num_niti) as executor:
        results = list(executor.map(fetch_data, interval))
    
    return timeit.default_timer()-start_time


def test_async(interval):
    """
    Asinhrono prenaša podatke iz spleta za dani interval in izlušči informacije iz HTML vsebine.

    :param interval: Seznam intervalov za pridobivanje podatkov s spleta.
    :return: Čas, porabljen za izvedbo celotnega asinhronega testa.
    """
    async def fetch_data(session, interval):
        """
        Asinhrono pridobi podatke iz spletne strani za dani interval.

        :param session: Aiohttp seja za spletno povezavo.
        :param interval: Interval za pridobivanje podatkov s spleta.
        :return: Seznam podatkov za dani interval ali None, če zahteva ne uspe.
        """
        async with session.get(link + str(interval)) as response:
            if response.status in [410, 200]:
                html_text = await response.text()
                soup = bs(html_text, 'html5lib')
                okence = soup.find("div", {"class": "page-title"})
                data_temp = [item.get_text(strip=True) for item in okence.find_all("div", {"class": "boxItemGroup"})[0:4]]
                data_temp = [okence.findChildren()[1].get_text(strip=True)] + data_temp
                return data_temp
        return None

    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_data(session, i) for i in interval]
            results = await asyncio.gather(*tasks)
        

    # Začetni čas izvajanja
    start_time = timeit.default_timer()

    loop = asyncio.get_event_loop()
    # Izvedba asinhronega testiranja
    loop.run_until_complete(main())


    return timeit.default_timer() - start_time