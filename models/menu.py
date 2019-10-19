# -*- coding: utf-8 -*-

response.menu = [
    (T('Home'),     'flaticon-map',         URL('default', 'index'), []),
]

if auth.has_membership(group_id='Administrator'):
    response.menu += [ (T('Manage'),     'flaticon-interface-1',        None, 
                        [
                            (T('Users'),            False,      URL('manage', 'users'),     []),
                            ('Secciones',           False,      URL('class', 'secciones'),   []),
                            ('Grados',              False,      URL('class', 'grados'),    []),
                            ('Asignación SG',       False,      URL('class', 'secciones_grados'),    []),
                            ('Estudiantes',         False,      URL('class', 'estudiantes'),    []),
                        ]),
                    ]