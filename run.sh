SHELL_FOLDER=$(dirname $(readlink -f "$0"))
echo $SHELL_FOLDER
sudo rm -rf $SHELL_FOLDER/BACKEND/project/temp
sudo rm -rf $SHELL_FOLDER/BACKEND/project/data-test.db
sudo docker-compose -f $SHELL_FOLDER/ES/docker-compose.dev.yml up -d
sudo docker-compose -f $SHELL_FOLDER/BACKEND/docker-compose.dev.yml up -d
cd $SHELL_FOLDER/FRONTEND
npm install && npm run build
sudo docker-compose -f $SHELL_FOLDER/FRONTEND/docker-compose.dev.yml up -d