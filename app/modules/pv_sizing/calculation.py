from app.utils import pv_formulas


def calculate_pv_configuration(
    module: dict, modules_per_string: int, number_of_strings: int, inverter: dict,
    min_temperature_c: float, max_temperature_c: float, daily_energy_kwh: float,
    peak_sun_hours: float, performance_ratio: float, safety_margin_pct: float,
    bess_capacity_kwh: float, coupling_type: str, mounting_type: str,
    modules_per_row: int, rows_per_table: int, total_tables: int, module_orientation: str,
) -> dict:
    
    # Combines PV electrical, energy-sizing, mounting, and warning calculations.
    # """Compose independently testable PV electrical, energy, and mounting calculations."""
    # Calculate the selected PV array's electrical capacity, voltage, and current.
    array = pv_formulas.calculate_array(module, modules_per_string, number_of_strings)
    # Correct string voltage for the submitted cold and hot site temperatures.
    temperature = pv_formulas.calculate_temperature_voltages(
        module, modules_per_string, min_temperature_c, max_temperature_c
    )
    # Derive safe and recommended string lengths from inverter voltage limits.
    string_limits = pv_formulas.calculate_string_limits(inverter, temperature, module["vmp_v"])
    # Calculate total inverter capacity and available PV-string inputs.
    inverter_limits = pv_formulas.calculate_inverter_limits(inverter)

    # Size the PV target from daily energy, solar resource, losses, and margin.
    recommended = pv_formulas.calculate_recommended_pv(
        {"daily_energy_kwh": daily_energy_kwh, "peak_sun_hours": peak_sun_hours,
         "performance_ratio": performance_ratio, "safety_margin_pct": safety_margin_pct},
        module["max_power_w"], string_limits["recommended_modules_per_string"],
    )
    # Calculate module physical totals and verify mounting/electrical module counts agree.
    mounting = pv_formulas.calculate_mounting(
        module, array["total_modules"], {"modules_per_row": modules_per_row,
        "rows_per_table": rows_per_table, "total_tables": total_tables},
    )

    warnings: list[str] = []
    if modules_per_string > string_limits["max_modules_per_string"]:
        warnings.append("Cold-corrected string Voc exceeds the inverter maximum DC voltage.")
    if modules_per_string < string_limits["min_modules_per_string"]:
        warnings.append("Hot-corrected string Vmp is below the inverter MPPT minimum voltage.")
    if temperature["hot_string_vmp_v"] > inverter["mppt_max_voltage_v"]:
        warnings.append("Hot-corrected string Vmp exceeds the inverter MPPT maximum voltage.")
    if array["total_array_current_a"] > inverter["max_dc_input_current_a"]:
        warnings.append("Total PV array current exceeds the inverter maximum DC input current.")
    if array["total_capacity_kwp"] > inverter_limits["inverter_max_pv_capacity_kw"]:
        warnings.append("PV array capacity exceeds the inverter maximum PV capacity.")
    if number_of_strings > inverter_limits["max_strings_system"]:
        warnings.append("Number of strings exceeds the total inverter MPPT/string input capacity.")
    if not mounting["mounting_matches_electrical_design"]:
        warnings.append("Mounting layout module count does not match the electrical string configuration.")

    return {
        "total_modules": array["total_modules"],
        "total_capacity_kwp": round(array["total_capacity_kwp"], 3),
        "string_vmp_v": round(array["string_vmp_v"], 2),
        "string_voc_v": round(array["string_voc_v"], 2),
        "string_power_kw": round(array["string_power_kw"], 3),
        "dc_ac_ratio": round(array["total_capacity_kwp"] / inverter_limits["inverter_total_ac_capacity_kw"], 3),
        "warnings": warnings,
        "cold_string_voc_v": round(temperature["cold_string_voc_v"], 2),
        "hot_string_vmp_v": round(temperature["hot_string_vmp_v"], 2),
        **string_limits,
        "total_array_current_a": round(array["total_array_current_a"], 2),
        "inverter_ac_capacity_kw": inverter["ac_power_kw"],
        "inverter_quantity": inverter["quantity"],
        "inverter_max_dc_voltage_v": inverter["max_dc_voltage_v"],
        "inverter_mppt_min_v": inverter["mppt_min_voltage_v"],
        "inverter_mppt_max_v": inverter["mppt_max_voltage_v"],
        **inverter_limits,
        "suggested_pv_capacity_kwp": round(recommended["suggested_pv_capacity_kwp"], 3),
        "suggested_module_count": recommended["suggested_module_count"],
        "suggested_string_count": recommended["suggested_string_count"],
        "bess_capacity_kwh": bess_capacity_kwh,
        "coupling_type": coupling_type,
        "module_area_m2": round(mounting["module_area_m2"], 3),
        "module_power_density_w_per_m2": round(mounting["module_power_density_w_per_m2"], 2),
        "module_weight_kg": module["weight_kg"],
        "module_frame_type": module["frame_type"],
        "total_module_area_m2": round(mounting["total_module_area_m2"], 3),
        "total_module_weight_kg": round(mounting["total_module_weight_kg"], 2),
        "mounting_type": mounting_type,
        "module_orientation": module_orientation,
        "mounting_modules_per_table": mounting["mounting_modules_per_table"],
        "mounting_system_total_modules": mounting["mounting_system_total_modules"],
        "mounting_matches_electrical_design": mounting["mounting_matches_electrical_design"],
    }
