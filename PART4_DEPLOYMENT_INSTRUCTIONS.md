# Part 4: Deployment Automation

**Assigned Team Member:** Member 4
**Estimated Time:** 2-3 hours

## Overview
This part completes the CI/CD pipeline with automated deployment workflows, deployment scripts, health monitoring, backup automation, and Kubernetes configurations for production-scale deployments.

## Files Created

### GitHub Actions Workflows
1. `.github/workflows/deploy.yml` - Complete deployment pipeline with staging and production environments

### Deployment Scripts
2. `scripts/deploy.sh` - Automated deployment script
3. `scripts/rollback.sh` - Automated rollback script
4. `scripts/health-check.sh` - Health monitoring script
5. `scripts/backup.sh` - Database backup script

### Kubernetes Configuration (Optional/Advanced)
6. `kubernetes/backend-deployment.yaml` - Kubernetes deployment for backend
7. `kubernetes/frontend-deployment.yaml` - Kubernetes deployment for frontend
8. `kubernetes/secrets.yaml` - Kubernetes secrets template
9. `kubernetes/ingress.yaml` - Ingress configuration for routing

## What This Part Does

### 1. Automated Deployment Pipeline (deploy.yml)
- **Pre-deployment Checks**: Runs linting and tests before deploying
- **Build and Push**: Builds Docker images and pushes to GitHub Container Registry
- **Multi-Environment**: Supports staging and production environments
- **Deployment Methods**: Includes templates for SSH, AWS, and Kubernetes deployments
- **Post-Deployment Tests**: Verifies deployment health after completion
- **Automatic Rollback**: Rolls back on deployment failure

### 2. Deployment Scripts
- **deploy.sh**: One-command deployment with health checks
- **rollback.sh**: Emergency rollback to previous version
- **health-check.sh**: Continuous health monitoring
- **backup.sh**: Automated database backups with rotation

### 3. Kubernetes Support (Optional)
- **Scalable Deployment**: Run multiple replicas of services
- **Load Balancing**: Automatic traffic distribution
- **Auto-Healing**: Restarts failed containers automatically
- **Rolling Updates**: Zero-downtime deployments
- **Resource Management**: CPU and memory limits

## Installation and Setup

### Step 1: Make Scripts Executable (Linux/Mac)

```bash
chmod +x scripts/*.sh
```

For Windows, you can run scripts with Git Bash or WSL.

### Step 2: Configure GitHub Secrets (for automated deployment)

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:

**For SSH Deployment:**
- `PRODUCTION_HOST` - Your production server IP or hostname
- `PRODUCTION_USER` - SSH username
- `SSH_PRIVATE_KEY` - Your SSH private key

**For AWS Deployment (if using AWS):**
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key

**Optional:**
- `SLACK_WEBHOOK_URL` - For deployment notifications
- `DISCORD_WEBHOOK_URL` - For deployment notifications

### Step 3: Enable Workflow Environments

1. Go to GitHub repository → Settings → Environments
2. Create two environments:
   - `staging`
   - `production`
3. For production, enable "Required reviewers" for manual approval

### Step 4: Test Local Deployment

```bash
# Ensure .env file is configured
cp .env.example .env
# Edit .env with your settings

# Run deployment script
./scripts/deploy.sh production

# Check health
./scripts/health-check.sh

# Create backup
./scripts/backup.sh
```

## Deployment Workflows

### Workflow 1: Simple Docker Compose Deployment (Recommended for Small Projects)

```bash
# Step 1: SSH into your server
ssh user@your-server.com

# Step 2: Clone or pull repository
cd /opt
git clone https://github.com/your-username/Library-Management-System.git
cd Library-Management-System

# Step 3: Configure environment
cp .env.example .env
nano .env  # Edit secrets

# Step 4: Deploy
./scripts/deploy.sh production

# Step 5: Verify
./scripts/health-check.sh
```

### Workflow 2: Automated GitHub Actions Deployment

1. **Enable SSH deployment** in `.github/workflows/deploy.yml`:
   - Change `if: false` to `if: true` in "Deploy to production via SSH" step
   - Add required secrets to GitHub

2. **Push to main branch:**
   ```bash
   git add .
   git commit -m "Enable automated deployment"
   git push origin main
   ```

3. **Watch deployment:**
   - Go to GitHub → Actions tab
   - Monitor "Deploy to Production" workflow

