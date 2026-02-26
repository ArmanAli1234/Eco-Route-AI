# Deploy EcoRoute AI on Heroku – Get Your Link

Follow these **3 steps**. After that, your app will be live and you’ll get a link like:  
**https://ecoroute-ai-msme.herokuapp.com**

---

## Step 1: Install Heroku CLI (one time)

1. Download for Windows: **https://devcenter.heroku.com/articles/heroku-cli**
2. Run the installer and finish the setup.
3. Close and reopen your terminal (or Cursor).

---

## Step 2: Log in to Heroku (one time)

1. Open **PowerShell** or **Command Prompt**.
2. Run:
   ```bash
   heroku login
   ```
3. A browser window will open. Log in (or sign up) with your Heroku account.
4. When it says “Logged in”, you can close the browser and go back to the terminal.

**Note:** Heroku no longer has a free tier. You need to add a card in Account Settings (billing). A small app like this usually stays within low cost.

---

## Step 3: Deploy and get your link

1. In the terminal, go to the project folder:
   ```bash
   cd "c:\Users\arman\OneDrive\Desktop\arman khannn\EcoRouteAI"
   ```
2. Run the deploy script:
   ```bash
   deploy_heroku.bat
   ```
3. Wait 2–3 minutes. When it finishes, it will open your app in the browser.

**Your app link:**  
**https://ecoroute-ai-msme.herokuapp.com**

(If the name `ecoroute-ai-msme` is already taken, the script will show an error. Edit `deploy_heroku.bat`, change the line `set APPNAME=ecoroute-ai-msme` to something like `set APPNAME=ecoroute-ai-yourname`, save, and run the script again.)

---

## Summary

| Step | What to do |
|------|------------|
| 1 | Install Heroku CLI from the link above |
| 2 | Run `heroku login` and complete login in the browser |
| 3 | Run `deploy_heroku.bat` from the EcoRouteAI folder |

Your live link will be: **https://ecoroute-ai-msme.herokuapp.com** (or the name you set in the script).
