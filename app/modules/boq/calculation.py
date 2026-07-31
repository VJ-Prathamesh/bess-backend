"""
BOQ Calculation Engine - Rule Engine

Converts engineering outputs into structured Bill of Quantities (BOQ) line items.

Rules:
- Pure deterministic mapping rules
- No database access
- No FastAPI imports
- No SQLAlchemy
- No repository calls
- No HTTP exceptions
- No financial calculations or price estimations
"""

from dataclasses import dataclass
from typing import List, Optional


# ==========================================================
# Engineering Input Data Classes
# ==========================================================

@dataclass
class ProjectInfo:
    project_id: int
    project_name: str
    location: str


@dataclass
class LoadProfileInfo:
    daily_energy_kwh: float
    peak_load_kw: float


@dataclass
class BESSConfigInfo:
    battery_capacity_kwh: float
    battery_chemistry: str
    rack_quantity: int
    pcs_rating_kw: float


@dataclass
class PVSizingInfo:
    pv_capacity_kwp: float
    pv_module_wattage_w: float
    pv_module_count: int
    mounting_type: str


@dataclass
class CableSizingInfo:
    dc_cable_length_m: float
    dc_cable_sqmm: float
    ac_cable_length_m: float
    ac_cable_sqmm: float
    cable_tray_length_m: float


@dataclass
class SystemLossesInfo:
    dcdb_quantity: int
    acdb_quantity: int


@dataclass
class SimulationInfo:
    annual_pv_generation_kwh: float


@dataclass
class EngineeringInput:
    project: ProjectInfo
    load_profile: LoadProfileInfo
    bess_config: BESSConfigInfo
    pv_sizing: PVSizingInfo
    cable_sizing: CableSizingInfo
    system_losses: SystemLossesInfo
    simulation: SimulationInfo


# ==========================================================
# BOQ Output Data Class
# ==========================================================

@dataclass
class BOQItemData:
    sl_no: int
    category: str
    description: str
    specification: str
    unit: str
    quantity: float
    manufacturer: Optional[str] = None
    model_number: Optional[str] = None
    remarks: Optional[str] = None


# ==========================================================
# BOQ Generation Rule Engine
# ==========================================================

