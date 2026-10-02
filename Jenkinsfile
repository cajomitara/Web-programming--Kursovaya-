pipeline {
    agent any

    stages {
        // скачивание исходного кода оттуда, где лежит этот Jenkinsfile
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // установка зависимостей для бэка
        stage('Install Backend Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        // запуск тестов бэка
        stage('Backend Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python manage.py test
                '''
            }
        }

        // установка зависимостей для фронта
        stage('Install Frontend Dependencies') {
            steps {
                dir('client') {
                    sh 'npm install'
                }
            }
        }

        // сборка фронта
        stage('Frontend Build') {
            steps {
                dir('client') {
                    sh 'npm run build'
                }
            }
        }

        // запуск бэка
        stage('Backend Deployment') {
            steps {
                sh '''
                . venv/bin/activate
                python manage.py runserver 0.0.0.0:8000
                '''
            }
        }

        // запуск фронта
        stage('Frontend Deployment') {
            steps {
                dir('client') {
                    sh 'npm run dev -- --host 0.0.0.0'
                }
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully!'
        }

        failure {
            echo 'CI pipeline failed!'
        }
    }
}