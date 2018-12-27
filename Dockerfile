FROM python:3.6.1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY static static

EXPOSE 8666
CMD ["python", "app.py"]