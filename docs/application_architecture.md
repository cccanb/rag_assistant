# Server and application architecture

## Architecture overview

- Application isolation: each application runs in a separate Docker container, which ensures isolation of environments and controllability of dependencies.

- Nginx as a reverse proxy: Nginx accepts incoming HTTP requests and forwards them to the appropriate Docker containers

- Serving static files: Nginx is configured to directly serve static files (JavaScript, CSS, images) from the server's file system, bypassing containers.

## Docker containers structure

Each application must have an isolated and quickly reproducible environment so that it can be deployed on any server in the shortest possible time in the same environment.

Mainly containers with django application and postgres database are used. Additionally there can be Redis and Celery containers.

## Available servers

- Development/Staging server IP 10.0.1.10
- Production server IP 10.0.1.20

## Staging/Dev Server folders structure

### Nginx settings

- /etc/nginx

### Project directories

- /home - directory for all projects
- /home/app1 - App1 Project (Old directory)
- /home/app1-production - App1 Project (Production Environment)
- /home/app1-staging - App1 Project (Staging Environment)
- /home/app2 - App2 Project
- /home/app3 - old implementation
- /home/app3-staging/app3-staging - App3 Project (Staging Environment)
- /home/app3-staging/app3-development - App3 Project (Development - Environment)
- /home/monitoring - Monitoring tools
- /home/preject-builder - ProjectBuilder
- /home/app4-analysis - App4 Analysis
- /home/app4-laravel - App4 Laravel
