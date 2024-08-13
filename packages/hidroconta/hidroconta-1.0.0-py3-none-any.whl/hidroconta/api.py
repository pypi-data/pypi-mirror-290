import requests as re
import pandas as pd
import json
import hidroconta.types as tp
import hidroconta.hist as hist
import hidroconta.endpoints as endpoints
import hidroconta.time as time
import datetime
# For python <3.9, replace list[] with List[] from 'from typing import List'

'''
Allows an easy access to Demeter API from Python and
implements pandas dataframes compatibility
'''

'''Session cookies stored'''
__stored_cookies = None

POST_HDR = {"Content-Type": "application/json"}

# Exception to be thrown when Demeter API returns an error status code
class DemeterStatusCodeException(Exception):
    pass

def set_server(server: endpoints.Server):
    endpoints.set_server(server)

def get_server():
    return endpoints.get_server()

def login(username: str, password: str):
    global __stored_cookies

    payload = '{{"username":"{}", "password":"{}"}}'.format(username, password)

    response = re.post(get_server() + endpoints.DEMETER_LOGIN ,data=payload, headers=POST_HDR)

    if response.status_code != 200:
        raise DemeterStatusCodeException(response.status_code)

    cookies = response.cookies.get_dict()
    __stored_cookies = cookies
    return cookies

def logout():
    response = re.post(get_server() + endpoints.DEMETER_LOGOUT, cookies=__stored_cookies)
    if response.status_code != 200:
        raise DemeterStatusCodeException(response.status_code)
    
def __get_elements(element: str, element_id: int = None, pandas = False):
    print(get_server() + endpoints.DEMETER_GET + element + ('' if element_id == None else ('/' + str(element_id))))
    response = re.get(get_server() + endpoints.DEMETER_GET + element + ('' if element_id == None else ('/' + str(element_id))), cookies=__stored_cookies)
    if response.status_code != 200:
        raise DemeterStatusCodeException(response.status_code)
    else:
        if pandas:
            data = json.loads(response.text)
            return pd.json_normalize(data)
        else:
            return response.text

def search(text:str = None, element_types:list[tp.Element] = None, status:tp.Status = tp.Status.ALL, pandas = False):

    payload = '{"status":"' + status + '"'
    if(text is not None):
        payload = payload + ',"searchText":"' + text + '"'
    if(element_types is None):
        element_types = [e for e in tp.Element.__dict__.values() if type(e) == str and e != 'demeterapitypes']
    payload = payload + ',"type":' + str(element_types).replace("'", '"')
    payload = payload + '}'
    print(payload)

    response = re.post(get_server() + endpoints.DEMETER_SEARCH, headers=POST_HDR, data=payload, cookies=__stored_cookies)
    if response.status_code != 200:
        raise DemeterStatusCodeException(response.status_code)
    else:
        if pandas:
            data = json.loads(response.text)
            return pd.json_normalize(data)
        else:
            return response.text

    
def get_rtus(element_id:int = None, pandas = False):
    return __get_elements('rtus', element_id, pandas)
        
def get_counters(element_id:int = None, pandas = False):
    return __get_elements('counters', element_id, pandas)
        
def get_analog_inputs(element_id:int = None, pandas = False):
    return __get_elements('analogInputs', element_id, pandas)

def get_digital_inputs(element_id:int = None, pandas = False):
    return __get_elements('digitalInputs', element_id, pandas)
        
def get_iris_nb(element_id:int = None, pandas = False):
    return __get_elements('iris/nbiot', element_id, pandas)
        
def get_iris_lw(element_id:int = None, pandas = False):
    return __get_elements('iris/lorawan', element_id, pandas)
        
def get_iris_sigfox(element_id:int = None, pandas = False):
    return __get_elements('iris/sigfox', element_id, pandas)

def get_iris_gprs(element_id:int = None, pandas = False):
    return __get_elements('iris/gprs', element_id, pandas)

def get_installations(element_id:int = None, pandas = False):
    return __get_elements('installations', element_id, pandas)

def get_rtus_installation_dict(pandas = False):
    installations = __get_elements('installations', pandas=pandas)
    rtus = __get_elements('rtus', pandas=pandas)
    match_installations = pd.merge(installations, rtus, on='installationId')
    timezones = {}
    for index, match in match_installations.iterrows():
        timezones[match['rtuId']] = match['timeZone']
    return timezones

def get_centinel(element_id:int = None, pandas = False):
    return __get_elements('centinel', element_id, pandas)

def get_centaurus(element_id:int = None, pandas = False):
    return __get_elements('centaurus', element_id, pandas)
    
def global_update(rtu_id: int, timestamp: datetime.datetime, liters:int):
    
    payload = '{"rtuId":' + str(rtu_id) + ',"timestamp":"' + time.strftime_demeter(timestamp) + '","value":' + str(int(liters)) + '}'
    print(payload)
    response = re.put(get_server() + endpoints.DEMETER_UPDATE_COUNTER_GLOBAL ,data=payload, headers=POST_HDR, cookies=__stored_cookies)
    if response.status_code != 200:
        raise DemeterStatusCodeException(response.status_code)
    
