import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Reservoir Engineering Application")

# Add selection option in sidebar
analysis_type = st.sidebar.selectbox(
    "Select Analysis Type",
    ["Select Analysis", "Pressure Profile", "Klinkenberg Effect"]
)

# Default state - Introduction
if analysis_type == "Select Analysis":
    st.markdown("""
    ## Welcome to Reservoir Engineering Application
    
    This application provides two main functionalities for reservoir engineering analysis:
    
    ### 1. Pressure Profile Analysis
    - Calculates and visualizes the pressure distribution in a reservoir
    - Takes into account parameters like permeability, viscosity, flow rate, and reservoir dimensions
    - Shows the pressure drop from reservoir boundary to wellbore
    
    ### 2. Klinkenberg Effect Analysis
    - Calculates absolute permeability from gas permeability measurements
    - Demonstrates the effect of gas slippage on permeability measurements
    - Provides visualization of the Klinkenberg effect
    
    Please select an analysis type from the sidebar to begin.
    """)

elif analysis_type == "Pressure Profile":
    st.subheader("Pressure Profile Analysis")
    st.markdown("This analysis calculates the pressure distribution in a reservoir from the outer boundary to the wellbore.")
    
    st.sidebar.title("Pressure Profile Inputs")
    
    k = st.sidebar.slider("Permeability", min_value=10, max_value=200, value=100, step=1)
    mu = st.sidebar.slider("Viscosity(cP)",min_value=10,max_value=20,value=11)
    q = st.sidebar.slider("Flowrate(STB/Day)",min_value=100,max_value=500,value=120)
    
    re = st.sidebar.number_input("Outer Reservoir Radius(ft)",min_value=100,max_value=10000,value=1000)
    rw = st.sidebar.number_input("Wellbore Radius(ft)",min_value=1,max_value=10,value=1)
    pe = st.sidebar.number_input("Pressure at the boundary of Reservoir(psi)",min_value=100,max_value=10000,value=4000)
    B = st.sidebar.number_input("Formation Volume Factor(bbl/stb)",min_value=1,max_value=2,value=1)
    h = st.sidebar.number_input('Net pay thickness of Reservoir (feet)',min_value=2,max_value=500,value=30)
    
    # Pressure profile logic
    r = np.linspace(rw,re,500)
    pressure = pe - (141.2*q*mu*B*(np.log(re/r))/(k*h))
    y_min = pressure[np.where(r==rw)]
    
    b = st.button("Show Pressure Profile")
    
    if b:
        plt.figure(figsize=(10,5))
        fig, ax = plt.subplots()
        ax.plot(r,pressure,linewidth=4,color='blue')
        ax.axhline(y=y_min, color='r', linestyle='--')
        ax.set_xlabel('Radius(ft)')
        ax.set_ylabel('Pressure(psi)')
        ax.set_title('Pressure Profile in Reservoir')
        ax.set_ylim(0,5000)
        ax.set_xlim(0,re+100)
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

else:  # Klinkenberg Effect
    st.subheader("Klinkenberg Effect Analysis")
    st.markdown("This analysis calculates absolute permeability from gas permeability measurements, accounting for the Klinkenberg effect.")
    
    st.sidebar.title("Klinkenberg Effect Inputs")
    
    kg = st.sidebar.number_input("Gas Permeability (md)", min_value=0.1, max_value=1000.0, value=100.0)
    pm = st.sidebar.number_input("Mean Pressure (psi)", min_value=1, max_value=100, value=2)
    k_guess = st.sidebar.number_input("Initial Guess for Absolute Permeability (md)", min_value=0.1, max_value=1000.0, value=50.0)
    
    def klinkenberg(kg, pm, k):
        count = 0
        while (abs(6.9*k**0.64+pm*k - pm*kg)>0.0000000001):
            k = k - ((6.9*k**0.64+pm*k - pm*kg)/(4.416*(k**(-0.36))+pm))
            count+=1
        
        st.write(f"The final value of Perm K is: {k:.4f} md")
        st.write(f"The number of iterations used = {count}")
        
        x = [0, 1/pm]
        y = [k, kg]
        
        plt.style.use('classic')
        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(x, y)
        ax.scatter(0, k, label="KL(Absolute Perm)", c="green", s=100)
        ax.scatter(1/pm, kg, label="User provided data", c="red", s=100)
        
        ax.set_xlabel('1/Mean_Pressure (psi^-1)')
        ax.set_ylabel('Permeability (md)')
        ax.set_xlim(-0.02,)
        ax.set_ylim(0,)
        ax.set_title('Klinkenberg Effect')
        ax.legend(loc="best")
        ax.grid(True)
        
        return k, fig
    
    if st.button("Calculate Klinkenberg Effect"):
        k_abs, fig = klinkenberg(kg, pm, k_guess)
        st.pyplot(fig)

