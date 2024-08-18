import requests
from bs4 import BeautifulSoup
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView, QPushButton, QTextBrowser
from PyQt5 import uic
import sys
from PyQt5.QtCore import QAbstractTableModel, Qt
import random

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super(PandasModel, self).__init__()
        self._data = data

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data.columns)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi("scrape_quote.ui", self)

        self.show()

        self.table_datas = self.findChild(QTableView, "table_datas")
        self.scrapeAll = self.findChild(QPushButton, "btn_scrapeQuotes")
        self.show_All = self.findChild(QPushButton, "btn_showAllQuotes")
        self.save_Excel = self.findChild(QPushButton, "btn_saveToExcel")
        self.text_Random = self.findChild(QTextBrowser, "textarea_random")
        self.random_Button = self.findChild(QPushButton, "btn_randomQuote")

        self.scrapeAll.clicked.connect(self.scrape_datas)
        self.show_All.clicked.connect(self.show_datas)
        self.save_Excel.clicked.connect(self.save_to_excel)
        self.random_Button.clicked.connect(self.pickRandom)


        self.data = []


    def show_datas(self):
        if self.data:
            df = pd.DataFrame(self.data)
            model = PandasModel(df)
            self.table_datas.setModel(model)
        else:
            print("No data yet!")

    def scrape_datas(self):
        self.data = []  
        for page in range(1, 11):
            url = f"https://quotes.toscrape.com/page/{page}/"
            print(f"Datas getting from {url}...")

            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            quote_box = soup.find_all("div", class_="quote")

            for quote in quote_box:
                text = quote.find(class_="text").text
                author = quote.find(class_="author").text
                tags = [tag.text for tag in quote.find_all("a", class_="tag")]

                quote_data = {
                    "text": text,
                    "author": author,
                    "tags": ", ".join(tags)
                }
                self.data.append(quote_data)
        
        print("Scrape operation completed!")

    def save_to_excel(self):
        if self.data:
            df = pd.DataFrame(self.data)
            df.to_excel("scraped_quotes.xlsx", index=False)
            print("Datas saved to excel file.")
        else:
            print("No data to save.")

    def pickRandom(self):
        if self.data:
            random_quote = random.choice(self.data)
            text = random_quote.get("text", "No quote available")
            author = random_quote.get("author", "Unknown")
            display_text = f'"{text}" - {author}'
            self.text_Random.setText(display_text)
        else:
            print("Please scrape data first!")


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
