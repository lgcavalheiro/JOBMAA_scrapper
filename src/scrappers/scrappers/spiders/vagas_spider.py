import scrapy
import re


class VagasSpider(scrapy.Spider):
    name = 'VagasSpider'
    start_urls = [
        'https://www.vagas.com.br/vagas-de-desenvolvedor?a[]=24&c[]=Rio+de+Janeiro&c[]=S%C3%A3o+Paulo&h[]=30&h[]=40&ordenar_por=mais_recentes'
    ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.links = []

    def parse(self, response):
        partial_links = response.css('h2[class=cargo] a')
        self.links.extend(partial_links)
        next_page = response.css('a.btMaisVagas::attr(data-url)').extract()

        if len(next_page) is not 0:
            next_page = f'https://www.vagas.com.br{next_page[0]}'
            yield response.follow(next_page, callback=self.parse)
        else:
            print('LINKS: ', self.links)
            print('LENGTH: ', len(self.links))
            yield from response.follow_all(self.links, callback=self.parse_job)

    def parse_job(self, response):
        def get_job_description():
            nodes = response.css('div.job-tab-content *::text').getall()
            return ' '.join([re.sub(r'[\n\r\xa0]', '', node).strip() for node in nodes])

        print(f'Targeting: {response.url}')

        yield {
            "job_title": response.css('h1.job-shortdescription__title::text').get().strip(),
            "company_name": response.css('h2.job-shortdescription__company::text').get().strip(),
            "hierarchy": ''.join(response.css('span.job-hierarchylist__item span::text').getall()).strip().replace(' ', '').replace('\n', ''),
            "job_url": response.url,
            "job_description": get_job_description()
        }
