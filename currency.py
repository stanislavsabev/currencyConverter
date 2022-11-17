import traceback
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

import requests


class CurrencyRepo:
    def __init__(self, url) -> None:
        self._url = url
        self._data: Dict[str, float] = {}
        self._eoh = 6
        self._timeout = 15

    def _getXml(self):
        resp = requests.get(url=self._url, timeout=self._timeout)
        if not resp.ok:
            resp.raise_for_status()
        return ET.fromstring(resp.text)

    def getCurrencies(self) -> Dict[str, float]:
        if not self._data:
            root = list(self._getXml().iter("*"))
            for i, child in enumerate(root):
                if i < self._eoh:
                    continue
                currency = child.attrib["currency"]
                rate = float(child.attrib["rate"])
                self._data[currency] = rate
        return self._data


def printAvailableCurrencies(currencyList: List[str]):
    print("List of currencies convertable", end="\n\n")
    print(" ".join(currencyList), end="\n\n")


def getUserAmount() -> Optional[int]:
    amount = None
    try:
        amount = int(input("Enter the amount to convert (whole number > 0) : "))
    except ValueError:
        print("Not a valid number")
        return None
    if amount < 0:
        print("Number must be > 0")
        return None
    return amount


def getUserCurrency(availableCurrencies: set) -> Optional[str]:
    currency = str(input("To which currency? (3 letters) : ")).upper()
    if currency not in availableCurrencies:
        print("Invalid currency code.")
        return None
    return currency


def convert(amount: int, toCurrency: str, currencyData: Dict[str, float]):
    rate = currencyData[toCurrency]
    return rate * amount


def main():
    try:
        repo = CurrencyRepo(
            url="https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
        )
        currencyData = repo.getCurrencies()
        printAvailableCurrencies(list(currencyData.keys()))
        amount = getUserAmount()
        if not amount:
            return
        currency = getUserCurrency(currencyData.keys())
        if not currency:
            return
        result = convert(amount, currency, currencyData)
        print(f"{amount:2f} EUR = {result:8f} {currency}")

    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()
