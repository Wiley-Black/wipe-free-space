@echo off

echo update:
poetry update
if errorlevel 1 goto Done

echo install:
poetry install --with dev --with test --with deploy
if errorlevel 1 goto Done

echo black:
poetry run black .
if errorlevel 1 goto Done

echo isort:
poetry run isort .
if errorlevel 1 goto Done

echo.
echo flake8:
poetry run flake8 wipe_free_space tests --count --max-line-length=120 --extend-ignore=E203,E266,E501,W503,F403,E722,F541 --statistics
if errorlevel 1 goto Done

echo.
echo mypy:
poetry run mypy wipe_free_space/__main__.py
if errorlevel 1 goto Done

echo.
echo pytest:
poetry run pytest tests/ --durations=0
if errorlevel 1 goto Done

echo.
echo pyinstaller:
poetry run pyinstaller wipe_free_space\__main__.py --onefile --name wipe_free_space.exe
if errorlevel 1 goto Done

:Done
echo.
