# otus_exam

## linux

Установить docker, docker-compose

_Узнать ip докера_

    apt install net-tools
    ifconfig
    
    
    
    docker network create -d bridge my-network

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
    
Стянуть нужные [образы браузеров](https://aerokube.com/images/latest/#_selenium), видеорекордер, и запустить
 
    docker pull selenoid/chrome:86.0
    ...
    docker pull selenoid/video-recorder:latest-release
    docker-compose up -d
    
- Адрес: http://localhost:8080
- Сессия автотеста: http://localhost:4444/wd/hub

__Поднять отдельно [Opencart](https://hub.docker.com/r/bitnami/opencart/)__

    cp -RT /opt/otus_exam/setup/opencart/ /opt/opencart/
    cd /opt/opencart
    docker-compose up -d

- Адрес: http://localhost  
- Админка: http://localhost/admin: Логин/пароль - user/bitnami  


__Поднять__
    
    cd /opt/selenoid_opencart
    docker-compose down && docker-compose up -d

__Редактировать config.php__
_Проблема_ opencart по каким-то причинам не принимает указанный в параметрах OPENCART_HOST. 
Пришлось применять "костыли": редактировать и подменять config.php и admin/config.php 
(задать в yml как volume или копировать через command нельзя из-за внутренних особенностей образов)
- для запуска из браузера 
  - поменять для HTTP_SERVER и HTTP_CATALOG: localhost на localhost:8080
  - поменять для HTTPS_SERVER и HTTPS_CATALOG: localhost на localhost:8080
- для запуска из selenoid 
  - _docker network inspect bridge_ 
    - посмотреть ip сети "IPAM":"Config":"Gateway"  
  - поменять для HTTP_SERVER: localhost на ip_сети:8080
 

    cd /opt/selenoid_opencart
    nano config.php
    nano admin/config.php
    docker cp config.php selenoid_opencart_opencart_1:/opt/bitnami/opencart/config.php
    docker cp config_admin.php selenoid_opencart_opencart_1:/opt/bitnami/opencart/admin/config.php