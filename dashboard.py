
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import numpy as np
from streamlit_option_menu import option_menu
import hydralit_components as hc
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

logo_image = Image.open(IMAGES_DIR / "rok_logo.png")
col1,col2,col3 = st.columns([5,40,65])
with col2:
    st.image(logo_image,width=400)
with col3:
    st.subheader("")
    st.subheader("")
    st.title("🏛️ Welcome Mighty Governors 🏛️")

selected = option_menu(
                        menu_title=None,
                        options=["HomePage","RoK Analytics","Contact"],
                        icons=["house-door","graph-up-arrow","envelope"],
                        default_index=0,
                        orientation="horizontal",
)

if selected == "HomePage": 

    PRODUCT_TAGLINE = "🚀 Ready To Visualize KvK Performance? 🚀"
    PRODUCT_DESCRIPTION = """

    As Sun Tzu said to win first, Kingdom should know yourself and build the strategy according to the organized fighters.
    Examining KvK results will help you to know yourself and prepare kingdom for the next KvK.

    The Kvk dashboard provides you with an easy way to understand your strengths and weaknesses. 
    (Kills show field presence, Deads show flag/structure defense) 
            
    On the other hand, it helps the recruitment team to strengthen your weak parts while selecting players.

    **Let's start the tour:**
    - Prepare your data (Δkills, Δdeads, exclude cheaters)
    - Go to RoK Analytics tab
    - Upload your data (apply template)
    - An awesome & informative dashboard will welcome you nicely 🎯
    - Check your results in detail
    - Monitor & Comparison tab is for players 🙌
    - In detailed statistics, leadership can find a good system to define deadweights 🤫
    - Last but not least, Leaderboards 👑
        - Motivate Warriors
        - Encourage Governors


    **This is your new superpower; upgrade your kingdom to a new level!!**
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
    with col2:
        st.subheader("")
    with col3:
        sun_image = Image.open(IMAGES_DIR / "sun_tzu.png")
        st.image(sun_image, width=500)
        st.write(sun_DESC)

if selected == "RoK Analytics":

    temp_DESC = """
        
        - Download the excel template            
        - Fill only 300 players
        - Do not change the number format!
        - Do not leave empty cells who has Username!
        - Template Link = 'https://rb.gy/cgzq36'

        """
    ### --- LOAD DATAFRAME
    col1, col2 = st.columns(2)
    with col1:
        st.info(temp_DESC)
        components.html(
            """
            <script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="TafaSensei" data-color="#FF5F5F" data-emoji="🎁"  data-font="Cookie" data-text="Buy me a Gold Chest" data-outline-color="#000000" data-font-color="#ffffff" data-coffee-color="#FFDD00" ></script>
            """
        )
    with col2:
        uploaded_file = st.file_uploader("", type=['xlsx'])

    col1,col2,col3 = st.columns([12.5,75,12.5])
    with col2:
        selected = option_menu(
                            menu_title=None,
                            options=["DashBoard","LeaderBoard"],
                            icons=["columns-gap","bar-chart"],
                            default_index=0,
                            orientation="horizontal")

    if uploaded_file:
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        def human_format(num):
            magnitude = 0
            while abs(num) >= 1000:
                magnitude += 1
                num /= 1000.0
            # add more suffixes if you need them
            return '%.0f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

        def human_format2(num):
            magnitude = 0
            while abs(num) >= 1000:
                magnitude += 1
                num /= 1000.0
            # add more suffixes if you need them
            return '%.1f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])
        
        def make_grid(cols,rows):
            grid = [0]*cols
            for i in range(cols):
                with st.container():
                    grid[i] = st.columns(rows)
            return grid

        df_pmin = int((np.percentile(df['Power'], 0)//5000000)*5000000)
        df_p25 = int((np.percentile(df['Power'], 10)//5000000)*5000000)
        df_p50 = int((np.percentile(df['Power'], 30)//5000000)*5000000)
        df_p60 = int((np.percentile(df['Power'], 60)//5000000)*5000000)
        df_p70 = int((np.percentile(df['Power'], 75)//5000000)*5000000)
        df_p80 = int((np.percentile(df['Power'], 85)//5000000)*5000000)
        df_p90 = int((np.percentile(df['Power'], 95)//5000000)*5000000)

        #concatenation example
        l_min = str(human_format(df_pmin)) + '-' + str(human_format(df_p25))
        l_p25 = str(human_format(df_p25)) + '-' + str(human_format(df_p50))
        l_p50 = str(human_format(df_p50)) + '-' + str(human_format(df_p60))
        l_p60 = str(human_format(df_p60)) + '-' + str(human_format(df_p70))
        l_p70 = str(human_format(df_p70)) + '-' + str(human_format(df_p80))
        l_p80 = str(human_format(df_p80)) + '-' + str(human_format(df_p90))
        l_p90 = 'over' + ' ' + str(human_format(df_p90))

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
            if value >=50000000:
                return "50M+"
            elif 30000000 <= value < 50000000:
                return "30M-50M"
            elif 15000000 <= value < 30000000:
                return "15M-30M"
            elif 5000000<= value < 15000000:
                return "05M-15M"
            elif 0< value < 5000000:
                return "0-5M"
            elif value == 0:
                return "0"
                
        df['t5_Label'] = df['t5'].map(t5_Label)

        def t4_Label(value):
            if value >=50000000:
                return "50M+"
            elif 30000000 <= value < 50000000:
                return "30M-50M"
            elif 15000000 <= value < 30000000:
                return "15M-30M"
            elif 5000000 <= value < 15000000:
                return "05M-15M"
            elif 0 < value < 5000000:
                return "0-5M"
            elif value == 0:
                return "0"
                
        df['t4_Label'] = df['t4'].map(t4_Label)

        def kills_Label(value):
            if value >=50000000:
                return "50M+"
            elif 30000000 <= value < 50000000:
                return "30M-50M"
            elif 15000000 <= value < 30000000:
                return "15M-30M"
            elif 5000000 <= value < 15000000:
                return "05M-15M"
            elif 0 < value < 5000000:
                return "0-5M"
            elif value == 0:
                return "0"
                
        df['kills_Label'] = df['kills'].map(kills_Label)

        def Deads_Label(value):
            if value >=5000000:
                return "5M+"
            elif 3000000 <= value < 5000000:
                return "3M-5M"
            elif 1500000 <= value < 3000000:
                return "1.5M-3M"
            elif 500000 <= value < 1500000:
                return "0.5M-1.5M"
            elif 0 < value < 500000:
                return "0-0.5M"
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

        if selected == "DashBoard":
            
            #Averages
            #Kills
            df_nonzero_kills=df[df['kills']!=0]
            df_avg_kills=human_format2(df_nonzero_kills.kills.mean())
            #st.write(df_avg_kills)

            df_nonzero_t5=df[df['t5']!=0]
            df_avg_t5=human_format2(df_nonzero_t5.t5.mean())
            #st.write(df_avg_t5)

            df_nonzero_t4=df[df['t4']!=0]
            df_avg_t4=human_format2(df_nonzero_t4.t4.mean())
            #st.write(df_avg_t4)

            #Deads
            df_nonzero_dead=df[df['dead']!=0]
            df_avg_dead=human_format2(df_nonzero_dead.dead.mean())
            #st.write(df_avg_dead)


            #by Power Label

            df_nz_kills=df[["Username","kills","Power_Label"]]
            df_nz_kills=df_nz_kills[df_nz_kills['kills']!=0]
            df_avg_power_kills=df_nz_kills.groupby(by=['Power_Label']).mean()
            df_avg_power_kills=df_avg_power_kills.rename(columns={'Power_Label': 'kills'})
            df_avg_power_kills=df_avg_power_kills.reset_index()
            kill0=human_format2(df_avg_power_kills.kills.loc[0])
            kill1=human_format2(df_avg_power_kills.kills.loc[1])
            kill2=human_format2(df_avg_power_kills.kills.loc[2])
            kill3=human_format2(df_avg_power_kills.kills.loc[3])
            kill4=human_format2(df_avg_power_kills.kills.loc[4])
            kill5=human_format2(df_avg_power_kills.kills.loc[5])
            kill6=human_format2(df_avg_power_kills.kills.loc[6])
            df_avg_power_kills['kills2'] = [kill0,kill1,kill2,kill3,kill4,kill5,kill6]
            #st.write(df_avg_power_kills)

            df_nz_t5=df[["Username","t5","Power_Label"]]
            df_nz_t5=df_nz_t5[df_nz_t5['t5']!=0]
            df_avg_power_t5=df_nz_t5.groupby(by=['Power_Label']).mean()
            df_avg_power_t5=df_avg_power_t5.rename(columns={'Power_Label': 't5'})
            df_avg_power_t5=df_avg_power_t5.reset_index()
            t50=human_format2(df_avg_power_t5.t5.loc[0])
            t51=human_format2(df_avg_power_t5.t5.loc[1])
            t52=human_format2(df_avg_power_t5.t5.loc[2])
            t53=human_format2(df_avg_power_t5.t5.loc[3])
            t54=human_format2(df_avg_power_t5.t5.loc[4])
            t55=human_format2(df_avg_power_t5.t5.loc[5])
            t56=human_format2(df_avg_power_t5.t5.loc[6])
            df_avg_power_t5['t5_2'] = [t50,t51,t52,t53,t54,t55,t56]
            #st.write(df_avg_power_t5)

            df_nz_t4=df[["Username","t4","Power_Label"]]
            df_nz_t4=df_nz_t4[df_nz_t4['t4']!=0]
            df_avg_power_t4=df_nz_t4.groupby(by=['Power_Label']).mean()
            df_avg_power_t4=df_avg_power_t4.rename(columns={'Power_Label': 't4'})
            df_avg_power_t4=df_avg_power_t4.reset_index()
            t40=human_format2(df_avg_power_t4.t4.loc[0])
            t41=human_format2(df_avg_power_t4.t4.loc[1])
            t42=human_format2(df_avg_power_t4.t4.loc[2])
            t43=human_format2(df_avg_power_t4.t4.loc[3])
            t44=human_format2(df_avg_power_t4.t4.loc[4])
            t45=human_format2(df_avg_power_t4.t4.loc[5])
            t46=human_format2(df_avg_power_t4.t4.loc[6])
            df_avg_power_t4['t4_2'] = [t40,t41,t42,t43,t44,t45,t46]
            #st.write(df_avg_power_t4)

            #Deads by power label
            df_nz_dead=df[["Username","dead","Power_Label"]]
            df_nz_dead=df_nz_dead[df_nz_dead['dead']!=0]
            df_avg_power_dead=df_nz_dead.groupby(by=['Power_Label']).mean()
            df_avg_power_dead=df_avg_power_dead.rename(columns={'Power_Label': 'dead'})
            df_avg_power_dead=df_avg_power_dead.reset_index()
            dead0=human_format2(df_avg_power_dead.dead.loc[0])
            dead1=human_format2(df_avg_power_dead.dead.loc[1])
            dead2=human_format2(df_avg_power_dead.dead.loc[2])
            dead3=human_format2(df_avg_power_dead.dead.loc[3])
            dead4=human_format2(df_avg_power_dead.dead.loc[4])
            dead5=human_format2(df_avg_power_dead.dead.loc[5])
            dead6=human_format2(df_avg_power_dead.dead.loc[6])
            df_avg_power_dead['dead2'] = [dead0,dead1,dead2,dead3,dead4,dead5,dead6]
            #st.write(df_avg_power_dead)

            tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Kills", "Deaths", "Monitor & Comparison"])

            with tab1:

                st.subheader("")

                # TOP KPI's
                sum_power=human_format2(sum(df.Power))
                sum_number=len(df.Username)
                sum_kills=human_format2(sum(df.kills))
                sum_dead=human_format2(sum(df.dead))

                #can apply customisation to almost all the properties of the card, including the progress bar
                theme_bad = {'bgcolor': '#FFF0F0','title_color': 'red','content_color': 'red','icon_color': 'red', 'icon': 'fa fa-times-circle'}
                theme_neutral = {'bgcolor': '#f9f9f9','title_color': 'orange','content_color': 'orange','icon_color': 'orange', 'icon': 'bi bi-bank'}
                theme_good = {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}
                theme_neutral2 = {'bgcolor': '#f9f9f9','title_color': 'skyblue','content_color': 'skyblue','icon_color': 'skyblue', 'icon': 'bi bi-people'}


                cc = st.columns(4)

                with cc[0]:
                # can just use 'good', 'bad', 'neutral' sentiment to auto color the card
                    hc.info_card(title='Power:', content=sum_power, bar_value=85,theme_override=theme_neutral)

                with cc[1]:
                    hc.info_card(title='Kills:', content=sum_kills, bar_value=70,theme_override=theme_good)

                with cc[2]:
                    hc.info_card(title='Deaths:', content=sum_dead, bar_value=35,theme_override=theme_bad)

                with cc[3]:
                #customise the the theming for a neutral content
                    hc.info_card(title='Players:',content=sum_number, bar_value=90,theme_override=theme_neutral2)
                
                st.title("")

            #Donut Chart

                df_grouped_power=df.groupby(by=['Power_Label']).count()[['Username']]
                df_grouped_power = df_grouped_power.rename(columns={'Username': '#_of_players'})
                df_grouped_power = df_grouped_power.reset_index()

                fig_donut_power = px.pie(df_grouped_power, hole=0.5,
                                    values= '#_of_players',
                                    names= 'Power_Label')

                fig_donut_power.update_traces(textposition='inside', textinfo='percent', rotation=90,
                                            marker=dict(line=dict(width=2,color='white')))

                fig_donut_power.update_layout(margin=dict(t=70, b=30, l=0, r=0),
                                        width=750, height=425,
                                        showlegend=True,
                                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                        title_font=dict(size=27, color='#222A2A', family="Lato, sans-serif"),
                                        font=dict(size=15, color='#222A2A'),
                                        legend=dict(font=dict(size=13),
                                                    yanchor="top",y=0.99,xanchor="left",x=0.01),
                                        annotations=[dict(text='<b>Number of Players</b>', x=0.5, y=0.5, 
                                                        font=dict(family="Comic Sans, sans-serif",
                                                                size=14,
                                                                color="slateblue"), 
                                                        showarrow=False)])
                
                PRODUCT_DESCRIPTION = """
                
                Firstly, we will start with defining power labels according to your data:

                - Power labels are generated by using percentiles
                - Your kingdom is divided in 7 groups based on:
                    - Min (0%)
                    - 10%th percentile
                    - 30%th percentile
                    - 60%th percentile
                    - 75%th percentile
                    - 85%th percentile
                    - 95%th percentile
                """
                col1, col2, col3 = st.columns([10,45,35])
                with col1:
                    st.subheader("")           
                with col2:
                    st.plotly_chart(fig_donut_power,use_container_width=True)
                with col3:
                    st.write(PRODUCT_DESCRIPTION)

                st.title("")
                st.title("")
                #Total Kills Average by Power Label

                fig_Avg_kills = go.Figure()
                fig_Avg_kills.add_trace(go.Bar(
                    y=df_avg_power_kills.Power_Label,
                    x=df_avg_power_kills.kills,
                    textposition = "inside",  
                    text = df_avg_power_kills['kills2'],
                    orientation='h',
                    marker=dict(
                        color='rgba(50, 171, 96, 0.7)',
                        line=dict(color='rgba(50, 171, 96, 1)', width=1)
                    )
                ))

                fig_Avg_kills.update_layout(title='<b>Total Kills Average by Power Label</b>',
                                margin=dict(t=100, b=50, l=100, r=70),
                                width=600, height=350,
                                xaxis_title=' ', yaxis_title=" ",
                                xaxis={'visible': False, 'showticklabels': False},
                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                title_font=dict(size=14, color='#222A2A', family="Lato, sans-serif"),
                                font=dict(color='#222A2A'))

                #Total Dead Average by Power Label

                fig_Avg_deads = go.Figure()
                fig_Avg_deads.add_trace(go.Bar(
                    y=df_avg_power_dead.Power_Label,
                    x=df_avg_power_dead.dead,
                    textposition = "inside",  
                    text = df_avg_power_dead['dead2'],
                    orientation='h',
                    marker=dict(
                        color='rgba(246, 78, 139, 0.7)',
                        line=dict(color='rgba(246, 78, 139, 1)', width=1)
                    )
                ))

                fig_Avg_deads.update_layout(title='<b>Deaths Average by Power Label</b>',
                                margin=dict(t=100, b=50, l=100, r=70),
                                width=600, height=350,
                                xaxis_title=' ', yaxis_title=" ",
                                xaxis={'visible': False, 'showticklabels': False},
                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                title_font=dict(size=14, color='#222A2A', family="Lato, sans-serif"),
                                font=dict(color='#222A2A'))

                #Total t5 Average by Power Label

                fig_Avg_t5s = go.Figure()
                fig_Avg_t5s.add_trace(go.Bar(
                    y=df_avg_power_t5.Power_Label,
                    x=df_avg_power_t5.t5,
                    textposition = "inside",  
                    text = df_avg_power_t5['t5_2'],
                    orientation='h',
                    marker=dict(
                        color='rgba(242, 183, 1, 0.7)',
                        line=dict(color='rgba(242, 183, 1, 1)', width=1)
                    )
                ))

                fig_Avg_t5s.update_layout(title='<b>T5 Kills Average by Power Label</b>',
                                margin=dict(t=100, b=20, l=70, r=70),
                                width=450, height=300,
                                xaxis_title=' ', yaxis_title=" ",
                                xaxis={'visible': False, 'showticklabels': False},
                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                title_font=dict(size=14, color='#222A2A', family="Lato, sans-serif"),
                                font=dict(color='#222A2A'))

                #Total t4 Average by Power Label

                fig_Avg_t4s = go.Figure()
                fig_Avg_t4s.add_trace(go.Bar(
                    y=df_avg_power_t4.Power_Label,
                    x=df_avg_power_t4.t4,
                    textposition = "inside",  
                    text = df_avg_power_t4['t4_2'],
                    orientation='h',
                    marker=dict(
                        color='rgba(0, 134, 149, 0.6)',
                        line=dict(color='rgba(0, 134, 149, 1)', width=1)
                    )
                ))

                fig_Avg_t4s.update_layout(title='<b>T4 Kills Average by Power Label</b>',
                                margin=dict(t=100, b=20, l=70, r=70),
                                width=450, height=300,
                                xaxis_title=' ', yaxis_title=" ",
                                xaxis={'visible': False, 'showticklabels': False},
                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                title_font=dict(size=14, color='#222A2A', family="Lato, sans-serif"),
                                font=dict(color='#222A2A'))

                with st.container():
                    mygrid = make_grid(5,9)
                    st.markdown("""
                                    <style>
                                    div[data-testid="metric-container"] {
                                    background-color: rgba(28, 131, 225, 0.1);
                                    border: 1px solid rgba(28, 131, 225, 0.1);
                                    padding: 5% 5% 5% 2%;
                                    border-radius: 10px;
                                    color: rgb(30, 103, 119);
                                    overflow-wrap: break-word;
                                    }
                                    </style>
                                    """
                                    , unsafe_allow_html=True)
                    
                    mygrid[0][4].metric("Averages 🎪","")
                    mygrid[1][3].metric("Kills ⚔️",df_avg_kills)
                    mygrid[1][5].metric("Deaths ☠️",df_avg_dead)
                    mygrid[1][2].metric(label="T5 Kills ⚔️",value="",delta=df_avg_t5)
                    mygrid[2][2].metric(label="T4 Kills ⚔️",value="",delta=df_avg_t4)
                    mygrid[3][0].plotly_chart(fig_Avg_kills)
                    mygrid[3][5].plotly_chart(fig_Avg_deads)
                    mygrid[4][0].plotly_chart(fig_Avg_t5s)
                    mygrid[4][3].plotly_chart(fig_Avg_t4s)

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
                                        width=750, height=425,
                                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                        title_font=dict(size=30, color='#222A2A', family="Lato, sans-serif"),
                                        font=dict(size=17, color='#222A2A'),
                                        legend=dict(font=dict(size=11),
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
                                        width=500, height=325,
                                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                        font=dict(size=10, color='#222A2A'),
                                        annotations=[dict(text='<b>T5</b>', x=0.5, y=0.5,  
                                                        font=dict(family="Comic Sans, sans-serif",
                                                                size=15 ,
                                                                color="slateblue"), showarrow=False)])

                #t4 Donut Chart

                fig_donut_kills_t4 = px.pie(df_kills_power, height=350, width=250, hole=0.5,
                                    values= 't4',
                                    names= 'Power_Label')

                fig_donut_kills_t4.update_traces(textposition='inside', textinfo='percent', rotation=90,
                                            marker=dict(line=dict(width=2,color='white')))

                fig_donut_kills_t4.update_layout(margin=dict(t=70, b=30, l=0, r=0), showlegend=True,
                                        width=500, height=325,
                                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                        font=dict(size=10, color='#222A2A'),
                                        annotations=[dict(text='<b>T4</b>', x=0.5, y=0.5,  
                                                        font=dict(family="Comic Sans, sans-serif",
                                                                size=15 ,
                                                                color="slateblue"), showarrow=False)])

                #Combine t5 & t4 in a row
                col1, col2,col3 = st.columns([45,30,5])
                with col1:
                    st.subheader("")
                    st.success(" 💡 Kills Distribution by Power Label ")
                    st.subheader(" ")
                    st.plotly_chart(fig_donut_kills)
                with col2:
                    st.plotly_chart(fig_donut_kills_t5,use_container_width=True)
                    st.plotly_chart(fig_donut_kills_t4,use_container_width=True)
                with col3:
                    st.subheader("")

                st.title("")
                st.title("")

                #Funnel Chart for Kills

                df_grouped_kills=df.groupby(by=['kills_Label']).count()[['Username']]
                df_grouped_kills = df_grouped_kills.rename(columns={'Username': '#_of_players'})
                df_grouped_kills = df_grouped_kills.reset_index()

                fig_kills_label = px.funnel(df_grouped_kills, 
                                            x='#_of_players', 
                                            y='kills_Label',
                                            title='<b>'+'Number of Killers vs Kill Range'+'</b>',
                                            height=450, 
                                            width=650, 
                                            color_discrete_sequence=['#F67280'])

                fig_kills_label.update_xaxes(showgrid=False, ticksuffix=' ', showline=True)
                fig_kills_label.update_traces(marker=dict(line=dict(width=4,color='white')),textfont=dict(size=14,color='white'))
                fig_kills_label.update_layout(margin=dict(t=70, b=30, l=70, r=40),
                                        xaxis_title=' ', yaxis_title=" ",
                                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                        title_font=dict(size=16, color='#222A2A', family="Lato, sans-serif"),
                                        font=dict(color='#222A2A'))

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
                fig_t5_label.update_layout(title='<b>'+'Number of T5 Killers vs Kill Range'+'</b>',
                                margin=dict(t=50, b=50, l=0, r=0),
                                width=500, height=500,
                                hovermode="x unified",
                                xaxis_title=' ', yaxis_title=" ",
                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                title_font=dict(size=15, color='#222A2A', family="Lato, sans-serif"),
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
                fig_t4_label.update_layout(title='<b>'+'Number of T4 Killers vs Kill Range'+'</b>',
                                margin=dict(t=50, b=50, l=0, r=0),
                                width=500, height=500,
                                hovermode="x unified",
                                xaxis_title=' ', yaxis_title=" ",
                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                title_font=dict(size=15, color='#222A2A', family="Lato, sans-serif"),
                                font=dict(color='#222A2A'))

                with st.container():
                    howto_image = Image.open(IMAGES_DIR / "howto.png")

                    mygrid = make_grid(5,6)
                    mygrid[0][0].image(howto_image, width=500)
                    mygrid[0][3].plotly_chart(fig_kills_label)            
                    mygrid[3][0].plotly_chart(fig_t5_label)
                    mygrid[3][3].plotly_chart(fig_t4_label)

            with tab3:
                
                #Deads Donut Chart

                fig_donut_deads = px.pie(df_kills_power, hole=0.5,
                                    values= 'dead',
                                    title='<b>'+'Deaths Distribution by Power Label'+'</b>',
                                    names= 'Power_Label')

                fig_donut_deads.update_traces(textposition='inside', textinfo='percent', rotation=90,
                                            marker=dict(line=dict(width=2,color='white')))

                fig_donut_deads.update_layout(margin=dict(t=70, b=30, l=0, r=0), showlegend=True,
                                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                        title_font=dict(size=17, color='#222A2A', family="Lato, sans-serif"),
                                        font=dict(size=13, color='#222A2A'),
                                        legend=dict(orientation="h", font=dict(size=11)),
                                        annotations=[dict(text='<b>Deaths</b>', x=0.5, y=0.5,  
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
                                            title='<b>'+'Number of Players vs Deaths Range'+'</b>',
                                            height=450, 
                                            width=700, 
                                            color_discrete_sequence=['#348781'])

                fig_dead_label.update_xaxes(showgrid=False, ticksuffix=' ', showline=True)
                fig_dead_label.update_traces(marker=dict(line=dict(width=4,color='white')))
                fig_dead_label.update_layout(margin=dict(t=50, b=0, l=68, r=0),
                                        xaxis_title=' ', yaxis_title=" ",
                                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                        title_font=dict(size=17, color='#222A2A', family="Lato, sans-serif"),
                                        font=dict(color='#222A2A'))

                col1, col2 = st.columns([51,50])
                with col1:
                    st.plotly_chart(fig_donut_deads,use_container_width=True)
                with col2:
                    st.plotly_chart(fig_dead_label,use_container_width=True)

            with tab4:
                
                def make_grid(cols,rows):
                    grid = [0]*cols
                    for i in range(cols):
                        with st.container():
                            grid[i] = st.columns(rows)
                    return grid
                
                col1, col2, col3, col4,col5 = st.columns([6,21,34,20,18])

                with col1:
                    st.header(" ")
                with col2:
                    Player_1 = st.selectbox("Choose Player 1",df["Username"])
                with col3:
                    st.subheader("")
                with col4:
                    Player_2 = st.selectbox("Choose Player 2",df["Username"])
                with col5:
                    st.subheader("")
                #st.dataframe(df)

                #Averages
                #Kills
                df_nonzero_kills=df[df['kills']!=0]
                df_avg_kills=human_format(df_nonzero_kills.kills.mean())
                #st.write(df_avg_kills)

                df_nonzero_t5=df[df['t5']!=0]
                df_avg_t5=human_format(df_nonzero_t5.t5.mean())
                #st.write(df_avg_t5)

                df_nonzero_t4=df[df['t4']!=0]
                df_avg_t4=human_format(df_nonzero_t4.t4.mean())
                #st.write(df_avg_t4)

                #Deads
                df_nonzero_dead=df[df['dead']!=0]
                df_avg_dead=human_format(df_nonzero_dead.dead.mean())
                #st.write(df_avg_dead)

                #by Power Label

                df_nz_kills=df[["Username","kills","Power_Label"]]
                df_nz_kills=df_nz_kills[df_nz_kills['kills']!=0]
                df_avg_power_kills=df_nz_kills.groupby(by=['Power_Label']).mean()
                df_avg_power_kills=df_avg_power_kills.rename(columns={'Power_Label': 'kills'})
                df_avg_power_kills=df_avg_power_kills.reset_index()
                #st.write(df_avg_power_kills)

                df_nz_t5=df[["Username","t5","Power_Label"]]
                df_nz_t5=df_nz_t5[df_nz_t5['t5']!=0]
                df_avg_power_t5=df_nz_t5.groupby(by=['Power_Label']).mean()
                df_avg_power_t5=df_avg_power_t5.rename(columns={'Power_Label': 't5'})
                df_avg_power_t5=df_avg_power_t5.reset_index()
                #st.write(df_avg_power_t5)

                df_nz_t4=df[["Username","t4","Power_Label"]]
                df_nz_t4=df_nz_t4[df_nz_t4['t4']!=0]
                df_avg_power_t4=df_nz_t4.groupby(by=['Power_Label']).mean()
                df_avg_power_t4=df_avg_power_t4.rename(columns={'Power_Label': 't4'})
                df_avg_power_t4=df_avg_power_t4.reset_index()
                #st.write(df_avg_power_t4)

                #Deads by power label
                df_nz_dead=df[["Username","dead","Power_Label"]]
                df_nz_dead=df_nz_dead[df_nz_dead['dead']!=0]
                df_avg_power_dead=df_nz_dead.groupby(by=['Power_Label']).mean()
                df_avg_power_dead=df_avg_power_dead.rename(columns={'Power_Label': 'dead'})
                df_avg_power_dead=df_avg_power_dead.reset_index()
                #st.write(df_avg_power_dead)

                #taking averages with Left join to main data 
                new_df=df.merge(df_avg_power_kills.rename({'kills': 'kills_avg_power'}, axis=1), on='Power_Label', how='left')
                new_df=new_df.merge(df_avg_power_t5.rename({'t5': 't5_avg_power'}, axis=1), on='Power_Label', how='left')
                new_df=new_df.merge(df_avg_power_t4.rename({'t4': 't4_avg_power'}, axis=1), on='Power_Label', how='left')
                new_df=new_df.merge(df_avg_power_dead.rename({'dead': 'dead_avg_power'}, axis=1), on='Power_Label', how='left')

                new_df['diff_kills'] = (new_df['kills'] / df_nonzero_kills.kills.mean())-1
                new_df['diff_t5'] = (new_df['t5'] / df_nonzero_t5.t5.mean())-1
                new_df['diff_t4'] = (new_df['t4'] / df_nonzero_t4.t4.mean())-1
                new_df['diff_dead'] = (new_df['dead'] / df_nonzero_dead.dead.mean())-1

                new_df['diff_kills_power'] = (new_df['kills'] / new_df['kills_avg_power'])-1
                new_df['diff_t5_power'] = (new_df['t5'] / new_df['t5_avg_power'])-1
                new_df['diff_t4_power'] = (new_df['t4'] / new_df['t4_avg_power'])-1
                new_df['diff_dead_power'] = (new_df['dead'] / new_df['dead_avg_power'])-1
                #st.dataframe(new_df)

                deneme = new_df[["Username","Power","Power_Label","kills","t5","t4","dead",
                            "diff_kills","diff_t5","diff_t4","diff_dead",
                            "diff_kills_power","diff_t5_power","diff_t4_power","diff_dead_power",
                            "KD_t5%","KD_t4%","KD_dead%",
                            "Label_t5%","Label_t4%","Label_dead%",
                            "KD_All_in","Label_All_in","PP"]].loc[df["Username"] == Player_1].reset_index(drop=True)

                #st.dataframe(deneme)

                deneme2 = new_df[["Username","Power","Power_Label","kills","t5","t4","dead",
                            "diff_kills","diff_t5","diff_t4","diff_dead",
                            "diff_kills_power","diff_t5_power","diff_t4_power","diff_dead_power",
                            "KD_t5%","KD_t4%","KD_dead%",
                            "Label_t5%","Label_t4%","Label_dead%",
                            "KD_All_in","Label_All_in","PP"]].loc[df["Username"] == Player_2].reset_index(drop=True)


                Username = deneme['Username'].loc[0]
                user_power = deneme['Power'].loc[0]
                user_power_l = deneme['Power_Label'].loc[0]
                user_kills = deneme['kills'].loc[0]
                user_t5kills = deneme['t5'].loc[0]
                user_t4kills = deneme['t4'].loc[0]
                user_dead = deneme['dead'].loc[0]
                diff_kills = deneme['diff_kills'].loc[0]
                diff_t5kills = deneme['diff_t5'].loc[0]
                diff_t4kills = deneme['diff_t4'].loc[0]
                diff_dead = deneme['diff_dead'].loc[0]
                diff_kills_power = deneme['diff_kills_power'].loc[0]
                diff_t5kills_power = deneme['diff_t5_power'].loc[0]
                diff_t4kills_power = deneme['diff_t4_power'].loc[0]
                diff_dead_power = deneme['diff_dead_power'].loc[0]
                t5_p = deneme['KD_t5%'].loc[0]
                t4_p = deneme['KD_t4%'].loc[0]
                dead_p = deneme['KD_dead%'].loc[0]
                t5_p_l = deneme['Label_t5%'].loc[0]
                t4_p_l = deneme['Label_t4%'].loc[0]
                dead_p_l = deneme['Label_dead%'].loc[0]
                kd_p = deneme['KD_All_in'].loc[0]
                label_p = deneme['Label_All_in'].loc[0]
                pp_p = deneme['PP'].loc[0]

                Username1 = deneme2['Username'].loc[0]
                user_power1 = deneme2['Power'].loc[0]
                user_power_l1 = deneme2['Power_Label'].loc[0]
                user_kills1 = deneme2['kills'].loc[0]
                user_t5kills1 = deneme2['t5'].loc[0]
                user_t4kills1 = deneme2['t4'].loc[0]
                user_dead1 = deneme2['dead'].loc[0]
                diff_kills1 = deneme2['diff_kills'].loc[0]
                diff_t5kills1 = deneme2['diff_t5'].loc[0]
                diff_t4kills1 = deneme2['diff_t4'].loc[0]
                diff_dead1 = deneme2['diff_dead'].loc[0]
                diff_kills_power1 = deneme2['diff_kills_power'].loc[0]
                diff_t5kills_power1 = deneme2['diff_t5_power'].loc[0]
                diff_t4kills_power1 = deneme2['diff_t4_power'].loc[0]
                diff_dead_power1 = deneme2['diff_dead_power'].loc[0]
                t5_p1 = deneme2['KD_t5%'].loc[0]
                t4_p1 = deneme2['KD_t4%'].loc[0]
                dead_p1 = deneme2['KD_dead%'].loc[0]
                t5_p_l1 = deneme2['Label_t5%'].loc[0]
                t4_p_l1 = deneme2['Label_t4%'].loc[0]
                dead_p_l1 = deneme2['Label_dead%'].loc[0]
                kd_p1 = deneme2['KD_All_in'].loc[0]
                label_p1 = deneme2['Label_All_in'].loc[0]
                pp_p1 = deneme2['PP'].loc[0]



                deneme = deneme.rename(columns={'Username':'Governor Name',
                                                'KD_t5%':'T5 Kills %',
                                                'KD_t4%':'T4 Kills %',
                                                'KD_dead%':'Deads %',
                                                'KD_All_in':'Contribution Within KD',
                                                'Label_All_in':'Contribution Within Power Label',
                                                'PP':'Performance Point (PP)'
                                                })

                deneme = deneme.round(4)
                deneme = deneme.T.rename(columns={0: 'Player 1'})

                deneme2 = df[["Username",
                            "KD_t5%","KD_t4%",
                            "KD_dead%",
                            "KD_All_in","Label_All_in","PP"]].loc[df["Username"] == Player_2].reset_index(drop=True)

                deneme2 = deneme2.rename(columns={'Username':'Governor Name',
                                                'KD_t5%':'T5 Kills %',
                                                'KD_t4%':'T4 Kills %',
                                                'KD_dead%':'Deads %',
                                                'KD_All_in':'Contribution Within KD',
                                                'Label_All_in':'Contribution Within Power Label',
                                                'PP':'Performance Point (PP)'
                                                })

                deneme2 = deneme2.round(4)
                deneme2 = deneme2.T.rename(columns={0: 'Player 2'})

                result = pd.concat([deneme, deneme2], 
                                    axis=1, 
                                    join='inner')

                #st.dataframe(result)

                r1 = df[["Username","KD_t5%","KD_t4%","KD_dead%","KD_All_in","Label_All_in","PP"]].loc[df["Username"] == Player_1].reset_index(drop=True)
                r1 = r1.round(4)

                r1_rank= df[[#"Username",
                            "t5_rank",
                            "t4_rank",
                            "dead_rank",
                            "Contribution Within KD",
                            "Contribution Within Power_Label",
                            "Performance Point (PP)"]].loc[df["Username"] == Player_1].reset_index(drop=True)

                #st.dataframe(r1_rank)

                r2 = df[["Username","KD_t5%","KD_t4%","KD_dead%","KD_All_in","Label_All_in","PP"]].loc[df["Username"] == Player_2].reset_index(drop=True)
                r2 = r2.round(4)

                r2_rank= df[[#"Username",
                            "t5_rank",
                            "t4_rank",
                            "dead_rank",
                            "Contribution Within KD",
                            "Contribution Within Power_Label",
                            "Performance Point (PP)"]].loc[df["Username"] == Player_2].reset_index(drop=True)

                #st.dataframe(r2_rank)

                categories = ['T5 Kills%','T4 Kills%','Deaths%',
                            'Kingdom Score', 'Power Label Score', 'Performance Point (PP)']

                per_mon = go.Figure()

                per_mon.add_trace(go.Scatterpolar(
                    r=r1_rank.loc[0].values,
                    theta=categories,
                    fill='toself',
                    name=r1['Username'].loc[0]
                ))
                per_mon.add_trace(go.Scatterpolar(
                    r=r2_rank.loc[0].values,
                    theta=categories,
                    fill='toself',
                    name=r2['Username'].loc[0]
                ))

                per_mon.update_layout(
                polar=dict(
                    radialaxis=dict(
                    visible=True,
                    range=[0,100]
                    )),
                showlegend=True
                )

                with st.container():
                    mygrid = make_grid(3,9)
                    st.markdown("""
                                    <style>
                                    div[data-testid="metric-container"] {
                                    background-color: rgba(28, 131, 225, 0.1);
                                    border: 1px solid rgba(28, 131, 225, 0.1);
                                    padding: 5% 5% 5% 2%;
                                    border-radius: 10px;
                                    color: rgb(30, 103, 119);
                                    overflow-wrap: break-word;
                                    }
                                    </style>
                                    """
                                    , unsafe_allow_html=True)
                    mygrid[0][1].metric("Power 🔱",human_format2(user_power),user_power_l)
                    mygrid[1][1].metric("Kills ⚔️",human_format2(user_kills))
                    mygrid[1][2].metric("Deaths ☠️",human_format2(user_dead))
                    mygrid[1][0].metric(label="ΔKingdom ⛳️",value="",delta='{:.1f}%'.format(diff_kills*100))
                    mygrid[2][0].metric(label="ΔPower Label 🎳",value="",delta='{:.1f}%'.format(diff_kills_power*100))
                    mygrid[1][3].metric(label="ΔKingdom ⛳️",value="",delta='{:.1f}%'.format(diff_dead*100))
                    mygrid[2][3].metric(label="ΔPower Label 🎳",value="",delta='{:.1f}%'.format(diff_dead_power*100))

                    mygrid[0][6].metric("Power 🔱",human_format2(user_power1),user_power_l1)
                    mygrid[1][6].metric("Kills ⚔️",human_format2(user_kills1))
                    mygrid[1][7].metric("Deaths ☠️",human_format2(user_dead1))
                    mygrid[1][5].metric(label="ΔKingdom ⛳️",value="",delta='{:.1f}%'.format(diff_kills1*100))
                    mygrid[2][5].metric(label="ΔPower Label 🎳",value="",delta='{:.1f}%'.format(diff_kills_power1*100))
                    mygrid[1][8].metric(label="ΔKingdom ⛳️",value="",delta='{:.1f}%'.format(diff_dead1*100))
                    mygrid[2][8].metric(label="ΔPower Label 🎳",value="",delta='{:.1f}%'.format(diff_dead_power1*100))

                notation_DESC = """

                    - ΔKingdom : Player/Kingdom Average     
                    - ΔPower Label : Player/Power Label Average
                    """

                with st.container():
                    col1,col2,col3 = st.columns([18,6,79])
                    with col1:
                        st.success(notation_DESC)
                    with col2:
                        st.subheader("")
                    with col3:
                        st.plotly_chart(per_mon)

                with st.container():
                    hide = """
                    <style>
                    ul.streamlit-expander {
                        border: 0 !important;
                    </style>
                    """

                    st.markdown(hide, unsafe_allow_html=True)
                    with st.expander("**See More Detailed Statistics:**"):

                        st.title("")

                        mygrid2 = make_grid(6,9)
                        mygrid2[0][1].metric("T5 Kills ⚔️",human_format2(user_t5kills))
                        mygrid2[0][2].metric("T4 Kills ⚔️",human_format2(user_t4kills))
                        mygrid2[0][0].metric(label="ΔKingdom ⛳️",value="",delta='{:.1f}%'.format(diff_t5kills*100))
                        mygrid2[1][0].metric(label="ΔPower Label 🎳",value="",delta='{:.1f}%'.format(diff_t5kills_power*100))
                        mygrid2[0][3].metric(label="ΔKingdom ⛳️",value="",delta='{:.1f}%'.format(diff_t4kills*100))
                        mygrid2[1][3].metric(label="ΔPower Label 🎳",value="",delta='{:.1f}%'.format(diff_t4kills_power*100))

                        mygrid2[0][6].metric("T5 Kills ⚔️",human_format2(user_t5kills1))
                        mygrid2[0][7].metric("T4 Kills ⚔️",human_format2(user_t4kills1))
                        mygrid2[0][5].metric(label="ΔKingdom ⛳️",value="",delta='{:.1f}%'.format(diff_t5kills1*100))
                        mygrid2[1][5].metric(label="ΔPower Label 🎳",value="",delta='{:.1f}%'.format(diff_t5kills_power1*100))
                        mygrid2[0][8].metric(label="ΔKingdom ⛳️",value="",delta='{:.1f}%'.format(diff_t4kills1*100))
                        mygrid2[1][8].metric(label="ΔPower Label 🎳",value="",delta='{:.1f}%'.format(diff_t4kills_power1*100))

                        mygrid2[2][1].metric(label="**% of Performance**", value="")
                        mygrid2[2][7].metric(label="**% of Performance**", value="")

                        mygrid2[3][0].metric(label="T5 % - KD",value="",delta='{:.1f}%'.format(t5_p*100))
                        mygrid2[3][3].metric(label="T5 % - PL",value="",delta='{:.1f}%'.format(t5_p_l*100))
                        mygrid2[4][0].metric(label="T4 % - KD",value="",delta='{:.1f}%'.format(t4_p*100))
                        mygrid2[4][3].metric(label="T4 % - PL",value="",delta='{:.1f}%'.format(t4_p_l*100))
                        mygrid2[3][1].metric(label="Death % - KD",value="",delta='{:.1f}%'.format(dead_p*100))
                        mygrid2[3][2].metric(label="Death % - PL",value="",delta='{:.1f}%'.format(dead_p_l*100))
                        mygrid2[4][1].metric("KD Score",'{:.1f}%'.format(kd_p*100))
                        mygrid2[4][2].metric("PL Score",'{:.1f}%'.format(label_p*100))
                        mygrid2[5][2].metric("Performance Point",'{:.1f}%'.format(pp_p*100))

                        mygrid2[3][5].metric(label="T5 % - KD",value="",delta='{:.1f}%'.format(t5_p1*100))
                        mygrid2[3][8].metric(label="T5 % - PL",value="",delta='{:.1f}%'.format(t5_p_l1*100))
                        mygrid2[4][5].metric(label="T4 % - KD",value="",delta='{:.1f}%'.format(t4_p1*100))
                        mygrid2[4][8].metric(label="T4 % - PL",value="",delta='{:.1f}%'.format(t4_p_l1*100))
                        mygrid2[3][6].metric(label="Death % - KD",value="",delta='{:.1f}%'.format(dead_p1*100))
                        mygrid2[3][7].metric(label="Death % - PL",value="",delta='{:.1f}%'.format(dead_p_l1*100))
                        mygrid2[4][6].metric("KD Score",'{:.1f}%'.format(kd_p1*100))
                        mygrid2[4][7].metric("PL Score",'{:.1f}%'.format(label_p1*100))
                        mygrid2[5][6].metric("Performance Point",'{:.1f}%'.format(pp_p1*100))

                        st.title("")

                        notation_DESC1 = """
                            Notations:
                            - T5 % - KD : Percentage of T5 kills in Kingdom
                            - T5 % - PL : Percentage of T5 kills in Power Label

                            """
                        notation_DESC2 = """
                        
                            - KD Score : Weighted average of Kingdom (T5%, T4% and Death%)
                            - PL Score : Weighted average of Power Label (T5%, T4% and Death%)
                            - Performance Point : Weighted average of (KD Score and PL Score)

                            """

                        with st.container():
                            col1,col2,col3 = st.columns([36,50,14])
                            with col1:
                                st.success(notation_DESC1)
                            with col2:
                                st.success(notation_DESC2)
                            with col3:
                                st.subheader("")

        if selected == "LeaderBoard":

            col1,col2,col3 = st.columns(3)
            with col1:
                st.subheader("")
            with col2:
                selected = option_menu(
                                        menu_title=None,
                                        options=["Top 5","Top 25"],
                                        icons=["diagram-2","diagram-3"],
                                        default_index=0,
                                        orientation="horizontal")
            with col3:
                st.subheader("")

            if selected == "Top 5":
                tab1, tab2 = st.tabs([" 🪖 Most Valuable Killers", " 🎗 Hall of Heroes"])
                with tab1 :
                    with st.container():
                        top25_option = ["🎖 All in One", "🏅 T5 Killers", "🏅 T4 Killers"]
                        col1,col2,col3,col4,col5 = st.columns(5)
                        with col1:
                            top25_choice = st.selectbox("",top25_option)

                        if top25_choice == "🎖 All in One":
                            x_Data_killers = [5,4.999]
                            y_Data_killers = ['KILLERS','LEADERBOARD']

                            fig_head_kills = go.Figure()
                            fig_head_kills.add_trace(go.Bar(
                                    y=y_Data_killers,
                                    x=x_Data_killers,
                                    textposition = "inside", 
                                    text = y_Data_killers,
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=13, color='white'),outsidetextfont=dict(family='Arial', size=12, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(47, 138, 196, 0.9)',
                                        line=dict(color='rgba(47, 138, 196, 1)', width=1)
                                    )
                                ))
                            fig_head_kills.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_head_kills.update_layout(margin=dict(t=20, b=0, l=0, r=0),
                                                width=250, height=75,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )
                            #st.plotly_chart(fig_head_kills)

                            df_top5_p90_kills=df[(df.Power_Label==l_p90)][["Username","kills"]].nlargest(5, 'kills').reset_index()
                            df_top5_p90_kills['top5_p90'] = [df_top5_p90_kills.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p90_kills.kills.loc[0]),
                                                            df_top5_p90_kills.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p90_kills.kills.loc[1]),
                                                            df_top5_p90_kills.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p90_kills.kills.loc[2]),
                                                            df_top5_p90_kills.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p90_kills.kills.loc[3]),
                                                            df_top5_p90_kills.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p90_kills.kills.loc[4])]
                            df_top5_p90_kills['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p90_kills)

                            fig_top5_p90_kills = go.Figure()
                            fig_top5_p90_kills.add_trace(go.Bar(
                                    y=df_top5_p90_kills.top5_p90,
                                    x=df_top5_p90_kills.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p90_kills['top5_p90'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),
                                    outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(17, 119, 51, 1)',
                                        line=dict(color='rgba(17, 119, 51, 1)', width=1)
                                    )
                                ))
                            fig_top5_p90_kills.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p90_kills.update_layout(title = "        🎖        "+'<b>'+l_p90+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},
                                                yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p90_kills)

                            df_top5_p80_kills=df[(df.Power_Label==l_p80)][["Username","kills"]].nlargest(5, 'kills').reset_index()
                            df_top5_p80_kills['top5_p80'] = [df_top5_p80_kills.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p80_kills.kills.loc[0]),
                                                            df_top5_p80_kills.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p80_kills.kills.loc[1]),
                                                            df_top5_p80_kills.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p80_kills.kills.loc[2]),
                                                            df_top5_p80_kills.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p80_kills.kills.loc[3]),
                                                            df_top5_p80_kills.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p80_kills.kills.loc[4])]
                            df_top5_p80_kills['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p80_kills)

                            fig_top5_p80_kills = go.Figure()
                            fig_top5_p80_kills.add_trace(go.Bar(
                                    y=df_top5_p80_kills.top5_p80,
                                    x=df_top5_p80_kills.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p80_kills['top5_p80'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(29, 105, 150, 1)',
                                        line=dict(color='rgba(29, 105, 150, 1)', width=1)
                                    )
                                ))
                            fig_top5_p80_kills.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p80_kills.update_layout(title = "        🎖        "+'<b>'+l_p80+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p80_kills)

                            df_top5_p70_kills=df[(df.Power_Label==l_p70)][["Username","kills"]].nlargest(5, 'kills').reset_index()
                            df_top5_p70_kills['top5_p70'] = [df_top5_p70_kills.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p70_kills.kills.loc[0]),
                                                            df_top5_p70_kills.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p70_kills.kills.loc[1]),
                                                            df_top5_p70_kills.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p70_kills.kills.loc[2]),
                                                            df_top5_p70_kills.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p70_kills.kills.loc[3]),
                                                            df_top5_p70_kills.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p70_kills.kills.loc[4])]
                            df_top5_p70_kills['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p70_kills)

                            fig_top5_p70_kills = go.Figure()
                            fig_top5_p70_kills.add_trace(go.Bar(
                                    y=df_top5_p70_kills.top5_p70,
                                    x=df_top5_p70_kills.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p70_kills['top5_p70'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(217, 95, 2, 1)',
                                        line=dict(color='rgba(160, 97, 119, 1)', width=1)
                                    )
                                ))
                            fig_top5_p70_kills.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p70_kills.update_layout(title = "        🎖        "+'<b>'+l_p70+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p70_kills)

                            df_top5_p60_kills=df[(df.Power_Label==l_p60)][["Username","kills"]].nlargest(5, 'kills').reset_index()
                            df_top5_p60_kills['top5_p60'] = [df_top5_p60_kills.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p60_kills.kills.loc[0]),
                                                            df_top5_p60_kills.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p60_kills.kills.loc[1]),
                                                            df_top5_p60_kills.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p60_kills.kills.loc[2]),
                                                            df_top5_p60_kills.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p60_kills.kills.loc[3]),
                                                            df_top5_p60_kills.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p60_kills.kills.loc[4])]
                            df_top5_p60_kills['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p60_kills)

                            fig_top5_p60_kills = go.Figure()
                            fig_top5_p60_kills.add_trace(go.Bar(
                                    y=df_top5_p60_kills.top5_p60,
                                    x=df_top5_p60_kills.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p60_kills['top5_p60'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(166, 118, 29, 1)',
                                        line=dict(color='rgba(166, 118, 29, 1)', width=1)
                                    )
                                ))
                            fig_top5_p60_kills.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p60_kills.update_layout(title = "        🎖        "+'<b>'+l_p60+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p60_kills)

                            df_top5_p50_kills=df[(df.Power_Label==l_p50)][["Username","kills"]].nlargest(5, 'kills').reset_index()
                            df_top5_p50_kills['top5_p50'] = [df_top5_p50_kills.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p50_kills.kills.loc[0]),
                                                            df_top5_p50_kills.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p50_kills.kills.loc[1]),
                                                            df_top5_p50_kills.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p50_kills.kills.loc[2]),
                                                            df_top5_p50_kills.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p50_kills.kills.loc[3]),
                                                            df_top5_p50_kills.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p50_kills.kills.loc[4])]
                            df_top5_p50_kills['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p50_kills)

                            fig_top5_p50_kills = go.Figure()
                            fig_top5_p50_kills.add_trace(go.Bar(
                                    y=df_top5_p50_kills.top5_p50,
                                    x=df_top5_p50_kills.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p50_kills['top5_p50'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(160, 97, 119, 1)',
                                        line=dict(color='rgba(160, 97, 119, 1)', width=1)
                                    )
                                ))
                            fig_top5_p50_kills.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p50_kills.update_layout(title = "        🎖        "+'<b>'+l_p50+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p50_kills)

                            df_top5_p25_kills=df[(df.Power_Label==l_p25)][["Username","kills"]].nlargest(5, 'kills').reset_index()
                            df_top5_p25_kills['top5_p25'] = [df_top5_p25_kills.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p25_kills.kills.loc[0]),
                                                            df_top5_p25_kills.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p25_kills.kills.loc[1]),
                                                            df_top5_p25_kills.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p25_kills.kills.loc[2]),
                                                            df_top5_p25_kills.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p25_kills.kills.loc[3]),
                                                            df_top5_p25_kills.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p25_kills.kills.loc[4])]
                            df_top5_p25_kills['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p25_kills)

                            fig_top5_p25_kills = go.Figure()
                            fig_top5_p25_kills.add_trace(go.Bar(
                                    y=df_top5_p25_kills.top5_p25,
                                    x=df_top5_p25_kills.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p25_kills['top5_p25'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(115, 111, 76, 1)',
                                        line=dict(color='rgba(115, 111, 76, 1)', width=1)
                                    )
                                ))
                            fig_top5_p25_kills.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p25_kills.update_layout(title = "        🎖        "+'<b>'+l_p25+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p25_kills)

                            df_top5_pmin_kills=df[(df.Power_Label==l_min)][["Username","kills"]].nlargest(5, 'kills').reset_index()
                            df_top5_pmin_kills['top5_pmin'] = [df_top5_pmin_kills.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_pmin_kills.kills.loc[0]),
                                                            df_top5_pmin_kills.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_pmin_kills.kills.loc[1]),
                                                            df_top5_pmin_kills.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_pmin_kills.kills.loc[2]),
                                                            df_top5_pmin_kills.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_pmin_kills.kills.loc[3]),
                                                            df_top5_pmin_kills.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_pmin_kills.kills.loc[4])]
                            df_top5_pmin_kills['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_pmin_kills)

                            fig_top5_pmin_kills = go.Figure()
                            fig_top5_pmin_kills.add_trace(go.Bar(
                                    y=df_top5_pmin_kills.top5_pmin,
                                    x=df_top5_pmin_kills.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_pmin_kills['top5_pmin'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(56, 166, 165, 1)',
                                        line=dict(color='rgba(56, 166, 165, 1)', width=1)
                                    )
                                ))
                            fig_top5_pmin_kills.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_pmin_kills.update_layout(title = "        🎖        "+'<b>'+l_min+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_pmin_kills)

                            with st.container():

                                mygrid = make_grid(9,19)
                                mygrid[0][7].plotly_chart(fig_head_kills)
                                mygrid[1][7].plotly_chart(fig_top5_p90_kills)
                                mygrid[2][5].plotly_chart(fig_top5_p80_kills)
                                mygrid[2][9].plotly_chart(fig_top5_p70_kills)
                                mygrid[3][1].plotly_chart(fig_top5_p60_kills)
                                mygrid[3][5].plotly_chart(fig_top5_p50_kills)
                                mygrid[3][9].plotly_chart(fig_top5_p25_kills)
                                mygrid[3][13].plotly_chart(fig_top5_pmin_kills)

                        if top25_choice == "🏅 T5 Killers":
                            x_Data_t5killers = [5,4.999]
                            y_Data_t5killers = ['T5 KILLERS','LEADERBOARD']

                            fig_head_t5 = go.Figure()
                            fig_head_t5.add_trace(go.Bar(
                                    y=y_Data_t5killers,
                                    x=x_Data_t5killers,
                                    textposition = "inside", 
                                    text = y_Data_t5killers,
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=13, color='white'),outsidetextfont=dict(family='Arial', size=12, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(47, 138, 196, 0.9)',
                                        line=dict(color='rgba(47, 138, 196, 1)', width=1)
                                    )
                                ))
                            fig_head_t5.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_head_t5.update_layout(margin=dict(t=20, b=0, l=0, r=0),
                                                width=250, height=75,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )
                            #st.plotly_chart(fig_head_t5)

                            df_top5_p90_t5=df[(df.Power_Label==l_p90)][["Username","t5"]].nlargest(5, 't5').reset_index()
                            df_top5_p90_t5['top5_p90'] = [df_top5_p90_t5.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p90_t5.t5.loc[0]),
                                                            df_top5_p90_t5.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p90_t5.t5.loc[1]),
                                                            df_top5_p90_t5.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p90_t5.t5.loc[2]),
                                                            df_top5_p90_t5.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p90_t5.t5.loc[3]),
                                                            df_top5_p90_t5.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p90_t5.t5.loc[4])]
                            df_top5_p90_t5['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p90_t5)

                            fig_top5_p90_t5 = go.Figure()
                            fig_top5_p90_t5.add_trace(go.Bar(
                                    y=df_top5_p90_t5.top5_p90,
                                    x=df_top5_p90_t5.dummy_value,                      
                                    textposition = "inside", 
                                    text = df_top5_p90_t5['top5_p90'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),
                                    outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(115, 111, 76, 1)',
                                        line=dict(color='rgba(115, 111, 76, 1)', width=1)
                                    )
                                ))
                            fig_top5_p90_t5.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p90_t5.update_layout(title = "        🎖        "+'<b>'+l_p90+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},
                                                yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p90_t5)

                            df_top5_p80_t5=df[(df.Power_Label==l_p80)][["Username","t5"]].nlargest(5, 't5').reset_index()
                            df_top5_p80_t5['top5_p80'] = [df_top5_p80_t5.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p80_t5.t5.loc[0]),
                                                            df_top5_p80_t5.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p80_t5.t5.loc[1]),
                                                            df_top5_p80_t5.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p80_t5.t5.loc[2]),
                                                            df_top5_p80_t5.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p80_t5.t5.loc[3]),
                                                            df_top5_p80_t5.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p80_t5.t5.loc[4])]
                            df_top5_p80_t5['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p80_t5)

                            fig_top5_p80_t5 = go.Figure()
                            fig_top5_p80_t5.add_trace(go.Bar(
                                    y=df_top5_p80_t5.top5_p80,
                                    x=df_top5_p80_t5.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p80_t5['top5_p80'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(56, 166, 165, 1)',
                                        line=dict(color='rgba(56, 166, 165, 1)', width=1)
                                    )
                                ))
                            fig_top5_p80_t5.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p80_t5.update_layout(title = "        🎖        "+'<b>'+l_p80+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )


                            df_top5_p70_t5=df[(df.Power_Label==l_p70)][["Username","t5"]].nlargest(5, 't5').reset_index()
                            df_top5_p70_t5['top5_p70'] = [df_top5_p70_t5.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p70_t5.t5.loc[0]),
                                                            df_top5_p70_t5.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p70_t5.t5.loc[1]),
                                                            df_top5_p70_t5.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p70_t5.t5.loc[2]),
                                                            df_top5_p70_t5.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p70_t5.t5.loc[3]),
                                                            df_top5_p70_t5.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p70_t5.t5.loc[4])]
                            df_top5_p70_t5['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p70_t5)

                            fig_top5_p70_t5 = go.Figure()
                            fig_top5_p70_t5.add_trace(go.Bar(
                                    y=df_top5_p70_t5.top5_p70,
                                    x=df_top5_p70_t5.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p70_t5['top5_p70'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(160, 97, 119, 1)',
                                        line=dict(color='rgba(160, 97, 119, 1)', width=1)
                                    )
                                ))
                            fig_top5_p70_t5.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p70_t5.update_layout(title = "        🎖        "+'<b>'+l_p70+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p70_kills)

                            df_top5_p60_t5=df[(df.Power_Label==l_p60)][["Username","t5"]].nlargest(5, 't5').reset_index()
                            df_top5_p60_t5['top5_p60'] = [df_top5_p60_t5.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p60_t5.t5.loc[0]),
                                                            df_top5_p60_t5.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p60_t5.t5.loc[1]),
                                                            df_top5_p60_t5.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p60_t5.t5.loc[2]),
                                                            df_top5_p60_t5.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p60_t5.t5.loc[3]),
                                                            df_top5_p60_t5.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p60_t5.t5.loc[4])]
                            df_top5_p60_t5['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p60_t5)

                            fig_top5_p60_t5 = go.Figure()
                            fig_top5_p60_t5.add_trace(go.Bar(
                                    y=df_top5_p60_t5.top5_p60,
                                    x=df_top5_p60_t5.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p60_t5['top5_p60'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(217, 95, 2, 1)',
                                        line=dict(color='rgba(217, 95, 2, 1)', width=1)
                                    )
                                ))
                            fig_top5_p60_t5.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p60_t5.update_layout(title = "        🎖        "+'<b>'+l_p60+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p60_kills)

                            df_top5_p50_t5=df[(df.Power_Label==l_p50)][["Username","t5"]].nlargest(5, 't5').reset_index()
                            df_top5_p50_t5['top5_p50'] = [df_top5_p50_t5.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p50_t5.t5.loc[0]),
                                                            df_top5_p50_t5.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p50_t5.t5.loc[1]),
                                                            df_top5_p50_t5.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p50_t5.t5.loc[2]),
                                                            df_top5_p50_t5.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p50_t5.t5.loc[3]),
                                                            df_top5_p50_t5.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p50_t5.t5.loc[4])]
                            df_top5_p50_t5['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p50_t5)

                            fig_top5_p50_t5 = go.Figure()
                            fig_top5_p50_t5.add_trace(go.Bar(
                                    y=df_top5_p50_t5.top5_p50,
                                    x=df_top5_p50_t5.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p50_t5['top5_p50'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(17, 119, 51, 1)',
                                        line=dict(color='rgba(17, 119, 51, 1)', width=1)
                                    )
                                ))
                            fig_top5_p50_t5.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p50_t5.update_layout(title = "        🎖        "+'<b>'+l_p50+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p50_kills)

                            df_top5_p25_t5=df[(df.Power_Label==l_p25)][["Username","t5"]].nlargest(5, 't5').reset_index()
                            df_top5_p25_t5['top5_p25'] = [df_top5_p25_t5.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p25_t5.t5.loc[0]),
                                                            df_top5_p25_t5.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p25_t5.t5.loc[1]),
                                                            df_top5_p25_t5.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p25_t5.t5.loc[2]),
                                                            df_top5_p25_t5.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p25_t5.t5.loc[3]),
                                                            df_top5_p25_t5.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p25_t5.t5.loc[4])]
                            df_top5_p25_t5['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p25_t5)

                            fig_top5_p25_t5 = go.Figure()
                            fig_top5_p25_t5.add_trace(go.Bar(
                                    y=df_top5_p25_t5.top5_p25,
                                    x=df_top5_p25_t5.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p25_t5['top5_p25'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(166, 118, 29, 1)',
                                        line=dict(color='rgba(166, 118, 29, 1)', width=1)
                                    )
                                ))
                            fig_top5_p25_t5.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p25_t5.update_layout(title = "        🎖        "+'<b>'+l_p25+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p25_kills)

                            df_top5_pmin_t5=df[(df.Power_Label==l_min)][["Username","t5"]].nlargest(5, 't5').reset_index()
                            df_top5_pmin_t5['top5_pmin'] = [df_top5_pmin_t5.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_pmin_t5.t5.loc[0]),
                                                            df_top5_pmin_t5.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_pmin_t5.t5.loc[1]),
                                                            df_top5_pmin_t5.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_pmin_t5.t5.loc[2]),
                                                            df_top5_pmin_t5.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_pmin_t5.t5.loc[3]),
                                                            df_top5_pmin_t5.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_pmin_t5.t5.loc[4])]
                            df_top5_pmin_t5['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_pmin_t5)

                            fig_top5_pmin_t5 = go.Figure()
                            fig_top5_pmin_t5.add_trace(go.Bar(
                                    y=df_top5_pmin_t5.top5_pmin,
                                    x=df_top5_pmin_t5.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_pmin_t5['top5_pmin'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(29, 105, 150, 1)',
                                        line=dict(color='rgba(29, 105, 150, 1)', width=1)
                                    )
                                ))
                            fig_top5_pmin_t5.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_pmin_t5.update_layout(title = "        🎖        "+'<b>'+l_min+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_pmin_kills)

                            with st.container():

                                mygrid = make_grid(9,19)
                                mygrid[0][7].plotly_chart(fig_head_t5)
                                mygrid[1][7].plotly_chart(fig_top5_p90_t5)
                                mygrid[2][5].plotly_chart(fig_top5_p80_t5)
                                mygrid[2][9].plotly_chart(fig_top5_p70_t5)
                                mygrid[3][1].plotly_chart(fig_top5_p60_t5)
                                mygrid[3][5].plotly_chart(fig_top5_p50_t5)
                                mygrid[3][9].plotly_chart(fig_top5_p25_t5)
                                mygrid[3][13].plotly_chart(fig_top5_pmin_t5)

                        if top25_choice == "🏅 T4 Killers":
                            x_Data_t4killers = [5,4.999]
                            y_Data_t4killers = ['T4 KILLERS','LEADERBOARD']

                            fig_head_t4 = go.Figure()
                            fig_head_t4.add_trace(go.Bar(
                                    y=y_Data_t4killers,
                                    x=x_Data_t4killers,
                                    textposition = "inside", 
                                    text = y_Data_t4killers,
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=13, color='white'),outsidetextfont=dict(family='Arial', size=12, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(47, 138, 196, 0.9)',
                                        line=dict(color='rgba(47, 138, 196, 1)', width=1)
                                    )
                                ))
                            fig_head_t4.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_head_t4.update_layout(margin=dict(t=20, b=0, l=0, r=0),
                                                width=250, height=75,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )
                            #st.plotly_chart(fig_head_t4)

                            df_top5_p90_t4=df[(df.Power_Label==l_p90)][["Username","t4"]].nlargest(5, 't4').reset_index()
                            df_top5_p90_t4['top5_p90'] = [df_top5_p90_t4.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p90_t4.t4.loc[0]),
                                                            df_top5_p90_t4.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p90_t4.t4.loc[1]),
                                                            df_top5_p90_t4.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p90_t4.t4.loc[2]),
                                                            df_top5_p90_t4.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p90_t4.t4.loc[3]),
                                                            df_top5_p90_t4.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p90_t4.t4.loc[4])]
                            df_top5_p90_t4['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p90_t5)

                            fig_top5_p90_t4 = go.Figure()
                            fig_top5_p90_t4.add_trace(go.Bar(
                                    y=df_top5_p90_t4.top5_p90,
                                    x=df_top5_p90_t4.dummy_value,                      
                                    textposition = "inside", 
                                    text = df_top5_p90_t4['top5_p90'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),
                                    outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(217, 95, 2, 1)',
                                        line=dict(color='rgba(217, 95, 2, 1)', width=1)
                                    )
                                ))
                            fig_top5_p90_t4.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p90_t4.update_layout(title = "        🎖        "+'<b>'+l_p90+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},
                                                yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p90_t4)

                            df_top5_p80_t4=df[(df.Power_Label==l_p80)][["Username","t4"]].nlargest(5, 't4').reset_index()
                            df_top5_p80_t4['top5_p80'] = [df_top5_p80_t4.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p80_t4.t4.loc[0]),
                                                            df_top5_p80_t4.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p80_t4.t4.loc[1]),
                                                            df_top5_p80_t4.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p80_t4.t4.loc[2]),
                                                            df_top5_p80_t4.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p80_t4.t4.loc[3]),
                                                            df_top5_p80_t4.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p80_t4.t4.loc[4])]
                            df_top5_p80_t4['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p80_t4)

                            fig_top5_p80_t4 = go.Figure()
                            fig_top5_p80_t4.add_trace(go.Bar(
                                    y=df_top5_p80_t4.top5_p80,
                                    x=df_top5_p80_t4.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p80_t4['top5_p80'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(160, 97, 119, 1)',
                                        line=dict(color='rgba(160, 97, 119, 1)', width=1)
                                    )
                                ))
                            fig_top5_p80_t4.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p80_t4.update_layout(title = "        🎖        "+'<b>'+l_p80+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )


                            df_top5_p70_t4=df[(df.Power_Label==l_p70)][["Username","t4"]].nlargest(5, 't4').reset_index()
                            df_top5_p70_t4['top5_p70'] = [df_top5_p70_t4.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p70_t4.t4.loc[0]),
                                                            df_top5_p70_t4.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p70_t4.t4.loc[1]),
                                                            df_top5_p70_t4.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p70_t4.t4.loc[2]),
                                                            df_top5_p70_t4.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p70_t4.t4.loc[3]),
                                                            df_top5_p70_t4.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p70_t4.t4.loc[4])]
                            df_top5_p70_t4['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p70_t5)

                            fig_top5_p70_t4 = go.Figure()
                            fig_top5_p70_t4.add_trace(go.Bar(
                                    y=df_top5_p70_t4.top5_p70,
                                    x=df_top5_p70_t4.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p70_t4['top5_p70'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(17, 119, 51, 1)',
                                        line=dict(color='rgba(17, 119, 51, 1)', width=1)
                                    )
                                ))
                            fig_top5_p70_t4.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p70_t4.update_layout(title = "        🎖        "+'<b>'+l_p70+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p70_kills)

                            df_top5_p60_t4=df[(df.Power_Label==l_p60)][["Username","t4"]].nlargest(5, 't4').reset_index()
                            df_top5_p60_t4['top5_p60'] = [df_top5_p60_t4.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p60_t4.t4.loc[0]),
                                                            df_top5_p60_t4.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p60_t4.t4.loc[1]),
                                                            df_top5_p60_t4.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p60_t4.t4.loc[2]),
                                                            df_top5_p60_t4.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p60_t4.t4.loc[3]),
                                                            df_top5_p60_t4.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p60_t4.t4.loc[4])]
                            df_top5_p60_t4['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p60_t4)

                            fig_top5_p60_t4 = go.Figure()
                            fig_top5_p60_t4.add_trace(go.Bar(
                                    y=df_top5_p60_t4.top5_p60,
                                    x=df_top5_p60_t4.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p60_t4['top5_p60'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(29, 105, 150, 1)',
                                        line=dict(color='rgba(29, 105, 150, 1)', width=1)
                                    )
                                ))
                            fig_top5_p60_t4.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p60_t4.update_layout(title = "        🎖        "+'<b>'+l_p60+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p60_kills)

                            df_top5_p50_t4=df[(df.Power_Label==l_p50)][["Username","t4"]].nlargest(5, 't4').reset_index()
                            df_top5_p50_t4['top5_p50'] = [df_top5_p50_t4.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p50_t4.t4.loc[0]),
                                                            df_top5_p50_t4.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p50_t4.t4.loc[1]),
                                                            df_top5_p50_t4.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p50_t4.t4.loc[2]),
                                                            df_top5_p50_t4.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p50_t4.t4.loc[3]),
                                                            df_top5_p50_t4.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p50_t4.t4.loc[4])]
                            df_top5_p50_t4['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p50_t4)

                            fig_top5_p50_t4 = go.Figure()
                            fig_top5_p50_t4.add_trace(go.Bar(
                                    y=df_top5_p50_t4.top5_p50,
                                    x=df_top5_p50_t4.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p50_t4['top5_p50'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(115, 111, 76, 1)',
                                        line=dict(color='rgba(115, 111, 76, 1)', width=1)
                                    )
                                ))
                            fig_top5_p50_t4.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p50_t4.update_layout(title = "        🎖        "+'<b>'+l_p50+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p50_t4)

                            df_top5_p25_t4=df[(df.Power_Label==l_p25)][["Username","t4"]].nlargest(5, 't4').reset_index()
                            df_top5_p25_t4['top5_p25'] = [df_top5_p25_t4.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p25_t4.t4.loc[0]),
                                                            df_top5_p25_t4.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p25_t4.t4.loc[1]),
                                                            df_top5_p25_t4.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p25_t4.t4.loc[2]),
                                                            df_top5_p25_t4.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p25_t4.t4.loc[3]),
                                                            df_top5_p25_t4.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p25_t4.t4.loc[4])]
                            df_top5_p25_t4['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p25_t4)

                            fig_top5_p25_t4 = go.Figure()
                            fig_top5_p25_t4.add_trace(go.Bar(
                                    y=df_top5_p25_t4.top5_p25,
                                    x=df_top5_p25_t4.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p25_t4['top5_p25'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(56, 166, 165, 1)',
                                        line=dict(color='rgba(56, 166, 165, 1)', width=1)
                                    )
                                ))
                            fig_top5_p25_t4.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_p25_t4.update_layout(title = "        🎖        "+'<b>'+l_p25+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p25_t4)

                            df_top5_pmin_t4=df[(df.Power_Label==l_min)][["Username","t4"]].nlargest(5, 't4').reset_index()
                            df_top5_pmin_t4['top5_pmin'] = [df_top5_pmin_t4.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_pmin_t4.t4.loc[0]),
                                                            df_top5_pmin_t4.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_pmin_t4.t4.loc[1]),
                                                            df_top5_pmin_t4.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_pmin_t4.t4.loc[2]),
                                                            df_top5_pmin_t4.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_pmin_t4.t4.loc[3]),
                                                            df_top5_pmin_t4.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_pmin_t4.t4.loc[4])]
                            df_top5_pmin_t4['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_pmin_t4)

                            fig_top5_pmin_t4 = go.Figure()
                            fig_top5_pmin_t4.add_trace(go.Bar(
                                    y=df_top5_pmin_t4.top5_pmin,
                                    x=df_top5_pmin_t4.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_pmin_t4['top5_pmin'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(166, 118, 29, 1)',
                                        line=dict(color='rgba(166, 118, 29, 1)', width=1)
                                    )
                                ))
                            fig_top5_pmin_t4.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                            fig_top5_pmin_t4.update_layout(title = "        🎖        "+'<b>'+l_min+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_pmin_t4)

                            with st.container():

                                mygrid = make_grid(9,19)
                                mygrid[0][7].plotly_chart(fig_head_t4)
                                mygrid[1][7].plotly_chart(fig_top5_p90_t4)
                                mygrid[2][5].plotly_chart(fig_top5_p80_t4)
                                mygrid[2][9].plotly_chart(fig_top5_p70_t4)
                                mygrid[3][1].plotly_chart(fig_top5_p60_t4)
                                mygrid[3][5].plotly_chart(fig_top5_p50_t4)
                                mygrid[3][9].plotly_chart(fig_top5_p25_t4)
                                mygrid[3][13].plotly_chart(fig_top5_pmin_t4)

                with tab2 :
                    with st.container():
                        x_Data_deads = [5,4.999]
                        y_Data_deads = ['DEATHS','LEADERBOARD']

                        fig_head_dead = go.Figure()
                        fig_head_dead.add_trace(go.Bar(
                                    y=y_Data_deads,
                                    x=x_Data_deads,
                                    textposition = "inside", 
                                    text = y_Data_deads,
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=13, color='white'),outsidetextfont=dict(family='Arial', size=12, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(47, 138, 196, 0.9)',
                                        line=dict(color='rgba(47, 138, 196, 1)', width=1)
                                    )
                                ))
                        fig_head_dead.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                        fig_head_dead.update_layout(margin=dict(t=20, b=0, l=0, r=0),
                                                width=250, height=75,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )
                            #st.plotly_chart(fig_head_kills)

                        df_top5_p90_dead=df[(df.Power_Label==l_p90)][["Username","dead"]].nlargest(5, 'dead').reset_index()
                        df_top5_p90_dead['top5_p90'] = [df_top5_p90_dead.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p90_dead.dead.loc[0]),
                                                            df_top5_p90_dead.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p90_dead.dead.loc[1]),
                                                            df_top5_p90_dead.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p90_dead.dead.loc[2]),
                                                            df_top5_p90_dead.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p90_dead.dead.loc[3]),
                                                            df_top5_p90_dead.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p90_dead.dead.loc[4])]
                        df_top5_p90_dead['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p90_kills)

                        fig_top5_p90_dead = go.Figure()
                        fig_top5_p90_dead.add_trace(go.Bar(
                                    y=df_top5_p90_dead.top5_p90,
                                    x=df_top5_p90_dead.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p90_dead['top5_p90'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),
                                    outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(237, 100, 90, 1)',
                                        line=dict(color='rgba(237, 100, 90, 1)', width=1)
                                    )
                                ))
                        fig_top5_p90_dead.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                        fig_top5_p90_dead.update_layout(title = "        🎖        "+'<b>'+l_p90+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},
                                                yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p90_dead)

                        df_top5_p80_dead=df[(df.Power_Label==l_p80)][["Username","dead"]].nlargest(5, 'dead').reset_index()
                        df_top5_p80_dead['top5_p80'] = [df_top5_p80_dead.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p80_dead.dead.loc[0]),
                                                            df_top5_p80_dead.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p80_dead.dead.loc[1]),
                                                            df_top5_p80_dead.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p80_dead.dead.loc[2]),
                                                            df_top5_p80_dead.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p80_dead.dead.loc[3]),
                                                            df_top5_p80_dead.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p80_dead.dead.loc[4])]
                        df_top5_p80_dead['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p80_kills)

                        fig_top5_p80_dead = go.Figure()
                        fig_top5_p80_dead.add_trace(go.Bar(
                                    y=df_top5_p80_dead.top5_p80,
                                    x=df_top5_p80_dead.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p80_dead['top5_p80'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(17, 165, 121, 1)',
                                        line=dict(color='rgba(17, 165, 121, 1)', width=1)
                                    )
                                ))
                        fig_top5_p80_dead.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                        fig_top5_p80_dead.update_layout(title = "        🎖        "+'<b>'+l_p80+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p80_dead)

                        df_top5_p70_dead=df[(df.Power_Label==l_p70)][["Username","dead"]].nlargest(5, 'dead').reset_index()
                        df_top5_p70_dead['top5_p70'] = [df_top5_p70_dead.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p70_dead.dead.loc[0]),
                                                            df_top5_p70_dead.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p70_dead.dead.loc[1]),
                                                            df_top5_p70_dead.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p70_dead.dead.loc[2]),
                                                            df_top5_p70_dead.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p70_dead.dead.loc[3]),
                                                            df_top5_p70_dead.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p70_dead.dead.loc[4])]
                        df_top5_p70_dead['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p70_dead)

                        fig_top5_p70_dead = go.Figure()
                        fig_top5_p70_dead.add_trace(go.Bar(
                                    y=df_top5_p70_dead.top5_p70,
                                    x=df_top5_p70_dead.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p70_dead['top5_p70'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(0, 134, 149, 1)',
                                        line=dict(color='rgba(0, 134, 149, 1)', width=1)
                                    )
                                ))
                        fig_top5_p70_dead.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                        fig_top5_p70_dead.update_layout(title = "        🎖        "+'<b>'+l_p70+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p70_dead)

                        df_top5_p60_dead=df[(df.Power_Label==l_p60)][["Username","dead"]].nlargest(5, 'dead').reset_index()
                        df_top5_p60_dead['top5_p60'] = [df_top5_p60_dead.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p60_dead.dead.loc[0]),
                                                            df_top5_p60_dead.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p60_dead.dead.loc[1]),
                                                            df_top5_p60_dead.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p60_dead.dead.loc[2]),
                                                            df_top5_p60_dead.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p60_dead.dead.loc[3]),
                                                            df_top5_p60_dead.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p60_dead.dead.loc[4])]
                        df_top5_p60_dead['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p60_kills)

                        fig_top5_p60_dead = go.Figure()
                        fig_top5_p60_dead.add_trace(go.Bar(
                                    y=df_top5_p60_dead.top5_p60,
                                    x=df_top5_p60_dead.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p60_dead['top5_p60'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(166, 118, 29, 1)',
                                        line=dict(color='rgba(166, 118, 29, 1)', width=1)
                                    )
                                ))
                        fig_top5_p60_dead.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                        fig_top5_p60_dead.update_layout(title = "        🎖        "+'<b>'+l_p60+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p60_kills)

                        df_top5_p50_dead=df[(df.Power_Label==l_p50)][["Username","dead"]].nlargest(5, 'dead').reset_index()
                        df_top5_p50_dead['top5_p50'] = [df_top5_p50_dead.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p50_dead.dead.loc[0]),
                                                            df_top5_p50_dead.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p50_dead.dead.loc[1]),
                                                            df_top5_p50_dead.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p50_dead.dead.loc[2]),
                                                            df_top5_p50_dead.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p50_dead.dead.loc[3]),
                                                            df_top5_p50_dead.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p50_dead.dead.loc[4])]
                        df_top5_p50_dead['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p50_dead)

                        fig_top5_p50_dead = go.Figure()
                        fig_top5_p50_dead.add_trace(go.Bar(
                                    y=df_top5_p50_dead.top5_p50,
                                    x=df_top5_p50_dead.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p50_dead['top5_p50'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(102, 17, 0, 1)',
                                        line=dict(color='rgba(102, 17, 0, 1)', width=1)
                                    )
                                ))
                        fig_top5_p50_dead.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                        fig_top5_p50_dead.update_layout(title = "        🎖        "+'<b>'+l_p50+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p50_dead)

                        df_top5_p25_dead=df[(df.Power_Label==l_p25)][["Username","dead"]].nlargest(5, 'dead').reset_index()
                        df_top5_p25_dead['top5_p25'] = [df_top5_p25_dead.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_p25_dead.dead.loc[0]),
                                                            df_top5_p25_dead.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_p25_dead.dead.loc[1]),
                                                            df_top5_p25_dead.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_p25_dead.dead.loc[2]),
                                                            df_top5_p25_dead.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_p25_dead.dead.loc[3]),
                                                            df_top5_p25_dead.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_p25_dead.dead.loc[4])]
                        df_top5_p25_dead['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_p25_kills)

                        fig_top5_p25_dead = go.Figure()
                        fig_top5_p25_dead.add_trace(go.Bar(
                                    y=df_top5_p25_dead.top5_p25,
                                    x=df_top5_p25_dead.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_p25_dead['top5_p25'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(0, 0, 0, 1)',
                                        line=dict(color='rgba(0, 0, 0, 1)', width=1)
                                    )
                                ))
                        fig_top5_p25_dead.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                        fig_top5_p25_dead.update_layout(title = "        🎖        "+'<b>'+l_p25+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_p25_kills)

                        df_top5_pmin_dead=df[(df.Power_Label==l_min)][["Username","dead"]].nlargest(5, 'dead').reset_index()
                        df_top5_pmin_dead['top5_pmin'] = [df_top5_pmin_dead.Username.loc[0]+" "+" | "+" "+" "+human_format2(df_top5_pmin_dead.dead.loc[0]),
                                                            df_top5_pmin_dead.Username.loc[1]+" "+" | "+" "+" "+human_format2(df_top5_pmin_dead.dead.loc[1]),
                                                            df_top5_pmin_dead.Username.loc[2]+" "+" | "+" "+" "+human_format2(df_top5_pmin_dead.dead.loc[2]),
                                                            df_top5_pmin_dead.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top5_pmin_dead.dead.loc[3]),
                                                            df_top5_pmin_dead.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top5_pmin_dead.dead.loc[4])]
                        df_top5_pmin_dead['dummy_value'] = ["5","4.9999","4.9998","4.9997","4.9996"]
                            #st.dataframe(df_top5_pmin_kills)

                        fig_top5_pmin_dead = go.Figure()
                        fig_top5_pmin_dead.add_trace(go.Bar(
                                    y=df_top5_pmin_dead.top5_pmin,
                                    x=df_top5_pmin_dead.dummy_value,
                                    textposition = "inside", 
                                    text = df_top5_pmin_dead['top5_pmin'],
                                    insidetextanchor="middle",
                                    insidetextfont=dict(family='Arial', size=11, color='white'),outsidetextfont=dict(family='Arial', size=11, color='white'),
                                    orientation='h',
                                    marker=dict(
                                        color='rgba(127, 60, 141, 1)',
                                        line=dict(color='rgba(127, 60, 141, 1)', width=1)
                                    )
                                ))
                        fig_top5_pmin_dead.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                            ticksuffix=' ', showline=False)
                        fig_top5_pmin_dead.update_layout(title = "        🎖        "+'<b>'+l_min+'</b>'+"        🎖        ",
                                                margin=dict(t=30, b=0, l=0, r=0),
                                                width=250, height=190,
                                                xaxis_title=' ', yaxis_title=" ",
                                                xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                                )

                            #st.plotly_chart(fig_top5_pmin_kills)

                        with st.container():

                            mygrid = make_grid(9,19)
                            mygrid[0][7].plotly_chart(fig_head_dead)
                            mygrid[1][7].plotly_chart(fig_top5_p90_dead)
                            mygrid[2][5].plotly_chart(fig_top5_p80_dead)
                            mygrid[2][9].plotly_chart(fig_top5_p70_dead)
                            mygrid[3][1].plotly_chart(fig_top5_p60_dead)
                            mygrid[3][5].plotly_chart(fig_top5_p50_dead)
                            mygrid[3][9].plotly_chart(fig_top5_p25_dead)
                            mygrid[3][13].plotly_chart(fig_top5_pmin_dead)

            if selected == "Top 25":
                tab1, tab2 = st.tabs([" 🪖 Most Valuable Killers", " 🎗 Hall of Heroes"])
                with tab1 :
                    with st.container():
                        top25_option = ["🎖 All in One", "🏅 T5 Killers", "🏅 T4 Killers"]
                        col1,col2,col3,col4,col5 = st.columns(5)
                        with col1:
                            top25_choice = st.selectbox("",top25_option)

                        if top25_choice == "🎖 All in One":
                            df_top25_kills=df.nlargest(25, 'kills')
                            df_top25_kills=df_top25_kills[["Username","kills"]].reset_index()

                            df_top25_kills_3to10=df_top25_kills.iloc[3:10]
                            df_top25_kills_3to10['killshuman'] = [df_top25_kills_3to10.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top25_kills_3to10.kills.loc[3]),
                                                        df_top25_kills_3to10.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top25_kills_3to10.kills.loc[4]),
                                                        df_top25_kills_3to10.Username.loc[5]+" "+" | "+" "+" "+human_format2(df_top25_kills_3to10.kills.loc[5]),
                                                        df_top25_kills_3to10.Username.loc[6]+" "+" | "+" "+" "+human_format2(df_top25_kills_3to10.kills.loc[6]),
                                                        df_top25_kills_3to10.Username.loc[7]+" "+" | "+" "+" "+human_format2(df_top25_kills_3to10.kills.loc[7]),
                                                        df_top25_kills_3to10.Username.loc[8]+" "+" | "+" "+" "+human_format2(df_top25_kills_3to10.kills.loc[8]),
                                                        df_top25_kills_3to10.Username.loc[9]+" "+" | "+" "+" "+human_format2(df_top25_kills_3to10.kills.loc[9])]
                            #st.dataframe(df_top25_3to10)
                            #Total t5 Average by Power Label

                            fig_top25_4to10_kills = go.Figure()
                            fig_top25_4to10_kills.add_trace(go.Bar(
                                y=df_top25_kills_3to10.killshuman,
                                x=df_top25_kills_3to10.kills,
                                textposition = "inside", 
                                text = df_top25_kills_3to10['killshuman'],
                                insidetextanchor="middle",
                                insidetextfont=dict(family='Arial', size=12, color='white'),outsidetextfont=dict(family='Arial', size=12, color='white'),
                                orientation='h',
                                marker=dict(
                                    color='rgba(55, 126, 184, 0.9)',
                                    line=dict(color='rgba(55, 126, 184, 1)', width=1)
                                )
                            ))
                            fig_top25_4to10_kills.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                        ticksuffix=' ', showline=False)
                            fig_top25_4to10_kills.update_layout(margin=dict(t=30, b=30, l=80, r=50),
                                            width=450, height=280,
                                            xaxis_title=' ', yaxis_title=" ",
                                            xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                            )

                            #st.plotly_chart(fig_top25_4to10_kills)

                            df_top25_kills_11to25=df_top25_kills.iloc[10:25]
                            df_top25_kills_11to25['killshuman'] = [df_top25_kills_11to25.Username.loc[10]+" "+" | "+" "+" "+human_format2(df_top25_kills_11to25.kills.loc[10]),
                                                        df_top25_kills_11to25.Username.loc[11]+" "+" | "+" "+" "+human_format2(df_top25_kills_11to25.kills.loc[11]),
                                                        df_top25_kills_11to25.Username.loc[12]+" "+" | "+" "+" "+human_format2(df_top25_kills_11to25.kills.loc[12]),
                                                        df_top25_kills_11to25.Username.loc[13]+" "+" | "+" "+" "+human_format2(df_top25_kills_11to25.kills.loc[13]),
                                                        df_top25_kills_11to25.Username.loc[14]+" "+" | "+" "+" "+human_format2(df_top25_kills_11to25.kills.loc[14]),
                                                        df_top25_kills_11to25.Username.loc[15]+" "+" | "+" "+" "+human_format2(df_top25_kills_11to25.kills.loc[15]),
                                                        df_top25_kills_11to25.Username.loc[16]+" "+" | "+" "+" "+human_format2(df_top25_kills_11to25.kills.loc[16]),
                                                        df_top25_kills_11to25.Username.loc[17]+" "+" | "+" "+" "+human_format2(df_top25_kills_11to25.kills.loc[17]),
                                                        df_top25_kills_11to25.Username.loc[18]+" "+" | "+" "+" "+human_format2(df_top25_kills_11to25.kills.loc[18]),
                                                        df_top25_kills_11to25.Username.loc[19]+" "+" | "+" "+" "+human_format2(df_top25_kills_11to25.kills.loc[19]),
                                                        df_top25_kills_11to25.Username.loc[20]+" "+" | "+" "+" "+human_format2(df_top25_kills_11to25.kills.loc[20]),
                                                        df_top25_kills_11to25.Username.loc[21]+" "+" | "+" "+" "+human_format2(df_top25_kills_11to25.kills.loc[21]),
                                                        df_top25_kills_11to25.Username.loc[22]+" "+" | "+" "+" "+human_format2(df_top25_kills_11to25.kills.loc[22]),
                                                        df_top25_kills_11to25.Username.loc[23]+" "+" | "+" "+" "+human_format2(df_top25_kills_11to25.kills.loc[23]),
                                                        df_top25_kills_11to25.Username.loc[24]+" "+" | "+" "+" "+human_format2(df_top25_kills_11to25.kills.loc[24])]
                            #st.dataframe(df_top25_11to25)
                            #Total t5 Average by Power Label

                            fig_top25_11to25_kills = go.Figure()
                            fig_top25_11to25_kills.add_trace(go.Bar(
                                y=df_top25_kills_11to25.killshuman,
                                x=df_top25_kills_11to25.kills,
                                textposition = "inside", 
                                text = df_top25_kills_11to25['killshuman'],
                                insidetextanchor="middle",
                                insidetextfont=dict(family='Arial', size=12, color='white'),outsidetextfont=dict(family='Arial', size=12, color='white'),
                                orientation='h',
                                marker=dict(
                                    color='rgba(228, 26, 28, 0.8)',
                                    line=dict(color='rgba(228, 26, 28, 1)', width=1)
                                )
                            ))
                            fig_top25_11to25_kills.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                        ticksuffix=' ', showline=False)
                            fig_top25_11to25_kills.update_layout(margin=dict(t=10, b=0, l=60, r=80),
                                            width=450, height=460,
                                            xaxis_title=' ', yaxis_title=" ",
                                            xaxis={'visible': False, 'showticklabels': False},yaxis={'visible': False, 'showticklabels': False},
                                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                            )

                            #st.plotly_chart(fig_top25_11to25_kills)

                            with st.container():

                                mygrid = make_grid(5,7)

                                t5cav2_image = Image.open(IMAGES_DIR / "t5cav2.png")
                                t5inf2_image = Image.open(IMAGES_DIR / "t5inf2.png")
                                t5arch2_image = Image.open(IMAGES_DIR / "t5arch2.png")
                                t5_mvk_image = Image.open(IMAGES_DIR / "mvkillers.png")

                                st.markdown("""
                                                <style>
                                                div[data-testid="metric-container"] {
                                                background-color: rgba(28, 131, 225, 0.1);
                                                border: 1px solid rgba(28, 131, 225, 0.1);
                                                padding: 5% 5% 5% 2%;
                                                border-radius: 10px;
                                                color: rgb(30, 103, 119);
                                                overflow-wrap: break-word;
                                                }
                                                </style>
                                                """
                                                , unsafe_allow_html=True)
                                
                                mygrid[0][3].metric(label=" 👑 " + df_top25_kills.Username.iloc[0],value="",delta=human_format2(df_top25_kills.kills.iloc[0]))
                                mygrid[1][2].metric(label=" 🥈 " + df_top25_kills.Username.iloc[1],value="",delta=human_format2(df_top25_kills.kills.iloc[1]))
                                mygrid[1][4].metric(label=" 🥉 " + df_top25_kills.Username.iloc[2],value="",delta=human_format2(df_top25_kills.kills.iloc[2]))

                                mygrid[2][1].plotly_chart(fig_top25_4to10_kills)
                                mygrid[0][4].image(t5cav2_image, width=85)
                                mygrid[1][3].image(t5inf2_image, width=85)
                                mygrid[1][5].image(t5arch2_image, width=85)
                                mygrid[2][3].plotly_chart(fig_top25_11to25_kills)
                                mygrid[2][5].image(t5_mvk_image, width=300)

                        if top25_choice == "🏅 T5 Killers":
                            df_top25_t5=df.nlargest(25, 't5')
                            df_top25_t5=df_top25_t5[["Username","t5"]].reset_index()

                            df_top25_t5_3to10=df_top25_t5.iloc[3:10]
                            df_top25_t5_3to10['t5human'] = [df_top25_t5_3to10.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top25_t5_3to10.t5.loc[3]),
                                                        df_top25_t5_3to10.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top25_t5_3to10.t5.loc[4]),
                                                        df_top25_t5_3to10.Username.loc[5]+" "+" | "+" "+" "+human_format2(df_top25_t5_3to10.t5.loc[5]),
                                                        df_top25_t5_3to10.Username.loc[6]+" "+" | "+" "+" "+human_format2(df_top25_t5_3to10.t5.loc[6]),
                                                        df_top25_t5_3to10.Username.loc[7]+" "+" | "+" "+" "+human_format2(df_top25_t5_3to10.t5.loc[7]),
                                                        df_top25_t5_3to10.Username.loc[8]+" "+" | "+" "+" "+human_format2(df_top25_t5_3to10.t5.loc[8]),
                                                        df_top25_t5_3to10.Username.loc[9]+" "+" | "+" "+" "+human_format2(df_top25_t5_3to10.t5.loc[9])]
                            #st.dataframe(df_top25_3to10)
                            #Total t5 Average by Power Label

                            fig_top25_4to10_t5s = go.Figure()
                            fig_top25_4to10_t5s.add_trace(go.Bar(
                                y=df_top25_t5_3to10.t5human,
                                x=df_top25_t5_3to10.t5,
                                textposition = "inside", 
                                text = df_top25_t5_3to10['t5human'],
                                insidetextanchor="middle",
                                insidetextfont=dict(family='Arial', size=12, color='white'),outsidetextfont=dict(family='Arial', size=12, color='white'),
                                orientation='h',
                                marker=dict(
                                    color='rgba(17, 119, 51, 0.8)',
                                    line=dict(color='rgba(17, 119, 51, 1)', width=1)
                                )
                            ))
                            fig_top25_4to10_t5s.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                        ticksuffix=' ', showline=False)
                            fig_top25_4to10_t5s.update_layout(margin=dict(t=30, b=30, l=80, r=50),
                                            width=450, height=280,
                                            xaxis_title=' ', yaxis_title=" ",
                                            xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                            )

                            #st.plotly_chart(fig_top25_4to10_t5s)

                            df_top25_t5_11to25=df_top25_t5.iloc[10:25]
                            df_top25_t5_11to25['t5human'] = [df_top25_t5_11to25.Username.loc[10]+" "+" | "+" "+" "+human_format2(df_top25_t5_11to25.t5.loc[10]),
                                                        df_top25_t5_11to25.Username.loc[11]+" "+" | "+" "+" "+human_format2(df_top25_t5_11to25.t5.loc[11]),
                                                        df_top25_t5_11to25.Username.loc[12]+" "+" | "+" "+" "+human_format2(df_top25_t5_11to25.t5.loc[12]),
                                                        df_top25_t5_11to25.Username.loc[13]+" "+" | "+" "+" "+human_format2(df_top25_t5_11to25.t5.loc[13]),
                                                        df_top25_t5_11to25.Username.loc[14]+" "+" | "+" "+" "+human_format2(df_top25_t5_11to25.t5.loc[14]),
                                                        df_top25_t5_11to25.Username.loc[15]+" "+" | "+" "+" "+human_format2(df_top25_t5_11to25.t5.loc[15]),
                                                        df_top25_t5_11to25.Username.loc[16]+" "+" | "+" "+" "+human_format2(df_top25_t5_11to25.t5.loc[16]),
                                                        df_top25_t5_11to25.Username.loc[17]+" "+" | "+" "+" "+human_format2(df_top25_t5_11to25.t5.loc[17]),
                                                        df_top25_t5_11to25.Username.loc[18]+" "+" | "+" "+" "+human_format2(df_top25_t5_11to25.t5.loc[18]),
                                                        df_top25_t5_11to25.Username.loc[19]+" "+" | "+" "+" "+human_format2(df_top25_t5_11to25.t5.loc[19]),
                                                        df_top25_t5_11to25.Username.loc[20]+" "+" | "+" "+" "+human_format2(df_top25_t5_11to25.t5.loc[20]),
                                                        df_top25_t5_11to25.Username.loc[21]+" "+" | "+" "+" "+human_format2(df_top25_t5_11to25.t5.loc[21]),
                                                        df_top25_t5_11to25.Username.loc[22]+" "+" | "+" "+" "+human_format2(df_top25_t5_11to25.t5.loc[22]),
                                                        df_top25_t5_11to25.Username.loc[23]+" "+" | "+" "+" "+human_format2(df_top25_t5_11to25.t5.loc[23]),
                                                        df_top25_t5_11to25.Username.loc[24]+" "+" | "+" "+" "+human_format2(df_top25_t5_11to25.t5.loc[24])]
                            #st.dataframe(df_top25_11to25)
                            #Total t5 Average by Power Label

                            fig_top25_11to25_t5s = go.Figure()
                            fig_top25_11to25_t5s.add_trace(go.Bar(
                                y=df_top25_t5_11to25.t5human,
                                x=df_top25_t5_11to25.t5,
                                textposition = "inside", 
                                text = df_top25_t5_11to25['t5human'],
                                insidetextanchor="middle",
                                insidetextfont=dict(family='Arial', size=12, color='white'),outsidetextfont=dict(family='Arial', size=12, color='white'),
                                orientation='h',
                                marker=dict(
                                    color='rgba(225, 124, 5, 0.9)',
                                    line=dict(color='rgba(225, 124, 5, 1)', width=1)
                                )
                            ))
                            fig_top25_11to25_t5s.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                        ticksuffix=' ', showline=False)
                            fig_top25_11to25_t5s.update_layout(margin=dict(t=10, b=0, l=60, r=80),
                                            width=450, height=460,
                                            xaxis_title=' ', yaxis_title=" ",
                                            xaxis={'visible': False, 'showticklabels': False},yaxis={'visible': False, 'showticklabels': False},
                                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                            )

                            #st.plotly_chart(fig_top25_11to25_t5s)

                            with st.container():

                                t5cav_image = Image.open(IMAGES_DIR / "t5cav.png")
                                t5inf_image = Image.open(IMAGES_DIR / "t5inf.png")
                                t5arch_image = Image.open(IMAGES_DIR / "t5arch.png")
                                t5pic_image = Image.open(IMAGES_DIR / "t5pic.png")

                                mygrid = make_grid(5,7)
                                st.markdown("""
                                                <style>
                                                div[data-testid="metric-container"] {
                                                background-color: rgba(28, 131, 225, 0.1);
                                                border: 1px solid rgba(28, 131, 225, 0.1);
                                                padding: 5% 5% 5% 2%;
                                                border-radius: 10px;
                                                color: rgb(30, 103, 119);
                                                overflow-wrap: break-word;
                                                }
                                                </style>
                                                """
                                                , unsafe_allow_html=True)
                                
                                mygrid[0][3].metric(label=" 👑 " + df_top25_t5.Username.iloc[0],value="",delta=human_format2(df_top25_t5.t5.iloc[0]))
                                mygrid[1][2].metric(label=" 🥈 " + df_top25_t5.Username.iloc[1],value="",delta=human_format2(df_top25_t5.t5.iloc[1]))
                                mygrid[1][4].metric(label=" 🥉 " + df_top25_t5.Username.iloc[2],value="",delta=human_format2(df_top25_t5.t5.iloc[2]))

                                mygrid[2][1].plotly_chart(fig_top25_4to10_t5s)
                                mygrid[1][5].image(t5arch_image, width=85)
                                mygrid[0][4].image(t5cav_image, width=85)
                                mygrid[1][3].image(t5inf_image, width=85)
                                mygrid[2][3].plotly_chart(fig_top25_11to25_t5s)
                                mygrid[2][5].image(t5pic_image, width=300)

                        if top25_choice == "🏅 T4 Killers":
                            df_top25_t4=df.nlargest(25, 't4')
                            df_top25_t4=df_top25_t4[["Username","t4"]].reset_index()

                            df_top25_t4_3to10=df_top25_t4.iloc[3:10]
                            df_top25_t4_3to10['t4human'] = [df_top25_t4_3to10.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top25_t4_3to10.t4.loc[3]),
                                                        df_top25_t4_3to10.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top25_t4_3to10.t4.loc[4]),
                                                        df_top25_t4_3to10.Username.loc[5]+" "+" | "+" "+" "+human_format2(df_top25_t4_3to10.t4.loc[5]),
                                                        df_top25_t4_3to10.Username.loc[6]+" "+" | "+" "+" "+human_format2(df_top25_t4_3to10.t4.loc[6]),
                                                        df_top25_t4_3to10.Username.loc[7]+" "+" | "+" "+" "+human_format2(df_top25_t4_3to10.t4.loc[7]),
                                                        df_top25_t4_3to10.Username.loc[8]+" "+" | "+" "+" "+human_format2(df_top25_t4_3to10.t4.loc[8]),
                                                        df_top25_t4_3to10.Username.loc[9]+" "+" | "+" "+" "+human_format2(df_top25_t4_3to10.t4.loc[9])]
                            #st.dataframe(df_top25_3to10)
                            #Total t5 Average by Power Label

                            fig_top25_4to10_t4s = go.Figure()
                            fig_top25_4to10_t4s.add_trace(go.Bar(
                                y=df_top25_t4_3to10.t4human,
                                x=df_top25_t4_3to10.t4,
                                textposition = "inside", 
                                text = df_top25_t4_3to10['t4human'],
                                insidetextanchor="middle",
                                insidetextfont=dict(family='Arial', size=12, color='white'),outsidetextfont=dict(family='Arial', size=12, color='white'),
                                orientation='h',
                                marker=dict(
                                    color='rgba(127, 60, 141, 0.8)',
                                    line=dict(color='rgba(127, 60, 141, 1)', width=1)
                                )
                            ))
                            fig_top25_4to10_t4s.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                        ticksuffix=' ', showline=False)
                            fig_top25_4to10_t4s.update_layout(margin=dict(t=30, b=30, l=80, r=50),
                                            width=450, height=280,
                                            xaxis_title=' ', yaxis_title=" ",
                                            xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                            )

                            #st.plotly_chart(fig_top25_4to10_t4s)

                            df_top25_t4_11to25=df_top25_t4.iloc[10:25]
                            df_top25_t4_11to25['t4human'] = [df_top25_t4_11to25.Username.loc[10]+" "+" | "+" "+" "+human_format2(df_top25_t4_11to25.t4.loc[10]),
                                                        df_top25_t4_11to25.Username.loc[11]+" "+" | "+" "+" "+human_format2(df_top25_t4_11to25.t4.loc[11]),
                                                        df_top25_t4_11to25.Username.loc[12]+" "+" | "+" "+" "+human_format2(df_top25_t4_11to25.t4.loc[12]),
                                                        df_top25_t4_11to25.Username.loc[13]+" "+" | "+" "+" "+human_format2(df_top25_t4_11to25.t4.loc[13]),
                                                        df_top25_t4_11to25.Username.loc[14]+" "+" | "+" "+" "+human_format2(df_top25_t4_11to25.t4.loc[14]),
                                                        df_top25_t4_11to25.Username.loc[15]+" "+" | "+" "+" "+human_format2(df_top25_t4_11to25.t4.loc[15]),
                                                        df_top25_t4_11to25.Username.loc[16]+" "+" | "+" "+" "+human_format2(df_top25_t4_11to25.t4.loc[16]),
                                                        df_top25_t4_11to25.Username.loc[17]+" "+" | "+" "+" "+human_format2(df_top25_t4_11to25.t4.loc[17]),
                                                        df_top25_t4_11to25.Username.loc[18]+" "+" | "+" "+" "+human_format2(df_top25_t4_11to25.t4.loc[18]),
                                                        df_top25_t4_11to25.Username.loc[19]+" "+" | "+" "+" "+human_format2(df_top25_t4_11to25.t4.loc[19]),
                                                        df_top25_t4_11to25.Username.loc[20]+" "+" | "+" "+" "+human_format2(df_top25_t4_11to25.t4.loc[20]),
                                                        df_top25_t4_11to25.Username.loc[21]+" "+" | "+" "+" "+human_format2(df_top25_t4_11to25.t4.loc[21]),
                                                        df_top25_t4_11to25.Username.loc[22]+" "+" | "+" "+" "+human_format2(df_top25_t4_11to25.t4.loc[22]),
                                                        df_top25_t4_11to25.Username.loc[23]+" "+" | "+" "+" "+human_format2(df_top25_t4_11to25.t4.loc[23]),
                                                        df_top25_t4_11to25.Username.loc[24]+" "+" | "+" "+" "+human_format2(df_top25_t4_11to25.t4.loc[24])]
                            #st.dataframe(df_top25_11to25)
                            #Total t5 Average by Power Label

                            fig_top25_11to25_t4s = go.Figure()
                            fig_top25_11to25_t4s.add_trace(go.Bar(
                                y=df_top25_t4_11to25.t4human,
                                x=df_top25_t4_11to25.t4,
                                textposition = "inside", 
                                text = df_top25_t4_11to25['t4human'],
                                insidetextanchor="middle",
                                insidetextfont=dict(family='Arial', size=12, color='white'),outsidetextfont=dict(family='Arial', size=12, color='white'),
                                orientation='h',
                                marker=dict(
                                    color='rgba(166, 118, 29, 0.9)',
                                    line=dict(color='rgba(166, 118, 29, 1)', width=1)
                                )
                            ))
                            fig_top25_11to25_t4s.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                        ticksuffix=' ', showline=False)
                            fig_top25_11to25_t4s.update_layout(margin=dict(t=10, b=0, l=65, r=80),
                                            width=450, height=460,
                                            xaxis_title=' ', yaxis_title=" ",
                                            xaxis={'visible': False, 'showticklabels': False},yaxis={'visible': False, 'showticklabels': False},
                                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                            )

                            #st.plotly_chart(fig_top25_11to25_t4s)

                            with st.container():

                                t4cav_image = Image.open(IMAGES_DIR / "t4cav.png")
                                t4inf_image = Image.open(IMAGES_DIR / "t4inf.png")
                                t4arch_image = Image.open(IMAGES_DIR / "t4arch.png")
                                t4_image = Image.open(IMAGES_DIR / "t4pic.png")

                                mygrid = make_grid(5,7)
                                st.markdown("""
                                                <style>
                                                div[data-testid="metric-container"] {
                                                background-color: rgba(28, 131, 225, 0.1);
                                                border: 1px solid rgba(28, 131, 225, 0.1);
                                                padding: 5% 5% 5% 2%;
                                                border-radius: 10px;
                                                color: rgb(30, 103, 119);
                                                overflow-wrap: break-word;
                                                }
                                                </style>
                                                """
                                                , unsafe_allow_html=True)
                                
                                mygrid[0][3].metric(label=" 👑 " + df_top25_t4.Username.iloc[0],value="",delta=human_format2(df_top25_t4.t4.iloc[0]))
                                mygrid[1][2].metric(label=" 🥈 " + df_top25_t4.Username.iloc[1],value="",delta=human_format2(df_top25_t4.t4.iloc[1]))
                                mygrid[1][4].metric(label=" 🥉 " + df_top25_t4.Username.iloc[2],value="",delta=human_format2(df_top25_t4.t4.iloc[2]))

                                mygrid[2][1].plotly_chart(fig_top25_4to10_t4s)
                                mygrid[1][5].image(t4arch_image, width=85)
                                mygrid[0][4].image(t4cav_image, width=85)
                                mygrid[1][3].image(t4inf_image, width=85)
                                mygrid[2][3].plotly_chart(fig_top25_11to25_t4s)
                                mygrid[2][5].image(t4_image, width=300)

                with tab2:
                    df_top25_dead=df.nlargest(25, 'dead')
                    df_top25_dead=df_top25_dead[["Username","dead"]].reset_index()

                    df_top25_dead_3to10=df_top25_dead.iloc[3:10]
                    df_top25_dead_3to10['deadhuman'] = [df_top25_dead_3to10.Username.loc[3]+" "+" | "+" "+" "+human_format2(df_top25_dead_3to10.dead.loc[3]),
                                                df_top25_dead_3to10.Username.loc[4]+" "+" | "+" "+" "+human_format2(df_top25_dead_3to10.dead.loc[4]),
                                                df_top25_dead_3to10.Username.loc[5]+" "+" | "+" "+" "+human_format2(df_top25_dead_3to10.dead.loc[5]),
                                                df_top25_dead_3to10.Username.loc[6]+" "+" | "+" "+" "+human_format2(df_top25_dead_3to10.dead.loc[6]),
                                                df_top25_dead_3to10.Username.loc[7]+" "+" | "+" "+" "+human_format2(df_top25_dead_3to10.dead.loc[7]),
                                                df_top25_dead_3to10.Username.loc[8]+" "+" | "+" "+" "+human_format2(df_top25_dead_3to10.dead.loc[8]),
                                                df_top25_dead_3to10.Username.loc[9]+" "+" | "+" "+" "+human_format2(df_top25_dead_3to10.dead.loc[9])]
                    #st.dataframe(df_top25_3to10)
                    #Total t5 Average by Power Label

                    fig_top25_4to10_deads = go.Figure()
                    fig_top25_4to10_deads.add_trace(go.Bar(
                        y=df_top25_dead_3to10.deadhuman,
                        x=df_top25_dead_3to10.dead,
                        textposition = "inside", 
                        text = df_top25_dead_3to10['deadhuman'],
                        insidetextanchor="middle",
                        insidetextfont=dict(family='Arial', size=12, color='white'),outsidetextfont=dict(family='Arial', size=12, color='white'),
                        orientation='h',
                        marker=dict(
                            color='rgba(0, 0, 0, 1)',
                            line=dict(color='rgba(0, 0, 0, 1)', width=1)
                        )
                    ))
                    fig_top25_4to10_deads.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                ticksuffix=' ', showline=False)
                    fig_top25_4to10_deads.update_layout(margin=dict(t=30, b=30, l=80, r=50),
                                    width=450, height=280,
                                    xaxis_title=' ', yaxis_title=" ",
                                    xaxis={'visible': False, 'showticklabels': False,'autorange':'reversed'},yaxis={'visible': False, 'showticklabels': False},
                                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'# Transparent background
                                    )

                    #st.plotly_chart(fig_top25_4to10_deads)

                    df_top25_dead_11to25=df_top25_dead.iloc[10:25]
                    df_top25_dead_11to25['deadhuman'] = [df_top25_dead_11to25.Username.loc[10]+" "+" | "+" "+" "+human_format2(df_top25_dead_11to25.dead.loc[10]),
                                                df_top25_dead_11to25.Username.loc[11]+" "+" | "+" "+" "+human_format2(df_top25_dead_11to25.dead.loc[11]),
                                                df_top25_dead_11to25.Username.loc[12]+" "+" | "+" "+" "+human_format2(df_top25_dead_11to25.dead.loc[12]),
                                                df_top25_dead_11to25.Username.loc[13]+" "+" | "+" "+" "+human_format2(df_top25_dead_11to25.dead.loc[13]),
                                                df_top25_dead_11to25.Username.loc[14]+" "+" | "+" "+" "+human_format2(df_top25_dead_11to25.dead.loc[14]),
                                                df_top25_dead_11to25.Username.loc[15]+" "+" | "+" "+" "+human_format2(df_top25_dead_11to25.dead.loc[15]),
                                                df_top25_dead_11to25.Username.loc[16]+" "+" | "+" "+" "+human_format2(df_top25_dead_11to25.dead.loc[16]),
                                                df_top25_dead_11to25.Username.loc[17]+" "+" | "+" "+" "+human_format2(df_top25_dead_11to25.dead.loc[17]),
                                                df_top25_dead_11to25.Username.loc[18]+" "+" | "+" "+" "+human_format2(df_top25_dead_11to25.dead.loc[18]),
                                                df_top25_dead_11to25.Username.loc[19]+" "+" | "+" "+" "+human_format2(df_top25_dead_11to25.dead.loc[19]),
                                                df_top25_dead_11to25.Username.loc[20]+" "+" | "+" "+" "+human_format2(df_top25_dead_11to25.dead.loc[20]),
                                                df_top25_dead_11to25.Username.loc[21]+" "+" | "+" "+" "+human_format2(df_top25_dead_11to25.dead.loc[21]),
                                                df_top25_dead_11to25.Username.loc[22]+" "+" | "+" "+" "+human_format2(df_top25_dead_11to25.dead.loc[22]),
                                                df_top25_dead_11to25.Username.loc[23]+" "+" | "+" "+" "+human_format2(df_top25_dead_11to25.dead.loc[23]),
                                                df_top25_dead_11to25.Username.loc[24]+" "+" | "+" "+" "+human_format2(df_top25_dead_11to25.dead.loc[24])]
                    #st.dataframe(df_top25_11to25)
                    #Total t5 Average by Power Label

                    fig_top25_11to25_deads = go.Figure()
                    fig_top25_11to25_deads.add_trace(go.Bar(
                        y=df_top25_dead_11to25.deadhuman,
                        x=df_top25_dead_11to25.dead,
                        textposition = "inside", 
                        text = df_top25_dead_11to25['deadhuman'],
                        insidetextanchor="middle",
                        insidetextfont=dict(family='Arial', size=12, color='white'),outsidetextfont=dict(family='Arial', size=12, color='white'),
                        orientation='h',
                        marker=dict(
                            color='rgba(102, 17, 0, 0.9)',
                            line=dict(color='rgba(204, 102, 119, 1)', width=1)
                        )
                    ))
                    fig_top25_11to25_deads.update_yaxes(showgrid=False, categoryorder='total ascending', 
                                ticksuffix=' ', showline=False)
                    fig_top25_11to25_deads.update_layout(margin=dict(t=10, b=0, l=60, r=80),
                                    width=450, height=530,
                                    xaxis_title=' ', yaxis_title=" ",
                                    xaxis={'visible': False, 'showticklabels': False},yaxis={'visible': False, 'showticklabels': False},
                                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',# Transparent background
                                    )

                    #st.plotly_chart(fig_top25_11to25_deads)

                    with st.container():

                        deads_image = Image.open(IMAGES_DIR / "deads.png")
                        hoh_image = Image.open(IMAGES_DIR / "hoh.png")

                        mygrid = make_grid(5,7)
                        st.markdown("""
                                        <style>
                                        div[data-testid="metric-container"] {
                                        background-color: rgba(28, 131, 225, 0.1);
                                        border: 1px solid rgba(28, 131, 225, 0.1);
                                        padding: 5% 5% 5% 2%;
                                        border-radius: 10px;
                                        color: rgb(30, 103, 119);
                                        overflow-wrap: break-word;
                                        }
                                        </style>
                                        """
                                        , unsafe_allow_html=True)
                        
                        mygrid[0][3].metric(label=" 👑 " + df_top25_dead.Username.iloc[0],value="",delta=human_format2(df_top25_dead.dead.iloc[0]))
                        mygrid[1][2].metric(label=" 🥈 " + df_top25_dead.Username.iloc[1],value="",delta=human_format2(df_top25_dead.dead.iloc[1]))
                        mygrid[1][4].metric(label=" 🥉 " + df_top25_dead.Username.iloc[2],value="",delta=human_format2(df_top25_dead.dead.iloc[2]))

                        mygrid[2][1].plotly_chart(fig_top25_4to10_deads)
                        mygrid[2][1].image(deads_image, width=400)
                        mygrid[2][3].plotly_chart(fig_top25_11to25_deads)
                        mygrid[2][5].image(hoh_image, width=325)

if selected == "Contact":

    col1, col2 = st.columns([1,1])

    with col1:
        st.write("")
        st.subheader(":mailbox: Any Question? Ask Away 🙌")
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
        st.subheader("")
        st.success("*Also open for recommendations! Just send an e-mail 👆 Constructive criticism is always acceptable :)")
    with col2:
        product_image = Image.open(IMAGES_DIR / "post_box.jpg")
        st.image(product_image)