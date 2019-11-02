# -*- coding: utf-8 -*-


def secciones_grados():
    sg = db((db.seccion_grado.id>0)&
            (db.seccion_grado.seccion==db.seccion.id)&
            (db.seccion_grado.grado==db.grado.id)).select(db.seccion.name,
                                                          db.grado.name,
                                                          db.seccion_grado.id)
    grados = []
    for element in sg:
        grados.append(dict(id=element.seccion_grado.id,
                            grado = element.grado.name + " " + element.seccion.name))
    return response.json(grados)


def estudiantes_grado():
    #return response.json(dict(vars=request.vars))
    result = db(db.estudiante.seccion_grado == request.vars.gradoId).select().as_list()
    import random
    for el in result:
        el["picture"] = "https://randomuser.me/api/portraits/men/" + str(random.randint(0,79))+".jpg"
    return response.json(result)


def pagos():
    estudiante_id = request.vars.estudianteId
    estudiante = db.estudiante[estudiante_id] if estudiante_id else None
    cantidad = estudiante.seccion_grado.grado.valor if estudiante else 0
    servicios = db(db.mes_servicio).select(orderby=db.mes_servicio.orden)
    pagos = []
    for servicio in servicios:
        pago = db( (db.pago.estudiante == estudiante_id)&
                  (db.pago.mes_servicio == servicio.id)  ).select().first()
        servicio.pagado = True if pago else False
        pagos.append(servicio)
    return response.json(pagos)

def estudiantes():
    return response.json(db(db.estudiante).select().as_list())
