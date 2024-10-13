pipeline{
    agent any 
    environment{
        WORKSPACE_DIR = "/home/www/app"
        VIRTUAL_ENV = "${WORKSPACE}/.venv"
        APP_NAME = "app_demo"
        SYSTEMD_SERVICE = "${APP_NAME}.service"
    }
    stages{
        stage('Checkout'){
            steps{
                git  'https://github.com/dengxuezhao/cash_debt_simulation.git'
            }
        }
        stage('PrepareEnviroment'){
            steps{
                script{
                    //创建虚拟环境并安装依赖
                    sh '''
                    cd ${WORKSPACE_DIR}
                    if [! -d ${VIRTUAL_ENV}]; then
                        python3 -m venv ${VIRTUAL_ENV}
                    fi
                    source ${VIRTUAL_ENV}/bin/activate
                    pip install --upgrade pip
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