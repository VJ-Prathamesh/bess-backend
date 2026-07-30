from math import ceil, floor


REFERENCE_TEMPERATURE_C = 25.0


def calculate_array(module: dict, modules_per_string: int, number_of_strings: int) -> dict:
    # Calculates installed PV modules, power, string voltage, and array current.
    total_modules = modules_per_string * number_of_strings
    return {
        "total_modules": total_modules,
        "total_capacity_kwp": total_modules * module["max_power_w"] / 1000,
        "string_vmp_v": modules_per_string * module["vmp_v"],
        "string_voc_v": modules_per_string * module["voc_v"],
        "string_power_kw": modules_per_string * module["max_power_w"] / 1000,
        "total_array_current_a": number_of_strings * module["imp_a"],
    }


def calculate_temperature_voltages(module: dict, modules_per_string: int, min_temperature_c: float, max_temperature_c: float) -> dict:
    # Corrects PV string voltage for the submitted cold and hot site temperatures.
    voc_coefficient = abs(module["temp_coeff_voc_pct_per_c"]) / 100
    vmp_coefficient = abs(module["temp_coeff_vmp_pct_per_c"]) / 100
    cold_voc_per_module = module["voc_v"] * (1 + voc_coefficient * (REFERENCE_TEMPERATURE_C - min_temperature_c))
    hot_vmp_per_module = module["vmp_v"] * (1 - vmp_coefficient * (max_temperature_c - REFERENCE_TEMPERATURE_C))
    return {
        "cold_voc_per_module": cold_voc_per_module,
        "hot_vmp_per_module": hot_vmp_per_module,
        "cold_string_voc_v": modules_per_string * cold_voc_per_module,
        "hot_string_vmp_v": modules_per_string * hot_vmp_per_module,
    }


def calculate_string_limits(inverter: dict, temperature: dict, module_vmp_v: float) -> dict:
    # Derives safe minimum, maximum, and midpoint-recommended modules per string.
    maximum = floor(inverter["max_dc_voltage_v"] / temperature["cold_voc_per_module"])
    minimum = ceil(inverter["mppt_min_voltage_v"] / temperature["hot_vmp_per_module"])
    midpoint = (inverter["mppt_min_voltage_v"] + inverter["mppt_max_voltage_v"]) / 2
    recommended = max(minimum, min(maximum, round(midpoint / module_vmp_v)))
    return {"max_modules_per_string": maximum, "min_modules_per_string": minimum,
            "recommended_modules_per_string": recommended}


def calculate_inverter_limits(inverter: dict) -> dict:
    # Calculates total inverter AC/DC capacity and available string input capacity.
    max_strings_per_inverter = inverter["mppt_input_count"] * inverter["strings_per_mppt"]
    return {
        "inverter_total_ac_capacity_kw": inverter["ac_power_kw"] * inverter["quantity"],
        "inverter_max_pv_capacity_kw": inverter["max_dc_power_kw"] * inverter["quantity"],
        "max_strings_per_inverter": max_strings_per_inverter,
        "max_strings_system": max_strings_per_inverter * inverter["quantity"],
    }


def calculate_recommended_pv(energy: dict, module_power_w: float, recommended_modules_per_string: int) -> dict:
    # Sizes PV from energy demand, solar resource, performance ratio, and margin.
    base_kwp = energy["daily_energy_kwh"] / (energy["peak_sun_hours"] * energy["performance_ratio"])
    suggested_kwp = base_kwp * (1 + energy["safety_margin_pct"] / 100)
    module_count = ceil(suggested_kwp * 1000 / module_power_w)
    return {"suggested_pv_capacity_kwp": suggested_kwp, "suggested_module_count": module_count,
            "suggested_string_count": ceil(module_count / recommended_modules_per_string)}


def calculate_mounting(module: dict, total_modules: int, mounting: dict) -> dict:
    # Calculates module physical metrics and checks mounting-layout module count.
    module_area_m2 = module["length_mm"] * module["width_mm"] / 1_000_000
    modules_per_table = mounting["modules_per_row"] * mounting["rows_per_table"]
    system_modules = modules_per_table * mounting["total_tables"]
    return {
        "module_area_m2": module_area_m2,
        "module_power_density_w_per_m2": module["max_power_w"] / module_area_m2,
        "total_module_area_m2": module_area_m2 * total_modules,
        "total_module_weight_kg": module["weight_kg"] * total_modules,
        "mounting_modules_per_table": modules_per_table,
        "mounting_system_total_modules": system_modules,
        "mounting_matches_electrical_design": system_modules == total_modules,
    }
