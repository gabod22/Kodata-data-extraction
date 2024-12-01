import requests
import time
import json

USERNAME = "consultoria@pixel-lap.com"
PASS = "P0nk3h4k13224"

K_ENDPOING = "https://biz.kordata.mx/graphql"
K_LOGIN_ENDPOINT = "https://one.kordata.mx/api/commons/iniciar-sesion"
K_LOGOUT_ENDPOINT = "https://one.kordata.mx/api/commons/cerrar-sesion"
K_MASIVE_LOGOUT_ENDPOINT = "https://one.kordata.mx/api/commons/cerrar-sesion-masivo"


def mide_tiempo(funcion):
    def funcion_medida(*args, **kwargs):
        inicio = time.time()
        c = funcion(*args, **kwargs)
        print(time.time() - inicio)
        return c

    return funcion_medida


def login(username, password):
    global currentToken
    headers = {
        "user-agent": "Pixel-kor_extraction/0.0.1",
        "Content-Type": "application/json",
    }
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
        # print(currentToken)
        f = open("token.txt", "w")
        f.write(currentToken)
        print("sesion iniciada")
    else:
        idsBitacora = []
        usuarioId = json["idUsuario"]
        empresaId = json["cicloCobro"]["empresaId"]
        for session in json["bitacoraAccesoDto"]["secciones"]:
            idsBitacora.append(session["id"])

        payload = [
            {"idsBitacora": idsBitacora, "usuarioId": usuarioId, "empresaId": empresaId}
        ]
        print(payload)
        print("No se ha podido iniciar sesión, revise si no hay una sesión iniciada")

        r = input("Deseas que se cierren las sesiones? (y/n): ")
        if r == "y":
            masive_logout(payload)
            print("Sesiones cerradas")
            login(USERNAME, PASS)
        else:
            print("no se han cerrado las sesiones")


def get_current_token():
    f = open("token.txt", "r")
    return f.read()


def masive_logout(payload):
    headers = {"user-agent": "pixel/0.0.1", "Content-Type": "application/json"}

    response = requests.post(
        K_MASIVE_LOGOUT_ENDPOINT,
        json=payload,
        headers=headers,
    )
    print(response.json())


def logout(token):
    headers = {
        "user-agent": "pixel/0.0.1",
        "Content-Type": "application/json",
        "authorization": "Bearer " + token,
    }
    payload = {"token": token}
    response = requests.post(
        K_LOGOUT_ENDPOINT,
        json=payload,
        headers=headers,
    )
    print(response.json())

def get_sales_invoices():
    currentToken = get_current_token()

    headers = {
        "user-agent": "pixel/0.0.1",
        "Content-Type": "application/json",
        "authorization": "Bearer " + currentToken,
    }
    query_report_list_invoices ={
        "operationName": "some",
        "variables": {},
        "query": "query some {\n  BasesReportesGenerarReportePorId(\n    data: {id: 100000105}\n    parametros: {columnasAdicionales: [{id: -1, baseCampoId: 2471, seLect: false, wheRe: true, groUp: false, baseReporteCondicionCatalogoId: 25, groupAscendente: null, andOr: \"AND\", visible: true, esId: false, isDeleted: false, secuencia: -1, baseReporteId: 100000105}], condicionesAdicionales: [{valorInicial: \"2023-01-01\", valorFinal: \"\", baseReporteColumnaId: -1}]}\n  ) {\n    datosListasSeleccion\n    resultadoReporteHashmap\n    baseReporte {\n      id\n      carpetaId\n      parasiteParent\n      compartida\n      esQuery\n      nombreReporte\n      tablaPrincipalId\n      moduloPrincipalId\n      baseReporteTipoId\n      baseReporteIdDetalle\n      basesReportesColumnas {\n        id\n        basesCampos {\n          nombreEtiqueta\n        }\n      }\n      basesReportesPivotConfiguracion {\n        baseReporteColumnaId\n        baseCampoAlias\n        pivotColumna\n        pivotRenglon\n        pivotValor\n      }\n    }\n  }\n}"
    }
    response = requests.post(
        K_ENDPOING,
        json=query_report_list_invoices,
        headers=headers,
    )
    invoices = response.json()["data"]["BasesReportesGenerarReportePorId"][
        "resultadoReporteHashmap"
    ][0]["encabezado"]
    invoices.pop(0)
    items = response.json()["data"]["BasesReportesGenerarReportePorId"][
        "resultadoReporteHashmap"
    ][0]["detalle"]
    items.pop(0)

    # print(type(data))
    return invoices, items
# @mide_tiempo
def get_sales_notes():
    currentToken = get_current_token()

    headers = {
        "user-agent": "pixel/0.0.1",
        "Content-Type": "application/json",
        "authorization": "Bearer " + currentToken,
    }
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
    sales_notes = response.json()["data"]["BasesReportesGenerarReportePorId"][
        "resultadoReporteHashmap"
    ][0]["encabezado"]
    sales_notes.pop(0)
    items = response.json()["data"]["BasesReportesGenerarReportePorId"][
        "resultadoReporteHashmap"
    ][0]["detalle"]
    items.pop(0)

    # print(type(data))
    return sales_notes, items


def get_clients():
    currentToken = get_current_token()

    headers = {
        "user-agent": "pixel/0.0.1",
        "Content-Type": "application/json",
        "authorization": "Bearer " + currentToken,
    }
    query_report_list_sales_notes = {
        "variables": {},
        "query": '{\n  BasesReportesGenerarConTerminosBusqueda(\n    reporteId: 894\n    terminosBusqueda: [{baseReporteColumnaId: 8564, terminoBusqueda: null, operador: null, ordenamiento: "DESC"}]\n    paginadoInformacion: {numeroPagina: 1, registrosPorPagina: 100000}\n  ) {\n    datosListasSeleccion\n    paginadoCount\n    resultadoReporteHashmap\n    baseReporte {\n      id\n      basesReportesColumnas {\n        id\n        seLect\n      }\n    }\n  }\n}',
    }
    response = requests.post(
        K_ENDPOING,
        json=query_report_list_sales_notes,
        headers=headers,
    )

    clients = response.json()["data"]["BasesReportesGenerarConTerminosBusqueda"]["resultadoReporteHashmap"]
    clients.pop(0)

    return clients


def join_notes_and_items():
    sales_notes, sales_notes_items = get_sales_notes()
    invoices, invoices_items = get_sales_invoices()
    
    clients = get_clients()
    for note in sales_notes:
        # Filtrar elementos de array2 que coincidan en id
        note["items"] = [sub_item for sub_item in sales_notes_items if sub_item["id"] == note["id"]]
    
    for note in sales_notes:
        note["client"] = [client for client in clients if client["Nombre del cliente"] == note["Cliente - Nombre del cliente"]]
        
    for invoice in invoices:
        # Filtrar elementos de array2 que coincidan en id
        note["items"] = [sub_item for sub_item in invoices_items if sub_item["id"] == invoice["id"]]
    
    for invoice in invoices:
        note["client"] = [client for client in clients if client["Nombre del cliente"] == invoice["Cliente - Nombre del cliente"]]
        
    data = invoices + sales_notes

    json_object = json.dumps(data, indent=4)
    with open("sample.json", "w",encoding='utf8') as outfile:
        outfile.write(json_object)


join_notes_and_items()

# login(USERNAME, PASS)

# get_clients()

# logout(get_current_token())