def add_historics(rtu_id: int, historics: list[hist.Hist]):

    hist = '['
    for historic in historics[:-1]:
        hist = hist + '{'
        hist = hist + '"timestamp":"' + str(historic.timestamp) + '",'
        hist = hist + '"subtype":' + str(historic.type.subtype) + ','
        hist = hist + '"subcode":' + str(historic.type.subcode) + ','
        hist = hist + '"value":' + str(historic.value) + ','
        hist = hist + '"position":' + str(historic.position) + ','
        hist = hist + '"expansion":' + str(historic.expansion) + '},'
    historic = historics[-1]
    hist = hist + '{'
    hist = hist + '"timestamp":"' + str(historic.timestamp) + '",'
    hist = hist + '"subtype":' + str(historic.type.subtype) + ','
    hist = hist + '"subcode":' + str(historic.type.subcode) + ','
    hist = hist + '"value":' + str(historic.value) + ','
    hist = hist + '"position":' + str(historic.position) + ','
    hist = hist + '"expansion":' + str(historic.expansion) + '}'
    hist = hist + ']'
    
    payload = '{{"rtuId":{}, "historicDataEntities":{}}}'.format(rtu_id, hist)
    print(payload)
    response = re.post(get_server() + endpoints.DEMETER_HISTORICS ,data=payload, headers=POST_HDR, cookies=__stored_cookies)
    if response.status_code != 200:
        raise DemeterStatusCodeException(response.status_code)

def get_historics(start_date: datetime.datetime, end_date: datetime.datetime, element_ids: list[int], subtype: int, subcode:list[int] = [], pandas=False):
    start_date = time.strftime_demeter(start_date)
    end_date = time.strftime_demeter(end_date)
    payload = '{{"from":"{}", "until":"{}", "subcode":{}, "subtype":{}, "elementIds":{}}}'.format(start_date, end_date, subcode, subtype, element_ids)
    
    response = re.post(get_server() + endpoints.DEMETER_HISTORY_DATA, headers=POST_HDR, data=payload, cookies=__stored_cookies)
    if response.status_code != 200:
        raise DemeterStatusCodeException(response.status_code)
    else:
        if pandas:
            data = json.loads(response.text)
            return pd.json_normalize(data)
        else:
            return response.text

def get_minute_consumption(start_date: datetime.datetime, end_date: datetime.datetime, element_ids: list[int], period_value: int, min_interval: bool = True, pandas=False):
    start_date = time.strftime_demeter(start_date)
    end_date = time.strftime_demeter(end_date)
    payload = '{{"from":"{}", "until":"{}", "minInterval":{}, "elementIds":{}, "periodValue":{}}}'.format(start_date, end_date, min_interval, element_ids, period_value)

    response = re.post(get_server() + endpoints.DEMETER_CONSUMPTION, headers=POST_HDR, data=payload, cookies=__stored_cookies)
    if response.status_code != 200:
        raise DemeterStatusCodeException(response.status_code)
    else:
        if pandas:
            data = json.loads(response.text)
            unfolded = pd.DataFrame(columns=['code', 'timestamp'])
            df = pd.json_normalize(data)
            for ix, row in df.iterrows():
                unfolded_row = row['values']
                unfolded_list = []
                for x in unfolded_row:
                    x['code'] = row['series'][0]
                    x['values'] = x['values'][0]
                    unfolded_list.append(x)
                    x['timestamp'] = time.strptime_demeter(x['timestamp'])
                unfolded = pd.concat([unfolded, pd.json_normalize(unfolded_list)])
            return unfolded
        else:
            return response.text

def update_analog_input_value(rtu_id:int, position:int, expansion:int, value:int, timestamp:datetime.datetime):
    timestamp = time.strftime_demeter(timestamp)
    payload = '{{"rtuId":{}, "position":{}, "expansion":{}, "value":{}, "timestamp":"{}"}}'.format(rtu_id, position, expansion, value, timestamp)
    print(payload)
    response = re.put(get_server() + endpoints.DEMETER_ANALOG_UPDATE ,data=payload, headers=POST_HDR, cookies=__stored_cookies)
    if response.status_code != 200:
        raise DemeterStatusCodeException(response.status_code)
    
def create_iris_nb(payload:str):
    response = re.post(get_server() + endpoints.DEMETER_IRIS_NB, data=payload, headers=POST_HDR, cookies=__stored_cookies)
    if response.status_code != 201:
        print(response.text)
        raise DemeterStatusCodeException(response.status_code)
    
def delete_iris_nb(elementid:int, confirmation = True):
    if confirmation:
        iris = get_iris_nb(element_id=elementid, pandas=True)
        print('{} será eliminado de {}.'.format(iris['code'].values.tolist()[0], get_server()))
        res = input('Desea continuar (y|n)? ')
        if res.capitalize() == 'Y': 
            print('Borrando')
            response = re.delete(get_server() + endpoints.DEMETER_IRIS_NB + '/' + str(elementid), cookies=__stored_cookies)
            if response.status_code != 200:
                raise DemeterStatusCodeException(response.status_code)
        else:
            print('Cancelado')
            return
    else:
        response = re.delete(get_server() + endpoints.DEMETER_IRIS_NB + '/' + str(elementid), cookies=__stored_cookies)
        if response.status_code != 200:
            raise DemeterStatusCodeException(response.status_code)