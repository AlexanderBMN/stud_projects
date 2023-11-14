import ctypes
import os
import queue
import socket
import threading
import tkinter as tk
import pyshark
from PIL import ImageTk, Image
import distance_calc
import sg_state
import konstanten
import maps
import speed_advisory
from datetime import datetime
import time

gps_queue = queue.LifoQueue()
status_queue = queue.LifoQueue()
spat_queue = queue.LifoQueue()
denm_queue = queue.LifoQueue()


class UdpPackets(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.denm_mode = False
        self.now = time.time()
        self.mode = konstanten.MODE

    def run(self):
        capture = pyshark.LiveCapture(interface=konstanten.INTERFACE)
        print("Start")
        for packet in capture.sniff_continuously():	       
            if "UDP" in str(packet.layers) and "DATA" in str(packet.layers) and int(
                    packet['UDP'].dstport) == konstanten.UDP_PORT_RCV_GPS:
                if len(bytearray.fromhex(packet[3].data).decode().splitlines()) == 4:
                    gps_queue.queue.clear()
                    gps_queue.put(packet)        
                    

            print(packet.layers)
            if "ITS" in str(packet.layers):
                print("its")
                if self.mode:
                    if packet[packet.highest_layer].messageid == konstanten.DENM_MESSAGE:
                        denm_queue.queue.clear()
                        denm_queue.put(packet)
                else:
                    if packet[packet.highest_layer].messageid == konstanten.SPAT_MESSAGE:
                        spat_queue.queue.clear()
                        spat_queue.put(packet)
                    elif packet[packet.highest_layer].messageid == konstanten.MAP_MESSAGE:
                        manage_maps(packet)

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for thread_id, thread in threading._active.items():
            if thread is self:
                return thread_id

    def stop_exception(self):
        thread_id = self.get_id()
        print("UDP Thread beenden....")
        exce = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if exce > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Fehler beim Beenden')


class UdpSending(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.status_bus = konstanten.MSG_BUS_OFF
        self.status_denm = konstanten.MSG_DENM_OFF
        self.status = 0


class Gui(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.mode = konstanten.MODE
        self.lat = 0
        self.lon = 0

        root.attributes('-fullscreen', True)
        root.wm_title("Test-Application")
        root.config(background="#FFFFFF")

        window = tk.Frame(root)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=4)
        root.rowconfigure(2, weight=1)

        root.columnconfigure(0, weight=1, uniform="fred")
        root.columnconfigure(1, weight=3, uniform="fred")
        root.columnconfigure(2, weight=1, uniform="fred")

        window.grid(row=0, column=0, sticky="news")
        window.config(background="#FFFFFF")
        grid = tk.Frame(window)
        grid.grid(sticky="news", column=2, row=2, columnspan=1)

        btn_exit = tk.Button(root, text="X", command=lambda: exit_func(udp_thread))
        btn_exit.grid(column=2, row=0, sticky="ne")

        self.gps_text = tk.StringVar()
        self.gps_text.set("Warten auf GPS-Position")
        self.gps_label = tk.Label(root, textvariable=self.gps_text)
        self.gps_label.grid(column=0, row=0)

        self.dist_text = tk.StringVar()
        self.dist_text.set("")
        self.dist_label = tk.Label(root, textvariable=self.dist_text)
        self.dist_label.grid(column=1, row=0)

        self.info_text = tk.StringVar()
        self.info_text.set("Warten auf LSA-Nachricht")
        self.info_label = tk.Label(root, textvariable=self.info_text)
        self.info_label.grid(column=1, row=2)

        img_startup = Image.open("ameise.png")
        startup = ImageTk.PhotoImage(img_startup)
        self.img_label = tk.Label(root, image=startup)
        self.img_label.image = startup
        self.img_label.grid(column=1, row=1)

        self.perm_label = tk.Label(root)
        self.perm_label.grid(column=2, row=1)

        # LSA-Images
        self.img_red = Image.open("red.png").resize((200, 320))
        self.red = ImageTk.PhotoImage(self.img_red)

        self.img_ylw = Image.open("ylw.png").resize((200, 320))
        self.ylw = ImageTk.PhotoImage(self.img_ylw)

        self.img_grn = Image.open("grn.png").resize((200, 320))
        self.grn = ImageTk.PhotoImage(self.img_grn)

        self.img_busstop = Image.open("bus.png").resize((200, 320))
        self.busstop = ImageTk.PhotoImage(self.img_busstop)

        self.img_perm = Image.open("Permissiv.jpg").resize((100, 100))
        self.perm = ImageTk.PhotoImage(self.img_perm)

        self.img_gw = Image.open("gw.png").resize((100, 100))
        self.gw = ImageTk.PhotoImage(self.img_gw)

        self.img_no_gw = Image.open("no_gw.png").resize((100, 100))
        self.no_gw = ImageTk.PhotoImage(self.img_no_gw)

        gui_thread = threading.Thread(target=self.update_gui, daemon=True)
        gui_thread.start()

        gps_thread = threading.Thread(target=self.update_gps, daemon=True)
        gps_thread.start()

    def update_gps(self):
        while True:
            self.lat, self.lon = get_pos()
            if self.lat != 0:
                self.gps_text.set(
                    "Position Lateral: " + str(self.lat / 1000000) + " Longitudinal: " + str(self.lon / 1000000))

    def update_gui(self):
        ttc, active, msg_age, distance, cause_code, sub_cause_code, distance_old = 0, 0, 0, 0, 0, 0, 0
        state = "Initial"
        approaching = 0
        while True:

            if self.mode:
                active, msg_age, distance, cause_code, sub_cause_code = get_denm(self.lat, self.lon)
                if active == 0:
                    self.info_text.set("")
                    self.info_label.configure(image="")

            else:
                distance_old = distance
                state, ttc, closest_map, distance = get_spat(self.lat, self.lon)

            if active == 1 and msg_age < konstanten.MAX_AGE_DENM:
                if cause_code == konstanten.STATIONARY_VEHICLE:
                    if sub_cause_code == konstanten.PUBLIC_TRANSPORT_STOP:
                        # Bushaltestelle voraus
                        self.info_text.set("Achtung, Bushalt voraus!")
                        self.info_label.configure(image=self.busstop)
                    else:
                        # unbekannter SubCauseCode, aber Stationary Vehicle
                        self.info_text.set("Achtung, stehendes Fahrzeug!")
                        self.info_label.configure(image="")
                else:
                    self.info_text.set("DENM mit Cause Code: " + str(cause_code) + " und Sub Cause Code: " + str(
                        sub_cause_code) + "empfangen")
                    self.info_label.configure(image="")

            elif state != "Initial":
                if distance_old >= distance:
                    # Annäherung an Kreuzung oder Bus-Stop
                    approaching = time.time()
                    state_etsi = sg_state.encode(state)
                    if state_etsi == 2:
                        ttc_adv = ttc + konstanten.ROT_GELB_ZEIT
                    else:
                        ttc_adv = ttc

                    speed = speed_advisory.speed_advisory(state_etsi, distance, ttc_adv, konstanten.TTC_GAP,
                                                          konstanten.MAX_SPEED, konstanten.MIN_SPEED)

                    if speed <= 0:
                        self.dist_text.set("Keine Grüne Welle möglich")
                        self.perm_label.configure(image=self.no_gw)
                    else:
                        self.dist_text.set("Geschwindigkeitsempfehlung: " + str(round(speed)) + " km/h")
                        self.perm_label.configure(image=self.gw)
                else:
                    # Keine Annäherung
                    if time.time() - approaching > 5:
                        self.dist_text.set("")
                        self.perm_label.configure(image="")

                if state == "Rot":
                    if ttc > konstanten.SMALLEST_GREEN_TIME:
                        self.info_text.set("Freigabe in " + str(int(ttc) + konstanten.ROT_GELB_ZEIT) + " Sekunden ")
                        self.img_label.configure(image=self.red)
                    else:
                        self.info_text.set("Freigabe steht kurz bevor")
                        self.img_label.configure(image=self.red)
                elif state == "Gelb":
                    self.info_text.set("Achtung, Freigabe-Ende!")
                    self.img_label.configure(image=self.ylw)
                elif state == "Gruen":
                    self.info_text.set("Lichtsignalanlage ist noch " + str(ttc) + " Sekunden Grün")
                    self.img_label.configure(image=self.grn)
                elif state == "Rot/Gelb":
                    self.info_text.set("Freigabe steht kurz bevor")
                    self.img_label.configure(image=self.red)


def timestamp_utc2004():
    # aktuellen UTC-Zeitstempel auf UTC Start 2004 umrechnen
    # alle Zeitstempel beziehen sich auf den 01.01.2004 00:00:00 (ETSI TS 102 894-2) in Millisekunden
    utc2004 = datetime.strptime('1.1.2004 00:00:00,00', '%d.%m.%Y %H:%M:%S,%f').timestamp() * 1000
    return datetime.utcnow().timestamp() * 1000 - utc2004


def get_pos():
    try:
        packet = gps_queue.get(block=True, timeout=3)

    except queue.Empty:
        lat, lon = 0, 0
        return lat, lon

    else:
        lat_degree = float(bytearray.fromhex(packet[3].data).decode().splitlines()[1].split(",")[2]) / 100
        lat = int((((lat_degree - int(lat_degree)) / 60 * 100) + int(lat_degree)) * 10 ** 6)

        lon_degree = float(bytearray.fromhex(packet[3].data).decode().splitlines()[1].split(",")[4]) / 100
        lon = int((((lon_degree - int(lon_degree)) / 60 * 100) + int(lon_degree)) * 10 ** 6)

    return lat, lon


def get_spat(lat, lon):
    try:
        packet = spat_queue.get(block=True, timeout=1.5)

    except queue.Empty:
        ttc = 0
        state = "Initial"
        closest_map = 0
        distance = 0
        return state, ttc, closest_map, distance

    else:
        # lat, lon = get_pos()
        closest_map, distance = get_closest_map(lat, lon)
        if closest_map == 0:
            state = "Initial"
            ttc, distance = 0, 0
            return state, ttc, closest_map, distance
        if map_dict[closest_map].intersection_id == packet[packet.highest_layer].dsrc_id:
            # MAP-File passt zu SPATEM
            state = sg_state.decode(packet[packet.highest_layer].dsrc_eventstate[0])
            ttc = int(packet[packet.highest_layer].dsrc_minEndTime)
            return state, ttc, closest_map, distance


def get_denm(lat, lon):
    try:
        packet = denm_queue.get(block=True, timeout=0.5)

    except queue.Empty:
        active = 0
        msg_age = 0
        distance = 0
        cause_code = 999
        sub_cause_code = 999

    else:
        msg_age = packet[packet.highest_layer].dsrc_detectiontime * 1000 - timestamp_utc2004()
        if msg_age < konstanten.MAX_AGE_DENM:
            active = 1
        else:
            active = 0
        # lat, lon = get_pos()
        distance = distance_calc.lat_lon_cmp(packet[packet.highest_layer].dsrc_latitude,
                                             packet[packet.highest_layer].dsrc_longitude, lat, lon)

        cause_code = sg_state.decode(packet[packet.highest_layer].dsrc_causecode[0])
        sub_cause_code = int(packet[packet.highest_layer].dsrc_subcausecode)

    return active, msg_age, distance, cause_code, sub_cause_code


def manage_maps(message):
    if message[message.highest_layer].dsrc_id in map_dict:
        if map_dict[message[message.highest_layer].dsrc_id].revision != message[message.highest_layer].dsrc_revision:
            # Neue Revision der gleichen Map, Daten updaten
            map_dict[message[message.highest_layer].dsrc_id].update(message)

    else:
        map_dict[message[message.highest_layer].dsrc_id] = maps.Map(message)
        print("map added")
        print(map_dict)

    if len(map_dict) > konstanten.MAXIMUM_MAPS:
        # TODO MAP die am längsten entfernt ist löschen
        print("To many maps")


def get_closest_map(lat, lon):
    distance = 99999999
    closest_key = 0
    for key in map_dict:
        distance_new = distance_calc.lat_lon_cmp(map_dict[key].ref_lat, map_dict[key].ref_lon, lat / 1000000,
                                                 lon / 1000000)
        if distance_new < distance:
            distance = distance_new
            closest_key = key
    return closest_key, distance


def exit_func(thread):
    thread.stop_exception()
    root.destroy()


if __name__ == "__main__":
    if os.environ.get('DISPLAY', '') == '':
        os.environ.__setitem__('DISPLAY', ':0.0')

    denm_lock = threading.Lock()
    root = tk.Tk()
    Gui(root)
    map_dict = {}

    udp_thread = UdpPackets('UDP')
    udp_thread.start()

    send_thread = UdpSending('SendData')
    send_thread.daemon = True
    send_thread.start()

    root.mainloop()
