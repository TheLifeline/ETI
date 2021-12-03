SHELL_FOLDER=$(dirname $(readlink -f "$0"))
echo $SHELL_FOLDER
sudo docker-compose -f $SHELL_FOLDER/ES/docker-compose.dev.yml up -d
sudo docker-compose -f $SHELL_FOLDER/BACKEND/docker-compose.dev.yml up -d
if ifconfig |grep eth0 >/dev/null ;then
echo window.axiosBaseUrl=\"http://`ip addr|grep inet|grep eth|awk '{print $2}'|awk -F '/' '{print $1}'`:5000/\" > $SHELL_FOLDER/FRONTEND/public/config.js;                        
else
echo window.axiosBaseUrl=\"http://`ip addr|grep inet|grep ens|awk '{print $2}'|awk -F '/' '{print $1}'`:5000/\" > $SHELL_FOLDER/FRONTEND/public/config.js;                     
fi
cd $SHELL_FOLDER/FRONTEND
npm install && npm run build
sudo docker-compose -f $SHELL_FOLDER/FRONTEND/docker-compose.dev.yml up -d