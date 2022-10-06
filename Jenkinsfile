

pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh "python3 --version"        
                echo "This should work"
                echo "Building...."
                sh "docker version"
                sh "docker build -t capstone ."
                echo "Build success!"
            }
        }

        stage('Test') {
            steps {
                echo "Testing..."
            }
        }

        stage('Deploy') {
            when {
                branch "master"
            }

            steps {
                echo "Deploying...."
                script {
                    try {
                        sh "docker stop capstone"
                    } catch (Exception err) {
                        echo "No service is running, will start one"
                    }
                    
                    try {
                        sh "docker rm capstone"
                        sh "docker rmi \$(docker images --filter "dangling=true" -q --no-trunc)"
                    } catch (Exception err) {
                        echo "No container exists, will create one"
                    }
                }
                sh "pwd"
                sh "export JENKINS_NODE_COOKIE=dontKillMe"
                sh "nohup docker run -p 8081:8081 --name capstone capstone > ~/capstone.log &"
                echo "Deploy success!"
            }
        }
    }
}
