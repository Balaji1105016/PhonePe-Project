#pip install streamlit_option_menu
#pip install pillow

import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector as sql
from pprint import pprint
from PIL import Image
from streamlit_option_menu import option_menu

# Establish a connection to the database
db = sql.connect(host="127.0.0.1", user="root", password="test", database="PhonePe_Streamlit")
cur = db.cursor(buffered=True)

# Application Logo Section
img_path = r"C:\Users\Balaji\Music\PhonePe_App_Logo.jpg"
img = Image.open(img_path)
st.image(img)
st.write("""
         Note: Blink-Time Is An Interactive, User-Friendly Web Application That Allows Users To Get Some Indepth Insights About The PhonePe Data By Doing The Data Extraction From PhonePe Pulse GitHub Repository,Transforming The Data By Doing Data Cleansing,Inserting the Transformed Data in SQL,Retriving the Data from SQL DB Using Python Code And Finally Presenting Them In Streamlit App With More Amazing Data Visuals Using Plotly. 
         """)


# Login and Logout Section
if 'login_status' not in st.session_state:
    st.session_state.login_status = False
    
username = st.text_input("User Name")
password = st.text_input("Password",type = 'password')
if st.button("Login"):
    if username == "Balaji" and password == "Balaji@123":
        st.session_state.login_status = True
        st.success("Login Successful!")
    
    else:
        st.session_state.login_status = False
        st.error("Invalid Credentials. Please try again.")

if st.session_state.login_status:      
    logout = st.sidebar.button("Logout")
    if logout:
        if 'login_status' in st.session_state:
            st.session_state.login_status = False
            st.experimental_rerun()
            
            
# Guidence Section:
    st.sidebar.write("""
                    Note: Incase Of Any Issues With Input Data,Kindly Refer Resource Section
                    """)

