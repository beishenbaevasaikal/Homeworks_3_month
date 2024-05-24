# import requests
# from parsel import Selector
#
# class SerialScraper:
#     URL = "https://serial-time.net/top/"
#     HEADERS = {
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#         "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
#     }
#
#     LINK_XPATH = '//div[@class="catalog_main"]//a/@href'
#
#     def scrape_data(self):
#         response = requests.get(self.URL, headers=self.HEADERS)
#         # print(response.text)
#         tree = Selector(text=response.text)
#         # serials = tree.xpath(self.SERIAL_XPATH).getall()
#
#         links = tree.xpath(self.LINK_XPATH).getall()
#         return links
#         # for serial in serials:
#         #     print(serial)
#
# if __name__ == "__main__":
#     scraper = SerialScraper()
#     scraper.scrape_data()
