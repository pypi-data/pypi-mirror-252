


<img src="https://github.com/lucbra21/images/blob/main/sdc_logo.jpeg" alt="Sports Data Campus" />

# API Data fbref.com by Sports Data Campus

A Python package to api data fbref.com

https://pypi.org/project/fbref-package/

# Aviso Importante sobre el Uso de Datos de Deportes-Reference.com

Esta librería está diseñada para facilitar el acceso a los datos disponibles en [Deportes-Reference.com](https://www.sports-reference.com/) con propósitos educativos y de investigación. Al utilizar esta librería, los usuarios deben adherirse a los siguientes términos y condiciones:

## Atribución de Datos
Todos los datos obtenidos a través de esta librería provienen de Deportes-Reference.com. Los usuarios deben asegurarse de atribuir claramente a Deportes-Reference.com como la fuente de los datos en cualquier publicación, análisis o proyecto donde se utilicen estos datos.

## Uso No Comercial
Esta librería se proporciona exclusivamente para uso no comercial. Cualquier uso de los datos obtenidos para propósitos comerciales está estrictamente prohibido.

## Adherencia a los Términos de Uso de Deportes-Reference.com
Se insta a los usuarios a revisar y seguir los términos de uso establecidos por Deportes-Reference.com, disponibles en [este enlace]([Términos de uso](https://www.sports-reference.com/termsofuse.html?__hstc=218152582.fec85327c513cabac009730b02616118.1702551847368.1704787354268.1705570980226.7&__hssc=218152582.1.1705570980226&__hsfp=1018840319)). El uso indebido de los datos puede resultar en la violación de estos términos.

## Prohibición de Uso Automatizado
El uso de métodos automatizados, incluidos bots, scrapers o mineros de datos, para acceder a Deportes-Reference.com a través de esta librería, está prohibido a menos que se cuente con un permiso expreso por escrito del sitio.

## Limitación de Responsabilidad
El creador de esta librería no se hace responsable del mal uso de la misma ni de cualquier violación de los términos de uso de Deportes-Reference.com por parte de los usuarios. Los usuarios son responsables de asegurar que su uso de los datos cumple con todas las leyes y regulaciones aplicables.

Al utilizar esta librería, usted reconoce y acepta estos términos.


## Usage

```python

## Comprobar si fbref-package esta instalado y su version
# !pip list

## Instalar
# !pip install fbref_package

## Actualizar a la ultima version
# !pip install fbref-package --upgrade

## Pre install
# !pip install sqlalchemy
# !pip install pandas mysql-connector-python
## En colab correr y luego reiniciar el kernel
# !pip install --upgrade 'sqlalchemy<2.0'


## Import package
import fbref_package as fbref

## Ejemplo de uso 1
# Obtenemos todos los nombres de los dataframe posibles
table_names = fbref.getTables()
table_names

## Ejemplo de uso 2
# Obtenemos todas las competiciones posibles
df_competition = fbref.getCompetitions()
df_competition

## Ejemplo de uso 3
# Obtenemos los partidos de una competicion en una temporada
# df_result = fbref.getData(copetition_id, season, dataframe)
df_result = fbref.getData('12', '2023-2024', 'matches')
df_result

## Ejemplo de uso 4
# Obtenemos el resumen por competicion y temporada
# df_result = fbref.getData(copetition_id, season, dataframe)
df_result = fbref.getData('12', '2023-2024', 'competition_summary')
df_result

## Ejemplo de uso 5
# Obtenemos el resumen de la competicion por equipo y temporada
# df_result = fbref.getData(copetition_id, season, dataframe)
df_result = fbref.getData('12', '2023-2024', 'competition_team_summary')
df_result

## Ejemplo de uso 6
# Obtenemos el resumen de la competicion por jugador y temporada
# df_result = fbref.getData(copetition_id, season, dataframe)
df_result = fbref.getData('12', '2023-2024', 'competition_player_summary')
df_result

## Ejemplo de uso 7
# Obtenemos el resumen de los jugadores por partido en la competicion y temporada
# df_result = fbref.getData(copetition_id, season, dataframe)
df_result = fbref.getData('12', '2023-2024', 'match_player_summary')
df_result

## Ejemplo de uso 8
# Obtenemos el resumen de los equipos por partido en la competicion y temporada
# df_result = fbref.getData(copetition_id, season, dataframe)
df_result = fbref.getData('12', '2023-2024', 'match_team_summary')
df_result


```

By Sports Data Campus

