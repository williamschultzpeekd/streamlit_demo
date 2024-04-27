import pandas as pd
import streamlit as st
st.set_page_config(layout="wide") 

df = pd.read_csv('https://github.com/WilliamSchultz/steamlit_app/blob/main/allb.csv?raw=true')

df = df[['domain', 'title', 'rev', 'items', 'category', 'brand', 'url']]

#st.set_option('theme.secondaryBackgroundColor', '#A670FF')
#st.set_option('theme.accent', '#A670FF')

# Convert 'rev' column to dollar format
#df['rev'] = df['rev'].apply(lambda x: '${:,.2f}'.format(x))
# -- Set page config
#st.set_page_config(page_title='Grips')

# Title the app
#st.header('Grips product analysis')

#app main image
#image = Image.open('F:\DYMO NA App\images\logo.svg.PNG')
#st.image(image,
        #use_column_width=True )

#st.markdown ('##')

#App title

st.title("Grips")
st.subheader("Allbirds.com Product Analysis")
st.markdown("February 2024")

#st.markdown('##')

#Slidebar filter
#st.sidebar.header("Choose your product")

# Filtering sidebar
#st.sidebar.title('* Grips')
#htp="https://github.com/WilliamSchultz/steamlit_app/blob/main/Logomark.png"
#st.image(htp, caption= 'logo', width=350)
st.sidebar.subheader('Filter Data')
min_rev, max_rev = st.sidebar.slider('Select revenue range', min_value=df['rev'].min(), max_value=df['rev'].max(), value=(df['rev'].min(), df['rev'].max()))

selected_brand = st.sidebar.selectbox('Select brand', df['brand'].unique())

url_filter = st.sidebar.text_input('Enter URL to filter')

selected_category = st.sidebar.selectbox('Select category', df['category'].unique())

min_items, max_items = st.sidebar.slider('Select item sold range', min_value=df['items'].min(), max_value=df['items'].max(), value=(df['items'].min(), df['items'].max()))

search_title = st.sidebar.text_input('Search by title')


# Apply filters
filtered_df = df[(df['rev'] >= min_rev) & (df['rev'] <= max_rev)]
if selected_brand:
    filtered_df = filtered_df[filtered_df['brand'] == selected_brand]
if url_filter:
    filtered_df = filtered_df[filtered_df['url'].str.contains(url_filter)]
if selected_category:
    filtered_df = filtered_df[filtered_df['category'] == selected_category]
if min_items and max_items:
    filtered_df = filtered_df[(filtered_df['items'] >= min_items) & (filtered_df['items'] <= max_items)]
if search_title:
    filtered_df = filtered_df[filtered_df['title'].str.contains(search_title)]

# Display the dataframe in full browser size
#st.sidebar.title('Sidebar Title')
#st.sidebar.write('Add your sidebar content here')
#st.write(df, width=0)

# Reset all filters button
if st.sidebar.button('Reset All Filters'):
    st.experimental_set_query_params()
    st.experimental_rerun()

# Display filtered data in table
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(filtered_df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='Grips-data-sample.csv',
    mime='text/csv',
)
st.write(filtered_df, width=1200)
st.write(f"Results: {len(filtered_df)}")
