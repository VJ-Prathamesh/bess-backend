from .calculation import (

    calculate_day_energy,

    calculate_night_energy,

    calculate_total_energy,

    calculate_peak_load,

    calculate_day_peak,

    calculate_night_peak

)



design_summary = {}



def calculate_design_assist(data):


    hourly_loads = data.hourly_loads



    daytime_energy = calculate_day_energy(
        hourly_loads
    )


    nighttime_energy = calculate_night_energy(
        hourly_loads
    )


    total_energy = calculate_total_energy(
        hourly_loads
    )


    peak_load = calculate_peak_load(
        hourly_loads
    )


    peak_day = calculate_day_peak(
        hourly_loads
    )


    peak_night = calculate_night_peak(
        hourly_loads
    )



    global design_summary



    design_summary = {


        "daytime_energy_kwh":
        round(daytime_energy,2),


        "nighttime_energy_kwh":
        round(nighttime_energy,2),


        "total_daily_energy_kwh":
        round(total_energy,2),


        "peak_load_kw":
        round(peak_load,2),


        "peak_daytime_load_kw":
        round(peak_day,2),


        "peak_nighttime_load_kw":
        round(peak_night,2),


        "solar_irradiation":
        data.solar_irradiation

    }


    return design_summary




def get_design_summary():

    return design_summary