pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/RaghavTheMan/<your-repo-name>.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('flask-chatbot:v1')
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-creds') {
                            docker.image('flask-chatbot:v1').push()
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
}
