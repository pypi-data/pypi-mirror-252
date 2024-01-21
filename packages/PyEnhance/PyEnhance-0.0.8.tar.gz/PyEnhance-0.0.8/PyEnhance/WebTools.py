import requests as r
import socket as s


class WebTools:

    def __init__(self):

        self.PositiveStatusCodes = [200, 201, 202, 203, 204, 205, 206,
                                    300, 301, 302, 303, 304, 305, 307,
                                    308, 401]
        self.DirsChecked = []

        self.Headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

    def FetchTLDS(self):

        self.TLDSs = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
        print("getting TLDSs")
        response = r.get(self.TLDSs, headers=self.Headers)
        response.raise_for_status()

        # The file uses line breaks for each TLD, and we filter out comments which start with '#'
        self.TLDS = [line.strip().lower() for line in response.text.splitlines() if not line.startswith('#')]

    def CheckTLDS(self, URL=None):

        self.FetchTLDS()

        TLDSValid = False

        for i in self.TLDS:
            if URL.endswith("/"):
                URL = URL[:-1]
            if URL.endswith(i):
                TLDSValid = True
                break

        if TLDSValid is False:
            return False
        else:
            return True

    def IsIP(self, URL):

        try:
            s.inet_aton(URL)
            IsURLAnIPOutput = True
            if IsURLAnIPOutput == True:
                return True

        except s.error:
            IsURLAnIPOutput = False
            if IsURLAnIPOutput == False:
                return False

    def Refactor(self, URL=None):  # defines the refactor function and passes the URL variable as a parameter

        if URL.endswith("/"):  # Checks if the URL ends with a forward slash
            URL = URL[:-1]  # Removes the forward slash from the URL

        for i in "https://", "http://":
            if URL.startswith(i):
                if i == "https://":
                    self.URLHTTPS = URL
                    self.URLHTTP = URL.replace("https://", "http://")

                if i == "http//":
                    self.URLHTTP = URL
                    self.URLHTTPS = URL.replace("http://", "https://")

                break
            else:
                self.URLHTTP = f"http://{URL}"
                self.URLHTTPS = f"https://{URL}"

        return self.URLHTTPS and self.URLHTTP



    def HTTPcheck(self, URL=None):

        self.Refactor(URL=URL)


        URL = WebTools.URLHTTP

        GetReqStatus = r.get(url=URL, headers=self.Headers)

        if GetReqStatus.status_code in self.PositiveStatusCodes:
            return True
        else:
            return False

    def HTTPScheck(self, URL=None):

        self.Refactor(URL=URL)

        URL = WebTools.URLHTTPS

        GetReqStatus = r.get(url=URL, headers=self.Headers)

        if GetReqStatus.status_code == 200:
            return True
        else:
            return False


WebTools = WebTools()


"""

===EXAMPLES===


Command:
    WebTools.Refactor(URL='www.google.com') # Refactors URL by adding http and https

Example:
    WebTools.Refactor(URL='www.google.com')

    print(WebTools.URLHTTPS)
    print(WebTools.URLHTTP)


Command: 
    WebTools.HTTPcheck(URL='www.google.com') # Checks if URL using http is valid  
    
Example:
    if WebTools.HTTPcheck(URL='www.google.com') == True:
        print('HTTP is Valid')


Command:
    WebTools.HTTPScheck(URL='www.google.com') # Checks if URL using https is valid

Example:  
    if WebTools.HTTPScheck(URL='www.google.com') == True:
        print('HTTPS is Valid')


Command:
    WebTools.CheckTLDS(URL='www.google.com') # Checks if the URLs TLDS is valid 

Example:
    if WebTools.CheckTLDS(URL='www.google.com') == False: 
        print('TLDS is invalid')
    else:
        print('TLDS is valid')

"""