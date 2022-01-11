FROM python:3.9
ADD webapplication /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python webapplication/app.py