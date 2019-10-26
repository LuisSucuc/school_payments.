# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

@auth.requires_login()
def pagos():
    estudiante_id = request.vars.estudiante_id
    estudiante = db.estudiante[estudiante_id] if estudiante_id else None
    estudiantes = db(db.estudiante).select()
    servicios = db(db.mes_servicio).select(orderby=db.mes_servicio.orden)
    cantidad = estudiante.seccion_grado.grado.valor
    if request.post_vars:
        
        if request.vars.servicio_id:
            print db.pago.validate_and_insert(estudiante = estudiante_id,
                                            mes_servicio = request.vars.servicio_id)
            response.flash = "Pagado"
    def get_pagos_pendientes(estudiante_id):
        pagos = []
        for servicio in servicios:
            pago = db( (db.pago.estudiante == estudiante_id)&
                        (db.pago.mes_servicio == servicio.id)  ).select().first()
            servicio.pagado = True if pago else False
            pagos.append(servicio)
        return pagos
    return dict(get_pagos_pendientes = get_pagos_pendientes,
                estudiante_id       = estudiante_id,
                estudiantes         = estudiantes,
                estudiante          = estudiante,
                cantidad            = cantidad)
