pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                    chmod +x mvnw
                    ./mvnw clean package -DskipTests
                    '''
            }
        }


        stage('Build Image') {
            steps {
                sh '''
                    oc new-build --name=camel-demo --binary=true --strategy=docker || true
                    oc start-build camel-demo --from-dir=target --follow
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