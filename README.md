# otus_exam

## linux

Установить docker, docker-compose

_Узнать ip докера_

    apt install net-tools
    ifconfig

__Стянуть проект__

    cd /opt
    git clone https://github.com/khmarailya/otus_exam.git
    git pull
    
_Если нужно виртуальное окружение_

    cd /opt/otus_exam
    bash setup/env.sh lin

__Поднять__ (opencart, selenoid, jenkins)

_можно скопировать в отдельную папку файлы настроек_

    cp -RT /opt/otus_exam/setup/selenoid/ /opt/selenoid_opencart/
    cd /opt/selenoid_opencart
    
_либо перейти в папку настроек без коирования_
    
    cd /opt/otus_exam/setup/
    
_(пере)запустить_    
    
    docker-compose down && docker-compose up -d
    
[Opencart](https://hub.docker.com/r/bitnami/opencart/)   
- Адрес: http://localhost:8080  
- Админка: https://localhost/admin: Логин/пароль - user/bitnami     

_selenoid_
Стянуть нужные [образы браузеров](https://aerokube.com/images/latest/#_selenium), видеорекордер
 
    docker pull selenoid/chrome:86.0
    ...
    docker pull selenoid/video-recorder:latest-release
- Адрес: http://localhost:8090
- Сессия автотеста: http://localhost:4444/wd/hub_

_jenkins_
- Адрес: http://localhost:8088

Добавить проект

- шаг1 (стягивание)


     https://github.com/khmarailya/otus_exam.git
    
- шаг 2 (запуск, при необходимости задайте переменные окружения - см. Dockerfile)


     if [ ! -d allure-results/ ]; then
	/bin/mkdir -p /var/jenkins_home/workspace/otus_exam/allure-results 
    fi
    /bin/chmod -R 777 /var/jenkins_home/workspace/otus_exam/allure-results
    docker build .
    docker run --rm -v "/var/jenkins_home/workspace/otus_exam/allure-results:/opt/app/allure-results" -e MARKS="ui" otus_exam
    ls -la
    
    
- шаг3 (аллюр)    


    allure-results

__Редактировать config.php__
_Проблема_ opencart по каким-то причинам не принимает указанный в параметрах OPENCART_HOST. 
Пришлось применять "костыли": редактировать и подменять config.php и admin/config.php 
(задать в yml как volume или копировать через command нельзя из-за внутренних особенностей образов)
- для запуска из браузера 
  - поменять для HTTP_SERVER и HTTP_CATALOG: к localhost добавить порт (если нужно, по умолчанию 8080)
  - поменять для HTTPS_SERVER и HTTPS_CATALOG: к localhost добавить порт (если нужноб по умолчанию стандартный)
- для запуска из selenoid 
  - _docker network inspect bridge_ 
    - посмотреть ip сети "IPAM":"Config":"Gateway"  
  - поменять в конфигах: аналогично, но вместо localhost - ip_сети + нужный порт
 
 
    cd /opt/selenoid_opencart
    nano config.php
    nano config_admin.php
    docker cp config.php selenoid_opencart_opencart_1:/opt/bitnami/opencart/config.php
    docker cp config_admin.php selenoid_opencart_opencart_1:/opt/bitnami/opencart/admin/config.php