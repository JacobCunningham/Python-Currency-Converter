from urllib import request
from currency import Currency
import urllib
import json, os, datetime



class FetchExchangeRateError(Exception):

    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class Converter:

    def __init__(self, base, filep="exchangerates.json",cache=False, **kwargs):
        
        self.base_currency = base.upper()
        self.exchange_file_path = filep
        self.cache_rates = cache
        
        if 'date' in kwargs.keys():
            self.exchange_date == kwargs['date']
        else:
            self.exchange_date = datetime.date.today()

        self.exchange_rates = self.get_exchange_rate()

    def convert_to_base(self, cur_obj):
        
        if cur_obj.type == self.base_currency:
            return cur_obj
        else:
            cur_obj.amount = cur_obj.amount * (1/self.exchange_rates['rates'][cur_obj.type])
            cur_obj.type = self.base_currency
            return cur_obj

    def get_exchange_rate(self):

        if self.cache_rates == True:
            if self.er_cache_exists():
                return self.get_er_from_file()
            else:
                return self.write_er_cache()
        else:
            return self.fetch_exchange_rate(self.exchange_date, self.base_currency)

    def get_er_from_file(self):
        with open(self.exchange_file_path, 'r+') as efile:
            e_rates = json.load(efile)
    
            if e_rates['date'] != datetime.date.today() or e_rates['base'] != self.base_currency:
                e_rates = self.fetch_exchange_rate(self.exchange_date, self.base_currency)
                efile.seek(0)
                json.dump(e_rates, efile)
                efile.close()
                return e_rates
            
            efile.close()
            return e_rates
    
    def fetch_exchange_rate(self, date, base):
        try:
            response =  request.urlopen(f"https://api.exchangeratesapi.io/{date}?base={base}")
        except urllib.error.URLError:
            raise FetchExchangeRateError("Failed to fetch exchange rates", urllib.error.URLError)
        return json.load(response)

    def convert_to(self, cur_obj, dest_cur):
        dest_cur = dest_cur.upper()

        if cur_obj.type == dest_cur:
            return cur_obj
        elif dest_cur == self.base_currency:
            return self.convert_to_base(cur_obj)
        else:
            cur_obj = self.convert_to_base(cur_obj)
            cur_obj.amount = cur_obj.amount * self.exchange_rates['rates'][dest_cur]
            cur_obj.type = dest_cur
            return cur_obj

    def check_er_cache(self):
        if os.path.exists(self.exchange_file_path):
            return True
        else:
            return False

    def write_er_cache(self):
        e_rates = self.fetch_exchange_rate(self.exchange_date, self.base_currency)
        with open(self.exchange_file_path, 'w') as efile:        
            json.dump(self.exchange_rates, efile)
            efile.close()
        return e_rates








