
sudo killall -9 python main.py 127.0.0.1:5000
current=/home/pi/work/weixin_server
cd $current
nohup python main.py 127.0.0.1:5000 &
