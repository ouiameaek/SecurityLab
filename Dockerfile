FROM python:3

MAINTAINER AitElKadiOuiame AnsariOthmane BoukrouhInsaf

RUN apt-get update
RUN apt-get -y install  libgmp3-dev \
			libmpfr-dev \
			libmpc-dev 

RUN pip3 install gmpy2 \
		 rsa

COPY src /src
COPY rsaOLD /rsaOLD

WORKDIR "/src"

CMD [ "python", "./server.py" ]
