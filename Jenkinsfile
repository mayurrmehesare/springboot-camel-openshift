pipeline {
    agent any

    options {
        durabilityHint('MAX_SURVIVABILITY')
        disableConcurrentBuilds()
    }

    environment {
        BASE_DIR = "/opt/springboot"
        APP_NAME = "springboot-camel.jar"
    }

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
                    allowEmptyResults: true
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
                    branch 'dev'
                    branch 'qa'
                }
            }
            steps {
                sh '''
                    ./mvnw package -DskipTests
                '''
            }
        }

        stage('Deploy DEV') {
    when {
        branch 'dev'
    }
    steps {
        sh '''
            echo "Deploying DEV on same EC2"

            pkill -f "spring.profiles.active=dev" || true

            mkdir -p /opt/springboot/logs

            cp target/camel-demo-1.0.0.jar /opt/springboot/dev/springboot-camel.jar

            nohup sh -c '
              java -jar /opt/springboot/dev/springboot-camel.jar \
                --spring.profiles.active=dev \
                --server.port=8081 \
                > /opt/springboot/logs/dev.log 2>&1
            ' &
        '''
    }
}


        stage('Deploy QA') {
            when {
                branch 'qa'
            }
            steps {
                sh '''
                    echo "Deploying QA on same EC2"

                    pkill -f "spring.profiles.active=qa" || true

                    cp target/*.jar ${BASE_DIR}/qa/${APP_NAME}

                    nohup java -jar ${BASE_DIR}/qa/${APP_NAME} \
                        --spring.profiles.active=qa \
                        --server.port=8082 \
                        > ${BASE_DIR}/logs/qa.log 2>&1 &
                '''
            }
        }
    }
}
