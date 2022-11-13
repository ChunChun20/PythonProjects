from bs4 import BeautifulSoup
import requests
from csv import writer
from csv import reader
import json
import sqlite3


def getInfoCSV(page, filename, count, cat, sort_type):
    url = f"https://balkanauction.com/bg/category/{cat}/{sort_type}&offset={page}"

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'lxml')
    lists = soup.find_all('a', class_="item")

    with open(f"{filename}", 'a', newline='') as f:
        thewriter = writer(f)
        header = ['Title', 'Price', 'Remaining time', 'Seller', "Link"]
        if count == 0:
            thewriter.writerow(header)
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

            info = [title, price, remaining_time.strip(), seller, link]
            thewriter.writerow(info)


def getInfoJSON(page, cat, sort_type):
    url = f"https://balkanauction.com/bg/category/{cat}/{sort_type}&offset={page}"

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'lxml')
    lists = soup.find_all('a', class_="item")
    jsonList = []

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

        # info = [title, price, remaining_time.strip(), seller, link]
        info = {
            "Title": title,
            "Price": price,
            "Remaining_time": remaining_time.strip(),
            "Seller": seller,
            "Link": link
        }
        jsonList.append(info)
    return jsonList


def getSQL(fname):
    conn = sqlite3.connect("C:\databases\coursework.db")
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS mytable')
    cur.execute('''
    CREATE TABLE "mytable"(
        "title" TEXT,
        "price" TEXT,
        "remaining_time" TEXT,
        "seller" TEXT,
        "link" TEXT
    )
    ''')

    with open(fname) as f:
        csv_reader = reader(f, delimiter=',')
        for row in csv_reader:
            print(row)
            title = row[0]
            price = row[1]
            remaining_time = row[2]
            seller = row[3]
            link = row[4]
            cur.execute('''INSERT INTO mytable(title,price,remaining_time,seller,link)
                VALUES (?,?,?,?,?)''', (title, price, remaining_time, seller, link))
            conn.commit()


theAnswer = input("Would you like to make csv , json file or sql?: ").lower()


def cat_func():
    try:
        categories = """
             1.stenni-chasovnitsi
             2.dzhobni-chasovnitsi
             3.nastolni-chasovnitsi
             4.ruchni-chasovnitsi
        """
        print(categories)
        user_cat = int(input("Choose category: "))
        if user_cat == 1:
            cat = "745/stenni-chasovnitsi"
            return cat
        elif user_cat == 2:
            cat = "257/dzhobni-chasovnitsi"
            return cat
        elif user_cat == 3:
            cat = "743/nastolni-chasovnitsi"
            return cat
        elif user_cat == 4:
            cat = "744/ruchni-chasovnitsi"
            return cat
        else:
            print("Wrong choice!")
            cat_func()
    except:
        cat_func()


def sort_func():
    try:
        sorting = """
             1.Nai-evtini
             2.Nai-skupi
             3.Nai-novi
             4.Zavurshvashti
        """
        print(sorting)
        user_sort = int(input("Sort by: "))
        if user_sort == 1:
            sort_type = "?sort=priceAsc"
            return sort_type
        elif user_sort == 2:
            sort_type = "?sort=priceDesc"
            return sort_type
        elif user_sort == 3:
            sort_type = "?sort=startDesc"
            return sort_type
        elif user_sort == 4:
            sort_type = "?sort=endAsc"
            return sort_type
        else:
            print("Wrong choice!")
            sort_func()
    except:
        sort_func()


if theAnswer == "csv":
    cat = cat_func()
    sort_type = sort_func()
    userInput = input("Enter the name of your file: ")
    filename = str(userInput) + ".csv"
    count = 0

    for i in range(0, 121, 60):
        getInfoCSV(i, filename, count, cat, sort_type)
        count += 1
elif theAnswer == "json":
    cat = cat_func()
    sort_type = sort_func()
    userInput = input("Enter the name of your file: ")
    filename = str(userInput) + ".json"
    finalList = []
    for i in range(0, 121, 60):
        finalList.append(getInfoJSON(i, cat, sort_type))
    with open(f"{filename}", 'a', newline='') as f:
        json.dump(finalList, f, indent=4, ensure_ascii=False)
elif theAnswer == "sql":
    userInput = input("Enter the name of your file: ")
    getSQL(userInput)
