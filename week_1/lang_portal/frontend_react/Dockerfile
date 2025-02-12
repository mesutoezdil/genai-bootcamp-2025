# Stage 1: Builder
FROM node:16-alpine AS builder

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . .

# Production build
RUN yarn build

# Stage 2: Nginx
FROM nginx:stable-alpine

# Copy build output to nginx html directory
COPY --from=builder /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 