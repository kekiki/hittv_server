
sudo nohup python3 -u /home/ubuntu/workspace/rainbow_server/app/app.py > /home/ubuntu/workspace/logs/app.log 2>&1 &

sudo nohup python3 -u /home/ubuntu/workspace/rainbow_server/reptile/book_update.py > /home/ubuntu/workspace/logs/book_update.log 2>&1 &

ssh ubuntu@18.189.190.235
scp /Users/kejie/Desktop/development/assets/resource/qqwry.dat ubuntu@18.189.190.235:/home/ubuntu/workspace/assets/resource/qqwry.dat

sudo nohup python3 -u /home/ubuntu/Aseries/Resources/all_novel.py > /home/ubuntu/logs/all_novel.log 2>&1 &