import streamlit as st

st.set_page_config(page_title='Vinos', page_icon='🍷',layout='wide')


import json

from streamlit_lottie import st_lottie

from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pandas as pd
import numpy as np

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode


import streamlit.components.v1 as stc

# Data Viz Pkgs
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

import seaborn as sns



HTML_SEPARADOR = """
    <div style="background-color:#464e5f;padding:5px;border-radius:20px">
    </div>
    """
HTML_SEP = """<hr width=100%  align="center"  size=10 color="blue">"""

hide_style = """
            <style>
            footer{visibility: hidden;}
            </style>
            """
st.markdown(hide_style, unsafe_allow_html=True)


@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

def transform_format(val):
    if val == 0:
        return 255
    else:
        return val

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

col1, col2, col3 = st.columns([1, 2.5, 1])
with col3: 
    lottie_btc1 = load_lottiefile("analytics.json")
    st_lottie(lottie_btc1,
    speed=1,
    reverse=False,
    loop=True,
    quality="low", # medium ; high
    #renderer="svg", # canvas
    height=200,
    width=160,
    key="lottie1",
    )

with col2:
    st.title("Magazine Vinos App")
    st.markdown(
    """
    Esta app utiliza un dataset con reseñas de sommeliers a vinos procedentes de distintos paises.
    Los vinos son puntuados de 1 a 100 y el precio es por botella.\n
    Datos tomados de [WineEnthusiast](https://www.winemag.com/?s=&drink_type=wine) y
    descargados de [Kagle](https://www.kaggle.com/datasets/zynicide/wine-reviews).
    No hay valores faltantes y se dispone de mucho texto para wordclouds (columna **description** 
    es la reseña), ademas de los datos categóricos y numéricos.

    """
    )
with col1: 
    lottie_btc2 = load_lottiefile("cheers-wine.json")
    st_lottie(lottie_btc2,
    speed=1,
    reverse=False,
    loop=True,
    quality="low", # medium ; high
    #renderer="svg", # canvas
    height=200,
    width=160,
    key="lottie2",
    )


col1 = st.sidebar
col2, col3 = st.columns((3, 1))

# Sidebar + Main panel
col1.header("Ingrese opciones")

df = pd.read_csv("winemag-data-130k-v2-ok.csv", index_col=0)
df['points'] = df['points'].astype(float)
df['price'] = df['price'].astype(float)


print(df.dtypes)
print(df.info(verbose=True))

# Borro Faltantes
df = df.dropna(subset=['country'])

# Relleno faltantes
values = {"points": 75, "price": 10}
df = df.fillna(value=values)

# Sidebar - Seleccion Pais
paises = sorted(df["country"].unique())
selected_country = col1.multiselect("Elija Pais", paises, paises)
                
df_selected_country = df[(df["country"].isin(selected_country))]  # Filtering data

# Sidebar - Seleccion Puntaje y Precio
col1.subheader("De los paises seleccionados:")
puntosi, puntosf = col1.select_slider(
     'Indique puntaje vinos y rango precios',
     options=[10,20,30,40,50,60,70,80,90,100],
     value=(50, 100))

precioi = col1.number_input("Precio Min",value=10,step=5)
preciof = col1.number_input("Precio Max",value=100,step=5)

mask = (df_selected_country['points'] >= puntosi) & (df_selected_country['points'] <= puntosf) & (df_selected_country['price'] >= precioi) & (df_selected_country['price'] <= preciof)

dffiltro = df_selected_country.loc[mask]
                

#df = pd.read_csv("winemag-data-130k-v2-ok.csv", index_col=0)
# st.dataframe(df)
#AgGrid(dffiltro)

with col2:

    st.subheader("Tabla Interactiva de Vinos Seleccionados")
    gb = GridOptionsBuilder.from_dataframe(dffiltro)
    #gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gb.configure_pagination()
    #gb.configure_side_bar()
    #gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="count", editable=True)
    gridOptions = gb.build()

    data = AgGrid(dffiltro, 
        gridOptions=gridOptions, 
        enable_enterprise_modules=True,
        fit_columns_on_grid_load=True,
        theme='streamlit', 
        allow_unsafe_jscode=True, 
        update_mode=GridUpdateMode.SELECTION_CHANGED)

    #print("existe? ===>", ' Estate Grown' in df.price.values) 
    #print(df.isin([' Estate Grown']).any()) # busco por columna
    #st.write(df.query('price == " Estate Grown"')) #busco en la columna

    #st.caption("There are {} observations and {} features in this dataset.".format(dffiltro.shape[0],dffiltro.shape[1]))
    #st.caption("There are {} types of wine in this dataset such as {}...".format(len(dffiltro.variety.unique()),
    #", ".join(dffiltro.variety.unique()[0:5])))
    #st.caption("There are {} countries producing wine in this dataset such as {}...".format(len(dffiltro.country.unique()),
    #", ".join(dffiltro.country.unique()[0:5])))

