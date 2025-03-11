FROM node:23-alpine
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install && npm cache clean --force

COPY . .

EXPOSE 5137
ENTRYPOINT npm run dev -- --host
