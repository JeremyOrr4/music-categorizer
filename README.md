# Music Categorizer V1.2

A tool for organizing, recommending, and categorizing your music collection using Apache Airflow and Docker.

---

## Setup Instructions

### 1. Prerequisites

* Ensure you have Docker installed and working, with Kubernetes enabled.
* Ensure you have helm installed.
* Make the setup script executable:

```bash
chmod +x init.sh
```

---

### 2. Initialize the Environment

Run the following command to set up persistent volume claims (PVCs) and build the Docker images:

```bash
kubectl create namespace airflow
./init.sh --init --docker
```

---

### 3. Configure GitHub DAG Syncing

Follow **Step 5** from this tutorial:
[https://medium.com/@jdegbun/deploying-apache-airflow-on-kubernetes-with-helm-and-minikube-syncing-dags-from-github-bce4730d7881](https://medium.com/@jdegbun/deploying-apache-airflow-on-kubernetes-with-helm-and-minikube-syncing-dags-from-github-bce4730d7881)

#### Step 5 Summary: Creating a Secret to Sync with GitHub

1. **Generate a GitHub Personal Access Token (PAT)**

   * Go to your GitHub account → Developer settings → Personal Access Tokens
   * Click **"Generate new token"**
   * Select scopes (at least `repo`)
   * Click **Generate token**, then copy and store it securely (it won’t be shown again)

2. **Base64 encode your GitHub credentials**

```bash
# Replace with your actual GitHub username
echo -n "your_github_username" | base64

# Replace with your actual GitHub PAT
echo -n "your_github_pat" | base64
```

3. **Edit the Airflow configuration files**

* Open `init_deploy/secret.yaml` and paste your base64-encoded values into the appropriate fields.
* Open `init_deploy/values.yaml` and change the `repo:` field to point to your forked/cloned GitHub repository. It could even be mine.

b.  
* Open `init_deploy/values.yaml` and add the webserver key so you can see logs  
  This is the line you need to change:  
  `# Flask secret key for Airflow Webserver: [webserver] secret_key in airflow.cfg`  
  `webserverSecretKey: XXXXXXXXXXXX`  

  Run this python code below (either python3 or python) and get the value and stick it in the XXXXXXXXX part for the webserverSecretKey:
  ```bash
  python -c "import secrets; print('webserverSecretKey:', secrets.token_hex(32))"

---
In secret.yaml
- You should now have your gitsync values filled
In values.yaml
- You should now have the webserverSecretKey filled
- Also you should have the repo: https://........ filled

### 4. Start Airflow
Make sure you double check you have all the values from previous steps. 

```bash
./init.sh --af
```

Then, in a **new terminal**, run the following to access the Airflow web UI:

```bash
kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow
```

---

### 5. Access the Airflow Web Interface

* Visit: [http://localhost:8080](http://localhost:8080)
* Login credentials:

  * **Username:** `admin`
  * **Password:** `admin`

Your DAGs should appear shortly after startup. Syncing from GitHub may take a few moments.

---

## DAGs

**TO DO** – Describe the DAGs here once implemented.


## Debug

# Error is about service account when you start Airflow up

If you have already installed Airflow, you may need to run this to remove the service account:

```bash
kubectl delete serviceaccount airflow-worker -n airflow
```

# Error with cannot delete pvc

Sometimes the PVC is weird.  
Delete all pods that use the PVC (if there even are any).

```bash
kubectl patch pv music-categorizer-pv -p '{"spec":{"claimRef": null}}' -n airflow
kubectl patch pvc music-categorizer-pvc -p '{"metadata":{"finalizers":null}}' --type=merge -n airflow
```

Make sure to delete again with:

```bash
kubectl delete pvc music-categorizer-pvc -n airflow
kubectl delete pv music-categorizer-pv -n airflow
```

> If you delete the PVC, it may still be stuck to the PV when you create the new claim.  
> This will unstick it.

Finally, re-run your init script:

```bash
./init.sh --init
```

## Debugging Full Memory in Workflow

If you get full memory when running the workflow and you know it will be more than **50 GB**, then check this file:

```
init_deploy/PVC.yaml
```

Go to this line:

```yaml
storageClassName: hostpath
```

Make sure the `hostpath` value matches what is returned from the following command:

```sh
kubectl get storageclass -o wide
```

# Airflow Re-initialization and Service Account Issue

If you are getting a problem re-initializing Airflow after uninstalling, or you receive an error from Helm regarding a service account, try this:

```bash
kubectl delete serviceaccount airflow-worker -n airflow
```

---

# Airflow Redis Pod Not Terminating

If your Airflow Redis pod is not terminating:

- Open Docker Desktop
- Go to **Containers**
- Find and delete the container named **redis**

# Something isnt working

Unforuantly you neeed to understand kubernetes for a lot of debugging. Keep trying as it will help you learn and please report any errors you find to the github.