with col3:
    # Start with one review:
    #text = df.description[0]
    text = " ".join(review for review in dffiltro.description)
    #st.text("There are {} words in the \ncombination of all review.".format(len(text)))
    
    st.subheader("Word Cloud Vinos")

    # Create stopword list:
    stopwords = set(STOPWORDS)
    stopwords.update(["drink", "now", "wine", "flavor", "flavors"])

    wine_mask = np.array(Image.open("iwine_mask.png"))
    print(wine_mask)

    # Transform your mask into a new one that will work with the function:
    transformed_wine_mask = np.ndarray((wine_mask.shape[0],wine_mask.shape[1]), np.int32)

    for i in range(len(wine_mask)):
        transformed_wine_mask[i] = list(map(transform_format, wine_mask[i]))

    # Check the expected result of your mask
    print(transformed_wine_mask)

    wordcloud = WordCloud(background_color="white", max_words=1000, mask=transformed_wine_mask,
            stopwords=stopwords, contour_width=1, contour_color='seashell').generate(text)
    fig4 = plt.figure(figsize=(60,30))
    plt.imshow(wordcloud)
    plt.axis("off")
    #plt.show();
    st.pyplot(fig4)

    wordcloud.to_file("reviews_botella.png")

    #st.text("There are {} words in the \ncombination of all review.".format(len(text)))

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    filas = (dffiltro.shape[0])
    st.metric("Registros", value=filas)
with col2:
    cols = (dffiltro.shape[1])
    st.metric("Columnas", value=cols) 
with col3:
    vars = len(dffiltro.variety.unique())
    st.metric("Tipos de Vino", value=vars)
with col4:
    paises = len(dffiltro.country.unique())
    st.metric("Paises", value=paises)
with col5:
    palabras=len(text)
    st.metric ("Palabras Reseñas", value=palabras)

col1, col2 = st.columns(2)
with col1:
    # Groupby by country
    country = dffiltro.groupby("country")

    st.subheader("Resumen Estadistico por Pais")
    st.write(country.describe())
    #AgGrid(country.describe())
    #st.write(country.mean().sort_values(by="points",ascending=False).head())
    
    #st.write(country.size().sort_values(ascending=False))
    st.subheader("Vinos Reseñados por Pais")
    fig = plt.figure(figsize=(15,10))
    country.size().sort_values(ascending=False).plot.bar()
    #plt.title("Vinos Reseñados por Pais")
    plt.xticks(rotation=50)
    plt.xlabel("Country of Origin")
    plt.ylabel("Number of Wines")
    #plt.show()
    st.pyplot(fig) 


