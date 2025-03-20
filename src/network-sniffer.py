import time
import os
import threading
import scapy.all as scapy
import asciichartpy as acp
from rich import print
from rich import box
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
from rich.table import Table
import keyboard as kb
import collections

default_config = {"graph_width": 100, "panel_border": "#d600ff"}
exit_script = False
packet_counts = {"incoming": 0, "outgoing": 0}
last_10_packets = collections.deque(maxlen=10) 

MAX_PACKETS = 20
packet_buffer_in = collections.deque(maxlen=MAX_PACKETS)
packet_buffer_out = collections.deque(maxlen=MAX_PACKETS)

MONITORED_HOSTS = []

def packet_sniffer(packet):
    global packet_counts, last_10_packets

    if packet.haslayer(scapy.IP):
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst

        if not MONITORED_HOSTS or (src_ip in MONITORED_HOSTS and dst_ip in MONITORED_HOSTS):
            packet_info = {"src": src_ip, "dst": dst_ip}
            last_10_packets.append(packet_info)

            if dst_ip == scapy.get_if_addr("Ethernet"): # Interface de rede monitorada
                packet_counts["incoming"] += 1
            else:
                packet_counts["outgoing"] += 1

def start_sniffing():
    scapy.sniff(prn=packet_sniffer, store=False, iface="Ethernet") # Interface de rede monitorada

def discover_devices():
    devices = []
    arp_request = scapy.ARP(pdst="192.168.0.1/24")  # Utilize o Gateway da rede
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    for element in answered_list:
        devices.append({"IP": element[1].psrc, "MAC": element[1].hwsrc})
    
    return devices

def create_device_table():
    table = Table(title="Dispositivos na Rede", box=box.ROUNDED, border_style=default_config["panel_border"])
    table.add_column("IP", style="cyan", no_wrap=True)
    table.add_column("MAC", style="magenta", no_wrap=True)

    for device in discover_devices():
        table.add_row(device["IP"], device["MAC"])
    
    return table

def draw_graph_panel(data, graph_name, color):
    acp_config = {
        "width": default_config["graph_width"],
        "format": "{:5.0f} p/s",
    }

    return Panel(
        Align.left(acp.plot(data, acp_config), vertical="bottom"),
        title=f"[bold][yellow]{graph_name}[/bold][/yellow]",
        border_style="#d600ff",
        style=color,
    )

def exit_app():
    global exit_script
    exit_script = True
    os._exit(0)

def user_controls():
    kb.add_hotkey("tab", exit_app)

def create_packet_info_panel():
    panel_content = "\n".join(
        [f"[bold][yellow]Origem:[/bold][/yellow] {packet['src']} - [bold][yellow]Destino:[/bold][/yellow] {packet['dst']}" 
         for packet in last_10_packets]
    )
    
    return Panel(
        Align.center(panel_content),
        border_style=default_config["panel_border"],
        title="[bold][yellow]Últimos 10 Pacotes[/bold][/yellow]",
    )

def main():
    global exit_script, packet_buffer_in, packet_buffer_out, last_10_packets

    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3),
    )
    layout["main"].split_row(Layout(name="info", ratio=2), Layout(name="graphs", ratio=3))
    layout["graphs"].split_column(Layout(name="recv_graph"), Layout(name="sent_graph"))
    layout["info"].split(Layout(name="net_usage", size=3), Layout(name="devices_table", ratio=1), Layout(name="packet_info", ratio=1))

    layout["header"].update(
        Panel(
            Align.center("[bold][yellow] Monitoramento de Rede [/yellow][/bold]"),
            border_style=default_config["panel_border"],
        )
    )
    layout["footer"].update(
        Panel(
            Align.left("[bold][yellow]Tab para Sair[/yellow][/bold]"),
            title="Controles",
            border_style=default_config["panel_border"],
        )
    )

    user_controls()

    sniff_thread = threading.Thread(target=start_sniffing, daemon=True)
    sniff_thread.start()

    with Live(layout, refresh_per_second=60, screen=True) as live:
        while not exit_script:
            packet_buffer_in.append(packet_counts["incoming"])
            packet_buffer_out.append(packet_counts["outgoing"])

            packet_counts["incoming"] = 0
            packet_counts["outgoing"] = 0

            layout["recv_graph"].update(
                draw_graph_panel(packet_buffer_in, "Pacotes Recebidos", "#00ff9f")
            )
            layout["sent_graph"].update(
                draw_graph_panel(packet_buffer_out, "Pacotes Enviados", "#00b8ff")
            )
            layout["net_usage"].update(
                Panel(
                    Align.center(
                        f"IN: [bold][green]{packet_buffer_in[-1]}[/green][/bold] p/s OUT: [bold][red]{packet_buffer_out[-1]}[/red][/bold] p/s"
                    ),
                    border_style=default_config["panel_border"],
                    title="[bold][yellow]Tráfego de Rede[/bold][/yellow]",
                )
            )
            layout["devices_table"].update(
                Panel(
                    Align.center(create_device_table()),
                    border_style=default_config["panel_border"],
                    title="[bold][yellow]Dispositivos Conectados[/bold][/yellow]",
                )
            )
            layout["packet_info"].update(create_packet_info_panel())

if __name__ == "__main__":
    # Use essa variável para montorar 2 hosts. Caso seja vazio, monitora a rede inteira.
    # MONITORED_HOSTS = ["52.67.164.66", "192.168.0.2"]
    main()
