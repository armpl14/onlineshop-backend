clear
docker pull centos
docker pull centos:7
docker run -d -t --name cantcontainmyself centos:7
docker ps 
docker exec -it cantcontainmyself bash 
clear
docker pull alpine
docker run -t -d --name ohyeah alpine
docker ps
docker exec -it ohyeah sh
docker p
docker ps
docker thenetworkchuck/nccoffee:frenchpress 
docker pull thenetworkchuck/nccoffee:frenchpress
clear
docker run -t -d -p 80:80 --name nccoffee thenetworkchuck/nccoffee:frenchpress
docker ps
docker stop ohyeah
docker start ohyeah
docker stats
docker pull ubuntu:rolling
clear
docker run -t -d -p 80:80 --name nccoffe docker pull ubuntu:rolling
docker run -t -d --name nccoffe ubuntu:rolling sleep infinity
docker rm 160c6da1fd6ecf6578ea24dee82b44ac35214d8e85514e6f9e73959e90578e58+
docker rm "1                                                                                                                                                                                                                60c6da1fd6ecf6578ea24dee82b44ac35214d8e85514e6f9e73959e90578


docker rm 160c6da1fd6ecf6578ea24dee82b44ac35214d8e85514e6f9e73959e90578e58
docker ps
docker run -t -d --name nccoffe ubuntu:rolling sleep infinity
docker ps
docker run -t -d -p 80:80 --name ubuntu:rolling
docker run -t -d --name ubuntu-rolling -p 80:80 ubuntu:rolling sleep infinity
docker run -t -d --name ubuntu-rolling -p 8080:80 ubuntu:rolling sleep infinity
docker rm d4f6b991513b45c6151dacb8185230f9711bc0c08a63250a26fa8ed4193aed44
docker ps
docker rm ubuntu-rolling
docker run -t -d --name ubuntu-rolling -p 8080:80 ubuntu:rolling sleep infinity
docker exec -it ubuntu-rolling bash
docker exec -it ubuntu-rolling bas
docker stop 
docker stop nccoffee
docker rm nccoffee
docker run -d --name mein-nginx -p 80:80 nginx
mkdir -p /home/kamil/meineseite
nano /home/kamil/meineseite/index.html
,
exit
docker run -d --name meineseite -p 80:80 -v /home/kamil/meineseite:/usr/share/nginx/html:ro nginx
docker stop nccoffee
docker rm nccoffee
docker ps
docker rm mein-ngins
docker ps
[200~mkdir -p /home/kamil/meineseite
nano /home/kamil/meineseite/index.html
[200~docker run -d --name meineseite -p 80:80 -v /home/kamil/meineseite:/usr/share/nginx/html:ro nginx
~
docker run -d --name meineseite -p 80:80 -v /home/kamil/meineseite:/usr/share/nginx/html:ro nginx
docker ps
docker stop 4f87c49e07adf3c28f680e9ddc0c3dd7a4c8feec46b3562c105ce0c166d3e8c1
docker run -d --name meineseite -p 80:80 -v /home/kamil/meineseite:/usr/share/nginx/html:ro nginx
docker rm 4f87c49e07adf3c28f680e9ddc0c3dd7a4c8feec46b3562c105ce0c166d3e8c1
docker run -d --name meineseite -p 80:80 -v /home/kamil/meineseite:/usr/share/nginx/html:ro nginx
docker ps
docker stop mein-nginx
docker rm mein-nginx
docker run -d --name meineseite -p 80:80 -v /home/kamil/meineseite:/usr/share/nginx/html:ro nginx
docker rm meineseite
docker run -d --name meineseite -p 80:80 -v /home/kamil/meineseite:/usr/share/nginx/html:ro nginx
docker run -d   --name jenkins   -p 8082:8080   -p 50000:50000   -v jenkins_home:/var/jenkins_home   jenkins/jenkins:lts
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
docker ps
docker ps -a
docker logs jenkins
docker start jenkins
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
docker exec -it jenkins /bin/bash
docker ps
git branch -a
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sudo usermod -aG docker $USER
dpcler
docker ps
docker stop 
docker stop alpine
docker stop 3d58ccfc359a
docker ps
docker stop 15e8aa2467e6
docker ps
docker stop 05d1c29053f8
docker stop 66c04c410640
docker stop b91cdda3dfb7
docker stop 3b2c821d587f
docker ps
clear
docker ps
docker run jenkins
clear
docker run -p 80:80 nginx
docker ps
docker pull nginx:stable-perl
docker ps
docker run -p 80:80 nginx
ip a
docker run -p 80:80 nginx
nano docker-compose.yaml
docker ps
ss -tulpn | grep :53.
sudo ss -tulpn | grep ':53'
# eigene Drop-In-Konfig anlegen
sudo mkdir -p /etc/systemd/resolved.conf.d
echo -e '[Resolve]\nDNSStubListener=no' |   sudo tee /etc/systemd/resolved.conf.d/disable-stub.conf
# DNS-Stub sofort stoppen & neu starten
sudo systemctl restart systemd-resolved
docker compose up -d
docker ps
nano docker-compose.yaml
docker compose up -d
nano docker-compose.yaml
docker compose up -d
nano docker-compose.yaml
docker compose up -d
nano docker-compose.yaml
docker compose up -d
nano docker-compose.yaml
$ docker run -d     --name watchtower     -v /var/run/docker.sock:/var/run/docker.sock     containrrr/watchtower
docker pull containrrr/watchtower:latest-dev
nano docker-compose.yaml
docker compose up -d
nano docker-compose.yaml
docker compose up -d
docker pull kalilinux/kali-rolling
docker run kalilinux -p 81:81 
docker run --rm -it   --name kali   -p 81:81   kalilinux/kali-rolling:latest   /bin/bash
FROM kalilinux/kali-rolling:latest
RUN apt update && apt install -y aircrack-ng
docker build -t kali-wifi .
cat << 'EOF' > Dockerfile
FROM kalilinux/kali-rolling:latest
RUN apt update && apt install -y aircrack-ng
EOF

cat Dockerfile
docker build -t kali-wifi .
docker run --rm -it   --name kali-wifi   --net=host   --cap-add=NET_ADMIN   --cap-add=NET_RAW   -v /lib/modules:/lib/modules:ro   kali-wifi   /bin/bash
