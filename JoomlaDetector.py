import sys
import requests
from colorama import Fore, Style
import xmltodict
from mechanize import Browser
from bs4 import BeautifulSoup

def JoomlaDetector(webpage, action):
    joomlaxml = f"{webpage}/administrator/manifests/files/joomla.xml"

    if action == "detect":
        try:
            req = requests.get(joomlaxml)
            if req:
                return True
            else:
                webhtml = JoomlaDetector(webpage, "html")
                soup = BeautifulSoup(webhtml, features="lxml")
                joomlameta = soup.find("meta", attrs={"name": "generator"})

                if "Joomla" in joomlameta["content"]:
                    return "no_info"
                else:
                    return False
        except requests.exceptions.RequestException as e:
            print(e)
            return "exc"
    elif action == "getinfo":
        req = requests.get(joomlaxml).text
        data = xmltodict.parse(req)
        return data
    elif action == "html":
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        req = requests.get(webpage, headers=headers).text
        return req



def main():
    webpage = sys.argv[1]
    if not webpage:
        print(f"{Fore.RED}[!] Set a URL!{Fore.RESET}")
    else:
        if not webpage.startswith("http"):
            print(f"{Fore.RED}[!] You need to write the complete URL! {Style.BRIGHT}(http/https){Style.RESET_ALL}{Fore.RESET}")
        else:
            detect = JoomlaDetector(webpage, "detect")
            if detect:
                try:
                    data = JoomlaDetector(webpage, "getinfo")

                    br = Browser()
                    br.open(webpage)
                    webtitle = br.title()

                    showdata = f"""
        {Fore.YELLOW}Webpage name: {Fore.LIGHTBLUE_EX}{webtitle}
        
        {Fore.YELLOW}Joomla! Version: {Fore.LIGHTBLUE_EX}{data["extension"]["version"]}
        {Fore.YELLOW}Creation date: {Fore.LIGHTBLUE_EX}{data["extension"]["creationDate"]}{Fore.RESET}
                    """
                    print(f"{Fore.LIGHTGREEN_EX}[✓] This webpage uses Joomla!{Fore.RESET}")

                    print(showdata)

                except:
                    print(f"{Fore.LIGHTRED_EX}[?] This webpage uses Joomla, but not info given{Fore.RESET}")

            elif detect == "exc":
                print(f"{Fore.RED}[!] Error requesting the webpage!{Fore.RESET}")
            elif detect == "exc":
                print(f"{Fore.LIGHTRED_EX}[?] This webpage uses Joomla, but not info given{Fore.RESET}")
            else:
                print(f"{Fore.RED}[!] This webpage doesn't use Joomla!{Fore.RESET}")


if __name__ == '__main__':
    main()
