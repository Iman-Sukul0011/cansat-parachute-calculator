import streamlit as st
import math

st.set_page_config(page_title="CanSat Recovery Calculator", page_icon="🪂")

# --- LOGIC ---
parachute_types = {
    "Round": {"Cd": 1.0, "shape": "circle"},
    "Cruciform": {"Cd": 0.8, "shape": "cross"},
    "Square": {"Cd": 0.9, "shape": "square"},
    "Hexagonal": {"Cd": 1.1, "shape": "hexagon"},
    "Elliptical": {"Cd": 0.95, "shape": "ellipse"}
}

def calculate_specs(mass, vel, rho, p_type, pack_height_cm):
    data = parachute_types[p_type]
    Cd = data["Cd"]
    shape = data["shape"]
    g = 9.81
    
    # 1. Physics: Area Calculation
    area = (2 * mass * g) / (Cd * rho * (vel**2))
    impact_energy = 0.5 * mass * vel**2
    
    # 2. Geometry Calculation
    dims = {}
    lines = 0
    
    if shape == "circle":
        d = math.sqrt(4 * area / math.pi)
        dims["Diameter (m)"] = round(d, 3)
        dims["Spill Hole (m)"] = round(d * 0.12, 3)
        lines = 8
    elif shape == "square":
        s = math.sqrt(area)
        dims["Side Length (m)"] = round(s, 3)
        lines = 4
    elif shape == "hexagon":
        s = math.sqrt(area / 2.598)
        dims["Side Length (m)"] = round(s, 3)
        lines = 6
    else:
        d = math.sqrt(4 * area / math.pi)
        dims["Equivalent Dia (m)"] = round(d, 3)
        lines = 8

    line_len = 1.2 * math.sqrt(4 * area / math.pi)
    
    # 3. Packing Calculation (New!)
    # Assumption: Nylon fabric thickness ~0.1mm + lines factor
    # Volume (m3) = Area * 0.0003 (conservative packing factor)
    packed_vol_m3 = area * 0.0003
    
    # Convert height to meters
    h_m = pack_height_cm / 100.0
    
    # V = pi * r^2 * h  ->  r = sqrt(V / (pi*h))
    if h_m > 0:
        pack_radius = math.sqrt(packed_vol_m3 / (math.pi * h_m))
        pack_dia_mm = pack_radius * 2 * 1000  # Convert to mm
    else:
        pack_dia_mm = 0

    return area, dims, lines, line_len, impact_energy, pack_dia_mm

# --- WEBSITE LAYOUT ---
st.title("🪂 CanSat Recovery Calculator")

# Input Columns
c1, c2 = st.columns(2)
with c1:
    mass = st.number_input("Mass (kg)", 0.1, 5.0, 1.0, 0.1)
    vel = st.number_input("Descent Velocity (m/s)", 1.0, 20.0, 5.0, 0.5)
    # New Input for Packing
    pack_h = st.number_input("Avail. Packing Height (cm)", 1.0, 15.0, 3.0, 0.5)
with c2:
    rho = st.number_input("Air Density (kg/m³)", 0.0, 2.0, 1.225, 0.001)
    ptype = st.selectbox("Parachute Type", list(parachute_types.keys()))

if st.button("Calculate", type="primary"):
    # Run calculation
    area, dims, lines, line_len, energy, pack_dia = calculate_specs(mass, vel, rho, ptype, pack_h)
    
    st.divider()
    
    # Top Metrics
    k1, k2, k3 = st.columns(3)
    k1.metric("Area", f"{area:.4f} m²")
    k2.metric("Line Length", f"{line_len:.3f} m")
    k3.metric("Impact Energy", f"{energy:.2f} J")
    
    # Packing Metric (New!)
    st.markdown("### 📦 Packing Estimates")
    p1, p2 = st.columns(2)
    p1.metric("Packing Height", f"{pack_h} cm")
    p2.metric("Min. Pack Diameter", f"{pack_dia:.1f} mm")
    
    # Warnings
    if pack_dia > 60:
         st.warning(f"⚠️ Warning: {pack_dia:.1f}mm might not fit in a standard CanSat (66mm)!")
    elif energy >= 15:
        st.error("⚠️ High Impact Energy!")
    else:
        st.success("✅ Design looks safe")
        
    st.write("---")
    st.write("**Geometry Details:**", dims)
