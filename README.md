# SecurityLab

Demonstrate python2.7's rsa signature forgery vulnerability

### Build an image from the Dockerfile :
`sudo docker build -t imagename PATH_TO_DOCKERFILE`

### Run the server :
`sudo docker run --name ="containername" imagename`

### Run the client :
`sudo docker exec -it containername bash`
`python client.py`
`exit` to exit the container bash

