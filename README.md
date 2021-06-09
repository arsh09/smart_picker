## Robot-Calling-Sytem

### A Python program for the robot calling device that allows the picker to call and interact with the fruit pallet carrying robots. :strawberry: 

### Raspi Configuration


The configuration files for the Raspberry PI are in the `config` folder. 

- `wvdial.pl`: is for connecting the SIM7600E device to the mobile network and setting up the GNSS connection. 
  For starting the connection automatically at startup copy the files: 
  - `sudo cp config/wvdial.pl /opt/wvdial.pl` and;
  - `cp config/4g.desktop ~/.config/autostart/4g.desktop`.
- `gpsd`: setup for the GPSD daemon. Run `sudo cp config/gpsd /etc/default/gpsd`.
- `launch_car.sh`: is the script that launches the call-a-robot application. For starting it automatically at boot: 
  - `ln -s gpsd_code/main.py $HOME/ex.py` and;
  - `sudo cp config/launch_car.sh /opt/launch_car.sh` and;
  - `cp config/car.desktop ~/.config/autostart/car.desktop`

### Program progress:

- [x] Button interactions
- [x] Display interface
- [x] Satellite navigation  
- [x] WiFi enabled 
- [x] 4G enabled 
- [x] Websocket communication 
