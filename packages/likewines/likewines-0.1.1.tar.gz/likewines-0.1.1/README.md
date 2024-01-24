# Push to PyPi
1. Install `twine`
```bash
pip install twine
```
2. Build the package
```bash
python setup.py sdist
```
3. Upload to PyPi
```bash
twine upload dist/*
```
Authenticating with PyPi:
- Enter your username: `__token__`
- Enter your password: `<your pypi token>`