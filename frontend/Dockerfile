# Dockerfile
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the source code
COPY . .

# Build the Vite app
RUN npm run build

# Use a lightweight web server (like nginx or serve) to serve the app
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "5173"]
