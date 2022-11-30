FROM python:3.11


WORKDIR /usr/src/app
COPY . .
# build frontend
WORKDIR /usr/src/app/frontend
RUN curl -fsSL https://deb.nodesource.com/setup_18.x -o nodesource_setup.sh && \
    bash nodesource_setup.sh && \
    apt install nodejs -y && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - &&\
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list &&\
    apt-get update && apt-get install --no-install-recommends yarn
RUN yarn install
RUN yarn build

# setup crontab
RUN apt-get install cron curl -y 
RUN crontab -l | { cat; echo "* * * * * curl 0.0.0.0/get_watt"; } | crontab -

# setup fastapi
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN chmod +x ./start.sh

CMD ["sh", "./start.sh"]
