# Memory Game Django Project

This repository contains a simple Memory Game built with Django and containerized using Docker.

## Development

1. Build and run the project using Docker Compose:

```bash
docker-compose up --build
```

2. Open your browser at [http://localhost:8000/](http://localhost:8000/).

3. Click `Restart Game` to reset the board at any time.

## Project Structure

- `memory_project/` – Django project and game app.
- `templates/`, `static/` – Frontend files.
- `Dockerfile`, `docker-compose.yml` – Container setup.

The game state is kept in `request.session` using a simple `GameBoard` class.
