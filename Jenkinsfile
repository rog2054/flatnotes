pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        DOCKER_REGISTRY = 'registry.kranica.com'
        DOCKER_IMAGE = "${DOCKER_REGISTRY}/flatnotes-enc"
        DOCKER_CREDENTIALS_ID = 'registry-kranica-com-user'
    }

    stages {
        stage('Checkout') {
            steps {
                git(
                    branch: 'feature/encrypted-notes',
                    url: 'https://github.com/rog2054/flatnotes.git'
                )
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    env.IMAGE_TAG = env.BUILD_NUMBER
                    docker.build("${DOCKER_IMAGE}:${env.IMAGE_TAG}", '.')
                }
            }
        }

        stage('Push to Private Registry') {
            steps {
                script {
                    docker.withRegistry(
                        "https://${DOCKER_REGISTRY}",
                        DOCKER_CREDENTIALS_ID
                    ) {
                        def dockerImage = docker.image(
                            "${DOCKER_IMAGE}:${env.IMAGE_TAG}"
                        )
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
    }
}
