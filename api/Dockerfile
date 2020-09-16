FROM python:3
WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
RUN chmod +x start.sh
CMD ["./start.sh"]
