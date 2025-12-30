pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Test') {
            steps {
                sh '''
                    chmod +x mvnw
                    ./mvnw clean test
                '''
            }
            post {
                always {
                    junit testResults: '**/target/surefire-reports/*.xml',
                          allowEmptyResults: false
                }
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                    ./mvnw clean package -DskipTests
                    oc new-build --name=camel-demo --binary=true --strategy=docker || true
                    oc start-build camel-demo --from-dir=. --follow
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    oc new-app camel-demo || true
                    oc expose svc/camel-demo || true
                '''
            }
        }
    }
}