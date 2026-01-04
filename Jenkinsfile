pipeline {
    agent any
//adding commenting to check the setup
        triggers 
        {
        pollSCM('H/2 * * * *') // every 2 minutes
        }

    options {
        durabilityHint('MAX_SURVIVABILITY')
        disableConcurrentBuilds()
    }

    options {
        durabilityHint('MAX_SURVIVABILITY')
        disableConcurrentBuilds()
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
                    ./mvnw clean test
                '''
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml', allowEmptyResults: true
                }
            }
        }

        stage('Code Quality Reports') {
            steps {
                sh '''
                    ./mvnw pmd:pmd site
                '''
            }
            post {
                always {
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

        stage('Package') {
            when {
                anyOf {
                    branch 'qa'
                    branch 'main'
                }
            }
            steps {
                sh '''
                    ./mvnw package -DskipTests
                '''
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    echo "Deploying from MAIN branch"
                    oc new-build camel-demo-prod --binary --strategy=docker || true
                    oc start-build camel-demo-prod --from-dir=. --follow
                '''
            }
        }
    }
}