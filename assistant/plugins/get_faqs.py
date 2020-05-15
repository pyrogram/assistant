from bs4 import BeautifulSoup
from aiohttp import ClientSession
import asyncio


class Scraper:
    """
    Scrape the FAQ from pyrogram's docs. (https://docs.pyrogram.org/faq)
    """
    URL_DOCS = "https://docs.pyrogram.org/faq"
    def __init__(self):
        self.__faqs = None
        self.scraper = asyncio.run(self.request())
    
    async def request(self):
        async with ClientSession() as request:
            async with request.get(X.URL_DOCS) as resp:
                scraper = BeautifulSoup(await resp.text(), 'html.parser')
                return scraper
    
    @staticmethod
    def _make_url_absolute(url: str) -> str:
        if not url.startswith('http'):
            return 'https://docs.pyrogram.org/faq' + url
        return url

    def get_faqs(self):
        faq_container = self.scraper.find(attrs={'id': 'pyrogram-faq'})
        _faqs = []
        for section in faq_container.find_all(attrs={'class': 'section'}):
            title = section.find('h2')
            title, link = title.text, title.find('a')['href']
            _faqs.append((title[:-2], self._make_url_absolute(link)))
        return _faqs

    def __list__(self):
        if self.__faqs is None:
            self.__faqs = self.get_faqs()
            return self.__faqs
        return self.__faqs

    def __iter__(self):
        return iter(self.__list__())

faq = Scraper()
