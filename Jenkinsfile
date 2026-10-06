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

        stage('Testes E2E') {
            steps {
                bat 'make test-e2e'
            }
        }

	stage('SonarQube') {
    		steps {
        		withCredentials([string(credentialsId: 'sonar-token-web', variable: 'SONAR_TOKEN')]) {
            			bat '"%SONAR_SCANNER_5%\\bin\\sonar-scanner.bat" -Dsonar.token=%SONAR_TOKEN% -Dsonar.host.url=http://127.0.0.1:9000 -Dsonar.qualitygate.wait=true'
        }
    }
}
        stage('Design Review') {
            when {
                expression { env.BRANCH_NAME == 'main' || env.BRANCH_NAME == null }
            }
            steps {
                script {
                    def aprovador = input(
                        message: 'Design Review: Aprovar release?',
                        ok: 'Aprovar',
                        parameters: [
                            string(name: 'APROVADOR_NOME', defaultValue: 'Joana Rego', description: 'Nome do aprovador')
                        ]
                    )
                    env.APROVADOR = aprovador
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