# Personal ID System Using Dashboard and Location Scanning APIs (For Bluetooth Clients)

## Global Variables
Enter the following into the terminal to avoid hardwired keys/links: 
**Restart VSCode after entering all lines

echo 'export SCANNING_VALIDATOR=99dfc74e4abb542eeb07195a89161d5303da09ab' >> ~/.bashrc

echo 'export MERAKI_DASHBOARD_API_KEY=9b14ebe4396e70c0aa903f0915edabf4794ca47b' >> ~/.bashrc

echo 'export MERAKI_URL_BT=https://api.meraki.com/api/v1/networks/L_634444597505819269/bluetoothClients?perPage=20' >> ~/.bashrc

echo 'export MERAKI_URL_WIFI=https://api.meraki.com/api/v1/networks/L_634444597505819269/clients/' >> ~/.bashrc

echo 'export MERAKI_URL_AP=https://api.meraki.com/api/v1/networks/L_634444597505819269/devices' >> ~/.bashrc

echo 'export TEAMS_WEBHOOK_URL=https://webexapis.com/v1/webhooks/incoming/Y2lzY29zcGFyazovL3VzL1dFQkhPT0svNzgxMWIyNTQtNTZjYS00NTdkLWI0M2MtM2JjOGY0N2U1OTky' >> ~/.bashrc


## Setup
1) Meraki Dashboard
    1) Log into Meraki Dashboard
    2) Navigate to Location Scanning settings (<b>Network-wide -> Configure -> General</b>)
    3) Ensure the Scanning API is enabled
    
2) Localtunnel
    1) Follow quick start instructions here -> https://localtunnel.github.io/www/
    <br><b>NOTE</b>: Once created, keep the Localtunnel session open! It should only be close on shutdown.
    
3) Project App
    1) Create a Virtual Environment: $python3 -m venv venv
    2) Activate Virtual Environment: $source venv/bin/activate
    3) Install requirements: (venv)$pip install -r requirements.txt
    
4) Wire everything together
    1) From the Localtunnel session created
        1) COPY the newly created public url
        2) PASTE the public url into the Meraki Dashboard -> Location Scanning Settings -> POST url
            1) Ensure you also select "Bluetooth" as the Radio Type
    2) From the Meraki Dashboard -> Location Scanning Settings
        1) COPY the validation string
        2) PASTE the validation string into the Project -> app.py -> get_validator()
            1) Paste over the 'HERE'
    
## Run Application
1) From Virtual Environment (created in Setup)
    1) python3 app.py

## Validate
1) From the Meraki Dashboard -> Location Scanning Settings
    1) Click "Verify" to send an inital GET request to test if everything is setup correctly
    2) IF SUCCESSFUL: You will being to see automatic updates on the current network Bluetooth clients being printed
    to the terminal!
    3) BONUS: The script also enables you to easily track WiFi clients in parallel! Give it a try once everything is working :)