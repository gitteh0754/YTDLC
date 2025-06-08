help:
	@echo Usage: make [build \| clean \| help]

clean:
	@rm -rf dist
	@rm -rf build
	@rm cli.spec

build:
	@pyinstaller -F cli/cli.py