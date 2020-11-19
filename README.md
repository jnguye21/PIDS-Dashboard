# Personal ID System Exclusively Using Cisco Meraki Dashboard API
Tailored for Bluetooth

## Global Variables
After replacing appropriate **&lt;variables&gt;**, enter the following into the terminal: 

    echo 'export MERAKI_DASHBOARD_API_KEY=<KEY>' >> ~/.bashrc

    echo 'export MERAKI_URL_BT=https://api.meraki.com/api/v1/networks/<NETWORK ID>/bluetoothClients?perPage=20' >> ~/.bashrc

    echo 'export MERAKI_URL_WIFI=https://api.meraki.com/api/v1/networks/<NETWORK ID>/clients/' >> ~/.bashrc

    echo 'export MERAKI_URL_AP=https://api.meraki.com/api/v1/networks/<NETWORK ID>/devices' >> ~/.bashrc

    echo 'export TEAMS_WEBHOOK_URL=<WEBHOOK URL>' >> ~/.bashrc

**Restart code editor after entering all lines


## Setup 
###### Courtesy of Alex Hoecht
1) Project App
    1) Create a Virtual Environment: $python3 -m venv venv
    2) Activate Virtual Environment: $source venv/bin/activate
    3) Install requirements: (venv)$pip install -r requirements.txt
    
2.) From Virtual Environment (created in Setup)
    1) python3 main.py
