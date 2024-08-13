# Integrations-PythonAPI
API Python para facilitar el acceso a los endpoints de la interfaz REST de Demeter

La API permite la gestión de grandes cantidades de datos mediante la librería Pandas, siempre y cuando se utilice la siguiente directiva en las llamadas a los métodos:
```
# Pandas = True returns a pandas dataframe instead a json
```

La forma de usar la API es la siguiente:

- Importar los modulos deseados:
```
import hidroconta.api as demeter
import hidroconta.types as hidrotypes
import pandas as pd
import datetime
import hidroconta.endpoints as hidroenpoints
```
- Seleccionar el servidor con el cual se quiere comunicar (se puede modificar en todo momento):
```
# Set server
demeter.set_server(hidroendpoints.Server.MAIN)
```

- Realizar el login en dicho servidor
```
# Login
demeter.login('USERNAME', 'PASSWORD')
```

Una vez seguidos los anteriores pasos, se puede realizar cualquier consulta sobre el sistema.
Algunas de ellas son:

- Búsqueda
```
# Search
df = demeter.search(text='SAT', element_types=[hidrotypes.Element.COUNTER, hidrotypes.Element.ANALOG_INPUT, hidrotypes.Element.RTU], status=hidrotypes.Status.ENABLED, pandas=True)
print(df)
```

- Obtención de historicos
```
# Get historics
df = demeter.get_historics(start_date=datetime.datetime.now(), end_date=datetime.datetime.now(), element_ids=[1000], subtype=hidrotypes.AnalogInputHist.subtype, subcode=[hidrotypes.AnalogInputHist.subcode], pandas=True)
print(df)
```

- Obtención de elementos
```
# Get
df = demeter.get_rtus(element_id=17512, pandas=True)
print(df)
```
La API define también una excepción especial cuando la llamada al endpoint de Demeter no devuelve el resultado esperado.
La excepción de denomina "DemeterStatusCodeException" y contiene el código de error HTTP.
```
# Exception treatment
try:
    df = demeter.get_rtus(element_id=17512, pandas=True)
except demeter.DemeterStatusCodeException as status_code:
    print('Error {}'.format(status_code))
```
- Por último, se debería hacer un logout en el servidor
```
demeter.logout()
```
