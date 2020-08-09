
install:
	pip3 install virtualenv
	python3 -m virtualenv env
	env/bin/pip install --upgrade pip && \
	env/bin/pip install -r requirements.txt

clean:
	rm -rf env __pycache__

aws-start:
	gunicorn application:app -b localhost:8000

eb-start:
	eb init -p python3.6 stock_prediction
	eb create ccEnv2

