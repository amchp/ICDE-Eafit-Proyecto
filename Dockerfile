# Start from the osgeo/gdal image that includes Python
FROM --platform=arm64 ghcr.io/andrii-rieznik/python-gdal:py3.12.6-gdal3.9.2 as build

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT [ "/usr/local/pyenv/shims/python", "-m", "awslambdaric" ]

CMD ["lambda_function.handler"]

