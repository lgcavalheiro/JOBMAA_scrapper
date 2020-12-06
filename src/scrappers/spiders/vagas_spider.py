from datetime import datetime, timedelta
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
            yield from response.follow_all(self.links, callback=self.parse_job)

    def parse_job(self, response):
        def get_job_info(selector):
            return ' '.join([re.sub(r'[\n\r\xa0]', '', node).strip() for node in response.css(selector).getall()]).strip()

        def get_job_wage_and_location():
            return [re.sub(r'[\n\r\xa0]', '', t).strip() for t in response.css('div.infoVaga span::text').getall()][1:]

        def get_job_publish_date():
            date = response.css('li.job-breadcrumb__item--published *::text').getall()[
                1].replace('\n', '').strip().split()[-1]
            if(date == 'ontem'):
                return (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
            else:
                return date

        wage, location = get_job_wage_and_location()

        yield {
            "source_id": response.url.split('/')[4],
            "job_title": get_job_info('h1.job-shortdescription__title::text'),
            "company_name": get_job_info('h2.job-shortdescription__company::text'),
            "hierarchy": get_job_info('span.job-hierarchylist__item span::text'),
            "wage": wage,
            "location": location,
            "publish_date": get_job_publish_date(),
            "job_url": response.url,
            "job_benefits": get_job_info('div.job-benefits *::text'),
            "job_description": get_job_info('div[data-testid=JobDescription] *::text'),
            "company_info": get_job_info('div[data-testid=JobCompanyPresentation] *::text'),
            "extraction_timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "source": "vagas.com"
        }
