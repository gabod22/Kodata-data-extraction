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
        "query": "query some {\n  BasesReportesGenerarReportePorId(\n    data: {id: 100000105}\n    parametros: {columnasAdicionales: [{id: -1, baseCampoId: 2471, seLect: false, wheRe: true, groUp: false, baseReporteCondicionCatalogoId: 25, groupAscendente: null, andOr: \"AND\", visible: true, esId: false, isDeleted: false, secuencia: -1, baseReporteId: 100000105}], condicionesAdicionales: [{valorInicial: \"2024-11-29\", valorFinal: \"\", baseReporteColumnaId: -1}]}\n  ) {\n    datosListasSeleccion\n    resultadoReporteHashmap\n    baseReporte {\n      id\n      carpetaId\n      parasiteParent\n      compartida\n      esQuery\n      nombreReporte\n      tablaPrincipalId\n      moduloPrincipalId\n      baseReporteTipoId\n      baseReporteIdDetalle\n      basesReportesColumnas {\n        id\n        basesCampos {\n          nombreEtiqueta\n        }\n      }\n      basesReportesPivotConfiguracion {\n        baseReporteColumnaId\n        baseCampoAlias\n        pivotColumna\n        pivotRenglon\n        pivotValor\n      }\n    }\n  }\n}"
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
        "query": 'query some {\n  BasesReportesGenerarReportePorId(\n    data: {id: 100000104}\n    parametros: {columnasAdicionales: [{id: -1, baseCampoId: 2519, seLect: false, wheRe: true, groUp: false, baseReporteCondicionCatalogoId: 25, groupAscendente: null, andOr: "AND", visible: true, esId: false, isDeleted: false, secuencia: -1, baseReporteId: 100000104}], condicionesAdicionales: [{valorInicial: "2024-11-29", valorFinal: "", baseReporteColumnaId: -1}]}\n  ) {\n    datosListasSeleccion\n    resultadoReporteHashmap\n    baseReporte {\n      id\n      carpetaId\n      parasiteParent\n      compartida\n      esQuery\n      nombreReporte\n      tablaPrincipalId\n      moduloPrincipalId\n      baseReporteTipoId\n      baseReporteIdDetalle\n      basesReportesColumnas {\n        id\n        basesCampos {\n          nombreEtiqueta\n        }\n      }\n      basesReportesPivotConfiguracion {\n        baseReporteColumnaId\n        baseCampoAlias\n        pivotColumna\n        pivotRenglon\n        pivotValor\n      }\n    }\n  }\n}',
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
    # print(clients)
    
    for note in sales_notes:
        # Filtrar elementos de array2 que coincidan en id
        note["items"] = [sub_item for sub_item in sales_notes_items if sub_item["id"] == note["id"]]
    
    for note in sales_notes:
        note["phone"] = [client['Teléfono'] for client in clients if client["Nombre del cliente"] == note["Cliente - Nombre del cliente"]][0]
        
    for invoice in invoices:
        # Filtrar elementos de array2 que coincidan en id
        invoice["items"] = [sub_item for sub_item in invoices_items if sub_item["id"] == invoice["id"]]
    
    for invoice in invoices:
        invoice["phone"] = [client['Teléfono'] for client in clients if client["Nombre del cliente"] == invoice["Cliente - Nombre del cliente"]][0]
        
    data = invoices + sales_notes
    
    # dictlist_to_str_list(data, [])

    json_object = json.dumps(data, indent=4)
    with open("sample.json", "w",encoding='utf8') as outfile:
        outfile.write(json_object)


def dictlist_to_str_list(list, cols):
    result = []
    for row in list:
        text = ""
        for col in cols:
            text = text + str(list[col][row])
            if col != len(list) - 1:
                text = text + " - "
        text = text.replace("\n", "").replace("\r", "").strip()
        result.append(text)
    

