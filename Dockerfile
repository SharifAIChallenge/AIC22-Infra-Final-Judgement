# FROM reg.aichallenge.ir/aic/infra/final_judgment :486-b2af3cf0  
FROM reg.aichallenge.ir/python:3.8 
RUN dpkg --add-architecture i386
RUN apt-get update && apt install -y vim curl gettext unrar-free libc6-i386 libc6-x32 libasound2 libxi6 libxtst6
ADD ./java /tmp
RUN cd /tmp && \
 unrar Java_SE_Development_Kit_18.0.2_Linux_Debian_x64_Downloadly.ir.rar && \
 cd "Java SE Development Kit 18.0.2 Linux Debian x64" && \
 dpkg -i jdk-18_linux-x64_bin_Downloadly.ir.deb


# log directory
RUN mkdir -p /var/log/final-judgment


#################################### install final_judgment ########################### 

WORKDIR /home
ADD ./requirements.txt ./requirements.txt
ENV PIP_NO_CACHE_DIR 1
RUN pip install -r ./requirements.txt
ADD ./src ./src

#################################### install match holder #############################

# download server jar file
RUN mkdir -p /usr/local/match && \

curl -s https://github.com/SharifAIChallenge/AIC22-Server/releases/publish | grep -Eo "SharifAIChallenge/AIC22-Server/releases/download/publish/.*-([0-9]\.)*jar" | awk '{ print "curl -Ls https://github.com/"$0, "-o /usr/local/match/match.jar"}'  | bash

# download server configfile
# RUN curl "https://raw.githubusercontent.com/SharifAIChallenge/final-judgment/master/resources/map.config" > /usr/local/match/map.config

# install match 
COPY scripts/match.sh /usr/bin/match
RUN chmod +x /usr/bin/match
################################### install spawn #####################################
COPY scripts/spawn.sh /usr/bin/spawn
COPY scripts/spawn1.sh /usr/bin/spawn1
COPY scripts/spawn2.sh /usr/bin/spawn2

RUN chmod +x /usr/bin/spawn && mkdir -p /etc/spawn && \
chmod +x /usr/bin/spawn1 && \
chmod +x /usr/bin/spawn2 

WORKDIR /home/src

CMD ["python3", "main.py"]
