# Flipkart Product Recommender - Tutorial Summary

This document outlines exactly how the Coursera tutorial structures and deploys the Flipkart Product Recommender project, based on their provided documentation and source code.

## 1. Application Tech Stack
* **Web Framework:** Flask (with HTML/CSS templates)
* **AI Orchestration:** LangChain (implementing a RAG Pipeline with memory)
* **Vector Database:** AstraDB (A cloud-based DataStax database)
* **LLM Provider:** Groq
* **Embeddings:** HuggingFace
* **Data Flow:** The `data_ingestion.py` script reads the `flipkart_product_review.csv` dataset, generates embeddings, and pushes them up to the AstraDB cloud vector database.

## 2. Infrastructure
* **Cloud Provider:** Google Cloud Platform (GCP)
* **Server:** A single Ubuntu 24.04 LTS Virtual Machine (E2 Standard series, 16 GB RAM, 256 GB Disk).
* **Containerization:** Docker (installed manually on the Ubuntu VM).
* **Kubernetes Environment:** Minikube (installed directly inside the GCP VM to act as the local cluster).

## 3. Deployment Process
The tutorial uses a highly manual deployment process:
1. **Code Versioning:** The developer pushes the source code to a GitHub repository.
2. **VM Preparation:** The developer SSHes into the Google Cloud VM via the browser and clones the GitHub repository into the VM.
3. **Building the Image:** The developer points the VM's Docker client to the internal Minikube Docker daemon (`eval $(minikube docker-env)`) and runs `docker build -t flask-app:latest .`
4. **Secrets Management:** The developer manually types `kubectl create secret generic` into the terminal, pasting their raw Groq, AstraDB, and HuggingFace API keys directly into the command line to create Kubernetes secrets.
5. **Deployment:** The developer applies the `flask-deployment.yaml` file to deploy the Flask pods.
6. **Application Exposure:** The developer uses a background port-forwarding command (`kubectl port-forward svc/flask-service 5000:80 --address 0.0.0.0`) to expose the application to the internet via the VM's public IP address.

## 4. Observability & Monitoring
The tutorial implements monitoring by deploying the full database stacks directly into the Minikube cluster:
1. **Namespace:** A dedicated `monitoring` namespace is created.
2. **Prometheus:** Deployed using raw `prometheus-configmap.yaml` and `prometheus-deployment.yaml` files.
3. **Grafana:** Deployed using a `grafana-deployment.yaml` file.
4. **Accessing Dashboards:** The developer uses two separate `kubectl port-forward` commands to bind the internal Prometheus (port 9090) and Grafana (port 3000) services to the GCP VM's public IP address so they can be viewed in a web browser.
