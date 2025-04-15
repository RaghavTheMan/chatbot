pipeline {
    // Run all stages inside a docker:20.10.16-cli container
    agent {
        docker {
            image 'docker:20.10.16-cli'
            // mount the host Docker socket so docker commands work
            args  '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        // Change this to your Docker Hub repo
        DOCKER_IMAGE = "raghavboi/flask-chatbot"
    }

    stages {
        stage('Checkout') {
            steps {
                // pull your code (uses the repo & branch configured in the job)
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // tag = first 7 chars of the Git commit SHA
                    def tag = env.GIT_COMMIT.take(7)
                    docker.build("${DOCKER_IMAGE}:${tag}")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    script {
                        // log in and push both the SHA tag and "latest"
                        docker.withRegistry('', 'dockerhub-creds') {
                            def tag = env.GIT_COMMIT.take(7)
                            docker.image("${DOCKER_IMAGE}:${tag}").push()
                            docker.image("${DOCKER_IMAGE}:${tag}").push("latest")
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // apply your K8s manifests to rollout the new image
                sh 'kubectl apply -f chatbot-deployment.yaml'
                sh 'kubectl apply -f chatbot-service.yaml'
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline complete! Deployed ${DOCKER_IMAGE}:${env.GIT_COMMIT.take(7)}"
        }
        failure {
            echo "❌ Pipeline failed. Check the logs above."
        }
    }
}
