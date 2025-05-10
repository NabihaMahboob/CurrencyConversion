import sys
import json
from warnings import catch_warnings

import requests

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QComboBox, QInputDialog, QLineEdit, QMessageBox


def get_currency_info():
    url = "https://v6.exchangerate-api.com/v6/f6343c16215ac8b049640cac/latest/USD"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data

    else:
        return None



global currentExchangeRate
currencyData = get_currency_info()
if currencyData is None:
    sys.exit()

exchangeInfo = currencyData['conversion_rates']

with open("code_to_currency.json", "r") as currenciesFile:
    currencyToCountry = json.load(currenciesFile)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('Currency Convertor App')
window.setGeometry(100, 100, 500, 500)

label = QLabel('<center>Select your currencies</center>', parent=window)
label.setGeometry(125, 10, 200, 30)

fromLabel = QLabel('From', parent=window)
fromLabel.setGeometry(30, 50, 60, 30)

toLabel = QLabel('To', parent=window)
toLabel.setGeometry(30, 100, 60, 30)

fromDropdown = QComboBox(parent=window)
fromDropdown.setGeometry(100, 50, 250, 30)

toDropdown = QComboBox(parent=window)
toDropdown.setGeometry(100, 100, 250, 30)


for currency, rate in exchangeInfo.items():
    fromDropdown.addItem(currency + ' ' + currencyToCountry[currency])
    toDropdown.addItem(currency + ' ' + currencyToCountry[currency])

currency1 = fromDropdown.currentText()
currency2 = toDropdown.currentText()
rateLabel = QLabel('', parent=window)
rateLabel.setGeometry(50, 150, 500, 100)


def change_from_currency():
    global currentExchangeRate
    currency1 = fromDropdown.currentText()
    currency2 = toDropdown.currentText()

    if currency1 == 'USD United States Dollar':
        rate = exchangeInfo[currency2[:3]]
        rateLabel.setText('1 USD United States Dollar = ' + str(rate) + ' '+ currency2)
        currentExchangeRate = rate
    elif currency2 == 'USD United States Dollar':
        rate = exchangeInfo[currency1[:3]]
        rateLabel.setText(str(rate) + ' ' + currency1 + ' = 1 USD United States Dollar')
        currentExchangeRate = rate
    else:
        rate = exchangeInfo[currency2[0:3]]/exchangeInfo[currency1[0:3]]
        rateLabel.setText('1 ' + currency1 + " = "+ str(round(rate, 4)) + ' ' + currency2)
        currentExchangeRate = rate


change_from_currency()
fromDropdown.currentIndexChanged.connect(change_from_currency)
toDropdown.currentIndexChanged.connect(change_from_currency)

amountLabel = QLabel('<center> Enter an amount to exchange</center>', parent=window)
amountLabel.setGeometry(125, 250, 200, 30)

amountInput = QLineEdit(parent=window)
amountInput.setGeometry(50, 300, 100, 30)

amountfromLabel = QLabel(currency1[:3], parent=window)
amountfromLabel.setGeometry(160, 300, 100, 30)

exchangedAmountLabel = QLabel('  ' + currency2[:3], parent=window)
exchangedAmountLabel.setGeometry(300, 300, 200, 30)



def exchangeAmount():
    info = amountInput.text()
    try:
        amount = float(info)
        currency = toDropdown.currentText()
        exchangedAmount = amount * currentExchangeRate
        exchangedAmountLabel.setText(str(round(exchangedAmount, 4)) + ' ' + currency[0:3])
    except:
        print('Invalid input')
        currency = toDropdown.currentText()
        exchangedAmountLabel.setText(currency[0:3])
        QMessageBox(QMessageBox.Critical, 'Error', 'Please enter a number')



amountInput.textChanged.connect(exchangeAmount)
fromDropdown.currentIndexChanged.connect(exchangeAmount)
toDropdown.currentIndexChanged.connect(exchangeAmount)



window.show()
sys.exit(app.exec_())








