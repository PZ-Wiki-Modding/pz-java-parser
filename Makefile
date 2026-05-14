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
# 	@echo "Downloading ZomboidDecompiler.zip..."
# 	@curl -s https://api.github.com/repos/demiurgeQuantified/ZomboidDecompiler/releases/latest | grep -oE 'https://github\.com/[^"]*ZomboidDecompiler\.zip' | head -n1 | xargs curl -L -o ZomboidDecompiler.zip
# 	@echo "Download complete: ZomboidDecompiler.zip"

# unzip
# 	@echo "Unzipping ZomboidDecompiler.zip..."
# 	@unzip -o ZomboidDecompiler.zip -d ./
# 	@echo "Unzip complete"

# run decompiler
	cd ZomboidDecompiler
	@echo "Running decompiler..."
	@$(DECOMPILER_PATH) "$(PZ_GAME_PATH)"
	@echo "Decompiler finished"


run:
	@echo "Fetch colors"
	./.venv/bin/python ./scripts/colors.py
