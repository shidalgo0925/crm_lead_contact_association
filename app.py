from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Obtener las credenciales de Odoo desde las variables de entorno
ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")
API_KEY = os.getenv("API_KEY")

@app.route('/crm_lead_contact_association', methods=['POST'])
def crm_lead_contact_association():
    # Obtener los datos de la solicitud
    data = request.get_json()

    lead_id = data.get('lead_id')

    if not lead_id:
        return jsonify({"error": "lead_id es requerido"}), 400

    # Lógica para integrar con Odoo
    try:
        # Usamos la API de Odoo para autenticar y realizar acciones
        # Establecer conexión a Odoo a través de XML-RPC
        url = f'{ODOO_URL}/xmlrpc/2/common'
        common = xmlrpc.client.ServerProxy(url)
        uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})

        # Lógica para asociar el lead con el contacto
        # Aquí puedes realizar todas las verificaciones que necesitas

        # Responder con éxito
        return jsonify({"status": "success", "message": "Lead asociado con contacto."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
