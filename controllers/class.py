# -*- coding: utf-8 -*-

@auth.requires_login()
def secciones():
    grid = SQLFORM.grid(db.seccion)
    return locals()

@auth.requires_login()
def grados():
    grid = SQLFORM.grid(db.grado)
    return locals()


@auth.requires_login()
def secciones_grados():
    grid = SQLFORM.grid(db.seccion_grado)
    return locals()


@auth.requires_login()
def estudiantes():
    grid = SQLFORM.grid(db.estudiante)
    return locals()