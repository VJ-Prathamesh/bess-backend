def calculate_day_energy(hourly_loads):

    # 06:00 to 18:00

    return sum(hourly_loads[6:18])



def calculate_night_energy(hourly_loads):

    # 18:00 to 24:00
    # 00:00 to 06:00

    return sum(hourly_loads[18:24]) + sum(hourly_loads[0:6])



def calculate_total_energy(hourly_loads):

    return sum(hourly_loads)



def calculate_peak_load(hourly_loads):

    return max(hourly_loads)



def calculate_day_peak(hourly_loads):

    return max(hourly_loads[6:18])



def calculate_night_peak(hourly_loads):

    night_loads = (
        hourly_loads[18:24]
        +
        hourly_loads[0:6]
    )

    return max(night_loads)