4. **Verify deployment:**
   - Check production URL
   - Review logs in GitHub Actions

### Workflow 3: Kubernetes Deployment (Advanced)

```bash
# Step 1: Install kubectl
# Follow: https://kubernetes.io/docs/tasks/tools/

# Step 2: Configure kubectl to connect to your cluster
# For AWS EKS:
aws eks update-kubeconfig --name your-cluster-name --region us-east-1

# For Google GKE:
gcloud container clusters get-credentials your-cluster-name --zone us-central1-a

# For Azure AKS:
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster

# Step 3: Create namespace
kubectl create namespace library-production

# Step 4: Update image names in kubernetes/*.yaml files
# Replace 'your-username' with your actual GitHub username

# Step 5: Create secrets
kubectl create secret generic library-secrets \
  --from-literal=secret-key='your-secret-key' \
  --from-literal=jwt-secret-key='your-jwt-secret-key' \
  -n library-production

# Step 6: Deploy backend
kubectl apply -f kubernetes/backend-deployment.yaml -n library-production

# Step 7: Deploy frontend
kubectl apply -f kubernetes/frontend-deployment.yaml -n library-production

# Step 8: Deploy ingress (optional)
kubectl apply -f kubernetes/ingress.yaml -n library-production

# Step 9: Check status
kubectl get all -n library-production

# Step 10: Get external IP
kubectl get service library-frontend-service -n library-production
```

## Deployment Script Usage

### deploy.sh

```bash
# Basic deployment
./scripts/deploy.sh production

# Deploy with git pull
./scripts/deploy.sh production --pull

# Deploy using pre-built registry images
./scripts/deploy.sh production --use-registry
```

**What it does:**
1. Checks Docker and docker-compose installation
2. Verifies .env file exists
3. Stops existing containers
4. Builds new images or pulls from registry
5. Starts services
6. Performs health checks
7. Cleans up old images

### rollback.sh

```bash
# Rollback to previous version
./scripts/rollback.sh previous

# Rollback to specific version tag
./scripts/rollback.sh v1.2.3
```

**What it does:**
1. Confirms rollback with user
2. Creates backup of current state
3. Checks out previous version from git
4. Rebuilds containers
5. Restarts services
6. Verifies health

### health-check.sh

```bash
# Check local deployment
./scripts/health-check.sh

# Check custom URLs
BACKEND_URL=https://api.library.com FRONTEND_URL=https://library.com ./scripts/health-check.sh production
```

**What it checks:**
- Backend health endpoint
- Frontend accessibility
- Database connectivity
- Docker container status

### backup.sh

```bash
# Create backup
./scripts/backup.sh
```

**What it does:**
1. Backs up SQLite database
2. Backs up .env file
3. Creates compressed archive
4. Rotates old backups (keeps last 5)

## Kubernetes Management Commands

```bash
# View deployments
kubectl get deployments -n library-production

# View pods
kubectl get pods -n library-production

# View services
kubectl get services -n library-production

# View logs
kubectl logs -f deployment/library-backend -n library-production
kubectl logs -f deployment/library-frontend -n library-production

# Scale deployments
kubectl scale deployment library-backend --replicas=3 -n library-production

# Update image
kubectl set image deployment/library-backend \
  backend=ghcr.io/your-username/library-management-system-backend:v1.2.3 \
  -n library-production

# Rollback deployment
kubectl rollout undo deployment/library-backend -n library-production

# Check rollout status
kubectl rollout status deployment/library-backend -n library-production

# Delete resources
kubectl delete -f kubernetes/ -n library-production
```

## Environment-Specific Configurations

### Development Environment
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  backend:
    environment:
      - FLASK_ENV=development
      - DEBUG=True
    volumes:
      - ./backend:/app  # Hot reload
```

### Staging Environment
```yaml
# docker-compose.staging.yml
version: '3.8'
services:
  backend:
    environment:
      - FLASK_ENV=staging
      - DEBUG=False
```

### Production Environment
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  backend:
    environment:
      - FLASK_ENV=production
      - DEBUG=False
    restart: always
```

## Monitoring and Logging

### View Live Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100 backend

# Since specific time
docker-compose logs --since 2024-01-01T10:00:00 backend
```

### Container Metrics
```bash
# Resource usage
docker stats

# Inspect container
docker inspect library-backend

