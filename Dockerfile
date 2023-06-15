FROM python:3.10-slim-buster
RUN pip3 install https://github.com/tomquirk/linkedin-api/archive/refs/tags/v2.0.0.zip
RUN apt-get update --fix-missing
RUN apt-get install -y wkhtmltopdf

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "-u", "bot.py"]
