from bs4 import BeautifulSoup
import requests
from csv import writer
import json

url = "https://balkanauction.com/bg/category/257/dzhobni-chasovnitsi/?sort=startDesc"

page = requests.get(url)

soup = BeautifulSoup(page.content, 'lxml')
lists = soup.find_all('a',class_="item_type-fixedPrice")


theAnswer = input("Would you like to make csv or json file?: ").lower()

if theAnswer == "csv":
    userInput = input("Enter the name of your file: ")
    filename = str(userInput) + ".csv"

    #with open(f"{filename}",'w',encoding='utf8',newline='') as f:
    #encoding='utf8' is making issues at the moment.Might need it later tho.

    with open(f"{filename}",'w',newline='') as f:
        thewriter = writer(f)
        header = ['Title','Price','Remaining time','Seller',"Link"]
        thewriter.writerow(header)
        for list in lists:
            title = list.find("div",class_="title").text
            price_int = list.find("span",class_="int-part").text
            price_frac = list.find("sup",class_="frac-part").text
            price = str(price_int) + "." + str(price_frac) + "лв."
            remaining_time = list.find("div",class_="time-remaining").text
            remaining_time = str(remaining_time)
            seller = list.find("span",class_="username").text
            tag = list['href']
            link = "https://balkanauction.com/" + str(tag)

            info = [title,price,remaining_time.strip(),seller,link]
            thewriter.writerow(info)
elif theAnswer == "json":
    userInput = input("Enter the name of your file: ")
    filename = str(userInput) + ".json"
    with open(f"{filename}", 'w', newline='') as f:
        for list in lists:
            title = list.find("div", class_="title").text
            price_int = list.find("span", class_="int-part").text
            price_frac = list.find("sup", class_="frac-part").text
            price = str(price_int) + "." + str(price_frac) + "лв."
            remaining_time = list.find("div", class_="time-remaining").text
            remaining_time = str(remaining_time)
            seller = list.find("span", class_="username").text
            tag = list['href']
            link = "https://balkanauction.com/" + str(tag)

            #info = [title, price, remaining_time.strip(), seller, link]
            info = {
                "Title": title,
                "Price": price,
                "Remaining_time": remaining_time.strip(),
                "Seller": seller,
                "Link": link
            }
            json_object = json.dumps(info, indent=4,ensure_ascii=False)
            f.write(json_object)