def save_device_to_kordata():
    currentToken = get_current_token()

    headers = {
        "user-agent": "pixel/0.0.1",
        "Content-Type": "application/json",
        "authorization": "Bearer " + currentToken,
    }
    payload = {
        "variables": {},
        "query": "mutation {\n  VehiculosGuardar(\n    data: {modelo: \"DELL RUGGED\", color: \"NO\", clienteId: 5805, placas: \"NA\", marca: \"DESCONOCIDO\", motor: \"SI, CARGADOR\", ano: \"SE LE CAMBIO LA BATERÍA PORQUE YA NO TENIA ENERGIA, PERO YA NO ENCENDIÓ\", serie: \"VINO POR PAQUETERÍA\", nombreAseguradora: \"NO\", numeroEconomico: \"56 1915 9383\", numeroPolizaSeguro: \"4\"}\n  ) {\n    id\n    modelo\n    color\n    clienteId\n    placas\n    marca\n    motor\n    ano\n    serie\n    nombreAseguradora\n    numeroEconomico\n    numeroPolizaSeguro\n  }\n}"
    }
    response = requests.post(
        K_ENDPOING,
        json=payload,
        headers=headers,
    )

def save_os_to_kordata():
    currentToken = get_current_token()

    headers = {
        "user-agent": "pixel/0.0.1",
        "Content-Type": "application/json",
        "authorization": "Bearer " + currentToken,
    }
    payload = {
        "variables": {},
        "query": "mutation {\n  OrdenesServiciosGuardar(\n    data: {sucursalId: 1, almacenId: 1, clienteId: 5805, monedaId: 1, ordenesServiciosVehiculos: [{vehiculoId: 4403, isDeleted: false}], automotrizKms: \"Se le recomienda, no dejar el equipo apagado por mucho tiempo sin la batería\", campoAdicionalTexto2: \"Se le hizo un drenado de energia, se abrio el equipo para quitar la batería interna de reloj y la ram, se procedio a presionar el boton de encendido y se conectó el equipo, finalmente encendió, se hicieron pruebas de funcionamiento con y sin batería, el equipo funcionó bien\", nombreEntrego: \"Sin orden de compra\", ejecutivoId: 14880, comentarios: \"2\", impuestos: 0, descuento: 0, importeTotal: 0, subtotal: 0, ordenesServiciosDetalle: [{productoId: 3398, descripcion: \"MANO DE OBRA GARANTÍA\", precioUnitario: 0, cantidad: 2, impuestos: 0, tasasDocumentos: [], subtotal: 0, trazabilidadId: null, asesorServicioId: null, porcentajeDescuento: 0, horasTrabajo: 0, id: null, isDeleted: false}]}\n  ) {\n    id\n  }\n}"
    }
    response = requests.post(
        K_ENDPOING,
        json=payload,
        headers=headers,
    )



payload_service_order ={
  "variables": {},
  "query": "{\n  OrdenesServiciosBuscarPorId(data: {id: 4513}) {\n    cotizacionId\n    sucursalId\n    almacenId\n    clienteId\n    descuento\n    subtotal\n    importeTotal\n    impuestos\n    listaPrecioId\n    monedaId\n    comprasVentasRelaciones {\n      id\n      ordenServicioId\n      compraId\n      isDeleted\n    }\n    id\n    estado\n    monedaTipoCambio\n    folioPrefijo\n    vehiculoId\n    ordenesServiciosVehiculos {\n      id\n      ordenServicioId\n      vehiculoId\n      isDeleted\n    }\n    automotrizKms\n    campoAdicionalTexto2\n    nombreEntrego\n    ordenesServiciosDetalle {\n      id\n      vehiculoId\n      productoId\n      descripcion\n      cantidad\n      precioUnitario\n      tasasDocumentos {\n        id\n        monto\n        montoImporte\n        ordenServicioDetalleId\n        tasaId\n        tasaMontoTipo\n      }\n      impuestos\n      porcentajeDescuento\n      subtotal\n      ordenServicioId\n      asesorServicioId\n      trazabilidadId\n      horasTrabajo\n      detallePaquete {\n        id\n        productoId\n        sku\n        descripcion\n        cantidad\n        cantidadUnitaria\n        costo\n        importe\n        trazabilidadId\n        isDeleted\n      }\n    }\n    ejecutivoId\n    comentarios\n    fechaRegistro\n    usuarioRegistro\n    fechaModificacion\n    usuarioModificador\n    fechaRevision\n    usuarioRevision\n    fechaReparacion\n    usuarioReparacion\n    fechaCerrada\n    usuarioCerrada\n    fechaCerradaSinFactura\n    usuarioCerradaSinFactura\n    fechaFacturada\n    usuarioFacturada\n    fechaCancelacion\n    usuarioCancelo\n  }\n}"
}

join_notes_and_items()

# login(USERNAME, PASS)

# get_clients()

# logout(get_current_token())
