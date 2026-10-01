pipeline {
    agent any

    stages {
        // скачивание исходного кода оттуда, где лежит этот Jenkinsfile
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // сборка образов
        stage('Build') {
            steps {
                sh 'docker compose build'
            }
        }

        // развёртывание контейнера бэкенда для запуска тестов
        stage('Backend Tests') {
            steps {
                sh 'docker compose run --rm backend python manage.py test'
            }
        }

        // развёртывание контейнеров
        stage('Up') {
            steps {
                sh 'docker compose up -d'
                sh 'sleep 5'
            }
        }

        // смок тест доступа к приложению
        stage('Smoke Test') {
            steps {
                sh 'docker compose exec -T nginx wget -qO- http://localhost/ > /dev/null'
            }
        }
    }

    post {
        always {
            sh 'docker compose down -v || true'
        }
        success {
            echo 'CI pipeline completed successfully!'
        }
        failure {
            echo 'CI pipeline failed!'
        }
    }
}