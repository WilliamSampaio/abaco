from abaco.dataframes import load_posicoes_df
import matplotlib.pyplot as plt

title = 'Dashboard'


def page_dashboard():

    import streamlit as st

    df = load_posicoes_df()

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = df['ticker']
    sizes = df['valor_total']
    # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # st.pyplot(fig1)

    st.write('# ' + title)
    st.divider()

    row = st.columns([1, 0.5])

    row[0].success('oi')
    row[1].pyplot(fig1)

    st.dataframe(df.iloc['ticker'])

    st.dataframe(df)
