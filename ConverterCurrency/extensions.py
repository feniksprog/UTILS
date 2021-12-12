import requests
import json
from config import keys


class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):          
        if quote == base:
            raise APIException(f'Указаны одинаковые валюты - {base}!')

        try:
            quote_ticker= keys[quote]
        except KeyError:
            raise APIException(f'Не удается обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удается обработать валюту {base}')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удается обработать количество {amount}')
              
        try:
            r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
            total_base = json.loads(r.content)[keys[base]]   
            total_base = float(total_base)*amount 
            # total_base = round(total_base, 6)
        except ValueError:
            raise APIException(f'Не удается обработать количество {total_base}')
        
        return total_base