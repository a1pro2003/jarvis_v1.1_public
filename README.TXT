##THIS are all the extra steps you need to take

#Install this before running 'requirements.txt'

1. sudo apt-get install libffi-dev
2. sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev$


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



