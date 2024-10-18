pipeline{
    agent any 
    environment{
        WORKSPACE_DIR = "/var/jenkins_home/workspace"
        VIRTUAL_ENV = "${WORKSPACE}/.venv"
        APP_NAME = "app_demo"
        SYSTEMD_SERVICE = "${APP_NAME}.service"
        PYTHON_PATH = "/opt/python/mini/bin/python"
        PATH = "/opt/python/mini/bin:${PATH}"
    }
    stages{
        stage('Checkout'){
            steps{
                git branch: 'main', credentialsId: '069fe1f6-cd6e-47a8-a730-1f834556e05e', 
                url: 'https://github.com/dengxuezhao/cash_debt_simulation.git'
            }
        }
        stage('PrepareEnvironment'){
            steps{
                script{
                    sh '''
                    cd ${WORKSPACE_DIR}
                    echo "Python path: ${PYTHON_PATH}"
                    ${PYTHON_PATH} --version || echo "Unable to get Python version"
                    if [ ! -d ${VIRTUAL_ENV} ]; then
                        ${PYTHON_PATH} -m venv ${VIRTUAL_ENV} || echo "Failed to create virtual environment"
                    fi
                    source ${VIRTUAL_ENV}/bin/activate
                    ${VIRTUAL_ENV}/bin/pip install --upgrade pip
                    ${VIRTUAL_ENV}/bin/pip install -r requirements.txt
                    '''
                }
            }
        }
        stage('Test'){
            steps{
                script{
                    //运行测试
                    sh '''
                    cd ${WORKSPACE_DIR}
                    source ${VIRTUAL_ENV}/bin/activate
                    pytest
                    '''
                }
            }
        }
        stage('Deploy'){
            steps{
                script{
                    //停止旧的服务
                    sh "sudo systemctl stop ${SYSTEMD_SERVICE}"
                    //将新代码复制到目标目录
                    sh "sudo cp -r ${WORKSPACE_DIR} /var/www/${APP_NAME}"
                    //启动新服务
                    sh "sudo systemctl start ${SYSTEMD_SERVICE}"
                }
            }
        }
    }
    post{
        always{
        //清理或通知等后处理操作
        echo 'This will always run'
        }
        failure{
            //构建失败时的操作
            echo 'Build failed:('
            mail to :'zhm_275@outlook.com',
                subject:"Jenkins Build Failed for ${env.JOB_NAME}",
                body: "Something is wrong with ${env.BUILD_URL}"
        }
    }

}
