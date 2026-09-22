pipeline {
    agent any

    tools {
        nodejs 'NodeJS 26.8.2'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                bat 'make install'
            }
        }

        stage('Lint') {
            steps {
                bat 'make lint'
            }
        }

        stage('Type-check') {
            steps {
                bat 'make type-check'
            }
        }

        stage('Testes Unitarios') {
            steps {
                bat 'make test'
            }
        }

        stage('SonarQube') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    bat 'make sonar'
                }
            }
        }

        stage('Build') {
            steps {
                bat 'make build'
            }
        }

        stage('Relatorio Auditoria') {
            steps {
                bat '"C:/Users/jrego/AppData/Local/Python/pythoncore-3.14-64/python.exe" scripts/gerar_relatorio.py'
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'auditoria.html',
                    reportName: 'Relatorio de Auditoria (ISO/FDA)'
                ])
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'dist/**, bin/**, reports/**, coverage/**, coverage.out', fingerprint: true
            echo 'Build aprovado'
        }
        failure {
            echo 'Build reprovado - ver logs'
        }
    }
}