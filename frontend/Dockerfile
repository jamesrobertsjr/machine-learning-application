# Use an official Node.js image as a parent image
FROM node:18.17-alpine

# Install pnpm globally
RUN npm install -g pnpm

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install

# Copy the rest of the application
COPY . .

# Build the Next.js app
RUN pnpm run build

# Expose port 3000
EXPOSE 3000

# Start the Next.js app
CMD ["pnpm", "run", "start"]