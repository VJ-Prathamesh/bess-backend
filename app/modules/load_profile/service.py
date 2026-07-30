from .calculation import (

    calculate_daily_energy,

    calculate_peak_load,

    calculate_average_load,

    calculate_load_factor

)



load_summary = {}



def calculate_load_profile(data):


    hourly_loads = data.hourly_loads


    total_energy = calculate_daily_energy(
        hourly_loads
    )


    peak_load = calculate_peak_load(
        hourly_loads
    )


    average_load = calculate_average_load(
        total_energy
    )


    load_factor = calculate_load_factor(
        average_load,
        peak_load
    )


    global load_summary


    load_summary = {


        "total_daily_energy_kwh":
        round(total_energy,2),



        "peak_load_kw":
        round(peak_load,2),



        "average_load_kw":
        round(average_load,2),



        "load_factor_percent":
        round(load_factor*100,2),



        "battery_autonomy_days":
        data.battery_autonomy_days

    }


    return load_summary




def get_load_summary():

    return load_summary