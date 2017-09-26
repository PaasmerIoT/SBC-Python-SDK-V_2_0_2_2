#/bin/bash
touch output.txt
path=`pwd`


sudo timeout 2s stdbuf -oL hcitool lescan | grep $1 > $path/output.txt


out=$(sudo cat $path/output.txt | grep $1 | awk '{print $1}')
if [ "$out" ]
then
        #printf $out
        for word in $out
        do
                echo $word
        done
fi

sudo hciconfig hci0 down
sudo hciconfig hci0 up
sudo rm output.txt
~
~

