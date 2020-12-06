run:
	python3 -m src.apis.vagas.vagas_api

test:
	python3 -m unittest discover -t . -s src/ -p "*_test.py"

vagas_spider:
	cd ./src \
	&& scrapy crawl VagasSpider -o ../results/vagas_spider_raw_results.json