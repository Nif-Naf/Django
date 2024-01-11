FROM python:3.10
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR project
COPY . $WORKDIR
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
