import xmlrpc.client
import os
from dotenv import load_dotenv
import requests

load_dotenv()  # Cargar las variables del entorno

# Obtener las credenciales de Odoo desde el archivo .env
username = os.getenv("ODOO_USERNAME")
password = os.getenv("ODOO_PASSWORD")
url = os.getenv("ODOO_URL")  # Url
db = os.getenv("ODOO_DB")  # DB

# Conectar a Odoo usando XML-RPC
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Autenticación en Odoo
uid = common.authenticate(db, username, password, {})
print(f"Usuario autenticado: {uid}")

def verificar_lead(lead_id):
    """Verifica el correo electrónico del lead y lo asocia a un contacto si es necesario."""
    # Obtener los detalles del lead
    lead_details = models.execute_kw(db, uid, password,
                                     'crm.lead', 'read',
                                     [lead_id], {'fields': ['email_from', 'name']})

    lead_email = lead_details[0]['email_from']

    if lead_email:
        # Buscar si el contacto ya existe
        contact = models.execute_kw(db, uid, password,
                                     'res.partner', 'search',
                                     [[('email', '=', lead_email)]], {'limit': 1})

        if contact:
            # Si el contacto existe, asociarlo con el lead y marcarlo como calificado
            models.execute_kw(db, uid, password,
                              'crm.lead', 'write',
                              [lead_id, {'partner_id': contact[0], 'stage_id': 2}])  # 2 es la etapa de "Calificado"
            print(f"Lead {lead_id} asociado con el contacto {contact[0]}")
        else:
            # Si no existe el contacto, no hacer nada (solo se crea el lead sin calificar)
            print(f"No se creó un contacto para el lead {lead_id}.")
        
        # Crear una tarea para completar los datos del cliente
        task_vals = {
            'name': f'Completar datos de {lead_email}',
            'user_id': uid,  # Asignar la tarea al usuario que creó el lead
            'date_deadline': '2025-02-28',  # Ajusta la fecha según tus necesidades
            'description': f'Revisar y completar la información del cliente {lead_email}.'}
        
        task_id = models.execute_kw(db, uid, password,
                                    'project.task', 'create', [task_vals])
        print(f"Tarea creada con el ID {task_id} para completar los datos del cliente {lead_email}")
    else:
        print(f"El lead {lead_id} no tiene correo electrónico.")

# Aquí se llamaría a esta función con el lead_id que es pasado al servidor desde Odoo.
