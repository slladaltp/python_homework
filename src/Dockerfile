FROM python:3.8.9
ENV PYTHONUNBUFFERED 1


# Set work directory
RUN mkdir /code
WORKDIR /code


# Install dependencies into a virtualenv
RUN pip install --upgrade pipenv
COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN pipenv install --dev --deploy


# Install requirements
RUN pip install -U pip && \
    pip install -r requirements


COPY . /code/