# Container processes
docker-compose top
```

## Production Deployment Checklist

Before deploying to production:

- [ ] Update SECRET_KEY and JWT_SECRET_KEY in .env
- [ ] Configure production database (consider PostgreSQL)
- [ ] Set up SSL/TLS certificates
- [ ] Configure proper CORS origins
- [ ] Set up firewall rules
- [ ] Configure automated backups
- [ ] Set up monitoring and alerting
- [ ] Test rollback procedure
- [ ] Document recovery procedures
- [ ] Set up log aggregation
- [ ] Configure rate limiting
- [ ] Enable health check endpoints
- [ ] Test load balancing (if using multiple instances)
- [ ] Verify all GitHub secrets are set
- [ ] Test deployment in staging first

## Deployment Platforms

### Option 1: VPS (DigitalOcean, Linode, AWS EC2)

1. **Provision server** (Ubuntu 22.04 recommended)
2. **Install Docker and docker-compose**
3. **Clone repository**
4. **Run deployment script**
5. **Configure nginx reverse proxy** (optional but recommended)

### Option 2: Container Platforms (AWS ECS, Google Cloud Run, Azure Container Instances)

1. **Push images to registry** (automated via GitHub Actions)
2. **Create task definitions** or services
3. **Configure load balancer**
4. **Set environment variables**
5. **Deploy**

### Option 3: Kubernetes (AWS EKS, Google GKE, Azure AKS, DigitalOcean Kubernetes)

1. **Create Kubernetes cluster**
2. **Configure kubectl**
3. **Apply Kubernetes manifests** (provided in kubernetes/ directory)
4. **Configure ingress controller**
5. **Set up cert-manager** for SSL

### Option 4: Platform-as-a-Service (Heroku, Render, Railway)

1. **Connect GitHub repository**
2. **Configure build settings**
3. **Set environment variables**
4. **Deploy** (automatic on git push)

## Troubleshooting

### Deployment fails with "connection refused"
**Solution:** Check that services are running and firewall allows traffic on ports 5000 and 80

### Health check fails after deployment
**Solution:** Check container logs with `docker-compose logs backend`

### Database changes not reflected
**Solution:** May need to run migrations or recreate database volume

### Rollback fails
**Solution:** Check that git tags exist for the version you're rolling back to

### GitHub Actions deployment fails with permission denied
**Solution:** Verify SSH keys are correctly added to GitHub secrets and server

### Kubernetes pods not starting
**Solution:** Check pod logs with `kubectl logs` and describe pod with `kubectl describe pod`

## Commit and Push

```bash
# Make scripts executable (Linux/Mac)
chmod +x scripts/*.sh

# Add all files
git add .github/workflows/deploy.yml
git add scripts/
git add kubernetes/
git add PART4_DEPLOYMENT_INSTRUCTIONS.md

# Commit
git commit -m "Part 4: Add deployment automation, scripts, and Kubernetes configs"

# Push
git push origin main
```

## Next Steps: Monitoring and Maintenance

After deployment automation is set up, consider adding:

1. **Application Performance Monitoring (APM)**
   - New Relic
   - Datadog
   - Prometheus + Grafana

2. **Log Aggregation**
   - ELK Stack (Elasticsearch, Logstash, Kibana)
   - CloudWatch Logs
   - Google Cloud Logging

3. **Uptime Monitoring**
   - UptimeRobot
   - Pingdom
   - StatusCake

4. **Error Tracking**
   - Sentry
   - Rollbar
   - Bugsnag

5. **Automated Backups**
   - Scheduled cron jobs
   - Cloud provider snapshots
   - Backup rotation policies

## Summary

After completing Part 4, you'll have:
- ✅ Automated deployment pipeline
- ✅ Multi-environment support (staging/production)
- ✅ Deployment scripts for quick deployments
- ✅ Health monitoring and checks
- ✅ Automated backup system
- ✅ Rollback capabilities
- ✅ Kubernetes configurations for scalable deployments
- ✅ Complete CI/CD pipeline from code to production

**Your complete CI/CD pipeline now includes:**
1. **Part 1:** Linting and code quality checks
2. **Part 2:** Automated testing
3. **Part 3:** Docker containerization
4. **Part 4:** Deployment automation

**Congratulations!** You now have a production-ready CI/CD pipeline! 🎉
