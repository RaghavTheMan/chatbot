 pipeline {
-    agent any
+    agent any

     stages {
-        stage('Clone Repo') {
-            steps {
-                git 'https://github.com/RaghavTheMan/chatbot.git'
-            }
-        }
-
         stage('Build Docker Image') {
             steps {
                 script {
                     docker.build("flask-chatbot:${env.GIT_COMMIT.take(7)}")
                 }
             }
         }
 
         stage('Push to Docker Hub') {
             steps {
                 withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                  usernameVariable: 'DOCKER_USER',
                                                  passwordVariable: 'DOCKER_PASS')]) {
                     script {
                         docker.withRegistry('', 'dockerhub-creds') {
                             docker.image("flask-chatbot:${env.GIT_COMMIT.take(7)}").push()
                             docker.image("flask-chatbot:${env.GIT_COMMIT.take(7)}").push('latest')
                         }
                     }
                 }
             }
         }

         stage('Deploy to Kubernetes') {
             steps {
-                sh 'kubectl apply -f chatbot-deployment.yaml'
-                sh 'kubectl apply -f chatbot-service.yaml'
+                sh 'kubectl apply -f chatbot-deployment.yaml'
+                sh 'kubectl apply -f chatbot-service.yaml'
             }
         }
     }
 }
