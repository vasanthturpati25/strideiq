# ── Stage 1: Build React ──────────────────────────────────────────────────
FROM node:20-alpine AS build

WORKDIR /app
COPY package.json ./
RUN npm install --legacy-peer-deps
RUN npm install ajv@^8 --legacy-peer-deps   # ← add this line

COPY . .
ARG REACT_APP_API_URL=/api
ENV REACT_APP_API_URL=$REACT_APP_API_URL

RUN npm run build

# ── Stage 2: Serve with Nginx ─────────────────────────────────────────────
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]