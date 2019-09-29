# plugApps
Projeto para gerenciar reuniões


## Como instalar?
Precisamos fazer o download do nosso código fonte, digite:
```shell
git clone https://github.com/gilvanti/plugApps.git
```
O app está em docker quanto a dependencias não se preocupe, porem precisamos configurar configurar nossa maquina, para executar. Segue abaixo link que utilizei para configurar meu computador, utilizo o ubuntu 18.04.

https://www.hostinger.com.br/tutoriais/install-docker-ubuntu

Outro procedimento que realizei é configurar seu usuário para executar os comando docker, para evitar está usando o sudo a todo comando, se você não tem problema com isto pode pular esta etapa.

https://luizsouza.com.br/2018/11/01/docker-sem-sudo-no-ubuntu-18-04/

Após estás etapas vamos gerar nossas imagens docker, pois temos um app que se comunica com um worker celery e um broker redis, vá até a raiz do diretório criado ao fazer o clone do projeto e execute o comando abaixo:
```shell
docker-compose up
```

Concluimos, agora só acessar o http://localhost:8000/
