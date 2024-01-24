"""DD Domain Module"""
from __future__ import annotations
import dataclasses
from datetime import datetime, UTC
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from roche_datachapter_lib.db_config import DbConfig
from roche_datachapter_lib.data_transformer import DataTransformer

try:
    app = Flask(__name__)
    app.config.from_object(DbConfig())
    db = SQLAlchemy(app)

    @dataclasses.dataclass
    class LogModel(db.Model):
        """Log entity class"""
        __bind_key__ = DbConfig.validate_bind(
            'sqlserver_latam_ar')  # Bind para la conexión
        __table_args__ = {"schema": 'dbo'}  # Debe existir el esquema en la bd
        __tablename__ = 'TXN_LogTable'
        job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        originating_server_id = db.Column(db.Integer, nullable=False)
        name = db.Column(db.String(128), nullable=False)
        enabled = db.Column(db.Boolean, nullable=False)
        description = db.Column(db.String(512), nullable=True)
        start_step_id = db.Column(db.Integer, nullable=False)
        category_id = db.Column(db.Integer, nullable=False)
        owner_sid = db.Column(db.String(85), nullable=False)
        notify_level_eventlog = db.Column(db.Integer, nullable=False)
        notify_level_email = db.Column(db.Integer, nullable=False)
        notify_level_netsend = db.Column(db.Integer, nullable=False)
        notify_level_page = db.Column(db.Integer, nullable=False)
        notify_email_operator_id = db.Column(db.Integer, nullable=False)
        notify_netsend_operator_id = db.Column(db.Integer, nullable=False)
        notify_page_operator_id = db.Column(db.Integer, nullable=False)
        delete_level = db.Column(db.Integer, nullable=False)
        date_created = db.Column(db.DateTime, nullable=False)
        date_modified = db.Column(db.DateTime, nullable=False)
        version_number = db.Column(db.Integer, nullable=False)
        def __init__(self, log_data):
            try:
                self.job_id = log_data['job_id']
                self.originating_server_id = log_data['originating_server_id']
                self.name = log_data['name']
                self.enabled = log_data['enabled']
                self.description = log_data['description']
                self.start_step_id = log_data['start_step_id']
                self.category_id = log_data['category_id']
                self.owner_sid = log_data['owner_sid']
                self.notify_level_eventlog = log_data['notify_level_eventlog']
                self.notify_level_email = log_data['notify_level_email']
                self.notify_level_netsend = log_data['notify_level_netsend']
                self.notify_level_page = log_data['notify_level_page']
                self.notify_email_operator_id = log_data['notify_email_operator_id']
                self.notify_netsend_operator_id = log_data['notify_netsend_operator_id']
                self.notify_page_operator_id = log_data['notify_page_operator_id']
                self.delete_level = log_data['delete_level']
                self.date_created = log_data['date_created']
                self.date_modified = log_data['date_modified']
                self.version_number = log_data['version_number']
            except KeyError as err:
                raise ValueError(
                    f"No se pudo inicializar {self.__class__}: Clave faltante - {err}") from err

        def __repr__(self):
            """String representation"""
            attributes = ', '.join(
                f"{key}: {value}" for key, value in self.__dict__.items())
            return f"{self.__class__.__name__} -> {attributes}"

    @dataclasses.dataclass
    class DemoModel(db.Model):
        """Demo entity class"""
        __bind_key__ = DbConfig.validate_bind(
            'sqlserver_latam_ar')  # Bind para la conexión
        __table_args__ = {"schema": 'dbo'}  # Debe existir el esquema en la bd
        __tablename__ = 'TXN_LogCatalogoDeProcesos'
        LogProcesoId = db.Column(db.Integer, primary_key=True)
        ProcesoId = db.Column(db.Integer, foreign_key='SYSCatalogoProcesos.ProcesoId')
        DT_Desde = db.Column(db.Date, nullable=True)
        DT_Hasta = db.Column(db.Date, nullable=True)
        EstadoId = db.Column(db.integer, foreign_key='SYSEstadoProcesos.EstadoId')
        FalloEnPaso = db.Column(db.String(1000))
        Auxiliar1 = db.Column(db.int, nullable = True)
        Auxiliar2 = db.Column(db.int, nullable = True)
        Auxiliar3 = db.Column(db.int, nullable = True)
        FechaInicioCorrida = db.Column(db.DateTime, nullable = True)
        FechaFinCorrida = db.Column(db.DateTime, nullable = True)

        def __init__(self, data_dic):
            try:
                self.id = data_dic['LogProcesoId']
                self.proceso_id = data_dic['ProcesoId']
                self.desde = data_dic['DT_Desde']
                self.hasta = data_dic['DT_Hasta']
                self.estado_id = data_dic['EstadoId']
                self.fallo_en_paso = data_dic['FalloEnPaso']
                self.auxiliar1 = data_dic['Auxiliar1']
                self.auxiliar2 = data_dic['Auxiliar2']
                self.auxiliar3 = data_dic['Auxiliar3']
                self.fecha_inicio_corrida = data_dic['FechaInicioCorrida']
                self.fecha_fin_corrida = data_dic['FechaFinCorrida']
            except KeyError as err:
                raise ValueError(
                    f"No se pudo inicializar {self.__class__}: Clave faltante - {err}") from err

        def __repr__(self):
            """String representation"""
            attributes = ', '.join(
                f"{key}: {value}" for key, value in self.__dict__.items())
            return f"{self.__class__.__name__} -> {attributes}"

except Exception as e:
    raise ConnectionError(f"Error en definición de dominio. {e}") from e