FROM kennethreitz/pipenv

COPY . /app
CMD python3 -m bruce_operator