def generate_boq(input_data: EngineeringInput) -> List[BOQItemData]:
    """
    Generates BOQ items from engineering inputs deterministically.
    """
    items: List[BOQItemData] = []
    sl = 1

    # 1. PV Module BOQ Item
    if input_data.pv_sizing.pv_module_count > 0:
        items.append(
            BOQItemData(
                sl_no=sl,
                category="Solar PV System",
                description="Solar PV Mono-PERC Modules",
                specification=f"{input_data.pv_sizing.pv_module_wattage_w:.0f}W Mono PERC High Efficiency Solar PV Module",
                manufacturer="Tier-1 Manufacturer",
                model_number=f"PV-{input_data.pv_sizing.pv_module_wattage_w:.0f}W",
                unit="Nos",
                quantity=float(input_data.pv_sizing.pv_module_count),
                remarks=f"Total PV Array Capacity: {input_data.pv_sizing.pv_capacity_kwp:.2f} kWp",
            )
        )
        sl += 1

    # 2. PV Mounting Structure Item
    if input_data.pv_sizing.pv_capacity_kwp > 0:
        items.append(
            BOQItemData(
                sl_no=sl,
                category="Solar PV System",
                description="PV Module Mounting Structure (MMS)",
                specification=f"{input_data.pv_sizing.mounting_type} Hot-Dip Galvanized Iron (HDGI) Mounting Structure",
                manufacturer="Standard OEM",
                model_number="MMS-HDGI-01",
                unit="kWp",
                quantity=float(input_data.pv_sizing.pv_capacity_kwp),
                remarks="Designed to withstand wind speed up to 150 km/h",
            )
        )
        sl += 1

    # 3. Battery BOQ Item
    if input_data.bess_config.battery_capacity_kwh > 0:
        items.append(
            BOQItemData(
                sl_no=sl,
                category="BESS Subsystem",
                description=f"Battery Energy Storage System ({input_data.bess_config.battery_chemistry})",
                specification=f"{input_data.bess_config.battery_chemistry} Battery Pack, High Energy Density Cell Stack",
                manufacturer="Tier-1 BESS Vendor",
                model_number=f"BESS-{input_data.bess_config.battery_chemistry}-500",
                unit="kWh",
                quantity=float(input_data.bess_config.battery_capacity_kwh),
                remarks=f"Nominal BESS Capacity: {input_data.bess_config.battery_capacity_kwh:.2f} kWh",
            )
        )
        sl += 1

    # 4. Battery Rack BOQ Item
    if input_data.bess_config.rack_quantity > 0:
        items.append(
            BOQItemData(
                sl_no=sl,
                category="BESS Subsystem",
                description="Standard Battery Enclosure / Rack Frame",
                specification="Modular Battery Enclosure Cabinet with integrated BMS & Busbars",
                manufacturer="Tier-1 BESS Vendor",
                model_number="BESS-RACK-STD",
                unit="Nos",
                quantity=float(input_data.bess_config.rack_quantity),
                remarks=f"Holds {input_data.bess_config.battery_capacity_kwh:.2f} kWh total storage",
            )
        )
        sl += 1

    # 5. Battery PCS / Inverter Item
    if input_data.bess_config.pcs_rating_kw > 0:
        items.append(
            BOQItemData(
                sl_no=sl,
                category="BESS Subsystem",
                description="Power Conversion System (PCS / Bi-directional Inverter)",
                specification=f"{input_data.bess_config.pcs_rating_kw:.0f} kW Bi-directional Battery PCS Inverter",
                manufacturer="Standard Inverter OEM",
                model_number=f"PCS-{input_data.bess_config.pcs_rating_kw:.0f}K",
                unit="Nos",
                quantity=1.0,
                remarks="Grid-forming and Grid-following capable",
            )
        )
        sl += 1

    # 6. DC Cable Item
    if input_data.cable_sizing.dc_cable_length_m > 0:
        items.append(
            BOQItemData(
                sl_no=sl,
                category="Electrical & Cabling",
                description="Solar DC Cable",
                specification=f"{input_data.cable_sizing.dc_cable_sqmm:.1f} sq.mm XLPO Insulated UV Resistant Flexible Copper Solar Cable",
                manufacturer="Standard Cable OEM",
                model_number=f"DC-SOLAR-{input_data.cable_sizing.dc_cable_sqmm:.1f}",
                unit="Meters",
                quantity=float(input_data.cable_sizing.dc_cable_length_m),
                remarks="1.5kV DC rated",
            )
        )
        sl += 1

    # 7. AC Cable Item
    if input_data.cable_sizing.ac_cable_length_m > 0:
        items.append(
            BOQItemData(
                sl_no=sl,
                category="Electrical & Cabling",
                description="Armored AC Power Cable",
                specification=f"{input_data.cable_sizing.ac_cable_sqmm:.1f} sq.mm 3.5C/4C Armored Aluminium/Copper XLPE Cable",
                manufacturer="Standard Cable OEM",
                model_number=f"AC-ARM-{input_data.cable_sizing.ac_cable_sqmm:.1f}",
                unit="Meters",
                quantity=float(input_data.cable_sizing.ac_cable_length_m),
                remarks="1.1kV LT AC rated",
            )
        )
        sl += 1

    # 8. Earthing Item
    items.append(
        BOQItemData(
            sl_no=sl,
            category="Electrical & Protection",
            description="Earthing System",
            specification="Chemical Maintenance-Free Copper Bonded Earth Electrode with Earth Pit Chambers",
            manufacturer="Standard Protection OEM",
            model_number="EARTH-KIT-50",
            unit="Set",
            quantity=6.0,
            remarks="Dedicated earthing for PV array, BESS, PCS, and lightning arrestor",
        )
    )
    sl += 1

    # 9. Lightning Protection / SPD Item
    items.append(
        BOQItemData(
            sl_no=sl,
            category="Electrical & Protection",
            description="Lightning Protection & Surge Protection Device (SPD)",
            specification="Class I+II Surge Protection Device & ESE Lightning Protection Terminal",
            manufacturer="Standard Protection OEM",
            model_number="SPD-T1T2-1000",
            unit="Set",
            quantity=1.0,
            remarks="Complete protection zone coverage",
        )
    )
    sl += 1

    # 10. Cable Tray Item
    if input_data.cable_sizing.cable_tray_length_m > 0:
        items.append(
            BOQItemData(
                sl_no=sl,
                category="Electrical & Cabling",
                description="Galvanized Perforated Cable Tray",
                specification="Hot-Dip Galvanized Perforated Cable Tray with Cover (300mm x 50mm)",
                manufacturer="Standard Hardware OEM",
                model_number="CT-HDGI-300",
                unit="Meters",
                quantity=float(input_data.cable_sizing.cable_tray_length_m),
                remarks="Includes bends, tees, and hardware accessories",
            )
        )
        sl += 1

    # 11. DC Distribution Board (DCDB)
    if input_data.system_losses.dcdb_quantity > 0:
        items.append(
            BOQItemData(
                sl_no=sl,
                category="Balance of System",
                description="DC Distribution Board (DCDB)",
                specification="IP65 Enclosure with DC Fuse Disconnectors and Type-2 SPD",
                manufacturer="Standard Switchgear OEM",
                model_number="DCDB-1000V-4I1O",
                unit="Nos",
                quantity=float(input_data.system_losses.dcdb_quantity),
                remarks="Includes string monitoring functionality",
            )
        )
        sl += 1

    # 12. AC Distribution Board (ACDB)
    if input_data.system_losses.acdb_quantity > 0:
        items.append(
            BOQItemData(
                sl_no=sl,
                category="Balance of System",
                description="AC Distribution Board (ACDB)",
                specification="IP65 Wall/Floor Mounting AC Breaker Panel with MCCB, Metering & SPD",
                manufacturer="Standard Switchgear OEM",
                model_number="ACDB-415V-250A",
                unit="Nos",
                quantity=float(input_data.system_losses.acdb_quantity),
                remarks="Includes main incoming breaker and outgoing feeders",
            )
        )
        sl += 1

    # 13. Monitoring Equipment Item
    items.append(
        BOQItemData(
            sl_no=sl,
            category="Control & Monitoring",
            description="Energy Management System (EMS) & SCADA Controller",
            specification="Industrial Controller with Modbus/RS485, Cloud Telemetry Gateway, and Sensors",
            manufacturer="Standard Automation OEM",
            model_number="EMS-GATEWAY-v2",
            unit="Set",
            quantity=1.0,
            remarks="Includes weather monitoring sensor kit (Irradiance, Temp)",
        )
    )
    sl += 1

    # 14. Fire Protection Item
    items.append(
        BOQItemData(
            sl_no=sl,
            category="Safety & Fire Protection",
            description="BESS Container Fire Suppression System",
            specification="NOVEC 1230 / Aerosol Automatic Fire Extinguishing & Smoke Detection System",
            manufacturer="Standard Safety OEM",
            model_number="FIRE-SUPP-AUT-01",
            unit="Set",
            quantity=1.0,
            remarks="Integrated with BESS emergency shutdown protocol",
        )
    )
    sl += 1

    # 15. Installation Materials Item
    items.append(
        BOQItemData(
            sl_no=sl,
            category="Civil & Installation",
            description="Civil Foundations & Balance of Installation Materials",
            specification="Concrete pads for BESS/PCS, cable trenching, civil works, hardware and fasteners",
            manufacturer="Generic Civil",
            model_number="CIVIL-BOS-LOT",
            unit="Lot",
            quantity=1.0,
            remarks="Complete site preparation and civil works",
        )
    )
    sl += 1

    # 16. Testing & Commissioning Item
    items.append(
        BOQItemData(
            sl_no=sl,
            category="Services",
            description="Testing, Pre-commissioning & Commissioning Services",
            specification="Site Acceptance Testing (SAT), Insulation testing, Grid Code compliance testing",
            manufacturer="Certified Engineering Services",
            model_number="SERV-COMM-01",
            unit="Lot",
            quantity=1.0,
            remarks="Includes commissioning documentation and hand-over training",
        )
    )
    sl += 1

    return items
