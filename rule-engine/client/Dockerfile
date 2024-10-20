# Use official Node.js image for the client
FROM node:18.18.0

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies (including Vite)
RUN npm install

# Copy app files
COPY . .

# Expose the Vite development server port
EXPOSE 5173

# Run Vite development server
CMD ["npm", "run", "dev"]