with col2:

    #st.write(country.max().sort_values(by="points",ascending=False)["points"])
    st.subheader("Vinos por Puntaje y Pais")
    fig2 = plt.figure(figsize=(15,10))
    country.max().sort_values(by="points",ascending=False)["points"].plot.bar()
    #plt.title("Vinos por Puntaje y Pais")
    plt.xticks(rotation=50)
    plt.xlabel("Country of Origin")
    plt.ylabel("Highest point of Wines")
    #plt.show()
    st.pyplot(fig2)

    # Create and generate a word cloud image:
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)

    # Display the generated image:
    fig3 = plt.figure(figsize=(20,10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    #plt.savefig(f'wordcloud.png',dpi = 300)
    #plt.show()
    st.pyplot(fig3)

    # Save the image in the img folder:
    wordcloud.to_file("reviews_rectangulo.png")


#with st.expander("Borrador"):

    #st.write(dffiltro[["country", "description","points","price"]].head())

    
    #st.header('----------------------------------------------------------')

    #fig1 = plt.figure()
    #plt.xticks(rotation=90)
    #sns.countplot(df['country'])
    #st.pyplot(fig1)

    #st.header('----------------------------------------------------------')
            
    #st.text("<<Grafico: Cantidad de Vinos por Pais>>")
    #country_df = df['country'].value_counts().to_frame()
    #country_df = country_df.reset_index()
    #st.dataframe(country_df)

    #p1 = px.bar(country_df, x='index', y='country',orientation='v',color='country')
    #st.plotly_chart(p1, use_container_width=True)

    
with st.expander("Top 5 Paises - WordClouds Banderas",expanded=True):

    col1, col2 = st.columns([1,1.35])
    with col1:
        pass
    with col2:    
        st.subheader("Cantidad de Vinos")
        st.caption("(Dataset sin filtros)")
        #st.text("<<Grafico: Cantidad de Vinos por Pais>>")
        country_df = df['country'].value_counts().to_frame()
        country_df = country_df.reset_index()
        st.write(country_df.head())

        #st.write(country.size().sort_values(ascending=False).head())

        # Join all reviews of each country:
        usa = " ".join(review for review in df[df["country"]=="US"].description)
        fra = " ".join(review for review in df[df["country"]=="France"].description)
        ita = " ".join(review for review in df[df["country"]=="Italy"].description)
        spa = " ".join(review for review in df[df["country"]=="Spain"].description)
        por = " ".join(review for review in df[df["country"]=="Portugal"].description)
    

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        # Generate a word cloud image
        mask1 = np.array(Image.open("flag-port.png"))
        wordcloud_por = WordCloud(stopwords=stopwords, background_color="white", mode="RGBA", max_words=1000, mask=mask1).generate(por)

        # create coloring from image
        image_colors = ImageColorGenerator(mask1)
        fig5 = plt.figure(figsize=[7,7])
        plt.imshow(wordcloud_por.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")
        st.pyplot(fig5)

        wordcloud_por.to_file("flag-port-wc.png")
    with col2:
        # Generate a word cloud image
        mask2 = np.array(Image.open("flag-esp.png"))
        wordcloud_esp = WordCloud(stopwords=stopwords, background_color="white", mode="RGBA", max_words=1000, mask=mask2).generate(spa)

        # create coloring from image
        image_colors = ImageColorGenerator(mask2)
        fig6 = plt.figure(figsize=[7,7])
        plt.imshow(wordcloud_esp.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")
        st.pyplot(fig6)

        wordcloud_esp.to_file("flag-esp-wc.png")
    with col3:
        # Generate a word cloud image
        mask4 = np.array(Image.open("flag-ita.jpeg"))
        wordcloud_ita = WordCloud(stopwords=stopwords, background_color="white", mode="RGB", max_words=1000, mask=mask4).generate(ita)
         # create coloring from image
        image_colors = ImageColorGenerator(mask4)
        fig8 = plt.figure(figsize=[7,7])
        plt.imshow(wordcloud_ita.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")
        st.pyplot(fig8)

        wordcloud_ita.to_file("flag-ita-wc.png")
    with col4:
        # Generate a word cloud image
        mask3 = np.array(Image.open("flag-fra.jpg"))
        wordcloud_fra = WordCloud(stopwords=stopwords, background_color="white", mode="RGB", max_words=1000, mask=mask3).generate(fra)
         # create coloring from image
        image_colors = ImageColorGenerator(mask3)
        fig7 = plt.figure(figsize=[7,7])
        plt.imshow(wordcloud_fra.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")
        st.pyplot(fig7)

        wordcloud_fra.to_file("flag-fra-wc.png")
    with col5:
        # Generate a word cloud image
        mask5 = np.array(Image.open("flag-usa.jpg"))
        wordcloud_usa = WordCloud(stopwords=stopwords, background_color="white", mode="RGB", max_words=1000, mask=mask5).generate(usa)
         # create coloring from image
        image_colors = ImageColorGenerator(mask5)
        fig9 = plt.figure(figsize=[7,7])
        plt.imshow(wordcloud_usa.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")
        st.pyplot(fig9)

        wordcloud_usa.to_file("flag-usa-wc.png")

expander_bar = st.expander("About")
expander_bar.markdown(
    """
* **Python libraries:** pandas, streamlit (st_aggrid, st_lottie), numpy, matplotlib, seaborn, plotly, wordcloud, PIL
* **Data source:** [WineEnthusiast](https://www.winemag.com/?s=&drink_type=wine) y
    [Kagle](https://www.kaggle.com/datasets/zynicide/wine-reviews).
* **Credit:** Source Code adapted from the DataCamp article *[Generating WordClouds in Python Tutorial](https://www.datacamp.com/tutorial/wordcloud-python)* written by [Duong Vu](https://www.datacamp.com/profile/dqvu).
"""
)



