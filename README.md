# Meng Luo · Academic Homepage

Live site: [eurekaleo.github.io](https://eurekaleo.github.io/)

The production homepage uses the approved V5.1 design: a compact profile, all 2026 news visible by default, 17 selected works, institution logos, and academic service and honors. It is a static site with locally hosted fonts and images.

## Update the homepage

- Edit `homepage/content.json` for publications, news, and professional experience.
- Edit `homepage/build.py` for the introduction, section structure, and page metadata.
- Edit `homepage/styles.css` and `homepage/app.js` for presentation and interactions.
- Keep images, fonts, and organization logos in `homepage/assets/`.

Generate the root page with Python 3.12 or later:

```sh
python3 homepage/build.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Preview `http://127.0.0.1:8765/`, then commit the source files together with the generated `index.html`. CSS and JavaScript URLs receive content hashes during generation to prevent stale browser caches after updates.

## Publishing

GitHub Pages publishes the root of `main` using the repository's existing branch-based configuration. `.nojekyll` serves the generated static page directly. No package installation, third-party runtime, or new publishing service is required.

The canonical URL is `https://eurekaleo.github.io/`. `/about/` and `/about.html` redirect to the homepage. The original news, publication, professional activity, and honors heading anchors remain usable. `robots.txt` and `sitemap.xml` are included.

The old Jekyll source remains in Git for reference and recovery. `_pages/about.md` and `_config.yml` are **not** the active homepage editing entry points while `.nojekyll` is present. Preview and comparison pages are not included in the production release.

## Versions and rollback

- Original site: `homepage-before-v5.1-2026-09-29`, commit `3b4f17757eae9affc444a213aff590b7630e06d4`.
- Approved production release: `homepage-v5.1-2026-09-29`.

The release is one commit on top of the original site. To restore the original site in a clean checkout, revert the release commit and push the resulting commit to `main`:

```sh
git switch main
git pull --ff-only
git revert homepage-v5.1-2026-09-29
git push origin main
```

This restores the original publishing behavior without rewriting history. If there have been later changes, review any conflicts before pushing.

## Credits

The publication presentation and heading typography follow [Jiwen Yu's homepage](https://yujiwen.github.io/). Research images and profile content come from this repository. Organization logos identify the stated professional roles. Inter and Orbitron licenses are included in `homepage/assets/fonts/`; the GitHub icon license is included in `homepage/assets/logos/`.

The original site was based on [AcadHomepage](https://github.com/RayeRen/acad-homepage.github.io). Its original source and license remain in the repository.
