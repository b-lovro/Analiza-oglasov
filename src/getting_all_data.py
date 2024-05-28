from bs4 import BeautifulSoup as bs
import csv
import aiohttp
import asyncio
link='https://www.mojedelo.com/studentsko-delo/d-'

def write_rows(data, file_name='temp',type='a'):
    f = open(file_name+'.csv', type ,newline='', encoding='utf-8')
    writer = csv.writer(f)
    writer.writerows(data)
    f.close()

def get_data_async(start,end):
    interval=range(start,end)
    
    async def fetch_data(session, index):
        async with session.get(link + str(index)) as response:
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
        
        all_data = [result for result in results if result]

        write_rows(all_data,'podatki/Oglasi/all_data')


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
 
