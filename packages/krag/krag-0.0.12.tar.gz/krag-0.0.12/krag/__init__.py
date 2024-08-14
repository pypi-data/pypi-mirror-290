# krag/__init__.py

import toml
import os

# pyproject.toml 파일 경로
pyproject_path = os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")

# toml 파일 파싱하여 버전 정보 추출
with open(pyproject_path, "r") as f:
    pyproject_data = toml.load(f)

__version__ = pyproject_data["tool"]["poetry"]["version"]
