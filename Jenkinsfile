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

        stage('Build RPM') {
            when {
                anyOf {
                    branch 'dev'
                    branch 'qa'
                }
            }
            steps {
                sh '''
                    mkdir -p rpm/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

                    cp target/*.jar rpm/SOURCES/app.jar
                    cp deploy/systemd/*.service rpm/SOURCES/
                    cp deploy/rpm/springboot-camel.spec rpm/SPECS/
                      
                      rpmbuild \
                      --define "_topdir $(pwd)/rpm" \
                      --define "release ${BUILD_NUMBER}" \
                      -bb rpm/SPECS/springboot-camel.spec
                '''
            }
        }

        stage('Deploy DEV') {
            when {
                branch 'dev'
            }
            steps {
                sh '''
                    sudo yum localinstall -y rpm/RPMS/noarch/springboot-camel-*.rpm
                    sudo systemctl enable springboot-dev
                    sudo systemctl restart springboot-dev
                '''
            }
        }

        stage('Deploy QA') {
            when {
                branch 'qa'
            }
            steps {
                sh '''
                    sudo yum localinstall -y rpm/RPMS/noarch/springboot-camel-*.rpm
                    sudo systemctl enable springboot-qa
                    sudo systemctl restart springboot-qa
                '''
            }
        }
    }
}
