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
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\pip install --upgrade pip'
                bat 'venv\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Static Code Analysis (Lint & Format)') {
            steps {
                echo '🔍 Checking code quality...'
                bat 'venv\\Scripts\\pip install black flake8'
                bat 'venv\\Scripts\\black --check --exclude "(\\.git|venv|\\..*)" .'
                bat 'venv\\Scripts\\flake8 --ignore=E501,F401 --exclude=.git,__pycache__,venv,build,dist,.pytest_cache,*.csv,*.pkl,IMDB* .'
            }
        }

        stage('Security Vulnerability Scan') {
            steps {
                echo '🛡️ Scanning for security flaws...'
                bat 'venv\\Scripts\\pip install bandit safety'
                bat 'venv\\Scripts\\bandit -r . -x ./venv,./.pytest_cache,./__pycache__ -ll'
                bat 'venv\\Scripts\\safety check -r requirements.txt || echo "Non-critical dependency vulnerabilities found."'
            }
        }

        stage('Unit Testing') {
            steps {
                echo '🧪 Executing unit tests...'
                bat 'venv\\Scripts\\pytest test_sentiment_analyzer.py -v --junitxml=test-results.xml'
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
                bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
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
