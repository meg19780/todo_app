pipeline {
    agent any
    environment {

        VERSION = "${BUILD_NUMBER}"
        email = 'meg19780@gmail.com'

    }
    stages {
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t myapp ./app
                '''
            }
        }
        stage('Run app with Docker compose') {
            steps {
                sh '''
                    docker compose down || true
                    docker compose up -d
                '''
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                '''
            }
        }
    }
        post {
             failure {

                
                emailext(
                    subject: " FAILED",
                    mimeType: 'text/html',
                    to: "$email",
                    body: "FAILED"
                )
                emailext (
                to: 'meg19780@gmail.com',
                subject: 'Pipeline Notification',
                body: 'This is a fail email from Jenkins.'
            )
            }
            success {

                emailext(
                    subject: " PASSED",
                    mimeType: 'text/html',
                    to: "$email",
                    body: " PASSED"
                )    
                emailext (
                to: 'meg19780@gmail.com',
                subject: 'Pipeline Notification',
                body: 'This is a test email from Jenkins.'
                )
            }

        }
    }


