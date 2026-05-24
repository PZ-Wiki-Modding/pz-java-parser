.ONESHELL:
.PHONY: help run

SHELL := /bin/bash

# decompiler path based on Windows or Linux
ifeq ($(OS),Windows_NT)
	DECOMPILER_PATH := bin\ZomboidDecompiler.bat
else
	DECOMPILER_PATH := bin/ZomboidDecompiler
endif

help:
	@echo "PZ Lua Parser"
	@echo "Available targets:"
	@echo "  run:   Run the parser"

decompile:
# download the latest release of ZomboidDecompiler.zip from GitHub
	@if [ ! -d "ZomboidDecompiler" ]; then \
		echo "Downloading ZomboidDecompiler.zip..."; \
		curl -s https://api.github.com/repos/demiurgeQuantified/ZomboidDecompiler/releases/latest | grep -oE 'https://github\.com/[^"]*ZomboidDecompiler\.zip' | head -n1 | xargs curl -L -o ZomboidDecompiler.zip; \
		echo "Download complete: ZomboidDecompiler.zip"; \
		echo "Unzipping ZomboidDecompiler.zip..."; \
		unzip -o ZomboidDecompiler.zip -d ./; \
		echo "Unzip complete"; \
	else \
		echo "ZomboidDecompiler already present"; \
	fi

# run decompiler
	cd ZomboidDecompiler
	@echo "Running decompiler..."
	@$(DECOMPILER_PATH) "$(PZ_GAME_PATH)"
	@echo "Decompiler finished"


run: decompile
	./.venv/bin/python ./scripts/colors.py
	./.venv/bin/python ./scripts/item_tags.py
	./.venv/bin/python ./scripts/magazine_subjects.py
	./.venv/bin/python ./scripts/metabolics.py
	./.venv/bin/python ./scripts/action_sound_time.py
