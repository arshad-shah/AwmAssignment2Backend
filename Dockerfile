##
## Dockerfile to generate a Docker image from a GeoDjango project
##

# Start from an existing image with Miniconda installed
FROM continuumio/miniconda3

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=AwmAssignment2.settings

# Ensure that everything is up-to-date
RUN apt-get -y update && apt-get -y upgrade
RUN conda update -n base conda && conda update -n base --all

# Make a working directory in the image and set it as working dir.
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# You should have already exported your conda environment to an "ENV.yml" file.
# Now copy this to the image and install everything in it. Make sure to install uwsgi - it may not be in the source
# environment.
COPY env.yml /usr/src/app
RUN conda env create -n AwmAssignment2 --file env.yml

## Make RUN commands use the new environment
## See https://pythonspeed.com/articles/activate-conda-dockerfile/ for explanation
RUN echo "conda activate AwmAssignment2" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

## Set up conda to match our test environment
RUN conda config --add channels conda-forge && conda config --set channel_priority strict
RUN cat ~/.condarc

## Install the appropriate WSGI server. If ccoming from Linux or Macc, this will probably be already there. If coming
## from MS Windows, you'll need to install it here.

#RUN conda install uwsgi
RUN conda install gunicorn

## Copy everything in your Django project to the image and display a directory listing.
COPY . /usr/src/app
RUN ls -la

## Make sure that static files are up to date and available.
RUN python manage.py collectstatic --no-input

## Expose port on the image. We'll map a localhost port to this later. You can change this if desired.
EXPOSE 8002

#CMD uwsgi --ini uwsgi.ini
CMD gunicorn AwmAssignment2.wsgi --config gunicorn.conf.py