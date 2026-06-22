FROM php:8.2-fpm-alpine

# Install system dependencies
RUN apk add --no-cache \
    curl \
    libpng-dev \
    libxml2-dev \
    zip \
    unzip \
    postgresql-dev \
    linux-headers

# Install PHP extensions
RUN docker-php-ext-install pdo pdo_pgsql bcmath gd opcache

# Get latest Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/backend

# Copy application files
# COPY . .

# RUN composer install --no-dev --optimize-autoloader

# RUN chown -R www-data:www-data /var/www/backend/storage /var/www/backend/bootstrap/cache

EXPOSE 9000
CMD ["php-fpm"]
