
SHELL_FOLDER=$(dirname $(readlink -f "$0"))
echo $SHELL_FOLDER
if ifconfig |grep eth0 >/dev/null ;then
echo window.HOST_IP=\"`ifconfig eth0 |grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d 'addr:' `\" >> $SHELL_FOLDER/FRONTEND/public/config.js;                        
else
echo window.HOST_IP=\"`ifconfig ens33 |grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d 'addr:' `\" > $SHELL_FOLDER/FRONTEND/public/config.js;                     
fi
