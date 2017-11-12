TAG ?= dev
# docker

run-wheel-builder:
	docker run --rm \
		-v "$$(pwd)":/application -v "$$(pwd)"/wheelhouse:/wheelhouse \
		deepinvest-builder;

build-image:
	docker build -t joaogabriellima/stockmarketsignals-signals:$(TAG) -f docker.run .;

push-image: build-image
	docker push joaogabriellima/stockmarketsignals-signals:$(TAG)

pull-image:
	docker pull joaogabriellima/stockmarketsignals-signals:$(TAG)
