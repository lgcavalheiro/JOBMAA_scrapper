test:
	python3 -m unittest discover -t . -s src/ -p "*_test.py"

vagas_spider:
	rm results/vagas_spider_raw_results.json \
	&& cd ./src \
	&& scrapy crawl VagasSpider -o ../../results/vagas_spider_raw_results.json