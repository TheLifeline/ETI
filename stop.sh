SHELL_FOLDER=$(dirname $(readlink -f "$0"))
sudo docker-compose -f $SHELL_FOLDER/ES/docker-compose.dev.yml down
sudo docker-compose -f $SHELL_FOLDER/BACKEND/docker-compose.dev.yml down
sudo docker-compose -f $SHELL_FOLDER/FRONTEND/docker-compose.dev.yml down