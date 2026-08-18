.ONESHELL:
.PHONY: help decompile run

SHELL := /bin/bash
DECOMPILER_VERSION ?= v0.3.2

# decompiler path based on Windows or Linux
ifeq ($(OS),Windows_NT)
	DECOMPILER_PATH := bin\ZomboidDecompiler.bat
else
	DECOMPILER_PATH := bin/ZomboidDecompiler
endif

help:
	@echo "PZ Lua Parser"
	@echo "Available targets:"
	@echo "  decompile:   Download and run the ZomboidDecompiler"
	@echo "  run:   Run the parser"

download_zomboid_decompiler:
	@echo "Downloading ZomboidDecompiler..."
	@curl -s https://api.github.com/repos/demiurgeQuantified/ZomboidDecompiler/releases/tags/$(DECOMPILER_VERSION) \
		| grep -oE 'https://github\.com/[^"]*ZomboidDecompiler\.zip' \
		| head -n1 \
		| xargs curl -L -o ZomboidDecompiler.zip
	@echo "$(DECOMPILER_VERSION)" > ZomboidDecompiler.version
	@echo "Download complete: ZomboidDecompiler.zip"
	@echo "Unzipping ZomboidDecompiler.zip..."
	@unzip -o ZomboidDecompiler.zip
	@echo "Unzip complete"

decompile:
# download the latest release of ZomboidDecompiler.zip from GitHub
# check if the current version is the same as the one in ZomboidDecompiler.version
	@if [ -f "ZomboidDecompiler.version" ]; then
		CURRENT_VERSION=$$(cat ZomboidDecompiler.version);
		if [ "$$CURRENT_VERSION" != "$(DECOMPILER_VERSION)" ]; then
			echo "Current version ($$CURRENT_VERSION) is different from the requested version ($(DECOMPILER_VERSION)). Downloading new version...";
			rm -rf ZomboidDecompiler;
			rm -f ZomboidDecompiler.zip;
		fi
	else
		echo "ZomboidDecompiler.version not found. Downloading version $(DECOMPILER_VERSION)...";
		rm -rf ZomboidDecompiler;
		rm -f ZomboidDecompiler.zip;
	fi
	@if [ ! -d "ZomboidDecompiler" ]; then
		make download_zomboid_decompiler;
	else
		echo "ZomboidDecompiler already present";
	fi

# run decompiler
	cd ZomboidDecompiler
	@echo "Running decompiler..."
	@$(DECOMPILER_PATH) "$(PZ_GAME_PATH)"
	@echo "Decompiler finished"


run:
	@if [ ! -d "ZomboidDecompiler" ]; then
		echo "ZomboidDecompiler not found. Please run 'make decompile' first.";
		exit 1;
	fi

	./.venv/bin/python ./scripts/colors.py
	./.venv/bin/python ./scripts/item_tags.py
	./.venv/bin/python ./scripts/magazine_subject.py
	./.venv/bin/python ./scripts/metabolics.py
	./.venv/bin/python ./scripts/action_sound_time.py
	./.venv/bin/python ./scripts/sound_keys.py
	./.venv/bin/python ./scripts/tile_properties.py
