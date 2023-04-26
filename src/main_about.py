
def main_about(st):
    """ About and known issues"""
    st.header('Known issues')
    st.write('The Web-App appears not running when VPN connection is active.')
    st.write("""If you observe some strange behavior or know that certain calculations are not correct, please help inform us.
        Input and suggestions are welcome. Thanks!""")

    st.header('Planned implementations')
    st.write('The following items/ applications are to be implemented when time allows')
    st.markdown("""
        - Printing PDF reports
        - Application for building Plaxis2D model with calculation steps via Plaxis2D's Python API
        - Application for reinforced concrete dimensioning for wall's section forces calculated by Plaxis2D/ Plaxis3D
    """)