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
                    ./mvnw clean test site
                '''
            }
            post {
                always {
                    junit testResults: '**/target/surefire-reports/*.xml',
                          allowEmptyResults: true,
                          skipPublishingChecks: true

                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'target/site',
                        reportFiles: 'surefire-report.html',
                        reportName: 'JUnit Test Report'
                    ])
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
