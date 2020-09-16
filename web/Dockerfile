FROM node:lts-alpine

WORKDIR /app
COPY package*.json ./
RUN yarn install
COPY . .
EXPOSE 8080
RUN apk add --no-cache bash

CMD ["./wait-for-it.sh", "api:5000", "--", "yarn", "run", "serve"]
