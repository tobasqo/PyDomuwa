FROM node:23-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install && npm cache clean --force

COPY . .

ENTRYPOINT [ "npm", "run", "dev", "--", "--host" ]
