install:
	git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev
	pip install -r requirements.txt

format:
	black *.py

lint:
	mypy *.py

run:
	python3 main.py
