# Search engine with Hadoop


#ifconfig
sudo apt install net-tools

sudo apt-get update
sudo apt-get install openjdk-8-jdk
sudo apt install openjdk-8-jdk-headless
sudo apt install openjdk-8-jre-headless


#------------dowload hadoop 3.3.1
https://hadoop.apache.org/releases.html
tar -xzvf hadoop-3.1.1.tar.gz
sudo mv hadoop-3.1.1 /usr/local/hadoop


#instal ifcfig
sudo apt install net-tools

IP list:
master: 192.168.254.134 master
slave1: 192.168.254.133 slave1
slave2: 192.168.254.136 slave2
# hacer ping todos contra todos

notas en sudo gedit /etc/hosts----------

en cada mv asignar en nombre master o slave1,2

sudo gedit /etc/hostname --->master

copiar en sudo gedit /etc/hosts

192.168.254.134 master
192.168.254.133 slave1
192.168.254.136 slave2

#######RESTART############

ping slave1 & slave2

# error puertopinstalado en ssh
sudo apt install openssh-server
sudo apt list --installed | grep openssh-server

# en 
 sudo gedit /etc/environment 


PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/hadoop/bin:/usr/local/hadoop/sbin"
JAVA_HOME="/usr/lib/jvm/java-8-openjdk/amd64"

javac --version

readlink -f /usr/bin/java | sed "s:bin/java::"



#-------NEXT
user root
# adduser hadoop
# usermod -aG hadoop hadoop
# chown hadoop:root -R /usr/local/hadoop
# chmod g+rwx -R /usr/local/hadoop

# su - hadoop
$ ssh-copy-id hadoop@master
$ ssh-copy-id hadoop@slave1
$ ssh-copy-id hadoop@slave2


abrir 
sudo gedit /usr/local/hadoop/etc/hadoop/core-site.xml 


<configuration>
  <property>
    <name>fs.default.name</name>
    <value>hdfs://master:9000</value>
  </property>
</configuration>

NEXT<nano editor que quieras>

nano  /usr/local/hadoop/etc/hadoop/hdfs-site.xml



/usr/local/hadoop/etc/hadoop/workers

|
java
/usr/lib/jvm/java-8-openjdk-amd64/jre/


export HADOOP_HOME="/usr/local/hadoop"
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_YARN_HOME=$HADOOP_HOME


nvim /usr/local/hadoop/etc/hadoop/yarn-site.xml



http://192.168.254.134:9870

http://192.168.254.134:8088/cluster


// correr un programa

en usuario hadoop

export HADOOP_CLASSPATH=$(hadoop classpath)
echo $HADOOP_CLASSPATH

start-dfs.sh
start-yarn.sf

hadoop fs -mkdir /inverindex
hadoop fs -mkdir /inverindex/input

##revisa en GUI web si se crearon los directorios


hadoop fs -put '/home/master/Desktop/WordCountTutorial/Input_data/input.txt' /WordCountTutorial/Input

cd /home/master/Desktop/WordCountTutorial/

cd /home/master/Desktop/

javac InvertIndex.java -cp $(hadoop classpath) -d '/home/master/Desktop/WordCountTutorial/tutorial_classes' 


jar -cvf firstTutorial.jar -C tutorial_classes/ .


hadoop jar '/home/master/Desktop/WordCountTutorial/firstTutorial.jar' WordCount /WordCountTutorial/Input /WordCountTutorial/Output

##############################################
hadoop jar '/home/master/Desktop/inverindex/firstTutorial.jar' InvertIndexApp /inverindex/input /inverindex/output

######################################
hadoop fs -rmdir /inverindex/output


hadoop dfs -cat /WordCountTutorial/Output/*


hadoop dfs -cat /inverindex/input/file1.txt

# gugul 
echo "you? you,now" | python mapper.py | sort | python reducer.py
cat input.txt | python mapper.py | sort | python reducer.py



/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar



echo "******************** Calculating inverted index ********************"
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
        -file mapper.py \
        -mapper "python mapper.py" \
        -file reducer.py  \
        -reducer "python reducer.py" \
        -input /input/ \
        -output /output


echo "******************** Download results ********************"
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
               -Dmapred.reduce.tasks=1 \
               -input /output/ \
               -output /result \
               -mapper cat \
               -reducer cat

hdfs dfs -get /result/part-00000

echo "******************** Creating folder and upload files for pagerank ********************"
hdfs dfs -mkdir /input2
hdfs dfs -put pagerank.txt /input2


echo "******************** Calculating pagerank ********************"
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
        -file pagerank_mapper.py \
        -mapper "python pagerank_mapper.py" \
        -file pagerank_reducer.py  \
        -reducer "python pagerank_reducer.py" \
        -input /input2/ \
        -output /output2

echo "******************** Download results ********************"
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
               -Dmapred.reduce.tasks=1 \
               -input /output2/ \
               -output /result2 \
               -mapper cat \
               -reducer cat


echo "******************** Calculating pagerank ********************"
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
        -file rank_map.py \
        -mapper "python rank_map.py" \
        -input /result2/part-00000 \
        -output /output3


echo "******************** Download results ********************"
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
               -Dmapred.reduce.tasks=1 \
               -input /output2/ \
               -output /result2 \
               -mapper cat \
               -reducer cat

echo "******************** Calculating pagerank ********************"
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
        -file rank_map.py \
        -mapper "python rank_map.py" \
        -input /result2/part-00000 \
        -output /output3


hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
               -Dmapred.reduce.tasks=1 \
               -input /output3/ \
               -output /result3 \
               -mapper cat \
               -reducer cat
~~~
wget http://mirror.cogentco.com/pub/apache/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz

tar -xzvf hadoop-3.3.1.tar.gz
cd hadoop-3.3.1/share/hadoop/tools/lib/

~~~
~~~
crear carpetas
hdfs dfsadmin -safemode leave
hadoop fs -mkdir /input
~~~

 ~~~
 dubir archivos
 hadoop fs -put *.txt /
 ~~~
 
 
