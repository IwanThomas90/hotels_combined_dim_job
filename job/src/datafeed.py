# import requests
# import csv
#
# csv_url = 'Datafeeds.Hotelscombined.com/Datafeed.ashx?id=43186&type=HOTEL& \ ' \
#            'PrivateDataKey=11111&OutputType=CSV&LanguageCode=EN'
#
# with requests.Session() as s:
#     download = s.get(csv_url)

import pandas as pd

# should private key be private?
csv_url = 'Datafeeds.Hotelscombined.com/Datafeed.ashx?id=43186&type=HOTEL& \ ' \
           'PrivateDataKey=11111&OutputType=CSV&LanguageCode=EN'

download = pd.read_csv(csv_url)

# do i need to read csv?
# put into a function