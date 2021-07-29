.PHONY: init

init:
	{ \
	pipenv shell ;\
	pipenv install ;\
	bundle install --path vendor/bundle ;\
	}
