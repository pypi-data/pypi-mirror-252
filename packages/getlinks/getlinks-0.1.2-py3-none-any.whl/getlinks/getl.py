from bs4 import BeautifulSoup
import requests
import typer

def main(url):
    response=requests.get(url)
    if response.status_code == 200:
        parse=BeautifulSoup(response.text,'html.parser')

        links=parse.find_all('a')

        for link in links:
            href=link.get('href')
            print(href)


if __name__ == "__main__":
    url=input("enter url")
    main(url)


# url = "https://www.example3.com/"
# get_links(url)