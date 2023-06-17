import ccxt
from datetime import datetime, timedelta

# Print ASCII text message
print("""

                                         ██████╗███████╗ ██╗███████╗                                              
                                        ██╔════╝██╔════╝███║╚════██║                                              
                                        ██║     ███████╗╚██║    ██╔╝                                              
                                        ██║     ╚════██║ ██║   ██╔╝                                               
                                        ╚██████╗███████║ ██║   ██║                                                
                                         ╚═════╝╚══════╝ ╚═╝   ╚═╝                                                
                                                                                                                  
     ██████╗ █████╗ ███╗   ██╗██████╗ ██╗     ███████╗    ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
    ██╔════╝██╔══██╗████╗  ██║██╔══██╗██║     ██╔════╝    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ██║     ███████║██╔██╗ ██║██║  ██║██║     █████╗      ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
    ██║     ██╔══██║██║╚██╗██║██║  ██║██║     ██╔══╝      ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
    ╚██████╗██║  ██║██║ ╚████║██████╔╝███████╗███████╗    ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                                                                                  


""")

# Set up Binance API credentials
binance_api_key = "ENTER YOUR API KEY HERE"
binance_api_secret = "ENTER YOUR API SECRET HERE"

# Set up KuCoin API credentials
kucoin_api_key = "ENTER YOUR API KEY HERE"
kucoin_api_secret = "ENTER YOUR API SECRET HERE"

# Read coin data from the spreadsheet
coin_data = []
with open('data.csv', 'r') as file:
    lines = file.readlines()
    headers = lines[0].strip().split(',')
    for line in lines[1:]:
        data = line.strip().split(',')
        coin_data.append(dict(zip(headers, data)))

# Instantiate the Binance API
binance = ccxt.binance({
    'apiKey': binance_api_key,
    'secret': binance_api_secret
})

# Instantiate the KuCoin API
kucoin = ccxt.kucoin({
    'apiKey': kucoin_api_key,
    'secret': kucoin_api_secret
})

# Load the market symbols supported by Binance and KuCoin
binance.load_markets()
kucoin.load_markets()

# Fetch OHLCV data for each coin
total_coins = len(coin_data)
for index, coin in enumerate(coin_data):
    symbol = coin['Symbol']
    date_str = coin['Date']
    days = int(coin['Days'])

    # Set the start time for data collection
    start_time = datetime.strptime(date_str, "%d/%m/%Y")

    # Set the end time as the current datetime
    end_time = datetime.now()

    # Convert the start and end times to UNIX timestamps
    start_timestamp = int(start_time.timestamp() * 1000)
    end_timestamp = int(end_time.timestamp() * 1000)

    # Set the desired timeframe
    timeframe = '15m'

    # Check if the symbol is supported on Binance
    binance_symbol = binance.markets.get(symbol)
    if binance_symbol is None:
        print(f"Skipping {symbol} - Symbol not found on Binance.")
        continue

    # Check if the symbol is supported on KuCoin
    kucoin_symbol = kucoin.markets.get(symbol)
    if kucoin_symbol is None:
        print(f"Skipping {symbol} - Symbol not found on KuCoin.")
        continue

    # Determine the exchange with earlier data
    binance_start_timestamp = binance.fetch_ohlcv(symbol, timeframe, limit=1)[0][0]
    kucoin_start_timestamp = kucoin.fetch_ohlcv(symbol, timeframe, limit=1)[0][0]

    if binance_start_timestamp <= kucoin_start_timestamp:
        exchange = binance
    else:
        exchange = kucoin

    # Create a list to store the OHLCV data
    filtered_data = []

    # Fetch OHLCV data in chunks to cover the desired period
    current_timestamp = start_timestamp
    while current_timestamp <= end_timestamp:
        # Limit the number of data points to fetch in each request to avoid exceeding the API rate limits
        limit = 500

        # Fetch OHLCV data from the selected exchange
        try:
            ohlcv_data = exchange.fetch_ohlcv(symbol, timeframe, since=current_timestamp, limit=limit)
        except ccxt.BaseError as e:
            print(f"Failed to fetch OHLCV data for {symbol} from {exchange.name}: {str(e)}")
            break

        # Check if OHLCV data is empty
        if len(ohlcv_data) == 0:
            break

        # Extract data from the fetched OHLCV data and filter based on the specified timeframe
        for item in ohlcv_data:
            timestamp = datetime.fromtimestamp(item[0] / 1000)
            if start_time <= timestamp <= end_time:
                filtered_data.append([
                    timestamp,
                    item[1],
                    item[2],
                    item[3],
                    item[4],
                    item[5]
                ])

        # Update the current timestamp to the next available timestamp
        current_timestamp = ohlcv_data[-1][0] + (ohlcv_data[1][0] - ohlcv_data[0][0])

        # Break the loop if we've reached the end of the desired range
        if current_timestamp > end_timestamp:
            break

        # Calculate progress
        progress = (current_timestamp - start_timestamp) / (end_timestamp - start_timestamp) * 100

        # Display progress bar
        filled_length = int(50 * progress / 100)
        bar = '█' * filled_length + '-' * (50 - filled_length)
        print(f"\rProgress: |{bar}| {progress:.2f}%", end='', flush=True)

    # Save the filtered OHLCV data to a CSV file
    csv_filename = f"{symbol.replace('/', '_')}_ohlcv_data.csv"
    with open(csv_filename, 'w') as file:
        file.write("timestamp,open,high,low,close,volume\n")
        for row in filtered_data:
            file.write(",".join(str(value) for value in row) + "\n")

    print(f"\rProgress: |{'█' * 50}| 100.00%")
    print(f"OHLCV data for {symbol} saved to {csv_filename}.")

    # Calculate and print overall progress
    overall_progress = (index + 1) / total_coins * 100
    filled_length = int(50 * overall_progress / 100)
    bar = '█' * filled_length + '-' * (50 - filled_length)
    print(f"\rOverall Progress: |{bar}| {overall_progress:.2f}%", end='', flush=True)

print("\nData retrieval complete.")
