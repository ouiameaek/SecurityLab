# SecurityLab

Demonstrate python2.7's rsa signature forgery vulnerability

### Build an image from the Dockerfile :
`sudo docker build -t imagename PATH_TO_DOCKERFILE`

### Run the server in the container :
`sudo docker run --name ="containername" imagename`

### Connect to the container bash :
`sudo docker exec -it containername bash`

### Run the client :
`python client.py`

### Exit the container bash :
`exit`

