FROM docker.io/library/alpine:latest

# Set the working directory in Docker
WORKDIR /app

# Install necessary packages, including development packages
RUN apk add --no-cache \
  python3 \
  py3-pip \
  curl \
  git-lfs \
  mariadb-dev \
  build-base \
  mysql-dev \
  python3-dev

# Upgrade pip and install some packages
RUN pip3 install --upgrade pip

# Copy the dependencies file to the working directory
COPY src/requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY src/ .

CMD [ "python3" , "app.py" ]