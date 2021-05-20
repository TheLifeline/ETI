SHELL_FOLDER=$(dirname $(readlink -f "$0"))
echo $SHELL_FOLDER
sudo rm -rf $SHELL_FOLDER/BACKEND/project/temp
sudo rm -rf $SHELL_FOLDER/BACKEND/project/data-test.db
sudo docker-compose -f $SHELL_FOLDER/ES/docker-compose.dev.yml up -d
sudo docker-compose -f $SHELL_FOLDER/BACKEND/docker-compose.dev.yml up -d
if ifconfig |grep eth0 >/dev/null ;then
echo window.HOST_IP=\"`ifconfig eth0 |grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d 'addr:' `\" >> $SHELL_FOLDER/FRONTEND/public/config.js;                        
else
echo window.HOST_IP=\"`ifconfig ens33 |grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d 'addr:' `\" > $SHELL_FOLDER/FRONTEND/public/config.js;                     
fi
cd $SHELL_FOLDER/FRONTEND
npm install && npm run build
sudo docker-compose -f $SHELL_FOLDER/FRONTEND/docker-compose.dev.yml up -d