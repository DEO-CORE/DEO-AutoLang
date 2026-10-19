# Public DEO AutoLang website

React/Vite public site with route-specific Russian SEO metadata.

## Source structure

- `src/App.jsx` — route-to-page composition.
- `src/pages/` — home and content pages, grouped by page responsibilities.
- `src/components/` — shared navigation, page heading, callout, and footer.
- `src/services/` — website API client; only `/site-api/v1/` is allowed here.
- `src/content.js` — presentation copy and static status definitions.
- `src/styles.css` — global design system and responsive styles.

The UI calls only the Django website backend. Do not place platform API URLs or credentials in this project.

Run the full local stack from the monorepo root with `pnpm dev`. For frontend-only work run `pnpm --dir frontend_site dev`; Django website API should also be started with `pnpm dev:site-api` if checking data-backed pages and forms.

For production SEO metadata, set `VITE_SITE_URL` to the public HTTPS origin before building. The legal pages remain drafts until the product owner supplies legal details and approves them.
