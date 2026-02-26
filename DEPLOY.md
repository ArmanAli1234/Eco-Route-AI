# Deploy EcoRoute AI – Get Your Live Link

You have **two good options**. Option 1 is **free and easiest** (recommended).

---

## Option 1: Streamlit Community Cloud (FREE, ~5 min)

No credit card. You get a link like: **`https://your-app-name.streamlit.app`**

### Steps

1. **Put the project on GitHub**
   - Create a new repo (e.g. `EcoRouteAI`).
   - Upload all project files (or push with Git):
     - `app.py`, `requirements.txt`, `README.md`
     - `data/` (with `generate_orders.py`, keep `orders.csv` optional)
     - `ml/` (all `.py` files)
     - `.streamlit/config.toml` (optional)

2. **Go to Streamlit Cloud**
   - Open: **https://share.streamlit.io**
   - Sign in with your **GitHub** account.

3. **New app**
   - Click **“New app”**.
   - **Repository:** select **`ArmanAli1234/Eco-Route-AI`** (your Eco Route AI repo).
   - **Branch:** `main` (or `master`).
   - **Main file path:** `app.py`.
   - Click **“Deploy!”**.

4. **Get your link**
   - After the build finishes, the app URL is shown at the top, e.g.  
     **`https://ecorouteai-xxxxx.streamlit.app`**  
   - That is your live link. Share it or open it in a browser.

**Note:** If the repo is private, Streamlit Cloud may require a paid plan. For a free link, keep the repo **public**.

---

## Option 2: Heroku (Paid)

Heroku no longer has a free tier. You need a paid account and a card on file.

### Steps

1. **Install Heroku CLI**  
   https://devcenter.heroku.com/articles/heroku-cli

2. **Login and create app**
   ```bash
   cd EcoRouteAI
   heroku login
   heroku create ecoroute-ai
   ```

3. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Deploy EcoRoute AI"
   git push heroku main
   ```
   (If your branch is `master`, use `git push heroku master`.)

4. **Open app**
   ```bash
   heroku open
   ```
   Or use the URL shown in the dashboard, e.g. **`https://ecoroute-ai-xxxxx.herokuapp.com`**.

That URL is your live link on Heroku.

---

## Summary

| Platform              | Cost   | Your link |
|-----------------------|--------|-----------|
| **Streamlit Cloud**   | Free   | `https://<app-name>.streamlit.app` (you get it after deploy) |
| **Heroku**            | Paid   | `https://<app-name>.herokuapp.com` (from `heroku open` or dashboard) |

I can’t deploy or log in to your AWS/Heroku/Streamlit account from here, so **you** need to run the steps above. Once you deploy (we recommend **Streamlit Cloud**), the link shown there is the one you can share.

If you tell me whether you’ll use **Streamlit Cloud** or **Heroku**, I can give you a minimal checklist tailored to that option (e.g. exact repo layout or Heroku commands).
