from stock.utils import store_stock_api
import json, os

class StockAPI:
    def store_stock_data(self, period, file_name):
        """Stores stock data based on time period."""
        return store_stock_api(period, file_name)
    
    def get_stock_data_from_json(self, file_name):
        """Reading stored stock data from the specified filepath."""
        if os.path.exists(file_name):
            try:
                with open(file_name, 'r', encoding='utf-8') as json_file:
                    json_content = json.loads(json_file.read())
                    return json_content, None
            except Exception as exc:
                return None, f'Error reading file:\n{exc}'
        else:
            return None, f'No filepath such as {file_name} exists.'