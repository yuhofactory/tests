# Get base image
FROM ubuntu:18.04
MAINTAINER Hisyamuddin Jamirun <hisyamuddin.jamirun@gmail.com>
# Do not exclude man pages & other documentation
RUN rm /etc/dpkg/dpkg.cfg.d/excludes && \
	apt-get update && \
	# Execute updated packages installation only for security updates & bug fixes
	apt-get upgrade -y && \
	apt-get install -y \
		vim \
		net-tools \
		openssh-server \
		sudo \
		git \
		python-pip
# Create new user
ARG USER_PASS=ommohome
ARG HOME_DIR=/home/ommohome
RUN useradd --system --create-home --home-dir=$HOME_DIR \
	--shell=/bin/bash --user-group --groups=sudo \
	--password="$(openssl passwd -1 $USER_PASS)" $USER_PASS
# Export configuration file for automation
COPY config_ommohome.conf $HOME_DIR/.tests_conf/config_ommohome.conf
USER $USER_PASS
WORKDIR $HOME_DIR
ENV PASSWORD=$USER_PASS
ENTRYPOINT echo $PASSWORD | sudo -S service ssh start && bash

