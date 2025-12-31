pipeline {
    agent any
//adding commenting to check the setup
        triggers 
        {
        pollSCM('H/2 * * * *') // every 2 minutes
        }

        triggers 
        {
        pollSCM('H/2 * * * *') // every 2 minutes
        }

    options {
        durabilityHint('MAX_SURVIVABILITY')
        disableConcurrentBuilds()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build, Test & Reports') {
            steps {
                sh '''
                    chmod +x mvnw
                    ./mvnw clean test pmd:pmd site
                '''
            }
            post {
                always {
                    junit testResults: '**/target/surefire-reports/*.xml',
                          allowEmptyResults: true

                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'target/site',
                        reportFiles: 'surefire-report.html',
                        reportName: 'JUnit Test Report'
                    ])

                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'target/site',
                        reportFiles: 'pmd.html',
                        reportName: 'PMD Report'
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
                '''
            }
        }
    }
}
