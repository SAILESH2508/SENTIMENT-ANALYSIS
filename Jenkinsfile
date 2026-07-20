pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'docker.io'
        IMAGE_NAME = 'sailesh2508/sentiment-analyzer'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up venv & dependencies') {
            steps {
                echo '🔄 Creating virtual environment...'
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Static Code Analysis (Lint & Format)') {
            steps {
                echo '🔍 Checking code quality...'
                sh './venv/bin/pip install black flake8'
                sh './venv/bin/black --check --exclude "(\\.git|venv|\\..*)" .'
                sh './venv/bin/flake8 --ignore=E501,F401 --exclude=.git,__pycache__,venv,build,dist,.pytest_cache,*.csv,*.pkl,IMDB* .'
            }
        }

        stage('Security Vulnerability Scan') {
            steps {
                echo '🛡️ Scanning for security flaws...'
                sh './venv/bin/pip install bandit safety'
                sh './venv/bin/bandit -r . -x ./venv,./.pytest_cache,./__pycache__ -ll'
                sh './venv/bin/safety check -r requirements.txt || echo "⚠️ Non-critical dependency vulnerabilities found."'
            }
        }

        stage('Unit Testing') {
            steps {
                echo '🧪 Executing unit tests...'
                sh './venv/bin/pytest test_sentiment_analyzer.py -v --junitxml=test-results.xml'
            }
            post {
                always {
                    // Record JUnit test results in Jenkins UI
                    junit 'test-results.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Compiling production Docker container...'
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline execution completed successfully!'
        }
        failure {
            echo '❌ Pipeline execution failed. Please check build logs.'
        }
    }
}
