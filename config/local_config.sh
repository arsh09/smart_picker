export GREEN_LED=9
export GREEN_BTN=11
export RED_LED=19
export RED_BTN=26
export BLUE_LED=20
export BLUE_BTN=16


# GPSD is a service that connects 
# to model serial port, sends AT commands 
# to get GPS data and then opens a websocket 
# so multiple applications can access the properly 
# formatted GPS data. If True, application uses 
# GPSD service otherwise we use MODEM_SERIAL_PORT 
# and use serial port to get GPS data directly. 
export USE_GPSD=True
export MODEM_SERIAL_PORT="/dev/ttyUSB2"

export USERNAME="picker02-device1"

# Using HTTPS and WSS cause problems due to
# insufficient SSL encryption on server.
export SITE_ADDRESS="http://18.8.0.18:8127"
export WS_ADDRESS="ws://18.8.0.18:8128"

