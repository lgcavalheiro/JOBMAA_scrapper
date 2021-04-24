from datetime import datetime, timedelta
from hashlib import md5
import scrapy
import re


class VagasSpider(scrapy.Spider):
    name = 'VagasSpider'
    start_urls = [
        'https://www.vagas.com.br/vagas-de-desenvolvedor?c[]=Rio+de+Janeiro&c[]=S%C3%A3o+Paulo&ordenar_por=mais_recentes'
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
        def get_job_info(selector, shouldStringify=True):
            try:
                data = [re.sub(r'[\n\r\xa0]', '', node).strip()
                        for node in response.css(selector).getall()]
                if(shouldStringify):
                    return ' '.join(data)
                return data
            except Exception as e:
                raise Exception(e)
                # return '[DATA PROCESS ERROR] @ get_job_info'

        def get_job_wage_and_location():
            try:
                info_vaga = response.css('div.infoVaga li')
                span_text = info_vaga.css('span::text').getall()
                if(len(span_text) == 3):
                    return [re.sub(r'[\n\r\xa0]', '', t).strip() for t in span_text][1:]
                else:
                    b_text = [re.sub(r'[\n\r\xa0]', '', t).strip()
                              for t in info_vaga.css('b::text').getall()]
                    if(len(b_text) > 1):
                        wage = b_text[0] + ' a ' + b_text[1]
                    else:
                        wage = b_text[0]
                    location = re.sub(r'[\n\r\xa0]', '', span_text[-1]).strip()
                    return [wage, location]
            except Exception as e:
                raise Exception(e)
                # return ['[DATA PROCESS ERROR] @ get_job_wage_and_location', '[DATA PROCESS ERROR] @ get_job_wage_and_location']

        def get_job_publish_date():
            try:
                raw_date = response.css(
                    'li.job-breadcrumb__item--published *::text').getall()[1]
                date = raw_date.replace('\n', '').strip().split()[-1]
                if(date == 'hoje'):
                    return datetime.now()
                elif(date == 'ontem'):
                    return (datetime.now() - timedelta(days=1))
                elif(date == 'dias'):
                    date = raw_date.replace('\n', '').strip().split()[-2]
                    return (datetime.now() - timedelta(days=int(date)))
                else:
                    return datetime.strptime(date, "%d/%m/%Y")
            except Exception as e:
                raise Exception(e)
                # return '[DATA PROCESS ERROR] @ get_job_publish_date'

        wage, location = get_job_wage_and_location()
        hierarchy = get_job_info('span.job-hierarchylist__item span::text')
        description = get_job_info('div[data-testid=JobDescription] *::text')

        # hash used to prevent inter-source duplicates
        job_hash = ''.join([re.sub(r'\W', '', item)
                           for item in [hierarchy, description]])

        yield {
            "SOURCE_ID": response.url.split('/')[4],
            "JOB_HASH": md5(job_hash.encode()).hexdigest(),
            "TITLE": get_job_info('h1.job-shortdescription__title::text'),
            "COMPANY_NAME": get_job_info('h2.job-shortdescription__company::text'),
            "HIERARCHY": hierarchy,
            "WAGE": wage,
            "LOCATION": location,
            "PUBLISH_DATE": get_job_publish_date(),
            "URL": response.url,
            "BENEFITS": get_job_info('li.job-benefits__list-item span::text', False),
            "DESCRIPTION": description,
            "COMPANY_INFO": get_job_info('div[data-testid=JobCompanyPresentation] *::text'),
            "EXTRACTION_TIMESTAMP": datetime.now(),
            "SOURCE": "vagas.com"
        }
