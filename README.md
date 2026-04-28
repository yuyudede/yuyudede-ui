# yuyudede UI

Vue 3 frontend for yuyudede.com. It includes the portal, blog reader, article search, comments, admin dashboard, and toolbox.

## Tech Stack

- Vue 3 + Vite
- Vue Router + Pinia
- Element Plus
- Unhead for page metadata
- highlight.js core with selected languages for article code blocks

## Development

```bash
npm install
npm run dev
```

The Vite dev server proxies `/api` to `http://localhost:8080`.

## Scripts

```bash
npm run build
npm run preview
```

## Routes

- `/` portal
- `/blog` article list
- `/search` article search
- `/article/:slug` article detail, comments, and related articles
- `/categories`, `/category/:slug`
- `/tags`, `/tag/:slug`
- `/tools` toolbox
- `/tools/sudoku` Sudoku
- `/admin/**` admin dashboard

## Deployment

Pushes to `main` build a Docker image in GitHub Actions, upload it through COS, then reload the frontend service on the server with Docker Compose.
