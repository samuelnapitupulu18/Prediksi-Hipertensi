# Build stage
FROM node:20-alpine as build

WORKDIR /app
# COPY package*.json ./
# RUN npm ci
# COPY . .
# RUN npm run build

# Production stage
# In production, we actually just serve the static files from /app/dist via Nginx
# So this image might just be a builder or we can use a lightweight server
FROM nginx:alpine
# COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
