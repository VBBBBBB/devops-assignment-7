pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        PYTHON = 'python3'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Retrieving application source code from GitHub...'
                git branch: 'main',
                    url: 'https://github.com/VBBBBBB/devops-assignment-7.git'
            }
        }

        stage('Build') {
            steps {
                echo 'Building application...'
                sh 'python3 -m pip install --upgrade pip --ignore-installed'
                sh 'python3 -m pip install -r requirements.txt'
                sh 'python3 -m compileall app.py'
                echo 'Build stage completed successfully.'
            }
        }

        stage('Test') {
            steps {
                echo 'Running automated tests...'
                sh 'python3 -m pytest -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded: build and tests passed. ✅'
        }
        failure {
            echo 'Pipeline failed: inspect the stage logs above. ❌'
        }
    }
}
