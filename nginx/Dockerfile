FROM nginx:1.25-alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom configuration files
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d /etc/nginx/conf.d
COPY snippets /etc/nginx/snippets

# Create directory for SSL certs
RUN mkdir -p /etc/nginx/ssl

# We expose 80 and 443
EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
