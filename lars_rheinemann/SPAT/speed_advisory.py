import math


def round_speed(speed, interval):
    return interval * round(speed/interval)


def kmh_in_ms(speed):
    return speed / 3.6


def ms_in_kmh(speed):
    return speed * 3.6


def acc_time_needed(max_speed, distance, a):
    way_to_max_speed = 0.5 * ((kmh_in_ms(max_speed) ** 2) / a)
    if way_to_max_speed > distance:
        return math.sqrt((2 * distance) / a)
    else:
        return math.sqrt((2 * way_to_max_speed) / a) + (distance - way_to_max_speed) / kmh_in_ms(max_speed)


def speed_advisory(status, distance, time_left, ttc_gap, max_speed, min_speed):
    # Return = 0: keine Grüne Welle möglich
    # Return > 0: Geschwindigkeitsempfehlung
    # Status "Gruen"
    if status == 5 or status == 6:
        # Umschaltung steht kurz bevor
        if time_left <= ttc_gap:
            return 0

        # theoretisch notwendige Mindestgeschwindigkeit, um es noch bei Grün zu schaffen
        min_speed_adv = distance / (time_left - ttc_gap)
        # zu hohe Geschwindigkeit notwendig
        if min_speed_adv > kmh_in_ms(max_speed):
            return 0
        else:
            return max_speed

    elif status == 7 or status == 8:
        return 0

    # Status Rot oder Rot-Gelb:
    elif status == 2 or status == 3 or status == 4:
        max_speed_adv = distance / (time_left + ttc_gap)

        if ms_in_kmh(max_speed_adv) > max_speed:
            return max_speed

        elif ms_in_kmh(max_speed_adv) < min_speed:
            return 0

        else:
            return round_speed(ms_in_kmh(max_speed_adv),5)
    else:
        return 0


def speed_advisory_bus_stop(status, distance, time_left, ttc_gap, max_speed, a):
    # Bus steht, Startzeitpunkt
    time_needed = acc_time_needed(max_speed, distance, a)

    if status == 5 or status == 6:
        if time_needed > time_left - ttc_gap:
            return 0
        else:
            return 1

    elif status == 7 or status == 8:
        return 0

    # Status Rot oder Rot-Gelb:
    elif status == 2 or status == 3 or status == 4:
        if time_needed > time_left + ttc_gap:
            return 1
        else:
            return 0
    else:
        return 0
