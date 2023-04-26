import numpy as np
import pandas as pd
from src.common import get_reinf_rate_cross_section_plane

def main_reinforced_concrete_helper(st):
    """ Helper for steel reinforced concrete"""

    st.title('Helper for steel reinforced concrete')

    st.subheader('EC2 6.2.2, members not requiring design of shear reinforcement, calculation of shear resistance V_Rdc')
    cols = st.columns(4)
    b_w = cols[0].number_input('smallest width of section b_w [mm]', value=2000.0)
    d = cols[1].number_input('depth of section d [mm]', value=4000.0)
    f_ck = cols[2].number_input('concrete yield stress f_ck [MPa]', value=40.0)
    #gamma_c = cols[3].number_input('concrete safety factor gamma_c [MPa]', value=1.5)
    C_Rdc = cols[3].number_input('C_Rdc [-]', value=0.12)
    A_sl = cols[0].number_input('area of tensile reinforcement A_sl [cm^2]', value=200.0)
    k = cols[1].number_input('k [-] = 1 + sqrt(200/d) <= 2', value=1+(200/d)**(0.5))
    rho_1 = cols[2].number_input('rho_1 [-] = A_sl/(b_w*d) <= 0.02', value=A_sl*100/(b_w*d), format='%.4f')
    sigma_cp = cols[0].number_input('compressive stress at null line sigma_cp [MPa] = N_Ed/A_c <= 0.2f_cd', value=0.0)
    k1 = cols[1].number_input('factor for compression k1 [-]', value=0.15)

    v_min_BS = v_min = 0.035 * k**(3/2) * f_ck**(1/2)
    v_min_DIN = 0.0375 * k**(3/2) * f_ck**(1/2) 
    if d < 600:
        v_min_DIN = 0.0525 * k**(3/2) * f_ck**(1/2) 

    st.write('DIN NA EC2: C_Rdc = 0.15/gamma_C; k1 = 0.12; v_min = 0.0375 * k^(3/2) * f_ck^(1/2) for d > 800 mm; v_min = 0.0525 * k^(3/2) * f_ck^(1/2) for d <= 600 mm; v_min = {0:.4f} MPa'.format(v_min_DIN))
    st.write('BS NA EC2: C_Rdc = 0.18/gamma_C; k1 = 0.15; v_min = 0.035 * k^(3/2) * f_ck^(1/2) = {0:.4f} MPa'.format(v_min_BS))
    V_Rdc = (C_Rdc*k*(100.0*rho_1*f_ck)**(1/3) + k1*sigma_cp) * b_w*d*1.0e-6 # MN
    st.write('V_Rdc = (C_Rdc * k * (100.0 * rho_1 * f_ck)^(1/3) + k1 * sigma_cp) * b_w * d = {0:.2f} MN, v_Rdc = {1:.4f} MPa'.format(V_Rdc, V_Rdc/(b_w*d*1.0e-6)))



    st.subheader('EC2 7.3.2/ Ciria C660, minimum reinforcement against early age thermal cracks')
    cols = st.columns(4)
    Ac = cols[0].number_input('Concrete cross-section area A_c [cm^2]', value=50.0*1000.0)
    Act_over_Ac = cols[1].number_input('Ratio A_ct/A_c [-]', value=0.2)
    fctm = cols[2].number_input('Concrete mean tensile strength f_ctm [MPa]', value=3.5)
    fcteff_over_fctm = cols[3].number_input('Ratio f_ct,eff/f_ctm [-]', value=0.7)
    cols[0].write('Area of concrete within tensile zone A_ct [cm^2] = {:.2f}'.format(Ac*Act_over_Ac))
    cols[1].write('Effective tensile strength of concrete when first cracks occur f_ct,eff [MPa] = {:.2f}'.format(fctm*fcteff_over_fctm))
    k = cols[2].number_input('Coefficient k [-]', value=1.0)
    kc = cols[3].number_input('Coefficient k_c [-]', value=0.5)
    fyk = cols[0].number_input('Characteristic yield strength of steel f_yk [MPa]', value=500.0)
    st.write('It must satisfy the condition: A_s,min * sigma_s = k_c * k * f_ct,eff * A_ct')
    st.write('Thus, A_s,min = (k_c * k * f_ct,eff * A_ct) / sigma_s')
    st.write('Ciria C660: sigma_s = f_yk, so A_s,min = {:.2f} cm$^2$'.format(kc*k*fctm*fcteff_over_fctm*Ac*Act_over_Ac/fyk))



    st.subheader('Table of reinforcement areas indexed by bar diameters and spacings')
    col1, col2 = st.columns(2)
    dias_str = col1.text_input('List of bar diameters [mm]', value='10, 12, 14, 16, 20, 25, 28, 32, 40')
    spacings_str = col2.text_input('List of spacings [cm]', value='7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 20, 25')
    dias = [float(dia) for dia in list(dias_str.split(','))]
    spacings = [float(spacing) for spacing in list(spacings_str.split(','))]
    index_dias = [str(dia) + ' mm' for dia in dias]
    index_spacings = [str(spacing) + ' cm' for spacing in spacings]
    # initialize table
    df_1d = pd.DataFrame(index=index_spacings, columns=index_dias)	# empty dataframe
    df_2d = pd.DataFrame(index=index_spacings, columns=index_dias)	# empty dataframe
    df_1d = df_1d.fillna(0.0)
    df_2d = df_2d.fillna(0.0)
    # fill table with values
    for i, spacing in enumerate(spacings):
        for j, dia in enumerate(dias):
            df_1d.iloc[i, j] = get_reinf_rate_cross_section_plane(dia, spacing)
            df_2d.iloc[i, j] = get_reinf_rate_cross_section_plane(dia, spacing)*100/spacing

    # print table
    pd.options.display.float_format = '{:,.2f}'.format
    col1.write('Table 1d As [cm$^2$/m]: bars arranged in a line')
    col1.dataframe(df_1d.style.format("{:.2f}"))
    col2.write('Table 2d As [cm$^2$/m$^2$]: bars arranged in an equidistant and orthorgonal 2d grid (e.g. for shear reinforcement)')
    col2.dataframe(df_2d.style.format("{:.2f}"))
