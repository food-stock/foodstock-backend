# base image
FROM python:3.8

# setup environment variable
ENV DockerHOME=/home/app/webapp

# expose port
EXPOSE 8000

# set work directory
RUN mkdir -p $DockerHOME
WORKDIR $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# copy only necessary files
COPY requirements.txt $DockerHOME/
RUN pip install -r requirements.txt
COPY . $DockerHOME/

# run entrypoint script
COPY entrypoint.sh $DockerHOME/
RUN chmod +x $DockerHOME/entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]