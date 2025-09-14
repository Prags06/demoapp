
# From redhat/ubi8

# RUN yum install python3 -y

# RUN pip3 install flask

# COPY app.py /app.py

# CMD ["python3","/app.py"]

FROM registry.access.redhat.com/ubi8/ubi:latest
RUN yum install -y python3 python3-pip && yum clean all
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY app.py .
COPY tests ./tests
EXPOSE 5000
CMD ["python3", "app.py"]
