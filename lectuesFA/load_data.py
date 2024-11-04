import requests
import pandas as pd

class StockDataAPI:
    """
    class with methods to get and process data from alpha vantage
    """
    def __init__(self, api_key, data_function="TIME_SERIES_DAILY") -> None:
        """
        args:
            api_key: API key from alphavantage
        """
        self._data_function = data_function
        self.api_key = api_key

    def get_stock(self, symbol):
        url=f"https://www.alphavantage.co/query?function={self._data_function}&symbol={symbol}&apikey={self.api_key}&outputsize=full"
        
        try:
            data = requests.get(url).json()
            df = pd.DataFrame(data["Time Series (Daily)"]).transpose().astype(float)
            df.index = pd.to_datetime(df.index)
            df.columns = ["Open", "High", "Low", "Close", "Volume"]
            return df
        
        except ValueError as err:
            import pickle
            with open("/repos/AI24-Databehandling/Data/Stocksdata/AAPL_TIME_SERIES_DAILY_ADJUSTED.csv") as file:
                disk_data = pickle.load(file)
            disk_data = pd.concat(disk_data, axis=1)
            data=disk_data[symbol]
            df = pd.DataFrame(data["Time Series (Daily)"]).transpose().astype(float)
            df.index = pd.to_datetime(df.index)
            df.columns = ["Open", "High", "Low", "Close", "Volume"]
            
            return df

    



def run_test():
    import os
    api_key=os.getenv("ALPHA_API_KEY")
    test=StockDataAPI(api_key)
    print(f"result: {test.get_stock("AAPL")}")

if __name__ == "__main__":
    run_test()