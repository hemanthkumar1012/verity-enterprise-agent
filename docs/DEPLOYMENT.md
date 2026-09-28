# Verity Deployment

Verity is designed as two independent deployments.

## 1. Frontend — Vercel

Deploy the `frontend/` directory as a static site.

The frontend does not depend on FastAPI to render its page. This means the Verity interface can still open when the backend is unavailable.

The browser calls the backend through the URL in:

`frontend/config.js`

Before the production deployment, change:

```js
window.VERITY_CONFIG = {
  apiUrl: "https://YOUR-RENDER-SERVICE.onrender.com",
};
```

## 2. Backend — Render

The repository includes `render.yaml`.

Render should use:

- Root directory: repository root
- Runtime: Python
- Build: `pip install -e ".[dev]"`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check: `/health`

Render can automatically redeploy when the linked branch receives changes.

## 3. CORS

Set the Render environment variable:

`ALLOWED_ORIGINS=https://YOUR-VERCEL-APP.vercel.app`

For local development, keep localhost origins in `.env`.

## 4. Failure behavior

The frontend and backend are intentionally separate:

- Vercel frontend down → backend remains independently available.
- Render backend down → frontend UI still opens, but API-powered actions show an error.
- Frontend deployment fails → existing Vercel deployment remains available.
- Backend deployment fails → the previous successful Render deployment remains available.

This separation makes debugging much easier while Verity is being built.
