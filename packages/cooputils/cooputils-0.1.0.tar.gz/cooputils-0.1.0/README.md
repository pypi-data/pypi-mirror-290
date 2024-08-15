# Dev setup
`python3 -m venv venv`
`pip install -r requirements.txt`

# Publishing
`python setup.py sdist bdist_wheel`
`twine upload dist/*`