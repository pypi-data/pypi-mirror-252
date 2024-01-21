@echo off
echo Using PyPi
echo Use build for TestPyPi
timeout /t -1
py -m build
py -m twine upload --repository pypi dist/*