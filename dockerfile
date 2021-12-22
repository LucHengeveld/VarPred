FROM python:3.9
ADD /pictures /code
ADD /static /code
ADD /templates /code
ADD app_test.py /code
ADD requirements.txt /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python app_test.py