# Flipkart Product Recommender: Implementation Plan

This document outlines the step-by-step serialized plan to build the Flipkart Product Recommender from scratch, using the advanced, Cloud-Native architecture we established in Project 1. We will use the tutorial's `archive/` folder purely as a reference, writing our own clean, modular code.

---

## Phase 1: Environment & Architecture Initialization
Before writing any code, we must set up a clean workspace and isolate our dependencies.

**Steps:**
1. **Virtual Environment:** Create and activate a Virtual Environment (`venv`).
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Directory Structure:** Create the empty enterprise directory structure and all internal files.
   ```bash
   mkdir -p .github/workflows app/static app/templates core data k8s utils
   touch .env .gitignore Dockerfile run.py
   touch app/__init__.py app/routes.py app/templates/index.html
   touch core/__init__.py core/config.py core/data_ingestion.py core/rag_chain.py
   touch utils/__init__.py utils/custom_exception.py utils/logger.py
   ```
3. **Protect Secrets:** Define the `.gitignore` immediately to prevent secret leaks.
   ```bash
   echo "venv/" >> .gitignore
   echo ".env" >> .gitignore
   echo "__pycache__/" >> .gitignore
   ```
4. **Dependencies:** Move `requirements.txt` from the archive and install it.
   ```bash
   mv archive/requirements.txt .
   pip install -r requirements.txt
   ```
5. **Dataset:** Move only the dataset from the archive into the `data/` folder.
   ```bash
   mv archive/flipkart_product_review.csv data/
   ```

---

## Phase 2A: Backend & AI Engineering
We start by building the core "brain" of the application. This layer handles the database, the AI logic, and secure configurations.

**Steps:**
1. **`core/config.py` (Configuration):** The very first file. Safely loads all API keys (Groq, AstraDB, HuggingFace) from `.env`.
2. **`.env` Population:** We immediately generate the required API keys and place them in the local `.env` file so our configuration is active.
3. **`core/data_ingestion.py` (The Database Layer):** We write the script to read the CSV, generate embeddings, and push the data into AstraDB.
4. **`core/rag_chain.py` (The AI Brain):** We write the LangChain logic. This script handles conversational memory, retrieves data, and communicates with the Groq LLM.
5. **Redis Memory Upgrade:** We install the `redis` dependency, update `config.py` with `REDIS_URL`, and modify `rag_chain.py` to use `RedisChatMessageHistory` instead of RAM.
6. **Local Embeddings Upgrade:** We install `sentence-transformers` and update `data_ingestion.py` to run `HuggingFaceEmbeddings` locally on our CPU to bypass API paywalls.

---

## Phase 2B: Frontend & Web API Engineering
Once the backend is built, we wrap it in a web server and build the User Interface so people can actually interact with the AI.

**Steps:**
1. **`app/__init__.py` & `app/routes.py` (The Web API):** We write the Flask application. This connects the backend AI brain to HTTP web routes (like `/get`).
2. **`app/templates/index.html` (The UI):** We build the frontend web page that the user interacts with.
3. **`run.py` (The Entry Point):** We write the master file at the root of the project that boots up the Flask server.

---

## Phase 3: Database Population (Data Ingestion)
Now that our API keys are loaded and our data script is written, we must give the AI its memory.

**Steps:**
1. Execute `python -m core.data_ingestion` to read the CSV, generate local embeddings, and populate the AstraDB cloud database.

---

## Phase 4: Local Development Testing
**Steps:**
1. Execute `python run.py`.
2. Open `localhost:5000` in the browser to verify the web app and AI recommendations work perfectly.

---

## Phase 5: GitOps Security (Sealed Secrets)
**Steps:**
1. Fetch the public key from the OrbStack cluster using `kubeseal --fetch-cert > pub-cert.pem`.
2. Write a raw Kubernetes `secret.yaml` containing the Base64 encoded API keys.
3. Encrypt it completely offline using `kubeseal --cert pub-cert.pem -o yaml < secret.yaml > k8s/sealed-secret.yaml`.
4. Add `secret.yaml` and `pub-cert.pem` to `.gitignore` so they are never committed to GitHub.

---

## Phase 6: Containerization & Local Jenkins CI Pipeline
**Steps:**
1. Write an optimized `Dockerfile` and `.dockerignore`.
2. Write and apply `k8s/jenkins.yaml` to deploy a global Jenkins server into OrbStack.
3. **[PAT Requirement]:** Inject a GitHub Personal Access Token (PAT) into the Jenkins UI `Credentials` manager so Jenkins has permission to interact with GitHub and GHCR.
4. Write a declarative `Jenkinsfile` (Groovy) that includes an **SCM Polling trigger** (`pollSCM`) to automatically detect `git push` events.
5. Configure the `Jenkinsfile` to build the Docker image and push it to the GitHub Container Registry (GHCR) using the injected PAT.

---

## Phase 7: Kubernetes Deployment via Jenkins & Final Execution
**Steps:**
1. Write `k8s/redis-deployment.yaml` and `k8s/redis-service.yaml` to deploy an in-cluster Redis database.
2. **[PAT Requirement]:** Use `kubectl create secret docker-registry ...` to generate and seal an `imagePullSecret` containing your PAT, granting OrbStack permission to pull from GHCR.
3. Write `k8s/deployment.yaml` for the main Flask app, configuring it to use the sealed `imagePullSecret`.
4. Add a final stage to the `Jenkinsfile` that executes `kubectl apply` against the cluster, commanding OrbStack to perform a rolling update.
5. **[Big Bang Push]:** Create the remote GitHub repository and `git push` all project files to it.
6. Create a Pipeline Job in the Jenkins UI, configure it as **"Pipeline script from SCM"**, and provide your newly created GitHub Repository URL. Jenkins will instantly pull your code and execute the massive pipeline!
(http://localhost:8081) and follow these exact clicks:

On the left menu, click + New Item.
Type a name for your job (e.g., flipkart-pipeline), select Pipeline from the list below, and click the blue OK button at the bottom.
Scroll down to the Build Triggers section and check the box that says "Poll SCM". (You do not need to type anything in the schedule box here, because our Jenkinsfile code handles the timer).
Scroll all the way down to the Pipeline section.
Change the Definition dropdown from "Pipeline script" to "Pipeline script from SCM".
Change the SCM dropdown to Git.
In the Repository URL box, paste the link to your GitHub repository (e.g., https://github.com/mamunhabib/your-repo-name.git).
Under Branches to build, change the Branch Specifier from */master to */main.
Ensure the Script Path at the bottom says Jenkinsfile.
Click the blue Save button.

---

## Phase 8: Enterprise Observability
**Steps:**
1. Ensure the Flask `/metrics` endpoint is being scraped by the Helm Alloy Agent and pushed to Grafana Cloud.
