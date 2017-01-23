FROM node:6

RUN mkdir -p /usr/src


RUN npm install -g yo gulp-cli bower gulp

#RUN groupadd -r node &&  useradd -r -m -g node node 

WORKDIR /usr/src

RUN git clone https://github.com/antolikjan/mozaik_repository.git 

WORKDIR /usr/src/mozaik_repository

#COPY . /usr/src/app/
RUN chown -R node:node /usr/src/mozaik_repository

USER node
RUN npm install 

RUN pwd
RUN ls
WORKDIR /usr/src/mozaik_repository/client
RUN bower install
WORKDIR /usr/src/mozaik_repository

#\
# && gulp build # required for staging

#ENV NODE_ENV development # production for staging

# change to whatever port is to be used
EXPOSE 3000

CMD [ "gulp", "serve" ]
