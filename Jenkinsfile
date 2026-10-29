pipeline {
    agent any

    // тегирование + название проекта
    environment {
        TAG = "${BUILD_NUMBER}"
        COMPOSE_PROJECT_NAME = 'dotaesports'
    }

    
    stages {
        // скачивание исходного кода оттуда, где лежит этот Jenkinsfile
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // билд образов в docker-compose
        stage('Build') {
            steps {
                sh 'docker compose build'
            }
        }

        // запуск тестов бэка
        stage('Backend Tests') {
            steps {
                sh 'docker compose run --rm backend python manage.py test'
            }
        }

        // пуш образов в репозиторий docker hub
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub',
                                                  usernameVariable: 'DH_USER',
                                                  passwordVariable: 'DH_PASS')]) {
                    sh 'echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin'
                    sh 'docker compose push'
                }
            }
        }

        // деплой проекта
        stage('Up') {
            steps {
                sh 'docker compose up -d'
                sh 'sleep 5'
            }
        }

        // смок тест нгинкса
        stage('Smoke Test') {
            steps {
                sh 'docker compose exec -T nginx wget -qO- http://127.0.0.1/ > /dev/null'
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