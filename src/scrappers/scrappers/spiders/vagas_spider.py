import scrapy


class VagasSpider(scrapy.Spider):
    name = 'VagasSpider'
    start_urls = [
        'https://www.vagas.com.br/vagas-de-desenvolvedor?a[]=24&c[]=Rio+de+Janeiro&c[]=S%C3%A3o+Paulo&h[]=30&h[]=40&ordenar_por=mais_recentes'
    ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.links = []

    def parse(self, response):
        partial_links = response.css(
            'h2[class=cargo] a::attr(href)').extract()
        self.links.extend(partial_links)
        next_page = response.css(
            'a.btMaisVagas::attr(data-url)').extract()
        if len(next_page) is not 0:
            nextp = f'https://www.vagas.com.br{next_page[0]}'
            yield scrapy.Request(nextp, callback=self.parse)
        else:
            print('LINKS: ', self.links)
            print('LENGTH: ', len(self.links))
