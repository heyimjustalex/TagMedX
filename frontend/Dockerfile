FROM node:20
WORKDIR /app
COPY . .
RUN npm install --dev
RUN npm run build
EXPOSE 3000
CMD ["npm", "run","dev"]
