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

        stage('Unit Tests') {
            steps {
                bat 'make test'
            }
        }

        stage('E2E Tests') {
            steps {
                bat 'make test-e2e'
            }
        }

        stage('SonarQube') {
            steps {
                bat """
                    set /p SONAR_TOKEN=<C:\\Users\\jrego\\sonar-token.txt
                    C:\\SonarScanner-8.1.0\\sonar-scanner-8.1.0.6389-windows-x64\\bin\\sonar-scanner.bat -Dsonar.token=%SONAR_TOKEN% -Dsonar.host.url=http://127.0.0.1:9000 -Dsonar.qualitygate.wait=true
                """
            }
        }

        stage('Build') {
            steps {
                bat 'make build'
            }
        }

        stage('Audit Report') {
            steps {
                bat '"C:/Users/jrego/AppData/Local/Python/pythoncore-3.14-64/python.exe" scripts/generate_report.py'
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'auditoria.html',
                    reportName: 'Audit Report (ISO/FDA)'
                ])
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'dist/**, bin/**, reports/**, coverage/**, coverage.out', fingerprint: true
            echo 'Build passed'
        }
        failure {
            echo 'Build failed - check logs'
        }
    }
}