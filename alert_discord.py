#!/usr/bin/env python3

from discord import Intents, Client
from flask import Flask, request, jsonify
from threading import Thread

app = Flask(__name__)
token = "TOKEN_DISCORD_APPS"

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

def scraping(data):
    container_channel_ID    = "CHANNEL_ID_CONTAINER"
    node_channel_ID         = "CHANNEL_ID_NODE"
    traffic_channel_ID      = "CHANNEL_ID_TRAFFIC"
    nginx_channel_ID        = "CHANNEL_ID_NGINX"
    apache_channel_ID       = "CHANNEL_ID_APACHE"
    db = []
    for list_alert in data['alerts']:
        alertName   = list_alert['labels']['alertname']
        instance    = list_alert['labels']['instance']

        start_time = list_alert['startsAt']
#datetime.datetime.fromisoformat(list_alert['startsAt'])
        waktu = f"{start_time}"

        if instance.split(':')[0].split('.')[-1]   == "10":
            node = 'Node Monitoring'
        elif instance.split(':')[0].split('.')[-1] == "20":
            node = 'Node Client 1'
        elif instance.split(':')[0].split('.')[-1] == "30":
            node = 'Node Client 2'

        tmp_action_needed  = 'Checking {} in {} or {}'
        tmp_node_action_needed = 'Checking {}'

        if 'container' in alertName:
            jumlahContainer = list_alert['labels']['valueService']
            service_name = f'{jumlahContainer} Service Container'
            channel = container_channel_ID
            status = 'Down'
            action_needed = tmp_action_needed.format(service_name, node, instance)
            impact = ' Unavailable container disrupts dependent services, affecting application functionality.'

        elif 'nginx' in alertName:
            service_name = 'Web Server Nginx'
            channel = nginx_channel_ID
            status = 'Down'
            action_needed  = tmp_action_needed.format(service_name, node, instance)
            impact = 'Website or app in Nginx is inaccessible, potentially leading to user loss and degraded customer experience.'


        elif 'apache' in alertName:
            service_name = 'Web Server Apache'
            channel = apache_channel_ID
            status = 'Down'
            action_needed  = tmp_action_needed.format(service_name, node, instance)
            impact = 'Website or app in Apache is inaccessible, potentially leading to user loss and degraded customer experience.'



        elif 'traffic' in alertName:
            service_name = f'Traffic in {node}'
            channel = traffic_channel_ID
            status = 'Warning'
            action_needed = f'Checking {service_name}'
            impact = 'High network traffic may cause slowdowns or latency issues, affecting user experience and server load.'


        elif 'cpu' in alertName:
            service_name = f'CPU Available in {node}'
            channel = node_channel_ID
            cpuUsage = list_alert['labels']['cpuUsage']
            status = "Warning" if cpuUsage > 20 else "Critical"
            action_needed = f'Checking {service_name}'
            impact = 'Low CPU Available may lead to slow performance or timeouts, impacting normal operations.'


        elif 'memory' in alertName:
            service_name = f'Memory Available in {node}'
            channel = node_channel_ID
            memUsage = list_alert['labels']['memUsage']
            status = "Warning" if memUsage > 20 else "Critical"
            action_needed = f'Checking {service_name}'
            
        elif 'disk' in alertName:
            service_name = f'Disk Usage in {node}'
            channel = node_channel_ID
            diskUsage = list_alert['labels']['diskUsage']
            status = "Warning" if diskUsage < 85 else "Critical"
            action_needed = f'Checking {service_name}'
            impact = 'Limited disk space can prevent new data storage, risking system failure if disk becomes full.'


        pesan = f"""
**:warning: WARNING: {service_name} is {status} :warning:**

**Details:**
> **Status:** `{status}`
> **Service:** `{service_name}`
> **Impact:** {impact}

**Action Needed:**
> {action_needed}

**Timestamp:** `{waktu}`
        """
        db.append([channel,pesan])
    return db
#    return [channel, pesan]

@client.event
async def on_ready():
    print(f'{client.user} is running')

async def send_discord(channel, pesan):
    channel = client.get_channel(int(channel))
    await channel.send(pesan)

@app.route('/test', methods=['POST'])
def handle_request():
    data = request.get_json()
    hasil = scraping(data)
#    channel_id,pesan = scraping(data)
    for channel_id, pesan in hasil:
        client.loop.create_task(send_discord(channel_id, pesan))

    response_data = {
        "message": "Data berhasil diterima",
        "received_data": 'aman'
    }

    # Mengembalikan respon JSON
    return jsonify(response_data), 200


@client.event
async def setup_hook():
    # Jalankan server Flask di thread yang berbeda
    Thread(target=lambda: app.run(host='0.0.0.0', port=8081)).start()


if __name__ == '__main__':
    client.run(token=token)
