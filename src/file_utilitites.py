import json
import base64
import _pickle as cPickle
import pickle
from io import StringIO, BytesIO
import streamlit as st
#import fpdf as FPDF
from matplotlib.backends.backend_pdf import PdfPages
from tempfile import NamedTemporaryFile
#from src.report import Report


def st_csv_download_button(df, download_filename):
    csv = df.to_csv(index=False) #if no filename is given, a string is returned
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a download="{download_filename} "href="data:file/csv;base64,{b64}">Download CSV file</a>'
    st.markdown(href, unsafe_allow_html=True)  

def st_json_download_button(json_object, download_filename):
    json_object_to_download = json.dumps(str(json_object))
    b64 = base64.b64encode(json_object_to_download.encode()).decode()
    href = f'<a download="{download_filename}" href="data:file/csv;base64,{b64}">Download session state JSON file</a>'
    return href
    #st.markdown(href, unsafe_allow_html=True)  


def load_parameters_from_json_file(uploaded_file):
    """ Unpacks json data file """
    data_dict = eval(StringIO(uploaded_file.getvalue().decode("utf-8")).read())     # data_dict is str representation of dict
    parameters = eval(data_dict)                                                    # eval str to get dict
    return parameters

def load_parameters_from_json_file_sps(uploaded_file):
    """ Unpacks json data file for secant piled shaft"""
    data_dict = eval(StringIO(uploaded_file.getvalue().decode("utf-8")).read()) # data_dict is str representation of dict
    parameters = assign_session_state_parameters_shaft_secant_piles(**eval(data_dict))             # eval str to get dict, then unpack
    return parameters


def load_parameters_from_json_file_sdw(uploaded_file):
    """ Unpacks json data file for diaphragm panels shaft"""
    data_dict = eval(StringIO(uploaded_file.getvalue().decode("utf-8")).read()) # data_dict is str representation of dict
    parameters = assign_session_state_parameters_shaft_diaphragm_panels(**eval(data_dict))             # eval str to get dict, then unpack
    return parameters


def load_parameters_from_json_file_dw(uploaded_file):
    """ Unpacks json data file for diaphragm panels wall"""
    data_dict = eval(StringIO(uploaded_file.getvalue().decode("utf-8")).read()) # data_dict is str representation of dict
    parameters = assign_session_state_parameters_wall_diaphragm_panels(**eval(data_dict))             # eval str to get dict, then unpack
    return parameters


def load_parameters_from_json_file_spw(uploaded_file):
    """ Unpacks json data file for secant pile wall"""
    data_dict = eval(StringIO(uploaded_file.getvalue().decode("utf-8")).read()) # data_dict is str representation of dict
    parameters = assign_session_state_parameters_wall_secant_piles(**eval(data_dict))             # eval str to get dict, then unpack
    return parameters


def assign_session_state_parameters_shaft_secant_piles(project_name="Sample project", project_revision="First issue, rev0", shaft_name="Shaft 1", di=10.0, D=1.2,
            n_pieces=40, L=30.5, v=0.5, H_drilling_platform=0.0, E=3.0e6, F_hoop_at_base=700.0, gamma_G=1.35, f_ck=10.0, alpha_cc=0.7, gamma_c=1.5, 
            check_more=False, F_hoop=500.0, L_hoop=10.0, **kwargs):
    """ Assigns parameters for session state for secant piled shaft"""
    parameters_updated = {"project_name": project_name, "project_revision": project_revision, "shaft_name": shaft_name, "di": di, "D": D,
            "n_pieces": n_pieces, "L": L, "v": v, "H_drilling_platform": H_drilling_platform, "E": E, "F_hoop_at_base": F_hoop_at_base, "gamma_G": gamma_G, "f_ck": f_ck, "alpha_cc": alpha_cc, "gamma_c": gamma_c, 
            "check_more": check_more, "F_hoop": F_hoop, "L_hoop": L_hoop}
    return parameters_updated

