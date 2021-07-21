cli-init: build start

# START pre build docker hub image
dh-cli-init: dh-build dh-start

dh-build:
	docker pull enidoshatro/lab:warehouse_cli-latest

dh-start:
	docker run -it --name warehouse_app --rm enidoshatro/lab:warehouse_cli-latest warehouse-cli -if inventory.json -pf products.json

dh-run-tests:
	docker run --name warehouse_app --rm enidoshatro/lab:warehouse_cli-latest coverage run -m pytest --cov-report term --cov=warehouse_cli

dh-clean:
	docker image rm enidoshatro/lab:warehouse_cli-latest
# END pre build docker hub image

# BEGIN local image build
build:
	docker build -t warehouse_cli --rm .

start:
	docker run -it --name warehouse_app --rm warehouse_cli warehouse-cli -if inventory.json -pf products.json

run-tests:
	docker run --name warehouse_app --rm warehouse_cli coverage run -m pytest --cov-report term --cov=warehouse_cli

clean:
	docker image rm warehouse_cli
# END local image build
