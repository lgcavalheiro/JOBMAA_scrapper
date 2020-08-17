run:
	python3 -m src.apis.vagas.vagas_api

test:
	python3 -m unittest discover -t . -s src/ -p "*_test.py"