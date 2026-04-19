# Azure Deployment Configuration

## Resource Names
- **Container Apps Environment**: `flask-calc-prod-env`
- **Container App**: `flask-calc-prod-app`
- **Resource Group**: `my-flask-rg`
- **Azure Container Registry**: `myflaskacr007`
- **Docker Image Name**: `flask-calculator`
- **Region**: `eastus` (US East - Virginia)

## Setup Instructions

### Step 1: Create Container Apps Environment
```bash
az containerapp env create `
  --name flask-calc-prod-env `
  --resource-group my-flask-rg `
  --location eastus
```

### Step 2: Build and Push Docker Image
```bash
cd C:\Users\sudha\Desktop\project_Restructure
az acr login --name myflaskacr007
docker build -t myflaskacr007.azurecr.io/flask-calculator:latest .
docker push myflaskacr007.azurecr.io/flask-calculator:latest
```

### Step 3: Create Container App
```bash
az containerapp create `
  --name flask-calc-prod-app `
  --resource-group my-flask-rg `
  --environment flask-calc-prod-env `
  --image myflaskacr007.azurecr.io/flask-calculator:latest `
  --target-port 80 `
  --ingress external `
  --registry-server myflaskacr007.azurecr.io `
  --registry-username myflaskacr007 `
  --registry-password <YOUR_ACR_PASSWORD>
```

Replace `<YOUR_ACR_PASSWORD>` with your actual ACR admin password.

### Step 4: Verify Container App
```bash
az containerapp show --name flask-calc-prod-app --resource-group my-flask-rg
az containerapp show --name flask-calc-prod-app --resource-group my-flask-rg --query properties.configuration.ingress.fqdn -o tsv
```

## GitHub Actions Workflow
The workflow file `.github/workflows/deploy_to_azure_container_app.yml` has been updated to use:
- Container App Name: `flask-calc-prod-app`
- Container Apps Environment: `flask-calc-prod-env`

The workflow will automatically deploy updates when you push to the `main` branch.
