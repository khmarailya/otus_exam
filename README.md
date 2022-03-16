# otus_exam

## linux

Установить docker, docker-compose

__Стянуть проект__

    cd /opt
    git clone https://github.com/khmarailya/otus_exam.git
    cd otus_exam
    bash setup/env.sh lin
    
    cd /opt/otus_exam
    git pull
    
__Поднять Селеноид__

_Скопировать_

    cp -RT /opt/otus_exam/setup/selenoid/ /opt/selenoid/
    cd /opt/selenoid
    
_Стянуть нужные [образы браузеров](https://aerokube.com/images/latest/#_selenium)_   
 
    docker pull selenoid/chrome:86.0
    ...
    
_Запустить_
    
    docker-compose up -d
http://localhost:8080/


__Поднять Opencart__

_Скопировать_

    cp -RT /opt/otus_exam/setup/opencart/ /opt/opencart/
    cd /opt/selenoid
    docker-compose up -d
http://localhost    