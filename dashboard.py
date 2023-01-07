
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import numpy as np
from streamlit_option_menu import option_menu
import hydralit_components as hc
import webbrowser
import streamlit.components.v1 as components

THIS_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()
IMAGES_DIR = THIS_DIR / "images"
STYLES_DIR = THIS_DIR / "styles"
CSS_FILE = STYLES_DIR / "main.css"

def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title=" 🎯 RoK Analytics", layout="wide")

load_css_file(CSS_FILE)

col1,col2,col3 = st.columns([20,60,20])
with col1:
    st.subheader("")
with col2:
    st.title(" 🏛️ Welcome Mighty Governors 🏛️ ")
    st.markdown("##")
with col3:
    st.subheader("")

selected = option_menu(
                        menu_title=None,
                        options=["HomePage","DashBoard","Contact"],
                        icons=["house-door","columns-gap","envelope"],
                        default_index=0,
                        orientation="horizontal",
)

if selected == "HomePage":

    PRODUCT_TAGLINE = "Ready To Visualize KvK Performance? 🚀"
    PRODUCT_DESCRIPTION = """

    As Sun Tzu said to win first, Kingdom should know yourself and build the strategy according to the organized fighters.
    Examining KvK results will help you to know yourself and prepare kingdom for the next KvK.

    The Kvk dashboard provides you with an easy way to understand your strengths and weaknesses. 
    (Kills show field presence, Deads show flag/structure defense) 
            
    On the other hand, it helps the recruitment team to strengthen your weak parts while selecting players.

    **Let's start the tour:**
    - Prepare your data (Δkills, Δdeads, exclude cheaters)
    - Go to dashboard tab
    - Upload your data (apply template)
    - An awesome & informative dashboard will welcome you nicely
    - Check your results in detail
    - Get rid of deadweight
    - Build your new strategy


    **This is your new superpower; upgrade your kingdom to a new level!!**

    Dashboard is free!! If you are happy with your data visualization journey,             
    you can support me! 🫶
    """
    sun_DESC = """
        
        Victorious warriors win first and then go to war,             
        while defeated warriors go to war first and then seek to win.
        
        **Sun Tzu**    
        """
    col1, col2,col3 = st.columns([50,10,45])
    with col1:
        st.subheader(PRODUCT_TAGLINE)
        st.write(PRODUCT_DESCRIPTION)
        components.html(
            """
            <script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="TafaSensei" data-color="#FF5F5F" data-emoji="🎁"  data-font="Cookie" data-text="Buy me a Gold Chest" data-outline-color="#000000" data-font-color="#ffffff" data-coffee-color="#FFDD00" ></script>
            """
        )               
    with col2:
        st.subheader("")
    with col3:
        sun_image = Image.open(IMAGES_DIR / "sun_tzu.png")
        st.image(sun_image, width=550)
        st.write(sun_DESC)

