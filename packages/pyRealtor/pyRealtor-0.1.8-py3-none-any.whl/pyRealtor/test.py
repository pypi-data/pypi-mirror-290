import requests
from requests.adapters import HTTPAdapter, Retry

from pyRealtor.proxy import Proxy
import sys

proxy = Proxy()
proxy.set_proxies()

search_api_endpoint = "https://api2.realtor.ca/Listing.svc/PropertySearch_Post"
search_api_params = {
            'Version': '7.0',
            'ApplicationId': '1',
            'CultureId': '1',
            'Currency': 'CAD',
            'RecordsPerPage': 1,
            'MaximumResults': 100,
            'ZoomLevel': 13,
            'LatitudeMax': 45.31383,
            'LongitudeMax': -75.67768,
            'LatitudeMin': 45.22648,
            'LongitudeMin': -75.83373,
            'Sort': '6-D',
            'PropertyTypeGroupID': 1,
            'TransactionTypeId': 2,
            'PropertySearchTypeId': 0,
            'CurrentPage': 1
        }
search_api_headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-GB,en;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://www.realtor.ca",
            "Priority": "u=1, i",
            "Referer": "https://www.realtor.ca/",
            "DNT": "1",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36"
        }

#search_api_headers["Cookie"] = "reese84=3:mRfR0qp1S5Sd4zoF9KJ21Q==:8k9NMrxA+cyb2I9DzYceTEt1oMyt/Z/XGP5wKrXKXQ+fE4BSzUUAuu8ZGuyJ7raHNeGMN7dFIERRMXLmaEDFZy0vNk+uWD/Rmky1Qe2t04cxhwqSL1VVN2juyW5Bu5O3X1z39U27Al/etVLY+4aTlvP5yzVWrEbMNmk//OMPjq/orkteqvdtoVcQ20pdxA9VtQqau3k2tpoWzazIJoOvtzAm6tPy2pNczXYwiM0r9R/hmLOcCGKPnAkwv8MIxi0TMPsAvpTX/y1AMrPi76XxB8PrKLuZtSF8uGa6HYmbfSrLPz4AX+ovWWsrVIXm1F8y7OSF6oibavtS9EC2Kb5uJF1GzEew4dhdJKoj6YfBzOQGSNptQ5nGPsN83TfG9kXhCPYoL0rCJw1CLbAper5R8Cvh3q5Geny4rkuzzloihocmtNjxxjNqJ3BiDfpluyEC+tpfmOdBkYUcZKL3Pr4Gng==:f9IK7yh97SfZ8L4Tc4AI6yrsnwkQe6HWYo8WvEal7Bg=;"

s = requests.Session()
s.headers.update(search_api_headers)

print(s.headers)
resp = s.post(
                    "https://www.realtor.ca/dnight-Exit-shall-Braith-Then-why-vponst-is-proc",
                    json = {
                        "solution":{
                                "interrogation":None,
                                "version":"beta"
                            },
                            "old_token":None,
                            "error":None,
                            "performance":{"interrogation":1897}
                    },
                    params = {"d": "www.realtor.ca"}
                )
print(resp.content)
sys.exit(0)

while proxy.rotate_proxy():
    print(proxy.current_proxy)
    proxies = {
                        'http': proxy.current_proxy, 
                        'https': proxy.current_proxy
                    }

    try:
        realtor_api_response = requests.post(
                            search_api_endpoint,
                            headers=search_api_headers,
                            data = search_api_params
                        )
    except Exception as e:
        continue

    print(realtor_api_response.content)
    sys.exit(0)

