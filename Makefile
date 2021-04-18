test:
	python3 -m unittest discover -t . -s src/ -p "*_test.py"

format_topics:
	python3 -m src.utils.topic_formatter

analyze:
	python3 -m src.analysis-service.vagas_analyzer

vagas_spider:
	rm results/vagas_spider_raw_results.json \
	&& cd ./src \
	&& scrapy crawl VagasSpider -o ../../results/vagas_spider_raw_results.json