import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const siteUrl = process.env.VITE_SITE_URL?.replace(/\/$/, '')
const rootDir = dirname(fileURLToPath(import.meta.url))
const pageEntries = {
  home: 'index.html',
  product: 'product/index.html',
  process: 'process/index.html',
  compatibility: 'compatibility/index.html',
  safety: 'safety/index.html',
  docs: 'docs/index.html',
  about: 'about/index.html',
  privacy: 'privacy/index.html',
  terms: 'terms/index.html',
  operations: 'operations/index.html',
  requestCheck: 'request-check/index.html',
  updates: 'updates/index.html',
}
const routes = ['/', '/product/', '/process/', '/compatibility/', '/operations/', '/request-check/', '/updates/', '/safety/', '/docs/', '/about/', '/privacy/', '/terms/']

function searchMetadata() {
  return {
    name: 'search-metadata',
    transformIndexHtml(html, context) {
      if (!siteUrl) return html
      const path = (context.path || '/').replace(/index\.html$/, '')
      const canonicalPath = path.endsWith('/') ? path : `${path}/`
      const pageUrl = `${siteUrl}${canonicalPath}`
      return html.replace('</head>', `    <link rel="canonical" href="${pageUrl}" />
    <meta property="og:url" content="${pageUrl}" />
    <meta name="twitter:url" content="${pageUrl}" />
  </head>`)
    },
    generateBundle() {
      if (!siteUrl) return
      this.emitFile({
        type: 'asset',
        fileName: 'sitemap.xml',
        source: `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${routes.map((route) => `<url><loc>${siteUrl}${route}</loc><changefreq>monthly</changefreq></url>`).join('')}</urlset>\n`,
      })
      this.emitFile({
        type: 'asset',
        fileName: 'robots.txt',
        source: `User-agent: *\nAllow: /\nSitemap: ${siteUrl}/sitemap.xml\n`,
      })
    },
  }
}

export default defineConfig({
  plugins: [react(), searchMetadata()],
  server: {
    proxy: {
      '/site-api': process.env.VITE_SITE_API_TARGET || 'http://127.0.0.1:4179',
      '/catalog-api': {
        target: process.env.VITE_CATALOG_API_TARGET || 'http://127.0.0.1:4180',
        rewrite: (path) => path.replace(/^\/catalog-api/, '/api'),
      },
    },
  },
  build: {
    rollupOptions: {
      input: Object.fromEntries(Object.entries(pageEntries).map(([name, file]) => [name, resolve(rootDir, file)])),
    },
  },
})
