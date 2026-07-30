from pydantic import BaseModel, ConfigDict, Field, model_validator


class PVModuleOut(BaseModel):
    id: int
    manufacturer: str
    model_name: str
    max_power_w: float
    efficiency_pct: float
    vmp_v: float
    imp_a: float
    voc_v: float
    isc_a: float
    length_mm: float
    width_mm: float
    weight_kg: float
    frame_type: str
    temp_coeff_voc_pct_per_c: float
    temp_coeff_pmax_pct_per_c: float
    temp_coeff_vmp_pct_per_c: float
    max_system_voltage_v: float


class PVConfigIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pv_module_id: int
    modules_per_string: int = Field(ge=1)
    number_of_strings: int = Field(ge=1)
    inverter: "PVInverterIn"
    site_conditions: "SiteConditionsIn"
    energy_design: "EnergyDesignIn"
    scorecard: "ScorecardIn"
    mounting: "MountingIn"


class PVInverterIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    manufacturer: str
    model_name: str
    quantity: int = Field(ge=1)
    ac_power_kw: float = Field(gt=0, description="AC power of one inverter")
    max_dc_power_kw: float = Field(gt=0, description="Maximum PV DC power of one inverter")
    mppt_min_voltage_v: float = Field(gt=0)
    mppt_max_voltage_v: float = Field(gt=0)
    max_dc_voltage_v: float = Field(gt=0)
    mppt_input_count: int = Field(ge=1)
    strings_per_mppt: int = Field(ge=1)
    max_dc_input_current_a: float = Field(gt=0)

    @model_validator(mode="after")
    def validate_voltage_ranges(self):
        if self.mppt_min_voltage_v >= self.mppt_max_voltage_v:
            raise ValueError("mppt_min_voltage_v must be lower than mppt_max_voltage_v")
        if self.max_dc_voltage_v < self.mppt_max_voltage_v:
            raise ValueError("max_dc_voltage_v must be at least mppt_max_voltage_v")
        return self


class SiteConditionsIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    min_temperature_c: float
    max_temperature_c: float

    @model_validator(mode="after")
    def validate_temperature_range(self):
        if self.min_temperature_c > self.max_temperature_c:
            raise ValueError("min_temperature_c cannot be greater than max_temperature_c")
        return self


class EnergyDesignIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    daily_energy_kwh: float = Field(gt=0)
    peak_sun_hours: float = Field(gt=0)
    performance_ratio: float = Field(gt=0, le=1)
    safety_margin_pct: float = Field(ge=0)


class ScorecardIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bess_capacity_kwh: float = Field(ge=0)
    coupling_type: str


class MountingIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mounting_type: str
    modules_per_row: int = Field(ge=1)
    rows_per_table: int = Field(ge=1)
    total_tables: int = Field(ge=1)
    module_orientation: str


class PVConfigOut(BaseModel):
    project_id: int
    pv_module_id: int
    modules_per_string: int
    number_of_strings: int
    total_modules: int
    total_capacity_kwp: float
    string_vmp_v: float
    string_voc_v: float
    string_power_kw: float
    dc_ac_ratio: float
    warnings: list[str]

    # Extra deterministic checks used by the PV-sizing UI.
    cold_string_voc_v: float
    hot_string_vmp_v: float
    max_modules_per_string: int
    min_modules_per_string: int
    total_array_current_a: float
    inverter_ac_capacity_kw: float
    inverter_quantity: int
    inverter_total_ac_capacity_kw: float
    inverter_max_pv_capacity_kw: float
    inverter_max_dc_voltage_v: float
    inverter_mppt_min_v: float
    inverter_mppt_max_v: float
    max_strings_per_inverter: int
    max_strings_system: int
    recommended_modules_per_string: int
    suggested_pv_capacity_kwp: float
    suggested_module_count: int
    suggested_string_count: int
    bess_capacity_kwh: float
    coupling_type: str
    module_area_m2: float
    module_power_density_w_per_m2: float
    module_weight_kg: float
    module_frame_type: str
    total_module_area_m2: float
    total_module_weight_kg: float
    mounting_type: str
    module_orientation: str
    mounting_modules_per_table: int
    mounting_system_total_modules: int
    mounting_matches_electrical_design: bool
