ARG COMPOSE_PROJECT_NAME

FROM web-web:latest AS builder

FROM nginx:1.27-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY --from=builder /srv/build /usr/share/nginx/html/public
