test:
	python3 -m unittest discover -t . -s src/ -p "*_test.py"

local_db:
	cd ./local_db \
	&& docker build . -t jobmaa_db \ 
	&& docker run -p 5432:5432 jobmaa_db

vagas_spider:
	cd ./src \
	&& scrapy crawl VagasSpider -o ../../results/vagas_spider_raw_results.csv

vagas_spider_prod:
	cd ./src \
	&& scrapy crawl VagasSpider