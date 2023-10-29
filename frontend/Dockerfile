FROM node:alpine
WORKDIR /app
COPY . .
RUN npm install --include=dev
RUN npm run build
EXPOSE 3000
CMD ["npm", "run","dev"]
