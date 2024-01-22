from bs4 import BeautifulSoup
import requests
import typer

def get_links(url: str=typer.Argument()):
    response=requests.get(url)
    if response.status_code == 200:
        parse=BeautifulSoup(response.text,'html.parser')

        links=parse.find_all('a')

        for link in links:
            href=link.get('href')
            print(href)


if __name__ == "__main__":
    typer.run(get_links)


# url = "https://www.example3.com/"
# get_links(url)