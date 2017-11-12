TAG ?= dev

# docker

run-wheel-builder:
	docker run --rm \
		-v "$$(pwd)":/application -v "$$(pwd)"/wheelhouse:/wheelhouse \
		stockmarketsignals-builder;

build-image:
	docker build -t joaogabriellima/stockmarketsignals-gateway:$(TAG) -f docker.run .;

push-image:
	docker push joaogabriellima/stockmarketsignals-gateway:$(TAG)
