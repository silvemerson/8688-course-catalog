pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }

    environment {
        IMAGE_NAME="course-catalog"
        IMAGE_TAG="0.${BUILD_ID}"
        CONTAINER_IMAGE="${IMAGE_NAME}:${IMAGE_TAG}"
        DOCKER_REGISTRY = "35.224.51.209:8082"
        HTTP_PROTO = "http://"
    }

    stages{
        stage('Unit Test'){
            steps{
                script{
                    image = docker.build("${CONTAINER_IMAGE}")
                    image.inside("-v ${WORKSPACE}:/course-catalog/"){
                        sh "nosetests --with-xunit --with-coverage \
                        --cover-package=project test_users.py"
                    }
                }
            }

        }
        stage('SonarScanner'){
            steps{
                script{
                    def scannerPath = tool "SonarScanner"
                    withSonarQubeEnv('course-catalog-sonarqube'){
                        sh "${scannerPath}/bin/sonar-scanner -Dsonar.projectKey=courseCatalog -Dsonar.sources=."
                    }

                }
            }
        }
        // stage('SonarQube - Analysis Result'){
        //     steps{
        //         timeout(time:30, unit: 'SECONDS'){
        //             waitForQualityGate abortPipeline: false
        //         }
        //     }
        // }
        stage('Build'){
            steps{
                script{
                    docker.build("${DOCKER_REGISTRY}/${CONTAINER_IMAGE}")
                }
            }
        }
        stage('Push'){
            steps{
                script{
                    docker.withRegistry("${HTTP_PROTO}${DOCKER_REGISTRY}", "jenkins_docker"){
                        sh 'docker push ${DOCKER_REGISTRY}/${CONTAINER_IMAGE}'
                    }
                }
            }
        }
    }
    post{
        success{
            echo "A Pipeline foi executada com sucesso"
            junit 'nosetests.xml'
        }
        failure{
            echo "A Pipeline foi executada com falha"
        }
        cleanup{
            sh "docker image rm ${CONTAINER_IMAGE}"
            sh  "docker image rm ${DOCKER_REGISTRY}/${CONTAINER_IMAGE}"
        }
    }
}
