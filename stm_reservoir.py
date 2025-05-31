import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Reservoir Engineering Application")

st.sidebar.title("Inputs")

k = st.sidebar.slider("Permeability", min_value=10, max_value=200, value=100, step=1)
mu = st.sidebar.slider("Viscosity(cP)",min_value=10,max_value=20,value=11)

q = st.sidebar.slider("Flowrate(STB/Day)",min_value=100,max_value=500,value=120)


## Taking Inputs from number inputs 

re = st.sidebar.number_input("Outer Reservoir Radius(ft)",min_value=100,max_value=10000,value=1000)
rw = st.sidebar.number_input("Wellbore Radius(ft)",min_value=1,max_value=10,value=1)

pe = st.sidebar.number_input("Pressure at the boundary of Reservoir(psi)",min_value=100,max_value=10000,value=4000)

B = st.sidebar.number_input("Formation Volume Factor(bbl/stb)",min_value=1,max_value=2,value=1)

h= st.sidebar.number_input('Net pay thickness of Reservoir (feet)',min_value = 2,max_value=500, value =30)


#logic 

r = np.linspace(rw,re,500)
pressure = pe - (141.2*q*mu*B*(np.log(re/r))/(k*h))

y_min = pressure[np.where(r==rw)]

##button 

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

