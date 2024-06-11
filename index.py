import requests
import json
from datetime import date
import pprint
    
accuweatherAPIKey = 'APIKey'

def pegarCoordenadas():
    ##get my geoposition and return a json data
    r = requests.get('http://www.geoplugin.net/json.gp')

    ##check the status about requests
    if(r.status_code != 200):
        print('Não foi possível obter a localiação')
        return None

    ##if ok, get info inside json    
    else:
        try:
            localizacao = json.loads(r.text)
            coordenadas = {}
            coordenadas['lat'] = localizacao['geoplugin_latitude']
            coordenadas['long'] = localizacao['geoplugin_longitude']
            return coordenadas
        except:
            return None

def pegarCodigoLocal(lat,long):
    LocationAPIUrl="http://dataservice.accuweather.com/locations/v1/cities/geoposition/" \
    + "search?apikey=" + accuweatherAPIKey \
    + "&q=" + lat + "%2C" + long + "&language=en-us"

    r = requests.get(LocationAPIUrl)
    ##check the status about requests
    if(r.status_code != 200):
        print('Não foi possível obter o código do local')
        return None
    ##if ok, get info inside json    
    else:
        try:
            locationResponse = json.loads(r.text)
            infoLocal = {}
            infoLocal['nomeLocal'] = locationResponse['LocalizedName'] + ", " \
                       + locationResponse['AdministrativeArea']['LocalizedName'] + ". "  \
                       + locationResponse['Country']['LocalizedName']
            infoLocal['codigoLocal'] = locationResponse['Key']
            return infoLocal
        except:
            return None

def pegarTempoAgora(codigoLocal, nomeLocal):
    CurrentConditionsAPIUrl = "http://dataservice.accuweather.com/currentconditions/v1/" \
                              + codigoLocal + "?apikey=" + accuweatherAPIKey \
                              + "&language=en-us"

    r = requests.get(CurrentConditionsAPIUrl)
    ##check the status about requests
    if(r.status_code != 200):
        print('Não foi possível obter o clima atual')
        return None
    ##if ok, get info inside json    
    else: #converte json em dicionário para pegar as informaçao
        try:
            CurrentConditionsResponse = json.loads(r.text)
            infoClima = {}
            infoClima['textoClima'] = CurrentConditionsResponse[0]['WeatherText']
            infoClima['temperatura'] = CurrentConditionsResponse[0]['Temperature']['Metric']['Value']
            infoClima['nomeLocal'] = nomeLocal
            return infoClima
        except:
            return None

##Forecast next 5 days
def pegarPrevisao5Dias(codigoLocal):
    DailyAPIUrl = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/" \
                              + codigoLocal + "?apikey=" + accuweatherAPIKey \
                              + "&language=en-us&metric=true"

    r = requests.get(DailyAPIUrl)
    ##check the status about requests
    if(r.status_code != 200):
        print('Não foi possível obter o clima atual')
        return None
    ##if ok, get info inside json    
    else: ##Change Json to dictionary
        try:
            DailyResponse = json.loads(r.text)
            infoClima5Dias = []
            for dia in DailyResponse['DailyForecasts']:
                climaDia = {}
                climaDia['max'] = dia['Temperature']['Maximum']['Value']
                climaDia['min'] = dia['Temperature']['Minimum']['Value']
                climaDia['clima'] = dia['Day']['IconPhrase']
                diaSemana = date.fromtimestamp(dia['EpochDate']).strftime("%A")
                climaDia['dia'] = diaSemana
                infoClima5Dias.append(climaDia)
            return infoClima5Dias

        except:
            return None

##Start 
def mostrarPrevisao(lat, long):
    try:
        local = pegarCodigoLocal(lat, long)
        climaAtual = pegarTempoAgora(local['codigoLocal'], local['nomeLocal'])
           
        print('Clima atual em: ' + climaAtual['nomeLocal'])
        print(climaAtual['textoClima'])
        print('Temperatura: ' + str(climaAtual['temperatura']) + "\xb0" + "C")
    except:
        print('Erro ao obter o clima atual.')
        
    ##Forecast next 5 days
    opcao = input('\nDeseja ver a previsão para os próximos 5 dias? (s ou n): ').lower()

    if opcao =="s":
        print('\nClima para os próximos 5 dias:\n')
        try:
            previsao5dias = pegarPrevisao5Dias(local['codigoLocal'])
            for dia in previsao5dias:
                print(dia['dia'])
                print('Minima: '+str(dia['min']) + "\xb0" + "C")
                print('Maxima: '+str(dia['max']) + "\xb0" + "C")
                print('Clima: ' + dia['clima'])
                print('--------------------------')
        except:
            print('Erro ao obter a previsão para os próximos 5 dias.')

try:
    coordenadas = pegarCoordenadas()
    mostrarPrevisao(coordenadas['lat'], coordenadas['long'])
except:
    print('Erro ao processar o solicitação. Entre em contato com o suporte.')
