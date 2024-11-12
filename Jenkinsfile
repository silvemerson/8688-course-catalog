pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }

    environment {
        IMAGE_NAME="course-catalog"
        IMAGE_TAG="0.${BUILD_ID}"
        IMAGE_TAG_LATEST="latest"
        CONTAINER_IMAGE="${IMAGE_NAME}:${IMAGE_TAG}"
        CONTAINER_IMAGE_LATEST="${IMAGE_NAME}:${IMAGE_TAG_LATEST}"
        DOCKER_REGISTRY = "35.224.51.209:8082"
        HTTP_PROTO = "http://"
        KUBE_TOKEN = credentials('KUBE_TOKEN')
        K8S_API_SERVER = "https://34.44.213.10:6443"
        K8S_ACCESS = "--server=$K8S_API_SERVER --token=$KUBE_TOKEN --insecure-skip-tls-verify"       
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
                        sh "docker tag ${DOCKER_REGISTRY}/${CONTAINER_IMAGE} ${DOCKER_REGISTRY}/${CONTAINER_IMAGE_LATEST}"
                        sh "docker push ${DOCKER_REGISTRY}/${CONTAINER_IMAGE}"
                        sh "docker push ${DOCKER_REGISTRY}/${CONTAINER_IMAGE_LATEST}"
                    }
                }
            }
        }
        stage('Deploy'){
            steps{
                sh "kubectl -n homolog delete -f manifest $K8S_ACCESS"
                sh "kubectl -n homolog apply -f manifest $K8S_ACCESS"
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
