from flask import Flask, redirect
from flask import Flask, abort
from flask import Flask, render_template
from flask import jsonify
from flask import request
import http.server
import json

app=Flask(__name__)
print(app)
# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000
url='/drug/label.json'

@app.route('/searchDrug')
def get_drugs():
    drugs=request.args.get('active_ingredient')
    max=request.args.get('limit')

    if max:
        limit=max
    else:
        limit=10

    headers={'User-Agent':'http-client'}
    print(drugs)
    #https://api.fda.gov/drug/label.json?search=active_ingredient:aspirin&limit=10

    conn=http.client.HTTPSConnection('api.fda.gov')#establecemos connexion
    conn.request('GET',url+'?limit='+str(limit)+'&search=active_ingredient:'+drugs,None, headers)#solicitamos la busqueda de una empresa

    r=conn.getresponse()
    print(r.status,r.reason)
    respuesta=r.read().decode('utf-8')
    data=json.loads(respuesta)

    #data=json.loads(respuesta)
    mensaje='''<!doctype html>
                <html lang='es'>
                <head>
                    <meta charset="UTF-8">
                </head>
                  <title>drugs</title>
                  <body style= "background-color:#85E3FF;">
                    <p>información</p>

                '''
    for i in range(0,data['meta']['results']['limit']):
        try:
            drugs=data['results'][i]['openfda']['generic_name'][0]
            mensaje =mensaje + '<li>'+drugs
        except:
            mensaje+='<li>'+'desconocido'
            mensaje+=''

    mensaje=mensaje+'''</body>
    </html>'''
    #terminamos el mensaje
    conn.close()
    return mensaje

@app.route('/searchCompany')
def searchCompanies():
    companies=request.args.get('company')
    max=request.args.get('limit')
    if max:
        limit=max
    else:
        limit=10

    headers={'User-Agent':'http-client'}
    print(limit)
    conn=http.client.HTTPSConnection('api.fda.gov')#establecemos connexion
    conn.request('GET',url+'?search=openfda.manufacturer_name:'+companies+'&limit='+str(limit), None, headers)#solicitamos la busqueda de una empresa
    r=conn.getresponse()
    print(r.status,r.reason)
    respuesta=r.read().decode('utf-8')
    data=json.loads(respuesta)

    mensaje='''<!doctype html>
                <html>
                  <title>companies</title>
                  <body style= "background-color:#85E3FF;">
                    <p>medicamentos</p>
                    </body>
                    </html>
                '''
    for i in range(0,data['meta']['results']['limit']):
        try:
            companies=data['results'][i]['openfda']['generic_name'][0]
            mensaje =mensaje + '<li>'+companies#añadimos la informacion
            #de vuelta sobre la compañia buscada
        except:
            mensaje+='<li>'+'desconocido'

    #cerramos el mensaje
    conn.close()

    return mensaje


@app.route('/listDrugs')
def listaDrugs():
    max=request.args.get('limit')
    headers={'User-Agent':'http-client'}
    conn=http.client.HTTPSConnection('api.fda.gov')#establecemos connexion
    conn.request('GET',url+'?limit='+max,None, headers)#solicitamos la busqueda de una empresa
    r=conn.getresponse()
    print(r.status,r.reason)
    respuesta=r.read().decode('utf-8')
    conn.close()
    data=json.loads(respuesta)

    mensaje='''<!doctype html>
                <html>
                  <title>drugs list </title>
                  <body style= "background-color:#85E3FF;">
                    <p>esta es una lista de drogas</p>
                    </body>
                </html>

                '''
    limit=data['meta']['results']['limit']
    for i in range(0,limit):
        try:
            drug=data['results'][i]['openfda']['generic_name'][0]
            mensaje += '<li>'+str(i+1)+'.'+drug
        except:
            mensaje += '<li>'+str(i+1)+'.'+'desconocido'


    return mensaje



@app.route('/listCompanies')
def listCompanies():
    max=request.args.get('limit')
    headers={'User-Agent':'http-client'}

    conn=http.client.HTTPSConnection('api.fda.gov')#establecemos connexion
    conn.request('GET',url+'?limit='+str(max),None, headers)#solicitamos la busqueda de una empresa
    r=conn.getresponse()
    print(r.status,r.reason)
    respuesta=r.read().decode('utf-8')
    data=json.loads(respuesta)

    mensaje='''<!doctype html>
                <html>

                  <title>companies list </title>
                  <body style= "background-color:#85E3FF;">
                    <p>esta es una lista de compañias</p>
                    </body>
                </html>

                '''
    max=data['meta']['results']['limit']
    for i in range(0,max):
        try:
            comp=data['results'][i]['openfda']['company'][0]
            mensaje += '<li>'+str(i+1)+'.'+comp

        except:
            mensaje += '<li>'+str(i+1)+'.'+'desconocido'


    #terminamos el mensaje
    conn.close()
    return mensaje


@app.route('/listWarnings')
def list_Warnings():
    max=request.args.get('limit')
    headers={'User-Agent':'http-client'}
    conn=http.client.HTTPSConnection('api.fda.gov')#establecemos connexion
    conn.request('GET',url+'?limit='+str(max), None, headers)#solicitamos la busqueda de una empresa
    r=conn.getresponse()
    print(r.status,r.reason)
    respuesta=r.read().decode('utf-8')
    data=json.loads(respuesta)

    mensaje='''<!doctype html>
                <html>
                  <body style= "background-color:#85E3FF;">
                    <p>esta es una lista de compañias</p>

                '''
    for i in range(0,data['meta']['results']['limit']):
        try:
            warning=data['results'][i]['warnings'][0]
        except:
            warning='se desconoce el error'
        mensaje +='<li>' +warning

    mensaje+='</body></html>'
    conn.close()
    return mensaje


@app.route('/secret')
def secret():
    return abort(401)

@app.route('/redirect')
def index():
    return redirect('/'), abort(302),{'WWW-Authenticate', 'Basic realm="Mi servidor"'}#funcion de flask, te redirige como si hubieramos
    #escrito '/index' y nos aparece el formulario

@app.errorhandler(404)
def error(e):
    mensaje='''<!doctype html>
                <center>
                  <title>Error 404</title>
                  <body style= "background-color:#FFCCFF;"><br>
                  <h1>ERROR</h1>
                  </center><center>
                    <p>Disculpen las molestias, la</p>
                    <p>página web no ha sido encontrada</p>
                    </center>
                    </body></html>'''
    return mensaje


@app.route('/')
@app.route('/index')
def formulario():#lo usamos si no hemos escrito nada en el path
    with open('index.html', "r") as f:
        formulario = f.read()
    return formulario


print("serving at port", PORT)
if __name__=='__main__':
    app.run(IP,PORT)
