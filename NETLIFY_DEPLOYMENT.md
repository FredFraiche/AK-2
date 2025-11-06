# Netlify Deployment Guide

## Prerequisites

1. **GitHub Account** (to host code)
2. **Netlify Account** (free tier: https://netlify.com)
3. **Git installed** locally

---

## Step 1: Prepare Repository ✅ COMPLETE

### Code pushed to GitHub

**Repository**: https://github.com/FredFraiche/AK-2

```powershell
# Status: Successfully pushed!
# Branch: master
# Files: Complete implementation
# Message: "Complete U-Boat game implementation with React frontend and Netlify deployment"
```

**What's included**:
- ✅ Python backend (uboat_game/)
- ✅ FastAPI server (backend/)
- ✅ React frontend (frontend/)
- ✅ Netlify functions (netlify/functions/)
- ✅ Configuration files (netlify.toml, requirements.txt)
- ✅ Documentation (README.md, COMPLETE.md, etc.)

---

## Step 2: Deploy to Netlify

### Option A: Netlify UI (Recommended - Visual Interface)

1. Go to https://app.netlify.com
2. Click **"Add new site" → "Import an existing project"**
3. Choose **"GitHub"** and authorize Netlify
4. Select **`FredFraiche/AK-2`** repository
5. Configure build settings:
   - **Base directory**: (leave empty)
   - **Build command**: `cd frontend && npm install && npm run build`
   - **Publish directory**: `frontend/dist`
   - **Functions directory**: `netlify/functions`
6. Click **"Deploy site"**

**Note**: Your repository is already at https://github.com/FredFraiche/AK-2

### Option B: Netlify CLI (Advanced)

```powershell
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Initialize site
netlify init

# Deploy
netlify deploy --prod
```

---

## Step 3: Verify Deployment

### Check these URLs work:

1. **Main App**: `https://your-site-name.netlify.app`
2. **Play Game Tab**: Should load interactive game
3. **Simulate Round Tab**: Should run animations
4. **Probability Checker Tab**: Should call API and show results

### Test API Endpoint:

```powershell
curl -X POST https://your-site-name.netlify.app/.netlify/functions/simulate \
  -H "Content-Type: application/json" \
  -d '{"runs": 1000}'
```

Should return JSON with statistics.

---

## Step 4: Custom Domain (Optional)

1. In Netlify dashboard → **Domain settings**
2. Click **"Add custom domain"**
3. Enter your domain (e.g., `uboat-game.com`)
4. Follow DNS configuration instructions
5. Netlify automatically provisions SSL certificate

---

## Configuration Files

### netlify.toml ✅
Already configured in `d:\AK 2\netlify.toml`:
- Build command
- Publish directory
- Function redirects
- SPA routing

### package.json ✅
Frontend dependencies already set:
- React 18
- TypeScript
- Vite
- Axios

---

## Environment Variables (if needed)

If you want to use the Python backend instead of serverless functions:

1. Deploy Python backend to Railway/Render/Fly.io
2. In Netlify dashboard → **Site configuration → Environment variables**
3. Add: `VITE_API_URL` = `https://your-backend.railway.app`
4. Update `frontend/src/components/ProbabilityChecker.tsx`:
   ```typescript
   const API_URL = import.meta.env.VITE_API_URL || '/.netlify/functions'
   ```

---

## Troubleshooting

### Build fails
```powershell
# Check build logs in Netlify dashboard
# Common issues:
# 1. Node version mismatch - add to netlify.toml:
[build.environment]
  NODE_VERSION = "18"

# 2. Missing dependencies - ensure package.json includes all deps
```

### Functions not working
```powershell
# Verify netlify.toml has:
[functions]
  directory = "netlify/functions"

# Check function logs in Netlify dashboard → Functions
```

### API calls fail
```powershell
# Check browser console for CORS errors
# Ensure netlify/functions/simulate.ts has CORS headers
# Verify redirect in netlify.toml:
[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200
```

---

## Performance Optimization

### Enable Caching
In `netlify.toml`:
```toml
[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```

### Enable Compression
Netlify automatically compresses assets. No config needed.

### Analytics
Enable Netlify Analytics in dashboard for visitor tracking.

---

## Continuous Deployment

### Auto-deploy on Git Push
Netlify automatically rebuilds on every push to `main` branch.

### Deploy Previews
Every pull request gets a unique preview URL:
`https://deploy-preview-123--your-site.netlify.app`

### Branch Deploys
Configure branch deploys in **Site configuration → Build & deploy → Deploy contexts**

---

## Cost

**Free Tier Includes**:
- 100 GB bandwidth/month
- 300 build minutes/month
- 125k function invocations/month
- Unlimited sites
- Auto SSL certificates
- Deploy previews

**Perfect for this assignment!**

---

## Post-Deployment Checklist

- [ ] Site loads at Netlify URL
- [ ] All 3 tabs functional:
  - [ ] Play Game (add players, predictions, dice rolling)
  - [ ] Simulate Round (animation works)
  - [ ] Probability Checker (API returns data)
- [ ] Responsive on mobile
- [ ] No console errors
- [ ] API functions respond within 10 seconds
- [ ] Submit URL in Canvas

---

## Quick Deploy Commands

```powershell
# One-time setup
git init
git add .
git commit -m "Initial commit"
gh repo create uboat-game --public --source=. --remote=origin --push

# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod

# Done! Site URL will be shown in terminal
```

---

## Support

- **Netlify Docs**: https://docs.netlify.com
- **Community Forum**: https://answers.netlify.com
- **Status**: https://www.netlifystatus.com

---

**Your site will be live at**: `https://[random-name].netlify.app`

You can change the site name in Netlify dashboard → **Site configuration → Site details → Change site name**
