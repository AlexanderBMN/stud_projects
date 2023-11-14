class Map:
    def __init__(self, map_message):
        self.intersection_id = map_message[map_message.highest_layer].dsrc_id
        self.revision = map_message[map_message.highest_layer].dsrc_revision
        self.ref_lat = map_message[map_message.highest_layer].dsrc_lat
        self.ref_lon = map_message[map_message.highest_layer].dsrc_long
        self.lanecount = map_message[map_message.highest_layer].dsrc_laneset
        # Informationen zu Lanes auslesen:
        self.lane_dict = {}
        count = 0
        for i in range(0, self.lanecount - 1):
            node_dict = {}

            for k in range(count, count + int(
                    str(map_message[map_message.highest_layer].dsrc_nodes.all_fields[i]).split(":")[1].split(">")[0])):
                node_dict[k] = (
                    int(str(map_message[map_message.highest_layer].dsrc_x.all_fields[k]).split(":")[1].split(">")[0]),
                    int(str(map_message[map_message.highest_layer].dsrc_y.all_fields[k]).split(":")[1].split(">")[0]))

            # lane dict [Nummer der Lane] = [SG-Nummer, Node-Dicts, Connects to, Maneuver]
            self.lane_dict[i] = [int(
                str(map_message[map_message.highest_layer].dsrc_signalgroup.all_fields[i]).split(":")[1].split(">")[0]),
                                 node_dict,
                                 int(str(map_message[map_message.highest_layer].dsrc_lane.all_fields[i]).split(":")[
                                         1].split(">")[0]),
                                 int(str(map_message[map_message.highest_layer].dsrc_maneuver.all_fields[i]).split(":")[
                                         1].split(">")[0])]

    def update(self, map_message):
        self.revision = map_message[map_message.highest_layer].dsrc_revision
        self.ref_lat = map_message[map_message.highest_layer].dsrc_lat
        self.ref_lon = map_message[map_message.highest_layer].dsrc_long
