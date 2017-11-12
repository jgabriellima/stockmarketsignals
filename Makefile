HTMLCOV_DIR ?= htmlcov

IMAGES := signals gateway

# test

test:
	#coverage run -m pytest gateway/test $(ARGS)
	#coverage run --append -m pytest signals/test $(ARGS)

coverage: test

# docker

build-example-base:
	docker build -t stockmarketsignals-base -f docker/docker.base .;

build-wheel-builder: build-example-base
	docker build -t stockmarketsignals-builder -f docker/docker.build .;

run-wheel-builder: build-wheel-builder
	for image in $(IMAGES) ; do make -C $$image run-wheel-builder; done

build-images: run-wheel-builder
	for image in $(IMAGES) ; do make -C $$image build-image; done

build: build-images

docker-login:
	docker login --email=$(DOCKER_EMAIL) --password=$(DOCKER_PASSWORD) --username=$(DOCKER_USERNAME)

push-images: build
	for image in $(IMAGES) ; do make -C $$image push-image; done
