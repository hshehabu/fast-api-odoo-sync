import xmlrpc.client
import os
from typing import Dict, List, Optional

# Odoo connection details
ODOO_URL = os.getenv('ODOO_URL', 'http://localhost:8069')
ODOO_DB = os.getenv('ODOO_DB', 'odoo')
ODOO_USERNAME = os.getenv('ODOO_USERNAME', 'admin')
ODOO_PASSWORD = os.getenv('ODOO_PASSWORD', 'admin')

def get_odoo_connection():
    """Create and return Odoo connection"""
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    return uid, models

def get_all_employees() -> List[Dict]:
    """Get all employees from Odoo"""
    uid, models = get_odoo_connection()
    
    # Search for all employees
    employee_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
        'hr.employee', 'search',
        [[['active', '=', True]]]
    )
    
    # Read employee details
    employees = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
        'hr.employee', 'read',
        [employee_ids],
        {'fields': ['name', 'work_phone', 'address_id', 'job_id']}
    )
    
    return employees

def get_job(employee_id: int) -> Optional[Dict]:
    """Get job details for an employee"""
    uid, models = get_odoo_connection()
    
    # Get employee's job
    employee = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
        'hr.employee', 'read',
        [[employee_id]],
        {'fields': ['job_id']}
    )
    
    if not employee or not employee[0]['job_id']:
        return None
        
    # Get job details
    job = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
        'hr.job', 'read',
        [[employee[0]['job_id'][0]]],
        {'fields': ['name', 'description']}
    )
    
    if job:
        return {
            'id': job[0]['id'],
            'name': job[0]['name'],
            'description': job[0]['description']
        }
    return None