from stockstir import Stockstir

# Instantiate a new Stockstir object like we did above:
stockstir = Stockstir(print_output = True)
# Instantiate the classes within the Stockstir object (used to access the functions without having to stockstir.classname.function() every time):
providers = stockstir.providers
tools = stockstir.tools
api = stockstir.api

price = tools.get_single_price("AAPL")

print(price)