def assign_session_state_parameters_shaft_diaphragm_panels(project_name_dws="Sample project", project_revision_dws="First issue, rev0", shaft_name_dws="Shaft 1", di_dws=10.0, D_dws=1.2,
            B_dws=2.8, L_dws=30.5, v_dws=0.5, H_drilling_platform_dws=0.0, E_dws=3.0e6, F_hoop_at_base_dws=700.0, gamma_G_dws=1.35, f_ck_dws=10.0, alpha_cc_dws=0.7, gamma_c_dws=1.5, 
            check_more_dws=False, F_hoop_dws=500.0, L_hoop_dws=10.0, **kwargs):
    """ Assigns parameters for session state for secant piled shaft"""
    parameters_updated = {"project_name_dws": project_name_dws, "project_revision_dws": project_revision_dws, "shaft_name_dws": shaft_name_dws, "di_dws": di_dws, "D_dws": D_dws,
            "B_dws": B_dws, "L_dws": L_dws, "v_dws": v_dws, "H_drilling_platform_dws": H_drilling_platform_dws, "E_dws":E_dws, "F_hoop_at_base_dws": F_hoop_at_base_dws, "gamma_G_dws": gamma_G_dws, "f_ck_dws": f_ck_dws, "alpha_cc_dws": alpha_cc_dws, "gamma_c_dws": gamma_c_dws, 
            "check_more_dws": check_more_dws, "F_hoop_dws": F_hoop_dws, "L_hoop_dws": L_hoop_dws}
    return parameters_updated


def assign_session_state_parameters_wall_diaphragm_panels(project_name_dw="Sample project", project_revision_dw="First issue, rev0", wall_name_dw="Wall 1", D_dw=1.2,
            B_dw=2.8, L_dw=35.0, v_dw=0.5, H_drilling_platform_dw=0.0, E_dw=30.0e6, **kwargs):
    """ Assigns parameters for session state for secant piled shaft"""
    parameters_updated = {"project_name_dw": project_name_dw, "project_revision_dw": project_revision_dw, "wall_name_dw": wall_name_dw, "D_dw": D_dw,
            "B_dw": B_dw, "L_dw": L_dw, "v_dw": v_dw, "H_drilling_platform_dw": H_drilling_platform_dw, "E_dw":E_dw}
    return parameters_updated


def assign_session_state_parameters_wall_secant_piles(project_name_spw="Sample project", project_revision_spw="First issue, rev0", wall_name_spw="Wall 1", a_spw=0.75, D_spw=1.2,
            n_pieces_spw=10, L_spw=25.0, v_spw=0.75, H_drilling_platform_spw=0.0, E_spw=30.0e6, plotting_option_spw='Two piles apart', **kwargs):
    """ Assigns parameters for session state for secant piled wall"""
    parameters_updated = {"project_name_spw": project_name_spw, "project_revision_spw": project_revision_spw, "wall_name_spw": wall_name_spw, "a_spw": a_spw, "D_spw": D_spw,
            "n_pieces_spw": n_pieces_spw, "L_spw": L_spw, "v_spw": v_spw, "H_drilling_platform_spw": H_drilling_platform_spw, "E_spw":E_spw, "plotting_option_spw": plotting_option_spw}
    return parameters_updated



def create_download_link(val, filename):
    b64 = base64.b64encode(val).decode()  # val looks like b'...'
    href = f'<a href="data:application/octet-stream;base64,{b64}" download={filename}">Download file</a>'
    #href = f'<a download="{filename} "href="data:application/octet-stream;base64,{b64}">Download PDF file</a>'
    st.markdown(href, unsafe_allow_html=True)

#def export_as_pdf_bk():
#    pdf = FPDF
#    for fig in figs:
#        pdf.add_page()
#        with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
#            fig.savefig(tmpfile.name,bbox_inches="tight")#)
#            pdf.image(tmpfile.name)
#    html = create_download_link(pdf.output(dest="S").encode("latin-1"), "Resultatfil")
#    st.markdown(html, unsafe_allow_html=True)

def export_as_pdf(fig, output_file_name):
    #tfile = NamedTemporaryFile(delete=False)
    #pp = PdfPages(tfile)
    tfile = BytesIO()
    #for fig in figs:
    #    fig.savefig(buffered,format='PDF')#)
    fig.savefig(tfile, format='pdf')#)
    #fig.show()

    #pp_str = base64.b64encode(tfile).decode()
    pp_str = tfile.getvalue()
    create_download_link(pp_str, output_file_name)
    #st.write('Up here!!!')