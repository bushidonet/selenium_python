 🧪 Selenium Flask App
 
Este proyecto es una API construida con Flask que ejecuta pruebas automatizadas. 
Usando Selenium con un navegador Chrome en modo headless, todo dentro de contenedores Docker.
Es la estructura base para rellenar formularios y descargar en forma PDF


📁 Estructura del proyecto
.
├── app/
│   ├── test.py             # Script principal con Flask + Selenium
│   ├── Dockerfile          # Imagen para la API Flask
│   └── requirements.txt    # Dependencias de Python
├── docker-compose.yml      # Orquestación de servicios
├── .gitignore              # Archivos a excluir de Git


    
3. Construir y levantar los contenedores
  - Debes de tener instalado en tu maquina:
    * [Docker](https://www.docker.com/)
    * [Docker Compose](https://docs.docker.com/compose/)
    
    docker-compose up --build
   

