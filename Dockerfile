FROM python:3.8.2
ENV HOME /root
WORKDIR /root
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
CMD /wait && python -u -m flask --app app run --host=0.0.0.0 -p 8000