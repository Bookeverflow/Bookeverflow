# bookoverflow

An prototype of our Microsoft Azure ImagineHack project. This aims to become a platform for the book lover to exchange book much easier.

## How to setup 

```shell
# python version: 2.7

# install requirement
pip install -r  requirements.txt

# run
python run.py
```

## How to deploy using Microsoft Azure

```
# Reference: http://www.jamessturtevant.com/posts/Deploying-Python-Website-To-Azure-Web-with-Docker/
# First, build a docker image of this project
docker build -f Dockerfile -t bookeverflow:latest .

# Then, push it to dockerhub
docker tag {{The IMAGE ID of bookeverflow}} kitfung/bookeverflow
docker login
docker push kitfung/bookeverflow

# Lastly, setup it in Microsoft Azure platform

```

