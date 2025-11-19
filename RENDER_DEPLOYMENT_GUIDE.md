# Render Deployment Guide

This guide shows you how to automatically deploy your Library Management System to Render.

## What is Render?

Render is a cloud platform that automatically deploys your application from GitHub. It's free to start and supports Docker containers.

## Prerequisites

- GitHub account with your code pushed
- Render account (free): https://render.com/

## Step-by-Step Deployment Instructions

### Step 1: Push Your Code to GitHub

First, make sure all your changes are pushed to GitHub:

```bash
# Make sure you're on the CI/CD branch
git checkout CI/CD

# Push all commits (wait for GitHub to recover if still having issues)
git push origin CI/CD
```

### Step 2: Create Render Account

1. Go to https://render.com/
2. Click "Get Started for Free"
3. Sign up with your GitHub account (recommended for easier deployment)

### Step 3: Connect Your Repository

1. Once logged in, click "New +" button in the top right
2. Select "Blueprint"
3. Click "Connect GitHub" if not already connected
4. Find and select your repository: `Library-Management-System`
5. Render will automatically detect the `render.yaml` file

### Step 4: Configure the Blueprint

Render will read your `render.yaml` file and show you:

**Backend Service:**
- Name: `library-backend`
- Type: Web Service (Docker)
- Plan: Free
- Health Check: `/health` endpoint

**Frontend Service:**
- Name: `library-frontend`
- Type: Web Service (Docker)
- Plan: Free
- Auto-connects to backend

Click "Apply" to create both services.

### Step 5: Wait for Deployment

Render will now:
1. ✅ Pull your code from GitHub
2. ✅ Build backend Docker image (takes 3-5 minutes)
3. ✅ Build frontend Docker image (takes 3-5 minutes)
4. ✅ Deploy both services
5. ✅ Run health checks

You'll see build logs in real-time.

### Step 6: Access Your Application

Once deployed, Render gives you URLs:

- **Backend**: `https://library-backend-xxxxx.onrender.com`
- **Frontend**: `https://library-frontend-xxxxx.onrender.com`

Click on the frontend URL to access your application!

## Automatic Deployment

Now that it's set up, every time you push to the `main` branch (or CI/CD branch if configured), Render will:

1. Detect the push via GitHub webhook
2. Automatically pull the latest code
3. Rebuild Docker images
4. Deploy the new version
5. Run health checks to ensure it's working

**This is Continuous Deployment (CD)!** 🚀

## Environment Variables

Render automatically sets these for you (defined in render.yaml):

- `FLASK_ENV=production`
- `SECRET_KEY` (auto-generated)
- `JWT_SECRET_KEY` (auto-generated)
- `DATABASE_URL=sqlite:///data/library.db`

You can view/edit these in the Render dashboard under Environment → Environment Variables.

## Important Notes

### Free Tier Limitations

Render's free tier has some limitations:
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds to wake up
- 750 hours/month of runtime (enough for one service 24/7)
- Limited to 512MB RAM per service

### Database Persistence

The current setup uses SQLite with file storage. On Render's free tier:
- Data is stored in `/data/library.db`
- **Data persists across deploys** but not across service deletions
- For production, consider upgrading to Render's PostgreSQL

To use PostgreSQL instead:
1. Uncomment the database section in `render.yaml`
2. Update backend to use PostgreSQL instead of SQLite
3. Install `psycopg2` in `requirements.txt`

## Troubleshooting

### Build Fails

Check the build logs in Render dashboard:
- Click on the service → "Logs" tab
- Look for error messages during Docker build

### Service Won't Start

1. Check health check endpoint is working: `/health`
2. Verify environment variables are set correctly
3. Check container logs for errors

### Frontend Can't Connect to Backend

1. Verify `VITE_API_URL` environment variable is set on frontend service
2. It should point to: `https://library-backend-xxxxx.onrender.com`
3. Check CORS is enabled in backend (Flask-CORS)

### Database Issues

1. SQLite file may not persist - check disk space in Render dashboard
2. Consider using Render's PostgreSQL for production
3. Check file permissions for `/data` directory

## Monitoring

Render provides:
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory, request counts
- **Alerts**: Email notifications for failures

Access these in the Render dashboard for each service.

## Upgrading from Free Tier

To upgrade for production use:

1. **Starter Plan** ($7/month per service):
   - No spin-down
   - More RAM (512MB → 2GB)
   - Better performance

2. **PostgreSQL** ($7/month):
   - Managed database
   - Automatic backups
   - Better data persistence

## Alternative: Manual Deploy

If you prefer manual control:

1. Don't use the Blueprint
2. Create services manually:
   - Click "New +" → "Web Service"
   - Select repository and branch
   - Choose Dockerfile path
   - Configure environment variables manually

## Next Steps

Once deployed:

1. ✅ Test all features on the live site
2. ✅ Share the URL with your team
3. ✅ Set up custom domain (optional, requires paid plan)
4. ✅ Enable automatic deploys from main branch
5. ✅ Monitor logs and metrics

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com/
- Your CI/CD pipeline will still run on GitHub Actions
- Render handles the actual deployment

---

**Congratulations!** 🎉 Your application is now automatically deployed with Continuous Deployment!

Every push to main → Automatic deployment to Render
