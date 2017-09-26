#!/bin/sh
# Detects which OS and if it is Linux then it will detect which Linux
# Distribution.

echo " Installing the Board Requirements and Packages"
echo "Please wait....."

path=`pwd`
OS=`uname -s`
REV=`uname -r`
MACH=`uname -m`
board=`uname -a`
echo "import sys" >  $path/samples/basicPubSub/path.py
echo "sys.path.append('$path/')" >>  $path/samples/basicPubSub/path.py
echo "path = \"$path/\"" >> $path/samples/basicPubSub/path.py
GetVersionFromFile()
{
    VERSION=`cat $1 | tr "\n" ' ' | sed s/.*VERSION.*=\ // `
}
echo ${OS}
echo ${board}
#cd '/external_libs/mbedTLS/'
#cd ../../
if [ "${OS}" = "SunOS" ] ; then
    OS=Solaris
    ARCH=`uname -p` 
    OSSTR="${OS} ${REV}(${ARCH} `uname -v`)"

elif [ "${OS}" = "AIX" ] ; then
    OSSTR="${OS} `oslevel` (`oslevel -r`)"
elif [ "${OS}" = "Darwin" ] ; then
    OSSTR="${OS} ${DIST} ${REV}(${PSUEDONAME} ${KERNEL} ${MACH})"

elif [ "${OS}" = "Linux" ] ; then
    KERNEL=`uname -r`
    if [ -f /etc/redhat-release ] ; then
        DIST='RedHat'
        PSUEDONAME=`cat /etc/redhat-release | sed s/.*\(// | sed s/\)//`
        REV=`cat /etc/redhat-release | sed s/.*release\ // | sed s/\ .*//`
        sudo yum update
        sudo yum install -y python2.7 libssl-dev python-pip
        sudo yum install -y python-dev
        sudo yum install -y xterm
        sudo yum install -y expect
        sudo yum install -y mysql-client-core-5.7
	sudo yum install -y mysql-client
	sudo yum install -y uuid

    elif [ -f /etc/SuSE-release ] ; then
        DIST=`cat /etc/SuSE-release | tr "\n" ' '| sed s/VERSION.*//`
        REV=`cat /etc/SuSE-release | tr "\n" ' ' | sed s/.*=\ //`
        sudo zypper update
        sudo zypper install -y python2.7 libssl-dev python-pip
        sudo zypper install -y python-dev
        sudo zypper install -y xterm
        sudo zypper install -y expect
        sudo zypper install -y mysql-client-core-5.7
	sudo zypper install -y mysql-client
	sudo zypper install -y uuid
    elif [ -f /etc/mandrake-release ] ; then
        DIST='Mandrake'
        PSUEDONAME=`cat /etc/mandrake-release | sed s/.*\(// | sed s/\)//`
        REV=`cat /etc/mandrake-release | sed s/.*release\ // | sed s/\ .*//`
    elif [ -f /etc/debian_version ] ; then
        DIST="Debian `cat /etc/debian_version`"
        REV=""
        sudo apt-get update
		sudo apt-get install -y python2.7 libssl-dev python-pip
        sudo apt-get install -y python-dev
        sudo apt-get install -y xterm
        sudo apt-get install -y expect
        sudo apt-get install -y mysql-client-core-5.7
	sudo apt-get install -y mysql-client
	sudo apt-get install -y uuid
	sudo apt-get install -y libglib2.0-dev
	sudo pip3 install  magicblue
	sudo pip install enum
	sudo pip install  magicblue
	sudo apt-get install -y libcap2-bin
	sudo setcap 'cap_net_raw,cap_net_admin+eip' `which hcitool`

    elif [ -f /etc/lsb_version ] ; then
        DIST="ubuntu or Linux mint `cat /etc/lsb_version`"
        REV=""
        sudo apt-get update
        sudo apt-get install -y python2.7 libssl-dev python-pip
        sudo apt-get install -y python-dev
        sudo apt-get install -y xterm
        sudo apt-get install -y expect
        sudo apt-get install -y mysql-client-core-5.7
	sudo apt-get install -y mysql-client
	sudo apt-get install -y uuid
	sudo apt-get install -y libglib2.0-dev
	sudo pip3 install  magicblue
	sudo pip install enum
	sudo pip install  magicblue
	sudo apt-get install -y libcap2-bin
	sudo setcap 'cap_net_raw,cap_net_admin+eip' `which hcitool`
	
    elif [ -f /etc/fedora_version ] ; then
        DIST="fedora `cat /etc/lsb_version`"
        REV=""
        sudo dnf update
        sudo dnf install -y python2.7 libssl-dev python-pip
        sudo dnf install -y python-dev
        sudo dnf install -y xterm
        sudo dnf install -y expect
        sudo dnf install -y mysql-client-core-5.7
	sudo dnf install -y mysql-client
	sudo dnf install -y uuid
	sudo dnf install -y glib2-devel
	sudo pip3 install -y magicblue
	sudo dnf install -y libcap
	sudo setcap 'cap_net_raw,cap_net_admin+eip' `which hcitool`

    elif [ -f /etc/gentoo_version ] ; then
        DIST="gentoo `cat /etc/lsb_version`"
        REV=""
        sudo dnf update
        sudo dnf install -y python2.7 libssl-dev python-pip
        sudo dnf install -y python-dev
        sudo dnf install -y xterm
        sudo dnf install -y expect
        sudo dnf install -y mysql-client-core-5.7
	sudo dnf install -y mysql-client
	sudo dnf install -y uuid
    fi
    if [ -f /etc/UnitedLinux-release ] ; then
        DIST="${DIST}[`cat /etc/UnitedLinux-release | tr "\n" ' ' | sed s/VERSION.*//`]"
    fi

    OSSTR="${OS} ${DIST} ${REV}(${PSUEDONAME} ${KERNEL} ${MACH})"

fi

mac=$(ifconfig | grep 'HWaddr' |awk '{print $5}' | head -n 1)
echo "#define MAC \"$mac\"" > $path/samples/basicPubSub/mac.h

echo ${OSSTR}
echo ${board}
echo ${board} | awk '{print $2}'
xv=$(echo ${board} | awk '{print $2}')
echo "deviceType = \"$xv\"" > $path/samples/basicPubSub/deviceType.py
#wget -O ./certs/rootCA.crt https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem
echo $xv
if [ $xv = "raspberrypi" ] || [ $xv = "bananapi" ] || [ $xv = "orangepi" ] || [ $xv = "odroidxu4" ] ; then
   echo 'SBC Board Rpi,BPi,OPi, Odroid etc...'
else if [ $xv = "beaglebone" ] ; then
   #sudo apt-get install build-essential python-setuptools python-smbus
   echo 'Beagle Bone Board'

else
   echo 'Unknown or Local system'
fi
fi

