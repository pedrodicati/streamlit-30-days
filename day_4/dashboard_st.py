# import libs
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from datetime import datetime

# definição de funções
def style_negative(v, props=''):
    """ Style negative values in dataframe"""
    try: 
        return props if v < 0 else None
    except:
        pass
    
def style_positive(v, props=''):
    """Style positive values in dataframe"""
    try: 
        return props if v > 0 else None
    except:
        pass  


# load data
@st.cache # usado para armazenar os dados em cache e não precisar carregar novamente toda vez que o script for executado
def load_data():
    df_agg = pd.read_csv('./files_csv/Aggregated_Metrics_By_Video.csv').iloc[1:, :]
    df_agg.columns = ['Video','Titulo Video','Hora Publicacao Video','Comentários adicionados','Compartilhamentos','Nao gostei','Curtidas',
                    'Seguidores perdidos','Seguidores ganhados','RPM(USD)','CPM(USD)','Media % Visualizacoes','Duração de visualização média',
                    'Visualizações','Tempo de Vídeo (Horas)','Inscritos','Sua receita estimada (USD)','Impressões','Impressões ctr(%)']
    df_agg['Hora Publicacao Video'] = pd.to_datetime(df_agg['Hora Publicacao Video'])
    df_agg['Duração de visualização média'] = df_agg['Duração de visualização média'].apply(lambda x: datetime.strptime(x,'%H:%M:%S'))
    df_agg['Média de segundos'] = df_agg['Duração de visualização média'].apply(lambda x: x.second + x.minute*60 + x.hour*3600)
    df_agg['Engajamento'] =  (df_agg['Comentários adicionados'] + df_agg['Compartilhamentos'] +df_agg['Nao gostei'] + df_agg['Curtidas']) /df_agg.Visualizações
    df_agg['Visualizações / sub ganho'] = df_agg['Visualizações'] / df_agg['Seguidores ganhados']
    df_agg.sort_values('Hora Publicacao Video', ascending = False, inplace = True)    

    df_agg_sub = pd.read_csv('files_csv/Aggregated_Metrics_By_Country_And_Subscriber_Status.csv')
    df_comments = pd.read_csv('files_csv/Aggregated_Metrics_By_Video.csv')
    df_time = pd.read_csv('files_csv/Video_Performance_Over_Time.csv')
    df_time['Date'] = pd.to_datetime(df_time['Date'])

    return df_agg, df_agg_sub, df_comments, df_time

# criação dos dataframes
df_agg, df_agg_sub, df_comments, df_time = load_data()

# engenharia de dados
df_agg_diff = df_agg.copy()
meses_12_atras = df_agg_diff['Hora Publicacao Video'].max() - pd.DateOffset(months =12)
mediana_agg = df_agg_diff[df_agg_diff['Hora Publicacao Video'] >= meses_12_atras].median()

#create differences from the median for values 
#Just numeric columns 
numeric_cols = np.array((df_agg_diff.dtypes == 'float64') | (df_agg_diff.dtypes == 'int64'))
df_agg_diff.iloc[:,numeric_cols] = (df_agg_diff.iloc[:,numeric_cols] - mediana_agg).div(mediana_agg)

# criando dashboard
add_sidebar = st.sidebar.selectbox('Selecione a opção desejada', ['Métricas agregadas', 'Análise Individual de Vídeo'])

# fazendo com que mostre somente a métrica escolhida no sidebar
if add_sidebar == 'Métricas agregadas':
    
    df_agg_metrics = df_agg[['Hora Publicacao Video','Visualizações','Curtidas','Inscritos','Compartilhamentos','Comentários adicionados','RPM(USD)','Media % Visualizacoes',
                             'Média de segundos', 'Engajamento','Visualizações / sub ganho']]
    metric_date_6months = df_agg_metrics['Hora Publicacao Video'].max() - pd.DateOffset(months = 6)
    metric_date_12months = df_agg_metrics['Hora Publicacao Video'].max() - pd.DateOffset(months = 12)
    metric_medians6months = df_agg_metrics[df_agg_metrics['Hora Publicacao Video'] >= metric_date_6months].median()
    metric_medians12months = df_agg_metrics[df_agg_metrics['Hora Publicacao Video'] >= metric_date_12months].median()

    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]
    
    count = 0
    for i in metric_medians6months.index:
        with columns[count]:
            delta = (metric_medians6months[i] - metric_medians12months[i])/metric_medians12months[i]
            st.metric(label= i, value = round(metric_medians6months[i],1), delta = "{:.2%}".format(delta))
            count += 1
            if count >= 5:
                count = 0

    #get date information / trim to relevant data 
    df_agg_diff['Data de publicação'] = df_agg_diff['Hora Publicacao Video'].apply(lambda x: x.date())
    df_agg_diff_final = df_agg_diff.loc[:,['Titulo Video','Data de publicação','Visualizações','Curtidas','Inscritos','Compartilhamentos','Comentários adicionados','RPM(USD)','Media % Visualizacoes',
                             'Média de segundos', 'Engajamento','Visualizações / sub ganho']]
    
    df_agg_numeric_lst = df_agg_diff_final.median().index.tolist()
    df_to_pct = {}
    for i in df_agg_numeric_lst:
        df_to_pct[i] = '{:.1%}'.format
    
    st.dataframe(df_agg_diff_final.style.hide().applymap(style_negative, props='color:red;').applymap(style_positive, props='color:green;').format(df_to_pct))
    
if add_sidebar == 'Análise Individual de Vídeo':
    video_select = st.selectbox('Selecione o vídeo desejado', df_agg['Titulo Video'].unique())