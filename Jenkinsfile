pipeline {
    agent {
        docker {
            image 'docker:20.10.16-cli'
            args  '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    environment {
        DOCKER_IMAGE = "raghavboi/flask-chatbot"
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build Docker Image') {
            steps {
                script {
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
                sh 'kubectl apply -f chatbot-deployment.yaml'
                sh 'kubectl apply -f chatbot-service.yaml'
            }
        }
    }
    post {
        success { echo "✅ Deployed ${DOCKER_IMAGE}:${env.GIT_COMMIT.take(7)}" }
        failure { echo "❌ Pipeline failed. Check the logs above." }
    }
}
