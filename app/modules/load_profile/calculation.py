def calculate_daily_energy(hourly_loads):

    return sum(hourly_loads)



def calculate_peak_load(hourly_loads):

    return max(hourly_loads)



def calculate_average_load(total_energy):

    return total_energy / 24



def calculate_load_factor(
        average_load,
        peak_load
):

    if peak_load == 0:
        return 0

    return average_load / peak_load