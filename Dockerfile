# FROM reg.aichallenge.ir/aic/infra/final_judgment :486-b2af3cf0  
FROM reg.aichallenge.ir/python:3.8 
RUN apt update && apt install software-properties-common -y && apt update
RUN  add-apt-repository ppa:webupd8team/java -y && apt-get update && \
apt install -y default-jre vim curl gettext


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
