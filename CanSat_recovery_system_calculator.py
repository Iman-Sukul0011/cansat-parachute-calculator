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

def calculate_specs(mass, vel, rho, p_type):
    data = parachute_types[p_type]
    Cd = data["Cd"]
    shape = data["shape"]
    g = 9.81
    
    area = (2 * mass * g) / (Cd * rho * (vel**2))
    impact_energy = 0.5 * mass * vel**2
    
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

    return area, dims, lines, line_len, impact_energy

# --- WEBSITE LAYOUT ---
st.title("🪂 CanSat Recovery Calculator")

c1, c2 = st.columns(2)
with c1:
    mass = st.number_input("Mass (kg)", 0.1, 5.0, 1.0, 0.1)
    vel = st.number_input("Descent Velocity (m/s)", 1.0, 20.0, 5.0, 0.5)
with c2:
    rho = st.number_input("Air Density (kg/m³)", 0.0, 2.0, 1.225, 0.001)
    ptype = st.selectbox("Parachute Type", list(parachute_types.keys()))

if st.button("Calculate", type="primary"):
    area, dims, lines, line_len, energy = calculate_specs(mass, vel, rho, ptype)
    
    st.divider()
    k1, k2, k3 = st.columns(3)
    k1.metric("Area", f"{area:.4f} m²")
    k2.metric("Line Length", f"{line_len:.3f} m")
    k3.metric("Impact Energy", f"{energy:.2f} J")
    
    if energy < 15:
        st.success("✅ Safe Landing Energy")
    else:
        st.error("⚠️ High Impact Energy!")
        
    st.write("Dimensions:", dims)