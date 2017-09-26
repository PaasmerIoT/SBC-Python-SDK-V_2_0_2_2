if [ -f ../../config.py ] ; then
       out=$(sudo cat ../../config.py | grep "bluetoothDiscover" | awk '{print $3}')
       echo $out

       if [ $out = 1 ] ; then
		if [ -d "firstrunBLE" ] ; then
			firstrun=1
			echo "BLE Libraries are already installed"
		else
			echo "Installing dependencies for BLE Protocol Support.... This May take some time"
			if [ -f /etc/debian_version ] ; then
				sudo apt-get install -y libglib2.0-dev
				sudo pip3 install  magicblue
				sudo pip install enum
				sudo pip install  magicblue
				sudo apt-get install -y libcap2-bin
				sudo setcap 'cap_net_raw,cap_net_admin+eip' `which hcitool`
	
			elif [ -f /etc/fedora_version ] ; then
				echo "it is fedora"
				sudo dnf install -y glib2-devel
				sudo pip3 install -y magicblue
				sudo dnf install -y libcap
				sudo setcap 'cap_net_raw,cap_net_admin+eip' `which hcitool`
			
			fi
			sudo mkdir firstrunBLE
			sudo chmod 777 firstrunBLE
		fi
                echo "Discovering Nearby BLE devices"
       else
               echo "BLE devie Discovey is not selected by the User"
       fi
else
       echo "The Config File doesn't have Wifi Access"
fi

