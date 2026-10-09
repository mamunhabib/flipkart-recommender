pipeline {
    agent any

    triggers {
        // Step 4: SCM Polling - Tell Jenkins to check GitHub every 2 minutes for new code
        pollSCM('H/2 * * * *')
    }

    environment {
        // The destination URL in GitHub Container Registry
        IMAGE_NAME = 'ghcr.io/mamunhabib/flipkart-recommender'
        IMAGE_TAG  = "latest" 
    }

    stages {
        stage('Build Docker Image') {
            steps {
                echo "Building the Docker Image..."
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push to GHCR') {
            steps {
                echo "Logging into GHCR and pushing image..."
                // Step 5: Securely inject the PAT using the exact ID you just created!
                withCredentials([usernamePassword(credentialsId: 'github-pat', passwordVariable: 'GITHUB_PAT', usernameVariable: 'GITHUB_USER')]) {
                    sh """
                    echo \$GITHUB_PAT | docker login ghcr.io -u \$GITHUB_USER --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying the new architecture to Kubernetes..."
                // Phase 7, Step 4: Tell Jenkins to deploy all the YAML files we just wrote!
                sh "kubectl apply -f k8s/"
                
                // Force Kubernetes to pull the new 'latest' image
                sh "kubectl rollout restart deployment flipkart-app -n flipkart-recommender"
            }
        }
    }
}