if selected == "DashBoard":

    temp_DESC = """
        
        - Download the excel template            
        - Fill only 300 players
        - Do not change the number format!
        
        """
    temp_link = 'https://github.com/TafaSensei/RoKAnalytics/blob/main/template_data.xlsx'

    ### --- LOAD DATAFRAME
    col1, col2 = st.columns(2)
    with col1:
        st.info(temp_DESC)
        if st.button("Download Excel Template"):
            webbrowser.open(temp_link)
    with col2:
        uploaded_file = st.file_uploader("", type=['xlsx'])

    if uploaded_file:
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        #Float to integer of defined labels wrt percentiles
        df_pmin = int((np.percentile(df['Power'], 0)//5000000)*5)
        df_p25 = int((np.percentile(df['Power'], 25)//5000000)*5)
        df_p50 = int((np.percentile(df['Power'], 50)//5000000)*5)
        df_p60 = int((np.percentile(df['Power'], 60)//5000000)*5)
        df_p70 = int((np.percentile(df['Power'], 70)//5000000)*5)
        df_p80 = int((np.percentile(df['Power'], 80)//5000000)*5)
        df_p90 = int((np.percentile(df['Power'], 90)//5000000)*5)

        #concatenation example
        l_min = str(df_pmin) + '-' + str(df_p25)
        l_p25 = str(df_p25) + '-' + str(df_p50)
        l_p50 = str(df_p50) + '-' + str(df_p60)
        l_p60 = str(df_p60) + '-' + str(df_p70)
        l_p70 = str(df_p70) + '-' + str(df_p80)
        l_p80 = str(df_p80) + '-' + str(df_p90)
        l_p90 = 'over' + ' ' + str(df_p90)

        df['Power'] = df['Power']/1000000
        df['t5'] = df['t5']/1000000
        df['t4'] = df['t4']/1000000
        df['kills'] = df['kills']/1000000
        df['dead'] = df['dead']/1000000


        def Power_Label(value):
            if value >= df_p90:
                return l_p90
            elif df_p80 <= value < df_p90:
                return l_p80
            elif df_p70 <= value < df_p80:
                return l_p70
            elif df_p60 <= value < df_p70:
                return l_p60
            elif df_p50 <= value < df_p60:
                return l_p50
            elif df_p25 <= value < df_p50:
                return l_p25
            elif value < df_p25:
                return l_min
        
        df['Power_Label'] = df['Power'].map(Power_Label)

        def t5_Label(value):
            if value >=50:
                return "50+"
            elif 30 <= value < 50:
                return "30-50"
            elif 15 <= value < 30:
                return "15-30"
            elif 5<= value < 15:
                return "05-15"
            elif 0< value < 5:
                return "0-5"
            elif value == 0:
                return "0"
        
        df['t5_Label'] = df['t5'].map(t5_Label)

        def t4_Label(value):
            if value >=50:
                return "50+"
            elif 30 <= value < 50:
                return "30-50"
            elif 15 <= value < 30:
                return "15-30"
            elif 5<= value < 15:
                return "05-15"
            elif 0< value < 5:
                return "0-5"
            elif value == 0:
                return "0"
        
        df['t4_Label'] = df['t4'].map(t4_Label)

        def kills_Label(value):
            if value >=50:
                return "50+"
            elif 30 <= value < 50:
                return "30-50"
            elif 15 <= value < 30:
                return "15-30"
            elif 5<= value < 15:
                return "05-15"
            elif 0< value < 5:
                return "0-5"
            elif value == 0:
                return "0"
        
        df['kills_Label'] = df['kills'].map(kills_Label)

        def Deads_Label(value):
            if value >=5:
                return "5+"
            elif 3 <= value < 5:
                return "3-5"
            elif 1.5 <= value < 3:
                return "1.5-3"
            elif 0.5<= value < 1.5:
                return "0.5-1.5"
            elif 0 < value < 0.5:
                return "0-0.5"
            elif value == 0:
                return "0"
        
        df['Deads_Label'] = df['dead'].map(Deads_Label)

        # share in Kingdom Level
        df['KD_t5%'] = df['t5']/ sum(df.t5)
        df['t5_rank'] = pd.qcut(df['KD_t5%'],q=100,labels=False,duplicates='drop')

        df['KD_t4%'] = df['t4'] / sum(df.t4)
        df['t4_rank'] = pd.qcut(df['KD_t4%'],q=100,labels=False,duplicates='drop')

        df['KD_dead%'] = df['dead'] / sum(df.dead)
        df['dead_rank'] = pd.qcut(df['KD_dead%'],q=100,labels=False,duplicates='drop')

        # weighted kigdom share with t5=40%,t4=10% and dead=50%
        df['KD_All_in'] = df['KD_t5%']*0.4+df['KD_t4%']*0.1+df['KD_dead%']*0.5
        df['Contribution Within KD'] = pd.qcut(df['KD_All_in'],q=100,labels=False,duplicates='drop')

        # share in Power Label
        df['Label_t5%'] = df['t5'] / df.groupby('Power_Label')['t5'].transform('sum')
        df['Label_t4%'] = df['t4'] / df.groupby('Power_Label')['t4'].transform('sum')
        df['Label_dead%'] = df['dead'] / df.groupby('Power_Label')['dead'].transform('sum')

        # weighted Power Label share with t5=40%,t4=10% and dead=50%
        df['Label_All_in'] = df['Label_t5%']*0.4+df['Label_t4%']*0.1+df['Label_dead%']*0.5

        df['Contribution Within Power_Label'] = df.groupby(['Power_Label'])['Label_All_in'].transform(
                        lambda x: pd.qcut(x, 100,labels = False, duplicates='drop'))

        # Performance Point with Kingdom=60% and Label=40%
        df['PP'] = df['KD_All_in']*0.6+df['Label_All_in']*0.4
        df['Performance Point (PP)'] = pd.qcut(df['PP'],q=100,labels=False,duplicates='drop')

        # Performance Point with Kingdom=60% and Label=40%
        df['PP'] = df['KD_All_in']*0.6+df['Label_All_in']*0.4

        tab1, tab2, tab3 = st.tabs(["Overview", "Kills", "Deads"])

        with tab1:
            # TOP KPI's

            sum_power=round(sum(df.Power),1)
            sum_number=len(df.Username)
            sum_kills=round(sum(df.kills),1)
            sum_dead=round(sum(df.dead),1)

            #can apply customisation to almost all the properties of the card, including the progress bar
            theme_bad = {'bgcolor': '#FFF0F0','title_color': 'red','content_color': 'red','icon_color': 'red', 'icon': 'fa fa-times-circle'}
            theme_neutral = {'bgcolor': '#f9f9f9','title_color': 'orange','content_color': 'orange','icon_color': 'orange', 'icon': 'bi bi-bank'}
            theme_good = {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}
            theme_neutral2 = {'bgcolor': '#f9f9f9','title_color': 'skyblue','content_color': 'skyblue','icon_color': 'skyblue', 'icon': 'bi bi-people'}


            cc = st.columns(4)

            with cc[0]:
            # can just use 'good', 'bad', 'neutral' sentiment to auto color the card
                hc.info_card(title='Power:', content=f"{sum_power:,}", bar_value=85,theme_override=theme_neutral)

            with cc[1]:
                hc.info_card(title='Kills:', content=f"{sum_kills:,}", bar_value=70,theme_override=theme_good)

            with cc[2]:
                hc.info_card(title='Deads:', content=f"{sum_dead:,}", bar_value=35,theme_override=theme_bad)

            with cc[3]:
            #customise the the theming for a neutral content
                hc.info_card(title='Players:',content=f"{sum_number:,}", bar_value=90,theme_override=theme_neutral2)

        #Donut Chart

            df_grouped_power=df.groupby(by=['Power_Label']).count()[['Username']]
            df_grouped_power = df_grouped_power.rename(columns={'Username': '#_of_players'})
            df_grouped_power = df_grouped_power.reset_index()

            fig_donut_power = px.pie(df_grouped_power, hole=0.5,
                                values= '#_of_players',
                                names= 'Power_Label')

            fig_donut_power.update_traces(textposition='inside', textinfo='percent', rotation=90,
                                        marker=dict(line=dict(width=2,color='white')))

            fig_donut_power.update_layout(margin=dict(t=70, b=30, l=0, r=0), showlegend=True,
                                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    title_font=dict(size=27, color='#222A2A', family="Lato, sans-serif"),
                                    font=dict(size=15, color='#222A2A'),
                                    legend=dict(font=dict(size=17),
                                                yanchor="top",y=0.99,xanchor="left",x=0.01),
                                    annotations=[dict(text='<b>Number of Players</b>', x=0.5, y=0.5, 
                                                    font=dict(family="Comic Sans, sans-serif",
                                                            size=16,
                                                            color="slateblue"), 
                                                    showarrow=False)])
            
            PRODUCT_DESCRIPTION = """
            
            Firstly, we will start with defining power labels according to your data:

            - Power labels are generated by using percentiles
            - Your kingdom is divided in 7 groups based on:
                - Min (0%)
                - 25%th percentile
                - 50% (median)
                - 60%th percentile
                - 70%th percentile
                - 80%th percentile
                - 90%th percentile
            - Players are approxiamtely divided equally after median (50%th percentile) because mostly players between 35% and 50% of the kingdom are not playing efficiently
            """
            col1, col2, col3 = st.columns([10,65,35])
            with col1:
                st.subheader("")           
            with col2:
                st.plotly_chart(fig_donut_power,use_container_width=True)
            with col3:
                st.write(PRODUCT_DESCRIPTION)

        with tab2:
        #Kills Donut Chart

            df_kills_power=df.groupby(by=['Power_Label']).sum()
            df_kills_power = df_kills_power.reset_index()

            fig_donut_kills = px.pie(df_kills_power, hole=0.5,
                                values= 'kills',
                                names= 'Power_Label')

            fig_donut_kills.update_traces(textposition='inside', textinfo='percent', rotation=90,
                                        marker=dict(line=dict(width=2,color='white')))

            fig_donut_kills.update_layout(margin=dict(t=70, b=30, l=0, r=0), showlegend=True,
                                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    title_font=dict(size=30, color='#222A2A', family="Lato, sans-serif"),
                                    font=dict(size=17, color='#222A2A'),
                                    legend=dict(font=dict(size=12),
                                                yanchor="top",y=0.99,xanchor="left",x=0.01),
                                    annotations=[dict(text='<b>Kills</b>', x=0.5, y=0.5, 
                                                    font=dict(family="Comic Sans, sans-serif",
                                                            size=18 ,
                                                            color="slateblue"),  showarrow=False)])

            #t5 Donut Chart

            fig_donut_kills_t5 = px.pie(df_kills_power, height=350, width=250, hole=0.5,
                                values= 't5',
                                names= 'Power_Label')

            fig_donut_kills_t5.update_traces(textposition='inside', textinfo='percent', rotation=90,
                                        marker=dict(line=dict(width=2,color='white')))

            fig_donut_kills_t5.update_layout(margin=dict(t=70, b=30, l=0, r=0), showlegend=True,
                                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    title_font=dict(size=15, color='#222A2A', family="Lato, sans-serif"),
                                    font=dict(size=10, color='#222A2A'),
                                    annotations=[dict(text='<b>T5</b>', x=0.5, y=0.5,  
                                                    font=dict(family="Comic Sans, sans-serif",
                                                            size=18 ,
                                                            color="slateblue"), showarrow=False)])

            #t4 Donut Chart

            fig_donut_kills_t4 = px.pie(df_kills_power, height=350, width=250, hole=0.5,
                                values= 't4',
                                names= 'Power_Label')

            fig_donut_kills_t4.update_traces(textposition='inside', textinfo='percent', rotation=90,
                                        marker=dict(line=dict(width=2,color='white')))

            fig_donut_kills_t4.update_layout(margin=dict(t=70, b=30, l=0, r=0), showlegend=True,
                                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    title_font=dict(size=15, color='#222A2A', family="Lato, sans-serif"),
                                    font=dict(size=10, color='#222A2A'),
                                    annotations=[dict(text='<b>T4</b>', x=0.5, y=0.5,  
                                                    font=dict(family="Comic Sans, sans-serif",
                                                            size=18 ,
                                                            color="slateblue"), showarrow=False)])

            #Combine t5 & t4 in a row
            col1, col2 = st.columns([0.8,1.2])

            with col1:
                st.subheader("")
                st.info(" 💡 Kills Distribution by Power Label ")
                st.subheader(" ")
                st.plotly_chart(fig_donut_kills)

            with col2:
                st.plotly_chart(fig_donut_kills_t5,use_container_width=True)
                st.plotly_chart(fig_donut_kills_t4,use_container_width=True)

            #Funnel Chart for Kills

            df_grouped_kills=df.groupby(by=['kills_Label']).count()[['Username']]
            df_grouped_kills = df_grouped_kills.rename(columns={'Username': '#_of_players'})
            df_grouped_kills = df_grouped_kills.reset_index()

            fig_kills_label = px.funnel(df_grouped_kills, 
                                        x='#_of_players', 
                                        y='kills_Label',
                                        title='Kills Distribution (#)',
                                        height=450, 
                                        width=700, 
                                        color_discrete_sequence=['#F67280'])

            fig_kills_label.update_xaxes(showgrid=False, ticksuffix=' ', showline=True)
            fig_kills_label.update_traces(marker=dict(line=dict(width=4,color='white')),textfont=dict(size=14,color='white'))
            fig_kills_label.update_layout(margin=dict(t=70, b=30, l=70, r=40),
                                    xaxis_title=' ', yaxis_title=" ",
                                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    title_font=dict(size=20, color='#222A2A', family="Lato, sans-serif"),
                                    font=dict(color='#222A2A'))

            col1, col2, col3 = st.columns([0.3,1.4,0.3])

            with col1:
                st.subheader(" ")
            with col2:
                st.plotly_chart(fig_kills_label,use_container_width=True)
                st.info(" 💡 You can easily see how many players have how many kills according to kills range! ")
            with col3:
                st.subheader(" ")

            #Waterfall Chart

            df_grouped_t5=df.groupby(by=['t5_Label']).count()[['Username']]
            df_grouped_t5 = df_grouped_t5.rename(columns={'Username': '#_of_players'})
            df_grouped_t5 = df_grouped_t5.reset_index()

            fig_t5_label = go.Figure(go.Waterfall(
                orientation = "v", 
                x = df_grouped_t5['t5_Label'],
                textposition = "outside",
                text = df_grouped_t5['#_of_players'],
                y = df_grouped_t5['#_of_players'],
                connector = {"line":{"color":"white"}},
                increasing = {"marker":{"color":"orange"}},
                decreasing = {"marker":{"color":"orange"}}
            ))

            fig_t5_label.update_xaxes(showgrid=False)
            fig_t5_label.update_yaxes(showgrid=False, visible=False)
            fig_t5_label.update_traces(hovertemplate=None)
            fig_t5_label.update_layout(title='t5 Killers Distribution (#)',
                            margin=dict(t=100, b=50, l=100, r=70),
                            hovermode="x unified",
                            xaxis_title=' ', yaxis_title=" ",
                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                            title_font=dict(size=20, color='#222A2A', family="Lato, sans-serif"),
                            font=dict(color='#222A2A'))

            df_grouped_t4=df.groupby(by=['t4_Label']).count()[['Username']]
            df_grouped_t4 = df_grouped_t4.rename(columns={'Username': '#_of_players'})
            df_grouped_t4 = df_grouped_t4.reset_index()

            fig_t4_label = go.Figure(go.Waterfall(
                orientation = "v", 
                x = df_grouped_t4['t4_Label'],
                textposition = "outside",
                text = df_grouped_t4['#_of_players'],
                y = df_grouped_t4['#_of_players'],
                connector = {"line":{"color":"white"}},
                increasing = {"marker":{"color":"green"}},
                decreasing = {"marker":{"color":"green"}}
            ))

            fig_t4_label.update_xaxes(showgrid=False)
            fig_t4_label.update_yaxes(showgrid=False, visible=False)
            fig_t4_label.update_traces(hovertemplate=None)
            fig_t4_label.update_layout(title='t4 Killers Distribution (#)',
                            margin=dict(t=100, b=50, l=100, r=70),
                            hovermode="x unified",
                            xaxis_title=' ', yaxis_title=" ",
                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                            title_font=dict(size=20, color='#222A2A', family="Lato, sans-serif"),
                            font=dict(color='#222A2A'))

            col_1, col_2 = st.columns([1, 1])
            col_1.plotly_chart(fig_t5_label,use_container_width=True)
            col_2.plotly_chart(fig_t4_label,use_container_width=True)

        with tab3:
            
            #Deads Donut Chart

            fig_donut_deads = px.pie(df_kills_power, hole=0.5,
                                values= 'dead',
                                title='Deads Distribution by Power Label',
                                names= 'Power_Label')

            fig_donut_deads.update_traces(textposition='inside', textinfo='percent', rotation=90,
                                        marker=dict(line=dict(width=2,color='white')))

            fig_donut_deads.update_layout(margin=dict(t=70, b=30, l=0, r=0), showlegend=True,
                                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    title_font=dict(size=20, color='#222A2A', family="Lato, sans-serif"),
                                    font=dict(size=13, color='#222A2A'),
                                    legend=dict(orientation="h", font=dict(size=11)),
                                    annotations=[dict(text='<b>Deads</b>', x=0.5, y=0.5,  
                                                    font=dict(family="Comic Sans, sans-serif",
                                                            size=18 ,
                                                            color="slateblue"),  showarrow=False)])

            #Funnel Chart for Deads

            df_grouped_deads=df.groupby(by=['Deads_Label']).count()[['Username']]
            df_grouped_deads = df_grouped_deads.rename(columns={'Username': '#_of_players'})
            df_grouped_deads = df_grouped_deads.reset_index()

            fig_dead_label = px.funnel(df_grouped_deads, 
                                        x='#_of_players', 
                                        y='Deads_Label',
                                        title='Deads Distribution (#)',
                                        height=450, 
                                        width=600, 
                                        color_discrete_sequence=['#348781'])

            fig_dead_label.update_xaxes(showgrid=False, ticksuffix=' ', showline=True)
            fig_dead_label.update_traces(marker=dict(line=dict(width=4,color='white')))
            fig_dead_label.update_layout(margin=dict(t=70, b=20, l=40, r=0),
                                    xaxis_title=' ', yaxis_title=" ",
                                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    title_font=dict(size=22, color='#222A2A', family="Lato, sans-serif"),
                                    font=dict(color='#222A2A'))

            col1, col2 = st.columns([1,1])

            with col1:
                st.plotly_chart(fig_donut_deads,use_container_width=True)
            with col2:
                st.plotly_chart(fig_dead_label,use_container_width=True)
        
if selected == "Contact":

    col1, col2,col3 = st.columns([0.4,1.2,0.4])
    with col1:
        st.subheader("")
    with col2:
        st.title("Tools for Competitive Kingdoms")
        st.subheader("")
    with col3:
        st.subheader("")

    col1, col2 = st.columns([1.15,1])
    with col1:
        lead_image25 = Image.open(IMAGES_DIR / "lead_25.png")
        st.image(lead_image25)

    with col2:
        lead_image5 = Image.open(IMAGES_DIR / "lead_5.png")
        st.image(lead_image5)

    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader("Performance Monitoring")
        comp_tool_image = Image.open(IMAGES_DIR / "compare_tool.png")
        st.image(comp_tool_image)

    with col2:
        st.subheader(" ")
        comp_tool_exp_img = Image.open(IMAGES_DIR / "exp_comp_tool.png")
        st.image(comp_tool_exp_img)

    col1, col2 = st.columns([1,1])

    with col1:
        st.write("")
        st.subheader(":mailbox: How to get tools? 💸 Ask Away 🙌")
        contact_form = f"""
        <form action="https://formsubmit.co/{"usman.mustafa88@gmail.com"}" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here"></textarea>
            <button type="submit" class="button">Send ✉</button>
        </form>
        """
        st.markdown(contact_form, unsafe_allow_html=True)
        st.write("")
    with col2:
        product_image = Image.open(IMAGES_DIR / "post_box.jpg")
        st.image(product_image)
    
    st.info("*Also open for recommendations! Just send an e-mail 👆 Constructive critism is always acceptable :)")

