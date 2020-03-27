import xml.etree.ElementTree as ET
import requests

def getxml(url):
    resp = requests.get(url)
    root = ET.fromstring(resp.text)
    return root

def convert(amount, toCurrency):
    url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
    root = getxml(url)
    amountConverted = -1
    for i, child in enumerate(root.iter('*')):
        if i >= 6:
            if child.attrib['currency'] == toCurrency:
                rate = child.attrib['rate']
                amountConverted = float(rate) * amount
    if amountConverted == -1:
        return False
    return amountConverted
def getListCurrency():
    url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
    root = getxml(url)
    listCurrency = set()
    for i, child in enumerate(root.iter('*')):
        if i >= 6:
            listCurrency.add(child.attrib['currency'])
    return listCurrency
def main():
    try:
        listCurrency = getListCurrency()
        print('List of currency convertable\n')
        for currency in listCurrency:
            print(currency,end = ' ')
        print('\n')
        amount   = int(input('Enter the amount to convert : '))
        currency = str(input('To which currency (3 letters) : ')).upper()
        print(convert(amount, currency))
    except:
        print('Not a number')
    
        
main()