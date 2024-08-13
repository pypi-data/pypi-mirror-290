FROM cr.purplejay.net/keystone/base-images/python-build:3.7.1

WORKDIR /app
RUN python -m pip install hatch

COPY . .

CMD ["/app/package.sh"]