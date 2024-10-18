pipeline{
    agent any 
    environment{
        WORKSPACE_DIR = "${WORKSPACE}"
        VIRTUAL_ENV = "${WORKSPACE}/.venv"
        APP_NAME = "app_demo"
        SYSTEMD_SERVICE = "${APP_NAME}.service"
        PATH = "/usr/local/bin:/usr/bin:/bin:$PATH"
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
                    echo "Python version:"
                    python3 --version
                    echo "Python location:"
                    which python3
                    if [ ! -d ${VIRTUAL_ENV} ]; then
                        echo "Creating virtual environment..."
                        python3 -m venv ${VIRTUAL_ENV}
                    fi
                    echo "Activating virtual environment..."
                    . ${VIRTUAL_ENV}/bin/activate
                    echo "Upgrading pip..."
                    pip install --upgrade pip
                    echo "Installing requirements..."
                    pip install -r requirements.txt
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
