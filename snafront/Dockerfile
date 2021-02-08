# base image
FROM node:latest

# set working directory
WORKDIR /app

# install and cache app dependencies
COPY . /app
RUN npm cache clean --force
RUN npm install
RUN npm install -g @angular/cli

# start app
CMD ng serve --host 0.0.0.0 --port 4201

# docker build -t snafront .
# docker run --name snafront -p 4201:4201 snafront

# Open http://160.40.53.168:4201/