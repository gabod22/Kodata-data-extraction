import requests
import time
import json

USERNAME = "consultoria@pixel-lap.com"
PASS = "P0nk3h4k13224"

K_ENDPOING = "https://biz.kordata.mx/graphql"
K_LOGIN_ENDPOINT = "https://one.kordata.mx/api/commons/iniciar-sesion"
K_LOGOUT_ENDPOINT = "https://one.kordata.mx/api/commons/cerrar-sesion"
K_MASIVE_LOGOUT_ENDPOINT = None 

def mide_tiempo(funcion):
    def funcion_medida(*args, **kwargs):
        inicio = time.time()
        c = funcion(*args, **kwargs)
        print(time.time() - inicio)
        return c
    return funcion_medida

def login(username, password):
    global currentToken
    headers = {"user-agent": "pixel/0.0.1", "Content-Type": "application/json"}
    payload = {
        "username": username,
        "password": password,
        "verificarEmail": True,
        "tipoDispositivo": "desktop",
    }
    response = requests.post(
        K_LOGIN_ENDPOINT,
        json=payload,
        headers=headers,
    )
    json = response.json()
    print(json)
    if json["token"]:
        currentToken = json["token"]
        print(currentToken)
        f = open("token.txt", "w")
        f.write(currentToken)
    else:
        print("No se ha podido iniciar sesión, revise si no hay una sesión iniciada")


def get_current_token():
    f = open("token.txt", "r")
    return f.read()





def logout(token):
    headers = {"user-agent": "pixel/0.0.1", "Content-Type": "application/json", "authorization": "Bearer " + token, }
    payload = {"token": token}
    response = requests.post(
        K_LOGOUT_ENDPOINT,
        json=payload,
        headers=headers,
    )
    print(response.json())

# @mide_tiempo
def get_sales_notes():
    currentToken = get_current_token()
    
    headers = {"user-agent": "pixel/0.0.1", "Content-Type": "application/json", "authorization": "Bearer " + currentToken, }
    query_report_list_sales_notes = {
        "operationName": "some",
        "variables": {},
        "query": 'query some {\n  BasesReportesGenerarReportePorId(\n    data: {id: 100000104}\n    parametros: {columnasAdicionales: [{id: -1, baseCampoId: 2519, seLect: false, wheRe: true, groUp: false, baseReporteCondicionCatalogoId: 25, groupAscendente: null, andOr: "AND", visible: true, esId: false, isDeleted: false, secuencia: -1, baseReporteId: 100000104}], condicionesAdicionales: [{valorInicial: "2023-01-01", valorFinal: "", baseReporteColumnaId: -1}]}\n  ) {\n    datosListasSeleccion\n    resultadoReporteHashmap\n    baseReporte {\n      id\n      carpetaId\n      parasiteParent\n      compartida\n      esQuery\n      nombreReporte\n      tablaPrincipalId\n      moduloPrincipalId\n      baseReporteTipoId\n      baseReporteIdDetalle\n      basesReportesColumnas {\n        id\n        basesCampos {\n          nombreEtiqueta\n        }\n      }\n      basesReportesPivotConfiguracion {\n        baseReporteColumnaId\n        baseCampoAlias\n        pivotColumna\n        pivotRenglon\n        pivotValor\n      }\n    }\n  }\n}',
    }
    response = requests.post(
        K_ENDPOING,
        json=query_report_list_sales_notes,
        headers=headers,
    )
    sales_notes = response.json()['data']['BasesReportesGenerarReportePorId']['resultadoReporteHashmap'][0]['encabezado']
    sales_notes.pop(0)
    items = response.json()['data']['BasesReportesGenerarReportePorId']['resultadoReporteHashmap'][0]['detalle']
    items.pop(0)
    
    # print(type(data))
    return sales_notes, items 

# print(items)
# @mide_tiempo
def join_notes_and_items():
    sales_notes, items = get_sales_notes()
    for note in sales_notes:
        # Filtrar elementos de array2 que coincidan en id
        note['items'] = [sub_item for sub_item in items if sub_item['id'] == note['id']]
    
    json_object = json.dumps(sales_notes, indent=4)
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)    
        
    



join_notes_and_items()

# login(USERNAME, PASS)

# logout(get_current_token())


