# otus_exam

## linux

Установить docker, docker-compose

__Стянуть проект__

    cd /opt
    git clone https://github.com/khmarailya/otus_exam.git
    cd otus_exam
    bash setup/env.sh lin

__Поднять Селеноид__

http://localhost:8080/

    cd /opt/otus_exam
    git pull
    cp -rf otus_exam/setup/selenoid/ selenoid
    cd /opt/selenoid
    docker-compose up -d