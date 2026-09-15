# Red Door Collaborative - website

Static marketing site for reddoorcollaborative.com, built with [Astro](https://astro.build). Modernized from the current Squarespace site: same content and offices, refreshed dark/red visual system, no framework lock-in.

## Local development

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # outputs static site to ./dist
npm run preview   # serve the built ./dist locally
```

## Project structure

- `src/layouts/Layout.astro` - shared `<head>`, nav, footer wrapper
- `src/components/` - `Nav`, `Footer`, `CTASection`
- `src/pages/` - one file per route: `index`, `about`, `services`, `work`, `careers`, `contact`, `contact-success`
- `src/styles/global.css` - brand tokens (colors, type, spacing) and shared classes
- `public/` - static files served as-is (favicon, `CNAME` for the custom domain)

To retune the palette, edit the `:root` variables at the top of `src/styles/global.css` - nothing else needs to change.

## Contact form

The contact page posts to [Web3Forms](https://web3forms.com) (free, no backend needed - works fine on GitHub Pages). Before this goes live:

1. Sign up at web3forms.com with an RDC inbox and grab your access key.
2. In `src/pages/contact.astro`, replace `REPLACE_WITH_YOUR_WEB3FORMS_ACCESS_KEY` with that key.
3. Submissions land in that inbox; the form redirects to `/contact-success` after sending.

## Deploying to GitHub Pages

A workflow at `.github/workflows/deploy.yml` builds and deploys automatically on every push to `main`, using GitHub's official Pages actions. One-time setup once this repo exists on GitHub:

1. Push this project to the repo (all of it, `node_modules` is gitignored).
2. In the repo's **Settings -> Pages**, set **Source** to "GitHub Actions."
3. Push to `main` (or run the workflow manually) - the first run builds and publishes the site.
4. Under **Settings -> Pages -> Custom domain**, enter `www.reddoorcollaborative.com` (the `public/CNAME` file already carries this, so GitHub will pick it up automatically once DNS is pointed at it).

## Pointing the domain at GitHub Pages (do this last)

At your domain's DNS provider (wherever reddoorcollaborative.com is registered/managed):

- For the apex domain (`reddoorcollaborative.com`), add four **A records** pointing to GitHub Pages' IPs:
  - 185.199.108.153
  - 185.199.109.153
  - 185.199.110.153
  - 185.199.111.153
- For `www.reddoorcollaborative.com`, add a **CNAME record** pointing to `<your-github-username>.github.io`.
- Keep Squarespace live until GitHub Pages is confirmed working end-to-end (you can test via the `*.github.io` URL before the DNS cutover), then remove the equivalent DNS records that currently point at Squarespace.

DNS changes are outside what this session can do on your behalf - they need to happen in your registrar's dashboard.

## What's intentionally not carried over

- Squarespace's built-in contact-form backend, blog/comments, and Commerce (the current site doesn't use these, so nothing was lost).
- The current site's exact logo file - the header/footer currently use a text wordmark as a placeholder. Drop the real logo (SVG preferred) into `public/` and swap the `Nav.astro` / `Footer.astro` markup to an `<img>` tag once you have the file.
