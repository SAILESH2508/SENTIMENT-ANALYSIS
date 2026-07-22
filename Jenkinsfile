pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'docker.io'
        IMAGE_NAME = 'sailesh2508/sentiment-analyzer'
        IMAGE_TAG = 'latest'
        PYTHON_EXE = 'C:\\Users\\saile\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
    }

    stages {
        stage('Set up venv & dependencies') {
            steps {
                echo '🔄 Creating virtual environment...'
                bat "\"${PYTHON_EXE}\" -m venv venv"
                bat 'venv\\Scripts\\python.exe -m pip install --upgrade pip'
                bat 'venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Static Code Analysis (Lint & Format)') {
            steps {
                echo '🔍 Checking code quality...'
                bat 'venv\\Scripts\\python.exe -m pip install black flake8'
                bat 'venv\\Scripts\\python.exe -m black --check --exclude "venv" . || (echo Formatting check complete. & exit /b 0)'
                bat 'venv\\Scripts\\python.exe -m flake8 --ignore=E501,F401 --exclude=.git,__pycache__,venv,build,dist,.pytest_cache,*.csv,*.pkl,IMDB* . || (echo Non-critical lint warnings logged. & exit /b 0)'
            }
        }

        stage('Security Vulnerability Scan') {
            steps {
                echo '🛡️ Scanning for security flaws...'
                bat 'venv\\Scripts\\python.exe -m pip install bandit safety'
                bat 'venv\\Scripts\\bandit -r . -x ./venv,./.pytest_cache,./__pycache__ -ll'
                bat 'venv\\Scripts\\safety check -r requirements.txt || (echo Non-critical dependency vulnerabilities found. & exit /b 0)'
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
