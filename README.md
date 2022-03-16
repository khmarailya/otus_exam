# otus_exam

## linux

Установить docker, docker-compose

_Узнать ip докера_

    apt install net-tools
    ifconfig

__Стянуть проект__

    cd /opt
    git clone https://github.com/khmarailya/otus_exam.git
    cd otus_exam
    bash setup/env.sh lin
    
    cd /opt/otus_exam
    git pull
    
__Поднять отдельно Селеноид__

_Скопировать_

    cp -RT /opt/otus_exam/setup/selenoid/ /opt/selenoid/
    cd /opt/selenoid
    
Стянуть нужные [образы браузеров](https://aerokube.com/images/latest/#_selenium) и запустить
 
    docker pull selenoid/chrome:86.0
    ...
    docker-compose up -d
    
- Адрес: http://localhost:8080
- Сессия автотеста: http://localhost:4444/wd/hub

__Поднять отдельно [Opencart](https://hub.docker.com/r/bitnami/opencart/)__

    cp -RT /opt/otus_exam/setup/opencart/ /opt/opencart/
    cd /opt/opencart
    docker-compose up -d

- Адрес: http://localhost  
- Админка: http://localhost/admin: Логин/пароль - user/bitnami  