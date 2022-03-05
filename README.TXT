##THIS are all the extra steps you need to take

#Install this before running 'requirements.txt'

1. sudo apt-get install libffi-dev
2. sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
3. python3 -m pip install --upgrade pip



#Install tenserflow/neuralintents
  1.sudo rm /usr/lib/python3/dist-packages/wrapt-1.10.11.egg-info
  2.pip3 install --upgrade tensorflow==1.14 --no-cache-dir
  3.CONF_SWAPSIZE=1024  #increase number
  4.sudo dphys-swapfile setup  #setup new file
  5.sudo dphys-swapfile swapon  #start newf file
  6.reboot



#Incfrrease swap file
  1.sudo dphys-swapfile swapoff #turnswap off
  2.sudo nano /etc/dphys-swapfile  # edit swap file

#TV Wake-On-Lan
To enable your TV to be powered on via IP command, go to Settings>Connection>Mobile TV On and switch on "Turn on via Wi-Fi."

#Computer Wake-On-Lan
In Bios
Go to 'Bios'>Power Options>Wake On Lan

In computer
Device Manager>Network Adapters(Ethernet Adapter)>Power Management>Allow this device to wake the computer

#To install Spotify on linux
1. curl -sS https://download.spotify.com/debian/pubkey_0D811D58.gpg | sudo apt-key add - 

2. echo "deb http://repository.spotify.com stable non-free" | sudo tee /etc/apt/sources.list.d/spotify.list

3.sudo apt-get update && sudo apt-get install spotify-client



