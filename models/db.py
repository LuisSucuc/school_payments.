# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=[])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.create_user_groups = None

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------



db.define_table('mes_servicio',
    Field('nombre',         'string',           label = T('Nombre')),
    Field('orden',          'double',           label = T('Orden'),),
    format = '%(nombre)s')

db.mes_servicio.nombre.requires  = IS_NOT_EMPTY(error_message=T('Mes inválido'))
db.mes_servicio.orden.requires   = IS_FLOAT_IN_RANGE(0, error_message=T('Orden inválido'))

db.define_table('seccion',
    Field('name',           'string',           label = T('Name')),
    format = '%(name)s')

db.seccion.name.requires          = IS_NOT_EMPTY(error_message=T('Nombre invalido'))


db.define_table('grado',
    Field('name',           'string',               label = T('Name')),
    Field('valor',          'double',               label = T('Valor (Q.)')),
    format = '%(name)s')
db.grado.name.requires = IS_NOT_EMPTY(error_message=T('Nombre invalido'))
db.grado.valor.requires= IS_FLOAT_IN_RANGE(0, error_message=T('Precio inválido'))


db.define_table('seccion_grado',
    Field('grado',         'reference grado',     label = T('Grado')),
    Field('seccion',        'reference seccion',    label = T('Seccion')),
    format = lambda record: record.grado.name + ' - ' + record.seccion.name )

db.seccion_grado.seccion.requires  = IS_IN_DB(db, 'seccion.id', db.seccion._format,
                                        zero=T('Selecciona uno'), error_message=T('Selecciona seccion'),)
db.seccion_grado.grado.requires  = IS_IN_DB(db, 'grado.id', db.grado._format,
                                        zero=T('Selecciona uno'), error_message=T('Selecciona grado'), orderby='name')


db.define_table('estudiante',
    Field('nombres',            'string',                   label = 'Nombres'),
    Field('apellidos',          'string',                   label = 'Apellidos'),
    Field('email',              'string',                   label = 'Coreo electronico'),
    Field('fecha_nacimiento',   'date',                     label = 'Fecha de nacimiento'),
    Field('fecha_ingreso',      'date',                     label = 'Fecha de ingreso'),
    Field('sexo',               'string',                   label = 'Sexo'),
    Field('activo',             'boolean',                  label = T('Activo'), default=True),
    Field('seccion_grado',      'reference seccion_grado',  label = T('Grado')),
    format = '%(nombres)s')


db.estudiante.nombres.requires           = IS_NOT_EMPTY(error_message=T('Nombres invalidos'))
db.estudiante.apellidos.requires         = IS_NOT_EMPTY(error_message=T('Apellidos invalidos'))
db.estudiante.email.requires             = IS_EMAIL(error_message=T('Apellidos invalidos'))
db.estudiante.fecha_nacimiento.requires  = IS_DATE(format=T('%d/%m/%Y'), error_message='¡Debe ser YYYY-MM-DD!')
db.estudiante.fecha_ingreso.requires     = IS_DATE(format=T('%d/%m/%Y'), error_message='¡Debe ser YYYY-MM-DD!')
db.estudiante.sexo.requires              = IS_IN_SET(['Masculino', 'Femenino'])
db.estudiante.seccion_grado.requires  = IS_IN_DB(db, 'seccion_grado.id', db.seccion_grado._format,
                                        zero=T('Selecciona uno'), error_message=T('Selecciona un grado'))



db.define_table('pago',
    Field('estudiante',             'reference estudiante',         label = 'Estudiante'),
    Field('mes_servicio',           'reference mes_servicio',       label = 'Sección'),
    Field('fecha_ingreso',          'date',                         label = 'Fecha de pago', default=request.now),
    format = '%(estudiante)s')

db.pago.mes_servicio.requires  = IS_IN_DB(db, 'mes_servicio.id', db.mes_servicio._format,
                                        zero=T('Selecciona uno'), error_message=T('Selecciona mes-servicio'),)
db.pago.estudiante.requires  = IS_IN_DB(db, 'estudiante.id', db.estudiante._format,
                                        zero=T('Selecciona uno'), error_message=T('Selecciona estudiante'), orderby='name')
