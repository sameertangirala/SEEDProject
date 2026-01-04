# Step-by-Step Render Deployment Guide

This guide will walk you through deploying your SEED Portal to Render.

## Prerequisites

- [ ] Your code is pushed to a GitHub repository
- [ ] You have a GitHub account
- [ ] You have a Render account (sign up at [render.com](https://render.com) - it's free!)

---

## Part 1: Deploy the Backend (Django API)

### Step 1: Create a Render Account
1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with your GitHub account (recommended) or email

### Step 2: Create a PostgreSQL Database
1. In your Render dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Configure:
   - **Name**: `seed-portal-db` (or any name you like)
   - **Database**: `seed_portal`
   - **User**: `seed_user`
   - **Region**: Choose closest to you (e.g., `Oregon (US West)`)
   - **PostgreSQL Version**: `16` (or latest)
   - **Plan**: Select **"Free"** (or paid if you prefer)
4. Click **"Create Database"**
5. **IMPORTANT**: Wait for the database to be created (takes 1-2 minutes)
6. Once created, click on the database name
7. Copy the **"Internal Database URL"** - you'll need this!

### Step 3: Deploy the Backend Web Service
1. In your Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - If not connected, click "Connect GitHub" and authorize Render
   - Select your repository
4. Configure the service:
   - **Name**: `seed-portal-backend` (or any name)
   - **Region**: Same as your database
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `DjangoProject` ⚠️ **IMPORTANT: Set this!**
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```
     gunicorn DjangoProject.wsgi:application --bind 0.0.0.0:$PORT
     ```
   - **Plan**: Select **"Free"** (or paid)

### Step 4: Configure Backend Environment Variables
1. Scroll down to **"Environment Variables"** section
2. Click **"Add Environment Variable"** for each of these:

   | Key | Value | Notes |
   |-----|-------|-------|
   | `SECRET_KEY` | [Generate one - see below] | **Required** |
   | `DEBUG` | `False` | **Required** |
   | `ALLOWED_HOSTS` | `seed-portal-backend.onrender.com` | ⚠️ **Just the domain** (no `https://`, no trailing slash). Replace with your actual Render URL |
   | `DATABASE_URL` | [Paste from Step 2] | **Required** - The Internal Database URL |
   | `CORS_ALLOWED_ORIGINS` | `https://seed-portal-frontend.onrender.com` | We'll update this after frontend deploys |

3. **Generate SECRET_KEY**:
   - Open your terminal
   - Run: 
     ```bash
     python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - Copy the output and paste as the `SECRET_KEY` value

### Step 5: Deploy the Backend
1. Click **"Create Web Service"**
2. Render will start building and deploying (takes 3-5 minutes)
3. Watch the build logs - you should see:
   - Installing dependencies
   - Collecting static files
   - Starting gunicorn
4. Once deployed, you'll see: **"Your service is live at https://seed-portal-backend.onrender.com"**
5. **Copy this URL** - you'll need it for the frontend!

⚠️ **Important**: Right now, if you visit the URL, you'll likely get a **Bad Request (400)** or **500 Internal Server Error**. This is **normal** because:
- The database tables don't exist yet (migrations haven't run)
- Django can't query the database until migrations are complete
- **Don't worry** - we'll fix this in the next step!

### Step 6: Run Database Migrations
1. In your backend service dashboard, click **"Shell"** tab
2. Run:
   ```bash
   python manage.py migrate
   ```
3. (Optional) Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
   - Follow prompts to create admin account

### Step 7: Test the Backend
1. Visit: `https://your-backend-url.onrender.com/apps/`
2. **Now** you should see JSON data (might be empty array `[]` if no apps added yet)
3. If you see JSON (even if it's just `[]`), backend is working! ✅

### Step 7a: Troubleshooting 400 Bad Request Error

If you get a **400 Bad Request** error even after migrations, it's almost always an `ALLOWED_HOSTS` issue:

**Fix the ALLOWED_HOSTS setting:**

1. Go to your backend service in Render dashboard
2. Click on **"Environment"** tab
3. Find the `ALLOWED_HOSTS` variable
4. The value should be **just the domain name, without `https://`**
   - ✅ **Correct**: `seed-portal-backend.onrender.com`
   - ❌ **Wrong**: `https://seed-portal-backend.onrender.com`
   - ❌ **Wrong**: `seed-portal-backend.onrender.com/`
5. If your actual Render URL is different, use that exact domain
6. **Save changes** - Render will automatically redeploy
7. Wait for redeployment to complete (1-2 minutes)
8. Try the URL again

**Alternative: Allow all Render domains (for testing):**
- Set `ALLOWED_HOSTS` to: `*.onrender.com`
- This allows any Render subdomain (less secure, but good for testing)

**Other things to check:**
- Did migrations run successfully? (Check Step 6)
- Are all environment variables set correctly?
- Check the service logs in Render dashboard for specific error messages
- Make sure `DEBUG=False` is set (not `True`)

---

## Part 2: Deploy the Frontend (React App)

### Step 1: Create Static Site
1. In Render dashboard, click **"New +"**
2. Select **"Static Site"**
3. Connect your repository (same one)
4. Configure:
   - **Name**: `seed-portal-frontend`
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `seed-portal-frontend` ⚠️ **IMPORTANT: Set this!**
   - **Build Command**: 
     ```
     npm install && npm run build
     ```
   - **Publish Directory**: `build`
   - **Plan**: **"Free"** (or paid)

### Step 2: Configure Frontend Environment Variables
1. Scroll to **"Environment Variables"**
2. Add:
   - **Key**: `REACT_APP_API_URL`
   - **Value**: `https://your-backend-url.onrender.com` (the URL from Part 1, Step 5)
   - ⚠️ **No trailing slash!**

### Step 3: Deploy the Frontend
1. Click **"Create Static Site"**
2. Render will build (takes 2-4 minutes)
3. Once deployed, you'll get: **"https://seed-portal-frontend.onrender.com"**
4. **Copy this URL**

### Step 4: Update Backend CORS Settings
1. Go back to your **backend service** dashboard
2. Go to **"Environment"** tab
3. Find `CORS_ALLOWED_ORIGINS`
4. Update the value to your frontend URL:
   ```
   https://seed-portal-frontend.onrender.com
   ```
5. Click **"Save Changes"**
6. Render will automatically redeploy with the new setting

---

## Part 3: Final Configuration

### Step 1: Add Some Test Data (Optional)
1. Go to your backend admin: `https://your-backend-url.onrender.com/admin/`
2. Login with your superuser account
3. Go to "App Links" section
4. Add some test app links with:
   - Name
   - Icon URL
   - Link URL
   - Description

### Step 2: Test the Full Application
1. Visit your frontend URL: `https://your-frontend-url.onrender.com`
2. You should see the SEED Portal with app tiles
3. Click on an app tile to verify links work
4. The apps should load from your backend API

---

## Troubleshooting

### Backend Issues

**Build fails?**
- Check build logs in Render dashboard
- Verify `requirements.txt` is correct
- Make sure `Root Directory` is set to `DjangoProject`

**Database connection error?**
- Verify `DATABASE_URL` is set correctly
- Make sure database is fully created (wait 2 minutes)
- Check you're using "Internal Database URL" not "External"

**400 Bad Request Error?** ⚠️ **Most Common Issue!**
- This is almost always an `ALLOWED_HOSTS` problem
- Go to Environment tab in Render dashboard
- Check `ALLOWED_HOSTS` value - it should be **just the domain** (no `https://`, no trailing slash)
  - ✅ Correct: `seed-portal-backend.onrender.com`
  - ❌ Wrong: `https://seed-portal-backend.onrender.com`
- Make sure it matches your actual Render URL exactly
- Save and wait for redeployment
- For testing, you can use `*.onrender.com` to allow all Render domains

**500 Error?**
- Check service logs in Render dashboard
- Verify all environment variables are set
- Make sure migrations ran
- Check if `ALLOWED_HOSTS` is set correctly (see above)

**CORS Error?**
- Verify `CORS_ALLOWED_ORIGINS` includes your frontend URL
- No trailing slash in the URL
- Make sure it starts with `https://`

### Frontend Issues

**Can't connect to backend?**
- Verify `REACT_APP_API_URL` is set correctly
- Check browser console for errors
- Make sure backend URL has no trailing slash

**Build fails?**
- Check build logs
- Verify `Root Directory` is `seed-portal-frontend`
- Make sure `package.json` is correct

**Blank page?**
- Check browser console for errors
- Verify API URL is correct
- Check network tab to see if API calls are working

---

## Render Free Tier Limitations

⚠️ **Important Notes about Free Tier:**

1. **Spins down after 15 minutes of inactivity** - First request after inactivity takes ~30 seconds
2. **Limited resources** - May be slower than paid plans
3. **Sleeps when not in use** - Not ideal for production with many users
4. **Database has 90-day retention** - Data persists but check Render docs

**For Production:** Consider upgrading to a paid plan for better performance.

---

## Next Steps

- [ ] Both services deployed successfully
- [ ] Backend accessible at `/apps/` endpoint
- [ ] Frontend loads and displays apps
- [ ] App tiles display and links work correctly
- [ ] Test with real users
- [ ] Monitor logs for any errors
- [ ] Consider custom domains (Render supports this)

## Custom Domains (Optional)

Render allows you to add custom domains:
1. Go to your service settings
2. Click "Custom Domains"
3. Add your domain
4. Follow DNS configuration instructions
5. Update `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` with your custom domain

---

## Support

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Render Community**: [community.render.com](https://community.render.com)
- **Django Deployment**: [docs.djangoproject.com/en/stable/howto/deployment/](https://docs.djangoproject.com/en/stable/howto/deployment/)

Good luck with your deployment! 🚀