# Main Application Page:     
    with st.sidebar:
        menu_sel = option_menu("Menu", ["Home","Transactions","Top Brands","Registered Users","Access Frequency","Resources","Links","Process","Features","About"], 
                    icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle","gear","play","cloud-upload","list-task","list-task","list-task"],
                    styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-1px", "--hover-color": "#6F36AD"},
                            "nav-link-selected": {"background-color": "#6F36AD"}})
    
    #Home Section:    
    if menu_sel=="Home":
        st.subheader("!!!....Phonepe Pulse Data Visualization And Exploration....!!!")
        st.subheader("""
                        PhonePe Importance:\n
                        1)Unified Platform: PhonePe provides a unified platform for various financial transactions, including mobile recharges, bill payments, money transfers, and online shopping.\n
                        2)UPI Integration: PhonePe heavily utilizes Unified Payments Interface (UPI), allowing users to make seamless and instant bank-to-bank transfers.\n
                        3)Wide Acceptance: PhonePe is widely accepted across numerous online and offline merchants, making it convenient for users to make payments at various establishments.\n
                        4)In-app Services: Beyond payments, PhonePe offers in-app services such as mutual funds investments, insurance payments, and gold purchases, providing users with a comprehensive financial platform.\n
                        5)User-Friendly Interface: The app is known for its user-friendly interface, making it easy for both tech-savvy and non-tech-savvy users to navigate and conduct transactions.\n
                        6)Cashback and Rewards: PhonePe often runs cashback and reward programs, incentivizing users to make transactions through their platform.\n
            """)

    #Transaction Section:
    if menu_sel=="Transactions":
        with st.sidebar:
            trans_options = option_menu("Transaction",["State_Wise","District_Wise","Pincode_Wise","Year_Wise","Highiest_Trans_Amt","Highiest_Trans_Count"],
                            styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "FF7F50"},
                                    "nav-link-selected": {"background-color": "#6F36AD"}})
            
        if trans_options == "State_Wise":
            st.header("State Wise Transaction")
            st.success("""
                     Note: This Module Provides The Information About State,Transaction Type,Total Transaction Count,Total Transaction Amount,Average Transaction Amount Based On State Wise Category
                     """)
            state = st.text_input("Enter the State ")
            year = st.text_input("Enter the Year ")
            quarter = st.text_input("Enter the Quarter ")
            Ag_t_button = st.button("Submit")
            
            # Fetching the initial map without highlighting any specific state
            q0 = "SELECT State, sum(Transaction_Count) as Total_Transaction_Count, sum(Transaction_Amount) as Total_Transaction_Amount,Avg(Transaction_Amount) as Average_Transaction_Amount FROM ag_t GROUP BY State"
            cur.execute(q0)
            initial_result = cur.fetchall()
            initial_df = pd.DataFrame(initial_result, columns=['State', 'Total_Transaction_Count', 'Total_Transaction_Amount',"Average_Transaction_Amount"])

            # initial map
            st.subheader("India Map")
            fig = px.choropleth(
                initial_df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                locations='State',
                featureidkey='properties.ST_NM',
                color='Total_Transaction_Amount',
                hover_data=['State', 'Total_Transaction_Count', 'Total_Transaction_Amount','Average_Transaction_Amount'],
                color_continuous_scale='reds')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
            
            # Geo-Pie Chart:
               
            if Ag_t_button:
                st.success("""
                         Note: The user inputs like State,Year and Quarter will be applicable for the Geo-pie chart alone
                         """)
                q1 = f"select State, Year, Quarter, Transaction_Type, sum(Transaction_Count) as Total_Transaction_Count, sum(Transaction_Amount) as Total_Transaction_Amount,Avg(Transaction_Amount) as Average_Transaction_Amount FROM ag_t WHERE State='{state}' AND Year='{year}' AND Quarter='{quarter}' GROUP BY State, Year, Quarter, Transaction_Type"
                cur.execute(q1)
                result = cur.fetchall()
                df = pd.DataFrame(result, columns=['State', 'Year', 'Quarter', 'Transaction_Type', 'Total_Transaction_Count', 'Total_Transaction_Amount',"Average_Transaction_Amount"])

                if not df.empty:
                    fig_0 = px.choropleth(
                        df,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        locations='State',
                        featureidkey='properties.ST_NM',
                        color='Total_Transaction_Amount',
                        hover_data=['Transaction_Type', 'Total_Transaction_Count', 'Total_Transaction_Amount',"Average_Transaction_Amount"],
                        color_continuous_scale='reds',
                        title = "Geo-Pie Chart")
                    
                    fig_0.update_geos(fitbounds="locations", visible=False)
                    st.plotly_chart(fig_0)
                    
        if trans_options == "District_Wise":
            st.header("District Wise Transaction")
            st.success("""
                     Note: This Module Provides The Information About District Name,Total Transaction Count,Total Transaction Amount,Average Transaction Amount Based On District Wise Category
                     """)
            
            District_Name = st.text_input("Enter the District Name ")
            year = st.text_input("Enter the Year ")
            quarter = st.text_input("Enter the Quarter ")
            Mp_t_button = st.button("Submit")

            if Mp_t_button:
                q2 = f"select District_Name,Year,Quarter,sum(Transaction_Count) as Total_Transaction_Count, sum(Transaction_Amount) as Total_Transaction_Amount,Avg(Transaction_Amount) as Average_Transaction_Amount FROM mp_t WHERE District_Name ='{District_Name}' AND Year='{year}' AND Quarter='{quarter}' GROUP BY District_Name, Year, Quarter"
                cur.execute(q2)
                result_1 = cur.fetchall()
                df_1 = pd.DataFrame(result_1, columns=[ "District_Name", "Year", "Quarter", "Total_Transaction_Count", "Total_Transaction_Amount","Average_Transaction_Amount"])

                if not df_1.empty:
                    st.subheader(f"Details For District - {District_Name}, Year - {year}, Quarter - {quarter}")

                    # Sunburst chart
                    fig = px.sunburst(
                        df_1,
                        path=['Average_Transaction_Amount','Total_Transaction_Amount','Total_Transaction_Count','Quarter', 'Year', 'District_Name'],
                        hover_data = ['Average_Transaction_Amount','Total_Transaction_Count','Total_Transaction_Amount'],
                        title = "Sunburst Chart")
                    st.plotly_chart(fig)
        
        if trans_options == "Pincode_Wise":
            st.header("Pincode Wise Transaction")
            st.success("""
                     Note: This Module Provides The Information About Pincode Number,Total Transaction Count,Total Transaction Amount,Average Transaction Amount Based On Pincode Wise Category
                     """)
            
            Pincode_Number = st.text_input("Enter the Pincode")
            Year = st.text_input("Enter the Year")
            Quarter = st.text_input("Enter the Quarter")
            tp_t_button = st.button("Submit")
            if tp_t_button:
                q3 = f"Select Pincode,Year,Quarter,sum(Transaction_Count) as Total_Transaction_Count, sum(Transaction_Amount) as Total_Transaction_Amount,Avg(Transaction_Amount) as Average_Transaction_Amount FROM tp_t where pincode = {Pincode_Number} and Year = {Year} and Quarter = {Quarter} group by Pincode,Year,Quarter"
                cur.execute(q3)
                result_2 = cur.fetchall()
                df_2 = pd.DataFrame(result_2,columns = ["Pincode","Year","Quarter","Total_Transaction_Count","Total_Transaction_Amount","Average_Transaction_Amount"])
                
                if not df_2.empty:
                    st.subheader(f"Details For Pincode - {Pincode_Number}, Year - {Year}, Quarter - {Quarter}")
            
                    # Sunburst chart
                    fig = px.sunburst(
                        df_2,
                        path=["Average_Transaction_Amount","Total_Transaction_Amount","Total_Transaction_Count",'Quarter', 'Year', 'Pincode'],
                        hover_data=["Average_Transaction_Amount",'Total_Transaction_Count','Total_Transaction_Amount'],
                        title = "Sunburst Chart")
                    st.plotly_chart(fig)
                    
        if trans_options == "Year_Wise":
            st.header("Year-Wise Transactions")
            st.success("""
                     Note: This Module Provides The Information About Year,Quarter,Total Transaction Amount,Average Transaction Amount Based On Year Wise Category
                     """)
            
            q4 = "SELECT Year, Quarter, SUM(Transaction_Amount) as Total_Transaction_Amount,Avg(Transaction_Amount) as Average_Transaction_Amount FROM ag_t GROUP BY Year, Quarter ORDER BY Total_Transaction_Amount,Average_Transaction_Amount LIMIT 100"
            cur.execute(q4)
            result_3 = cur.fetchall()
            df_3 = pd.DataFrame(result_3, columns=["Year", "Quarter", "Total_Transaction_Amount","Average_Transaction_Amount"])
            if not df_3.empty:
                fig = px.line(
                    df_3,
                    x="Quarter",
                    y="Total_Transaction_Amount",
                    color="Year",
                    labels={"Total_Transaction_Amount": "Total Transaction Amount"},
                    hover_data=["Quarter","Year","Total_Transaction_Amount","Average_Transaction_Amount"],
                    title="Year-Wise Trend Chart"
                )
                
                st.plotly_chart(fig)

            

        if trans_options == "Highiest_Trans_Amt":
            st.header("Top 10 Transactions By Transaction Amount")
            q5 = f"select Year,State,Quarter,Sum(Transaction_Count) as Total_Transaction_Count,sum(Transaction_Amount) as Total_Transaction_Amount from ag_t group by year,State,Quarter Order By Total_Transaction_Amount desc limit 10"
            cur.execute(q5)
            result_4 = cur.fetchall()
            df_4 = pd.DataFrame(result_4,columns = ['Year','State','Quarter','Total_Transaction_Count','Total_Transaction_Amount'])
            if not df_4.empty:
                
                fig = px.bar(
                                df_4,
                                x='State',
                                y='Total_Transaction_Amount',
                                color='Year',
                                color_discrete_sequence="color_palette",
                                facet_col='Year',
                                labels={'Total_Transaction_Amount':'Total Transaction Amount'})
                                

                st.plotly_chart(fig)
            
            st.header("Top 5 Transactions By Transaction Amount")
            q6 = f"select Year,State,Quarter,Sum(Transaction_Count) as Total_Transaction_Count,sum(Transaction_Amount) as Total_Transaction_Amount from ag_t group by year,State,Quarter Order By Total_Transaction_Amount desc limit 5"
            cur.execute(q6)
            result_5 = cur.fetchall()
            df_5 = pd.DataFrame(result_5,columns = ['Year','State','Quarter','Total_Transaction_Count','Total_Transaction_Amount'])
            if not df_5.empty:
                fig = px.bar(
                                df_5,
                                x='State',
                                y='Total_Transaction_Amount',
                                color='Year',
                                color_discrete_sequence="color_palette",
                                facet_col='Year',
                                labels={'Total_Transaction_Amount':'Total Transaction Amount'})
                                

                st.plotly_chart(fig)
            st.subheader("Reason")
            st.write("""
                    Karnata Ranks the Highiest in the PhonePe Transactions Amount.\n
                    
                    Factors:\n
                    1) Digital Adoption: Karnataka might have a higher level of digital literacy and technology adoption compared to other regions, leading to a greater acceptance of digital payment platforms like PhonePe.\n
                    2) Urbanization and Tech Hubs: If Karnataka has urban centers or technology hubs like Bangalore (Bengaluru), the population there may be more inclined to use digital payment methods due to a higher concentration of tech-savvy individuals and businesses.\n
                    3) Promotion and Partnerships: PhonePe or associated businesses might have implemented targeted marketing strategies or partnerships in Karnataka, encouraging more people to use the platform.\n
                    4) Government Initiatives: Government policies or initiatives in Karnataka could be promoting digital payments, leading to a higher adoption rate in the state.\n
                    5) Ease of Use and Features: If PhonePe offers specific features or ease of use that resonates well with the people of Karnataka, it could contribute to higher transaction volumes.\n
                    6) Demographics: The demographic composition of Karnataka, including factors like age groups and income levels, may influence the preference for digital payment methods.\n
                    
                    """)
        
        if trans_options == "Highiest_Trans_Count":
            st.header("Top 10 Transactions By Transaction Count")
            q7 = f"select Year,State,Quarter,Sum(Transaction_Count) as Total_Transaction_Count,sum(Transaction_Amount) as Total_Transaction_Amount from ag_t group by year,State,Quarter Order By Total_Transaction_Count desc limit 10"
            cur.execute(q7)
            result_6 = cur.fetchall()
            df_6 = pd.DataFrame(result_6,columns = ['Year','State','Quarter','Total_Transaction_Count','Total_Transaction_Amount'])
            if not df_6.empty:
                
                fig = px.bar(
                                df_6,
                                x='State',
                                y='Total_Transaction_Count',
                                color='Year',
                                color_discrete_sequence="color_palette", 
                                facet_col='Year',
                                labels={'Total_Transaction_Count':'Total Transaction Count'})
                                

                st.plotly_chart(fig)
            
            st.header("Top 5 Transactions By Transaction Count")
            q8 = f"select Year,State,Quarter,Sum(Transaction_Count) as Total_Transaction_Count,sum(Transaction_Amount) as Total_Transaction_Amount from ag_t group by year,State,Quarter Order By Total_Transaction_Count desc limit 5"
            cur.execute(q8)
            result_7 = cur.fetchall()
            df_7 = pd.DataFrame(result_7,columns = ['Year','State','Quarter','Total_Transaction_Count','Total_Transaction_Amount'])
            if not df_7.empty:
                fig = px.bar(
                                df_7,
                                x='State',
                                y='Total_Transaction_Count',
                                color='Year',
                                color_discrete_sequence="color_palette", 
                                facet_col='Year',
                                labels={'Total_Transaction_Count':'Total Transaction Count'})
                               

                st.plotly_chart(fig)
                st.subheader("Reason")
                st.write("""
                    The usage of PhonePe Transaction in Karnataka ranks Highiest.\n
                    
                    Factors:\n
                    1) Digital Adoption: Karnataka might have a higher level of digital literacy and technology adoption compared to other regions, leading to a greater acceptance of digital payment platforms like PhonePe.\n
                    2) Urbanization and Tech Hubs: If Karnataka has urban centers or technology hubs like Bangalore (Bengaluru), the population there may be more inclined to use digital payment methods due to a higher concentration of tech-savvy individuals and businesses.\n
                    3) Promotion and Partnerships: PhonePe or associated businesses might have implemented targeted marketing strategies or partnerships in Karnataka, encouraging more people to use the platform.\n
                    4) Government Initiatives: Government policies or initiatives in Karnataka could be promoting digital payments, leading to a higher adoption rate in the state.\n
                    5) Ease of Use and Features: If PhonePe offers specific features or ease of use that resonates well with the people of Karnataka, it could contribute to higher transaction volumes.\n
                    6) Demographics: The demographic composition of Karnataka, including factors like age groups and income levels, may influence the preference for digital payment methods.\n
                    
                    """)
    
    # Top Brands Section:            
    if menu_sel == "Top Brands":
        with st.sidebar:
            Brands_options = option_menu("Brands",["Brands_Wise","Top Brands Insights"],
                            styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "FF7F50"},
                                    "nav-link-selected": {"background-color": "#6F36AD"}})
        if Brands_options == "Brands_Wise":
            st.subheader("Top Brand Contribution - State-wise")
            st.success("""
                     Note: This Module Provides The Information About State,Brand,Brand_Rank,Total Usage Count,Total Usage In Percentage Based On State Wise Category
                     """)
            q9 = f"""Select  State,Brand,Brand_Rank, Total_Usage_Count, Total_Usage_In_Percentage
                            FROM (select State,Year,Quarter,Brand,
                                    SUM(Count) AS Total_Usage_Count,
                                    SUM(Percentage) AS Total_Usage_In_Percentage,
                                    DENSE_RANK() OVER (PARTITION BY State ORDER BY SUM(Count) DESC) AS Brand_Rank
                                FROM ag_u GROUP BY State, Year, Quarter, Brand) ranked_data
                            WHERE Brand_Rank  = 1
                            ORDER BY Total_Usage_Count desc
                        """
            
            cur.execute(q9)
            result_8 = cur.fetchall()
            df_8 = pd.DataFrame(result_8, columns=["State","Brand","Brand_Rank", "Total_Usage_Count", "Total_Usage_In_Percentage"])
            
            if not df_8.empty:
                fig = px.choropleth(
                    df_8,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    locations='State',
                    featureidkey='properties.ST_NM',
                    color='State',
                    hover_data=['State', 'Brand','Brand_Rank', 'Total_Usage_Count', 'Total_Usage_In_Percentage'],
                    color_continuous_scale='reds',
                    title="Top Brand Contribution - State-wise"
                )
                fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
            
        if Brands_options == "Top Brands Insights":
            st.subheader("Top-10 Brands")
            st.write("Note: This module will be helpfull in PhonePe Marketting")
            q10 = f"select Brand,sum(Count) as Total_Usage_Count,sum(Percentage) as Total_Usage_In_Percentage from ag_u group by Brand order by Total_Usage_Count desc limit 10"
            cur.execute(q10)
            result_9 = cur.fetchall()
            df_9 = pd.DataFrame(result_9,columns= ["Brand","Total_Usage_Count","Total_Usage_In_Percentage"])
            if not df_9.empty:        
                fig = px.bar(
                    df_9,
                    x='Brand',
                    y='Total_Usage_Count',
                    color='Total_Usage_Count',
                    labels={'Total_Usage_In_Percentage': 'Total Usage In Percentage'},
                    title="Top 10 Brands Based on Total Usage Count")

                st.plotly_chart(fig)
                
            st.subheader("Top-5 Brands")
            q11 = f"select Brand,sum(Count) as Total_Usage_Count,sum(Percentage) as Total_Usage_In_Percentage from ag_u group by Brand order by Total_Usage_Count desc limit 5"
            cur.execute(q11)
            result_10 = cur.fetchall()
            df_10 = pd.DataFrame(result_10,columns= ["Brand","Total_Usage_Count","Total_Usage_In_Percentage"])
            if not df_10.empty:        
                fig = px.bar(
                    df_10,
                    x='Brand',
                    y='Total_Usage_Count',
                    color='Total_Usage_Count',
                    labels={'Total_Usage_In_Percentage': 'Total Usage In Percentage'},
                    title="Top 5 Brands Based on Total Usage Count")

                st.plotly_chart(fig)
            st.subheader("Reason:")
            st.write(""" 
                    Xiaomi Brand ranks the highiest in PhonePe Trasactions.\n
                    
                    Factors:\n
                    1) Market Presence: Xiaomi has a significant market presence, and if they have a large user base, it would naturally reflect in transaction data.\n
                    2) Affordability: Xiaomi is known for offering feature-rich smartphones at competitive prices. This affordability could attract a larger user base, including those who use digital payment platforms like PhonePe.\n
                    3) Partnerships and Offers: Companies often collaborate to provide exclusive deals or discounts to users of specific brands. If Xiaomi has such partnerships with PhonePe, it could encourage users to prefer that platform for transactions.\n
                    4) User Demographics: Different smartphone brands often have distinct user demographics. If Xiaomi's user base aligns well with the target audience of PhonePe, it could contribute to higher transaction numbers.\n
                    5) Pre-installed Apps: Some smartphone brands come with pre-installed apps, including digital payment apps. If PhonePe is pre-installed on Xiaomi phones or promoted through their ecosystem, it may influence user behavior
                    
                    """)
    
    #Registered Users Section:
    if menu_sel == "Registered Users":
            st.subheader("Top 10 PhonePe Registered Users Count - District Wise")
            q12 = f"select State,District_Name,year,Quarter,sum(Registered_Users) as Total_Registered_Users from mp_u group by State,District_Name,Year,Quarter order by Total_Registered_Users desc limit 10"
            cur.execute(q12)
            result_11 = cur.fetchall()
            df_11 = pd.DataFrame(result_11,columns = ["State","District_Name","Year","Quarter","Total_Registered_Users"])
            if not df_11.empty:
                fig = px.sunburst(
                        df_11,
                        path=["Total_Registered_Users",'Quarter', 'Year', 'District_Name','State'],
                        hover_data = ["Total_Registered_Users"])
                st.plotly_chart(fig)
                
            st.subheader("Reason:")
            st.write(""" 
                    On State - Karnataka State,District - Bengaluru Urban District,Year - 2023,Quarter - 4,Total_Registered_Users - 16895567 Ranks The Highiest In Total-Registered-User-Count.\n
                    
                    Factors:\n
                    1) Population Density: Higher population density areas tend to have more users of digital payment services.\n
                    2) Promotions and Marketing: If PhonePe has run targeted promotions or marketing campaigns in Muzaffarabad district, it could attract more users.\n
                    3) Local Partnerships: Collaborations with local businesses, governments, or financial institutions might lead to increased adoption in a particular area.\n
                    4) Network Effect: If a significant number of people in Muzaffarabad are already using PhonePe, it can create a network effect, encouraging more individuals to join.\n
                    5) Access to Smartphones and Internet: The availability and accessibility of smartphones and the internet play a crucial role in the adoption of digital payment services.
                    """)
    
    #Access Frequency Section:
    if menu_sel == "Access Frequency":
        st.subheader("Application Accessing Frequency")
        q13 = f"select District_Name,Year,sum(App_opens) as Application_Accessing_Frequency from mp_u group by District_Name,Year order by Application_Accessing_Frequency desc Limit 100"
        cur.execute(q13)
        result_12 = cur.fetchall()
        df_12 = pd.DataFrame(result_12,columns = ["District_Name","Year","Application_Accessing_Frequency"])
        if not df_12.empty:
            fig = px.line(
                    df_12,
                    x="Year",
                    y="Application_Accessing_Frequency",
                    color="District_Name",
                    labels={"Application_Accessing_Frequency": "Application Accessing Frequency"},
                    title="Application Accessing Frequency Trend Chart")
            st.plotly_chart(fig)
        st.subheader("Reason:")
        st.write("""
                Bengaluru Urban District Ranks The Highiest in PhonePe Application Accessing Frequency.
                
                Factors:\n
                1) Population Density: Bengaluru Urban district is one of the most populous and economically active regions in India. Higher population density often correlates with increased adoption of digital services, including mobile payment apps like PhonePe.\n
                2) Tech-Savvy Population: Bengaluru is known as the IT hub of India, with a large population working in the technology sector. This tech-savvy population is likely to be early adopters of digital payment solutions.\n
                3) Urban Lifestyle: Urban areas tend to have higher smartphone penetration and better internet connectivity, making it more convenient for residents to use mobile applications for various services, including payments.\n
                4) Business and Commerce: Bengaluru is a major business and commercial center, and businesses often prefer digital payment solutions for their convenience and efficiency. This can drive the adoption of mobile payment apps among residents.\n
                5) Marketing and Promotions: PhonePe, like other digital payment providers, may run targeted marketing campaigns and promotions in specific regions. If Bengaluru has been a focus for such initiatives, it could contribute to higher adoption.\n
                6) Partnerships and Tie-ups: Collaborations with local businesses, government bodies, or financial institutions can impact the popularity of a payment app in a specific region.\n
                7) Word of Mouth: Positive experiences and recommendations from friends, family, or colleagues can significantly influence the adoption of mobile payment apps in a community.\n
                
                """)
    
    #Resources Section:
    if menu_sel == "Resources":
        st.header("Available Resources")
        q14 = f"Select distinct(Year) from ag_t"
        cur.execute(q14)
        result_13 = cur.fetchall()
        st.subheader("Year Information")
        pprint(st.dataframe(pd.DataFrame(result_13,columns = ["Year"])))
        q15 = f"Select distinct(State) from ag_t"
        cur.execute(q15)
        result_14 = cur.fetchall()
        st.subheader("State Information")
        pprint(st.dataframe(pd.DataFrame(result_14,columns = ["State"])))
        q16 = f"Select distinct(District_Name) from mp_t"
        cur.execute(q16)
        result_15 = cur.fetchall()
        st.subheader("District Information")
        pprint(st.dataframe(pd.DataFrame(result_15,columns = ["District_Name"])))
        q17 = f"Select distinct(Pincode) from tp_u"
        cur.execute(q17)
        result_16 = cur.fetchall()
        st.subheader("Pincode Information")
        pprint(st.dataframe(pd.DataFrame(result_16,columns = ["Pincode"])))
        q18 = f"Select distinct(Quarter) from tp_u"
        cur.execute(q18)
        result_17 = cur.fetchall()
        st.subheader("Quarter Information")
        pprint(st.dataframe(pd.DataFrame(result_17,columns = ["Quarter"])))
    
    # About Section:    
    if menu_sel == "About":
        img_path = r"C:\Users\Balaji\Music\Personal_Pic\Balaji_pic.jpeg"
        img = Image.open(img_path)
    # Show the image using Streamlit
        st.image(img, caption="""Name: BALAJI BALAKRISHNAN(Data Engineer)""", use_column_width=True)
        st.write("Applitaion Name: Blink-Time")
        st.write("Developed By: Balaji Balakrishnan")
        st.write("Designation: Data Engineer")
        st.write("Industry Experience: 7+ Years")
        st.write("Worked Companies: FLEX,TCS,DvSuM India Private Limited")
        st.write("Tech Skills: SQL,PL-SQL,Oracle,Python,MongoDB,AWS,Tableau,Streamlit,ServiceNow")
        st.markdown("Linkedin URL: https://www.linkedin.com/in/balaji-balakrishnan-34471b167/")
        st.markdown("GitHub URL: https://github.com/Balaji1105016/PhonePe-Project.git")
    
    #Links Section:
    if menu_sel == "Links": 
        st.header("Useful Links")
        st.subheader("PhonePe GitHub Repo Source Link")    
        st.markdown("https://github.com/PhonePe/pulse.git")
        st.subheader("Streamlit")
        st.markdown("https://www.youtube.com/@streamlitofficial")
        st.subheader("Plotly")
        st.markdown("https://plotly.com/")
        st.subheader("GitHub Cloning")
        st.markdown("https://stackoverflow.com/questions/2472552/python-way-to-clone-a-git-repository")
    
    #Process Section:    
    if menu_sel == "Process":
        st.header("Application Process Overview")
        st.write("""
                     1. Data extraction: Cloning the Github using scripting to fetch the data from the
                        Phonepe pulse Github repository and store it in a suitable format such as CSV
                        or JSON.\n
                        
                     2. Data transformation: Using a scripting language such as Python, along with
                        libraries such as Pandas, to manipulate and pre-process the data. This may
                        include cleaning the data, handling missing values, and transforming the data
                        into a format suitable for analysis and visualization.\n
                     
                     3. Database insertion: Using the "mysql-connector-python" library in Python to
                        connect to a MySQL database and insert the transformed data using SQL
                        commands.\n

                     4. Dashboard creation: Using the Streamlit and Plotly libraries in Python to create
                        an interactive and visually appealing dashboard. Plotly's built-in geo map
                        functions can be used to display the data on a map and Streamlit can be used
                        to create a user-friendly interface with multiple dropdown options for users to
                        select different facts and figures to display.\n
                     
                     5. Data retrieval: Using the "mysql-connector-python" library to connect to the
                        MySQL database and fetch the data into a Pandas dataframe. Use the data in
                        the dataframe to update the dashboard dynamically.\n
                     
                     6. Deployment: Ensuring the solution is secure, efficient, and user-friendly. Test
                        the solution thoroughly and deploy the dashboard publicly, making it
                        accessible to users.\n
                        
                        This approach leverages the power of Python and its numerous libraries to extract,
                        transform, and analyze data, and to create a user-friendly dashboard for visualizing
                        the insights obtained from the data.
                     """)
    
    #Features Section:
    if menu_sel == "Features":
        st.header("Application Features")
        st.write("""
                 1) Easy To Interact
                 2) Get some indepth insights on PhonePe Data
                 3) Better Data Visualization
                 4) Easy to understand the process
                 """)
