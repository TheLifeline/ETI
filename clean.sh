SHELL_FOLDER=$(dirname $(readlink -f "$0"))
echo $SHELL_FOLDER
sudo rm -rf $SHELL_FOLDER/BACKEND/project/temp
sudo rm -rf $SHELL_FOLDER/BACKEND/project/data-test.db
sudo rm -rf $SHELL_FOLDER/BACKEND/data/postgresql
sudo rm -rf $SHELL_FOLDER/ES/es01/data
sudo rm -rf $SHELL_FOLDER/ES/es01/logs
sudo rm -rf $SHELL_FOLDER/ES/es02/data
sudo rm -rf $SHELL_FOLDER/ES/es02/logs