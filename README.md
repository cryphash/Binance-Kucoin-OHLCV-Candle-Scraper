

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
                                                                                                              



If you're reading this you'd like to run this code, I'd first like to credit ChatGPT for authoring this code with the help of it's lowly human assistant CH.

This script will return data from KuCoin or Binance depending on where the earliest availble data is, e.g. if Binance listed before KuCoin then the the data from Binance will be returned.

In order to run this code you will need to set up a .csv file with the headers Coin, Date and Days. This .csv file should be named "Data".

The "Coin" colunn should specify the ticker for the token you with the pair seperated by a forward slash, for example "BLUR/USDT".

The "Date" column should be populated in DD MM YYYY seperated by a forward slash, for example "01/01/23".

The "Days" column should be the number of days between todays date and the day you would like to pull data for, for example "4" would pull 4 days data.

Open your command terminal and paste "pip install ccxt" and hit return. This will install the libraries needed to run this code.

Open the CS17 python file in a code editor like Notepad++ and enter in your API Keys in the "ENTER YOUR API SECRET KEY HERE" & "ENTER YOUR API KEY HERE" fields, within the quotation marks.

Edit your candle size as desired by editing the value inside the quotation marks, for example "timeframe = '15'" will produce 15 minute candles.

In order to run the code navigate to the directory that contains the file and paste "python CS17.py".

The code will the run through the list of the coins you have provided outputting .csv files with the name format "(TICKER)_(PAIR)_ohlcv_data".


Until next time, 
CH
