pipeline {
    agent any

    // --- Environment Variables ---
    environment {
        // AWS settings
        AWS_REGION = 'ap-south-1'                       // Change to your region
        ECR_REPO = '513371322378.dkr.ecr.ap-south-1.amazonaws.com/mynewapp-app'                 // Change to your ECR repo URI
        IMAGE_TAG = "${BUILD_NUMBER}"                   // Use Jenkins build number as image tag

        // Kubernetes settings
        K8S_NAMESPACE = 'default'                       // Change if using custom namespace
        K8S_DEPLOYMENT_FILE = 'k8s/deployment.yml'     // Path to your deployment YAML
        K8S_SERVICE_FILE = 'k8s/svc.yml'               // Path to your service YAML

        // Optional: AWS credentials ID from Jenkins credentials store
        AWS_CREDENTIALS_ID = 'aws-credentials'          // Create in Jenkins > Credentials
    }

    stages {

        // --- 1. Checkout Code ---
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/Prags06/demoapp.git' // Change repo URL
            }
        }

        // --- 2. Run Unit Tests ---
        stage('Run Tests') {
            steps {
                
                sh 'python3 -m unittest discover -s tests'
            }
        }

        // --- 3. Build Docker Image ---
        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                    docker build -t ${ECR_REPO}:${IMAGE_TAG} .
                    """
                }
            }
        }

        // --- 4. Login to AWS ECR ---
        stage('Login to ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${AWS_CREDENTIALS_ID}"
                ]]) {
                    sh """
                    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                    aws configure set default.region ${AWS_REGION}

                    aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login --username AWS --password-stdin ${ECR_REPO.split('/')[0]}
                    """
                }
            }
        }

        // --- 5. Push Docker Image to ECR ---
        stage('Push to ECR') {
            steps {
                sh """
                docker push ${ECR_REPO}:${IMAGE_TAG}
                """
            }
        }

                stage('Approval Before Deploy') {
            steps {
                script {
                    timeout(time: 1, unit: 'HOURS') {   // Wait for max 1 hour
                        input message: "Approve deployment to EKS?", ok: "Deploy"
                    }
                }
            }
        }

        // --- 6. Deploy to Kubernetes ---
        stage('Deploy to EKS') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${AWS_CREDENTIALS_ID}"
                ]]) {
                    sh '''
                    # Update kubeconfig
                    aws eks update-kubeconfig --region ${AWS_REGION} --name jenkinscluster

                    # Replace image placeholder in deployment YAML
                    sed -i "s|PLACEHOLDER_IMAGE|${ECR_REPO}:${IMAGE_TAG}|g" ${K8S_DEPLOYMENT_FILE}

                    # Apply deployment and service
                    kubectl apply -f ${K8S_DEPLOYMENT_FILE} -n ${K8S_NAMESPACE}
                    kubectl apply -f ${K8S_SERVICE_FILE} -n ${K8S_NAMESPACE}

                    # Quick status check (no waiting)
                    DEPLOYMENT_NAME=$(grep 'name:' ${K8S_DEPLOYMENT_FILE} | head -1 | awk '{print $2}')
                    kubectl rollout status deployment/$DEPLOYMENT_NAME -n ${K8S_NAMESPACE} --watch=false
                    STATUS=$?

                    if [ $STATUS -ne 0 ]; then
                      echo "Deployment seems unhealthy, rolling back..."
                      kubectl rollout undo deployment/$DEPLOYMENT_NAME -n ${K8S_NAMESPACE}
                    else
                      echo "Deployment triggered successfully (not waiting for pods to be ready)."
                    fi
                    set -e
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Deployment Failed!'
        }
    }
}
