from bs4 import BeautifulSoup
import requests
import re
import csv 


def get_coins():
    url = "https://coinmarketcap.com/coins"
    html_content = requests.get(url).text
    with open('coins.csv', mode='w') as coins_file:
        coins_writer = csv.writer(coins_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        coins_writer.writerow(["SNo",'Name', 'Symbol', 'URL'])
        Data = {"Name": ' ', "Symbol": ' ', "URL": ' '}
        # Parse the html content
        soup = BeautifulSoup(html_content, "lxml")
        data_table = soup.find("table", attrs={"class": "cmc-table cmc-table___11lFC cmc-table-homepage___2_guh"})
        data_table_data = data_table.tbody.find_all("tr")
        #     count = 1
        #     for row in data_table.tbody.find_all("tr"):
        #         Data = {"Name": ' ', "Symbol": ' ', "URL": ' '}
        #         cells = row.findAll("td")[2]
        #         a_href_1 = cells.findAll("a")[0]
        #         # URL value here
        #         url_tag = a_href_1.get('href')
        #         div_2 = cells.findAll("div")[0]
        #         div_3 = div_2.findAll("div")[0]
        #         paragraph_1 = div_3.findAll("p")[0]
        #         Name = paragraph_1.get_text()
        #         div_4 = div_3.findAll("div")[0]
        #         div_5 = div_4.findAll("div")[0]
        #         paragraph_2 = div_5.findAll("p")[0]
        #         symbol = paragraph_2.get_text()
        #         Data["Name"] = Name
        #         Data["URL"] = url_tag
        #         Data["Symbol"] = symbol
        #         coins_writer.writerow(
        #             [count,Name, symbol, "https://coinmarketcap.com"+url_tag])
        #         count=count+1
        #         print(Data)
        for_except=0
        count=1
        while(count<=50):
            if(count<10):
                try:
                    for row in data_table.tbody.find_all("tr"):
                        cells = row.findAll("td")[2]
                        a_href_1 = cells.findAll("a")[0]
                        # URL value here
                        url_tag = a_href_1.get('href')
                        div_2 = cells.findAll("div")[0]
                        div_3 = div_2.findAll("div")[0]
                        paragraph_1 = div_3.findAll("p")[0]
                        Name = paragraph_1.get_text()
                        div_4 = div_3.findAll("div")[0]
                        div_5 = div_4.findAll("div")[0]
                        paragraph_2 = div_5.findAll("p")[0]
                        symbol = paragraph_2.get_text()
                        Data["Name"] = Name
                        Data["URL"] = url_tag
                        Data["Symbol"] = symbol
                        coins_writer.writerow([count,Name, symbol, "https://coinmarketcap.com"+url_tag])
                        count=count+1
                except:
                    continue
            else:
                div_10=soup.findAll("tr", {"class": "sc-14kwl6f-0 fletOv"})[for_except]
                #div = soup.find("div", {"id": "home-template"})
                tabel_data_div=div_10.findAll("td")[2]
                a_href_link=tabel_data_div.find("a")
                Name_span=a_href_link.findAll("span")[1]
                Name=Name_span.get_text()
                Symbol_span=a_href_link.findAll("span")[2]
                Symbol=Symbol_span.get_text()
                Data["Name"] = Name
                Data["URL"] = a_href_link.get('href')
                Data["Symbol"] = Symbol
                for_except+=1
                coins_writer.writerow([count,Name, Symbol, "https://coinmarketcap.com"+a_href_link.get('href')])
                count+=1
    

def get_coin_data(coin_symbol):
    value_tuple=[]
    new_value_tuple=[]
    with open('coins.csv', 'r') as file:
        reader = csv.reader(file,skipinitialspace=True)
        for row in reader:
            value_tuple.append(row)
    for i in range(0,len(value_tuple)):
        if i%2==0:
            new_value_tuple.append(value_tuple[i])
    for i in range(0,len(new_value_tuple)):
        if new_value_tuple[i][2]==coin_symbol:
            url=new_value_tuple[i][3] 
    with open('coins.csv', mode='a') as coins_file:
        coins_writer = csv.writer(
            coins_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        coins_writer.writerow(["Symbol",'Name', 'WatchlistCount	', 'Website URL',"Circulating Supply %","Price","Volume/Market Cap","Market Dominance","Rank","Market Cap","All Time High - DATE","All Time High - PRICE","All Time Low  - DATE","All Time Low  - PRICE","What is <Coin Name>?","Who are the founders?","What makes it unique?"])
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, "lxml")
        txt=soup.find("h2", attrs={"class": "sc-1q9q90x-0 iYFMbU h1___3QSYG"})
        txt2=soup.find("small", attrs={"class": "nameSymbol___1arQV"})
        #SYMBOL
        symbol=txt2.get_text()
        result = re.findall('[A-Z][^A-Z]*', txt.get_text())
        name=result[0]
        website=soup.find("a", attrs={"class": "button___2MvNi"})
        Website_URL=website.get("href")

        div_1=soup.find("div", attrs={"class": "sc-16r8icm-0 frLsAa container___E9axz"})
        table_1=div_1.find("table")
        value=table_1.tbody.findAll("tr")[0]
        #Price
        Price=value.findAll("td")[0].get_text()
        value_2=table_1.tbody.findAll("tr")[4]
        #Volume/Market Cap
        Volume=value_2.findAll("td")[0].get_text()
        value_3=table_1.tbody.findAll("tr")[5]
        #Market_Domin
        Market_Domain=value_3.findAll("td")[0].get_text()
        value_4=table_1.tbody.findAll("tr")[6]
        #Market_Rank
        Market_Rank=value_4.findAll("td")[0].get_text()
        #Market Cap
        table_2=div_1.find_all('table')[1]
        value=table_2.tbody.findAll("tr")[0]
        Market_cap=value.findAll("td")[0].get_text()
        #ALL TIME HIGH
        table_3=div_1.find_all('table')[3]
        value_1=table_3.tbody.findAll("tr")[4]
        All_Time_High_Date=value_1.findAll("small")[0]
        All_Time_High_Date=All_Time_High_Date.get_text()
        All_Time_High_Price=value_1.findAll("span")[0]
        All_Time_High_Price=All_Time_High_Price.get_text()
        #ALL TIME LOW
        table_3=div_1.find_all('table')[3]
        value_2=table_3.tbody.findAll("tr")[5]
        All_Time_Low_Date=value_2.findAll("small")[0]
        All_Time_Low_Date=All_Time_Low_Date.get_text()
        All_Time_Low_Price=value_2.findAll("span")[0]
        All_Time_Low_Date=All_Time_Low_Price.get_text()
         #WHAT IS ?
        try:
            paragraph_1=soup.find("div", attrs={"class": "sc-1lt0cju-0 srvSa"})
            value_7=paragraph_1.find_all("h2")[0]
            try:
                string_1=value_7.strong.get_text()
            except:
                string_1=value_7.get_text()
            tag_lister=["h4","h1","h2","h3","h5"]
            for element in value_7.next_siblings:
                if(element.name=="h3"):
                    break
                else:
                    
                    string_1=string_1+str(element.get_text())
        except:
            string_1="DATA NOT FOUND"
        #FOUNDER
        try:
            value_8=paragraph_1.find_all("h3")[0]
            try:
                string_2=value_8.strong.get_text()
            except:
                string_2=value_8.get_text()
            for element in value_8.next_siblings:
                if(element.name=="h4"):
                    break
                else:
                    string_2=string_2+str(element.get_text())
        except:
            string_2="DATA NOT FOUND"
        #UNIQUE
        try:
            value_9=paragraph_1.find_all("h4")[0]
            try:
                string_3=value_9.strong.get_text()
            except:
                string_3=value_9.get_text()
            for element in value_9.next_siblings:
                if(element.name=="h5"):
                    break
                else:  
                    string_3=string_3+str(element.get_text())
        except:
            string_3="Data NOT FOUND"
        
        #Watch List Count
        watch_list_div_1=soup.find("div", attrs={"class": "sc-16r8icm-0 cCqhlo"})
        watch_list_div_2=watch_list_div_1.findAll("div")[2]
        Watch_List_Count=watch_list_div_2.get_text()
        #Circulating Value
        circulating_supply_div=soup.find("div", attrs={"class": "statsValue___2iaoZ"})
        Circualting_value=circulating_supply_div.get_text()
        coins_writer.writerow(
                [symbol,name,Watch_List_Count,Website_URL,Circualting_value,Price,Volume,Market_Domain,Market_Rank,Market_cap,All_Time_High_Date,All_Time_High_Price,All_Time_Low_Date,All_Time_Low_Price,string_1,string_2,string_3])





get_coins()
get_coin_data("BTC")