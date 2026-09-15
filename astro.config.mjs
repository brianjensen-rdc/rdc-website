import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://www.reddoorcollaborative.com',
  // Serving from https://brianjensen-rdc.github.io/rdc-website/ until the
  // custom domain's DNS is cut over. Every internal link in this project
  // is built from import.meta.env.BASE_URL, so once DNS points at the
  // custom domain this can simply become '/' (or be removed) with no
  // other changes needed.
  base: '/rdc-website',
});
