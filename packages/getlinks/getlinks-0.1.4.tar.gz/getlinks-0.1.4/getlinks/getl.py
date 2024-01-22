from bs4 import BeautifulSoup
import requests
import typer

class Getlinkd:
    def main(self, url: str):
        response=requests.get(url)
        if response.status_code == 200:
            parse=BeautifulSoup(response.text,'html.parser')

            links=parse.find_all('a')
            href = []
            for link in links:
                href.append(link.get('href'))
        return href





# url = "https://www.example3.com/"
# # get_links(url)
# g = Getlinkd()
# print(g.main(url))