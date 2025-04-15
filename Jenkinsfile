pipeline {
    agent any

    environment {
        // change this to your own Docker Hub repo if needed
        DOCKER_IMAGE = "raghavboi/flask-chatbot"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // build image tagged with the short Git SHA
                    def tag = env.GIT_COMMIT.take(7)
                    docker.build("${DOCKER_IMAGE}:${tag}")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                  usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                  )
                ]) {
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
                // apply your K8s manifests
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
