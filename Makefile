VERSION := $(shell git describe | sed -e 's/^v//')
GH_REG_PREFIX := ghcr.io/zoomoid/wave-man

all: build tag push

version:
	@echo $(VERSION)

build:
	docker build -t wave-man:$(VERSION) .

tag:
	docker tag wave-man:$(VERSION) $(GH_REG_PREFIX)/wave-man:$(VERSION)

push:
	docker push $(GH_REG_PREFIX)/wave-man:$(VERSION)