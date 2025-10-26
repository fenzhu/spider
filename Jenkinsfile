/* Requires the Docker Pipeline plugin */
pipeline {
    agent { docker { image 'python' } }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}