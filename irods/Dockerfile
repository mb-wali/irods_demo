FROM ubuntu:bionic AS base

# note: cyverse/irods-adm uses bc
#
RUN apt-get update \
 && apt-get upgrade --assume-yes \
 && apt-get install --assume-yes \
        gnupg \
        wget \
        lsb-release \
        wait-for-it \
        bc \
 && wget -qO irods-signing-key.asc https://packages.irods.org/irods-signing-key.asc \
 && apt-key add irods-signing-key.asc \
 && echo "deb [arch=amd64] https://packages.irods.org/apt/ $(lsb_release -sc) main" \
    > /etc/apt/sources.list.d/renci-irods.list \
 && apt-get update

RUN apt-get install --assume-yes \
    irods-server \
    irods-database-plugin-postgres

# this is just to make working in a container more convenient
#
RUN apt-get install --assume-yes \
    iputils-ping \
    netcat \
    neovim \
    tmux \
    less \
    exuberant-ctags \
    ranger \
  && mkdir -p /root/.config/nvim

# COPY tmux.conf /root/.tmux.conf
# COPY nvim /root/.config/nvim/
#
# end of all convenience

FROM base

RUN useradd irods \
 && mkdir /home/irods \
 && mkdir /var/lib/irods/Vault \
 && chown -R irods. /home/irods /var/lib/irods/

# create a well known entrypoint
#
COPY run.sh /home/irods/

# nagios plugin from cyverse/irods-adm
COPY check_irods /home/irods/

COPY wait-for-irods-server /home/irods/

# prepared script to add zones
#
COPY add-remote-zone.py /home/irods/

# prepared script to enable SSL
#
COPY enable-ssl.py /home/irods

CMD ["bash"]
