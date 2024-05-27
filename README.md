# Taller 2 - Grupo 2


La aplicación se encuentra ejecutándose en dentro de la red de la Universidad:

     http://172.24.99.73:8080/


Para desplegar la aplicación se pueden seguir los siguientes pasos:

Crear la imagen de docker:
    
    docker build -t geo_grupo_2 .

Ejecutar la imagen:

    docker run -d -p 8080:8080 geo_grupo_2