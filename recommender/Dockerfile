FROM python:3
WORKDIR /recommender
ADD . /recommender
RUN pip install --user --no-cache-dir -r requirements.txt
EXPOSE 5002
CMD ["./wait-for-it.sh", "api:5000", "--", "python", "-u", "app.py"]
