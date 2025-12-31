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

        stage('Deploy to DEV') {
            when { branch 'dev' }
            steps {
                sh '''
                    ./mvnw clean package -DskipTests
                    oc new-build camel-demo-dev --binary --strategy=docker || true
                    oc start-build camel-demo-dev --from-dir=. --follow
                    oc expose svc/camel-demo-dev || true
                '''
            }
        }

        stage('Deploy to QA') {
            when { branch 'qa' }
            steps {
                sh '''
                    ./mvnw clean package -DskipTests
                    oc new-build camel-demo-qa --binary --strategy=docker || true
                    oc start-build camel-demo-qa --from-dir=. --follow
                    oc expose svc/camel-demo-qa || true
                '''
            }
        }

        stage('Deploy to PROD') {
            when { branch 'main' }
            steps {
                sh '''
                    ./mvnw clean package -DskipTests
                    oc new-build camel-demo-prod --binary --strategy=docker || true
                    oc start-build camel-demo-prod --from-dir=. --follow
                    oc expose svc/camel-demo-prod || true
                '''
            }
        }
    }
}
