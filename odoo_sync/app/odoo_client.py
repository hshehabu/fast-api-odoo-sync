import xmlrpc.client

ODOO_URL = "http://localhost:8069"
ODOO_DB = "odoo_fastapi"
ODOO_USERNAME = "admin"
ODOO_PASSWORD = "admin"

common =  xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

def get_all_employees():
    return models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'hr.employee','search_read',
        [[]], {'fields': ['id', 'name', 'address_id', 'work_phone', 'job_id']})
def get_job(job_id):
    job = models.execute_kw(ODOO_DB,uid,ODOO_PASSWORD,'hr.job','read',
        [job_id], {'fields': ['id', 'name']})
    return job[0] if job else None