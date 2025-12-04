#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importar archivo CSV con pandas
# La documentación de pandas: https://pandas.pydata.org/docs/
import pandas as pd
import numpy as np
import os

df = pd.read_csv('fifa_eda.csv')


# In[ ]:


# Visualizar una muestra de 5 líneas
df.sample(5)


# In[ ]:


df.describe()


# In[ ]:


# Se detecta que existen valores nulos por lo que se procede a reemplazarlos con 0s
df['International Reputation'] = df['International Reputation'].replace([np.nan, np.inf, -np.inf], 0)
df['Skill Moves'] = df['Skill Moves'].replace([np.nan, np.inf, -np.inf], 0)
df['Value'] = df['Value'].replace([np.nan, np.inf, -np.inf], 0)


# In[ ]:


df.describe()


# In[ ]:


df.dtypes


# In[ ]:


# Elemento1: Obtener matriz de correlación y dejarla como heatmap
import plotly.express as px
px.density_heatmap(df, x='Age', y='Overall')


# In[ ]:


# Elemento2: Gráfico de Correlación que responda – “Cuál es la relación entre la edad y el overall?
# Se calcula la correlación entre las variables numéricas del DataFrame
correla_edad_over = df[['Age', 'Overall']].corr()
print(correla_edad_over)


# In[ ]:


fig = px.imshow(correla_edad_over, text_auto=True)
fig.show()


# In[ ]:


# Elemento3: Generar un gráfico de barras por club que indique el número de jugadores
# Se genera un DataFrame basado en el Club y el número de jugadores
df_club = df.groupby(['Club']).size().rename('num_jugadores').reset_index().sort_values(by='num_jugadores', ascending=False)


# In[ ]:


df_club[:10]


# In[ ]:


fig = px.bar(df_club[:20], x='Club', y='num_jugadores', title='Club vs número de jugadores', text='num_jugadores')
fig.show()


# In[ ]:


# Elemento4: Hacer un gráfico multipanel que indique la relación altura (height) vs skill moves,
# siendo la variable del panel si es zurdo o derecho.
# Gráfico de faceta por movie / tv show
fig = px.strip(df, x='Height', y='Skill Moves', facet_col='Preferred Foot')
fig.show()


# In[ ]:


# Elemento 5: Próximos 15 jugadores a ganar el balón de oro
# Se genera un DataFrame basado en el Jugador y el número de goles (Potential)
df_goles = (
    df.groupby('Potential')
      .agg(num_jugadores=('Name', 'count'), nombres=('Name', list))
      .reset_index()
      .sort_values(by='Potential', ascending=False)
)
df_goles[:15]


# In[ ]:


# Expandimos la lista de nombres en filas individuales
df_expanded = df_goles.explode('nombres')

# Renombramos la columna para claridad
df_expanded = df_expanded.rename(columns={'nombres': 'Nombre'})


# In[ ]:


df_expanded[:15]


# In[ ]:


# Se genera el gráfico de barras nombre, potencial con color en Potential
fig = px.bar(df_expanded[:15], x='Nombre', y='Potential', title='Próximos jugadores a ganar el Balón de Oro', color='Potential', text='Potential')
fig.update_layout(xaxis_tickangle=-45)
fig.show()


# In[ ]:




