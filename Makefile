cli-init: build start


build:
	docker build -t warehouse_cli --rm .

start:
	docker run -it --name warehouse_app --rm warehouse_cli warehouse-cli -if inventory.json -pf products.json

run-tests:
	docker run --name warehouse_app --rm warehouse_cli coverage run -m pytest -vv

clean:
	docker image rm warehouse_cli
