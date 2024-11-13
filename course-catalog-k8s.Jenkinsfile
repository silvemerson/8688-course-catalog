podTemplate(
    containers: [
        containerTemplate(name: 'openjdk', image: 'openjdk:11', command: 'sleep', args: '99d'),
        containerTemplate(name: 'docker', image: 'docker:dind', command: 'sleep', args: '99d', ttyEnabled: true, privileged: true),
        containerTemplate(name: 'kubectl', image: 'alpine', command: 'sleep', args: '99d')
    ],
    volumes: [
        hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')
    ]
) {
    node(POD_LABEL) {
        container('openjdk') {
            stage('SonarQube Analysis'){
                script{
                    git 'http://35.224.51.209:3000/root/course-catalog.git'
                    def scannerPath = tool "SonarScanner"
                    withSonarQubeEnv('course-catalog-sonarqube'){
                        sh "${scannerPath}/bin/sonar-scanner -Dsonar.projectKey=courseCatalog -Dsonar.sources=."
                    }
                }
            }
        }
        container('docker'){
            stage('Git Clone'){
                git 'http://35.224.51.209:3000/root/course-catalog.git' 
            }
            stage('Build'){
                sh "docker build -t course-catalog:k8s-${BUILD_ID} ."
            }
            stage('Teste'){
                sh "docker run -dti --name course-catalog-${BUILD_ID} --rm course-catalog:k8s-${BUILD_ID}"
                sh "docker exec course-catalog-${BUILD_ID} nosetests --with-xunit --with-coverage --cover-package=project test_users.py"
                sh "docker stop course-catalog-${BUILD_ID}"
                sh "docker tag course-catalog:k8s-${BUILD_ID} 35.224.51.209:8082/course-catalog:k8s-${BUILD_ID}"
            }
            stage('Push'){
                script{
                    docker.withRegistry("http://35.224.51.209:8082", "jenkins_docker"){
                        sh "docker push 35.224.51.209:8082/course-catalog:k8s-${BUILD_ID}"
                }
            }
        }
    }
    container('kubectl'){
        stage('Deploy'){
            withKubeConfig([credentialsId: 'KUBE_TOKEN', serverUrl: "https://34.44.213.10:6443"]){
                sh 'apk update && apk add --no-cache curl'
                sh 'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"'
                sh 'chmod +x ./kubectl && mv ./kubectl /usr/local/bin/kubectl'
                sh 'sleep 5'
                sh "kubectl -n homolog set image deployment/web-initiate-db simple-python-flask-init-db=35.224.51.209:8082/course-catalog:k8s-${BUILD_ID}"
                sh "kubectl -n homolog set image deployment/web simplepythonflask=35.224.51.209:8082/course-catalog:k8s-${BUILD_ID}"
            }
        }
    }
    }
}