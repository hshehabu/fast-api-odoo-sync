import aiohttp
from odoo_sync.app.odoo_client import get_all_employees, get_job

API_GATEWAY_URL = "http://localhost:9000"

synced_ids = set()

async def sync_employees():
    global synced_ids
    employees = get_all_employees()
    
    async with aiohttp.ClientSession() as session:
        for emp in employees:
            if emp['id'] in synced_ids:
                continue

            job = get_job(emp['id']) if emp.get('job_id') else None

            if job:
                async with session.post(f"{API_GATEWAY_URL}/job/", json=job) as response:
                    if response.status != 200:
                        print(f"Failed to sync job for employee {emp['id']}")

            emp_payload = {
                "name": emp["name"],
                "address": emp.get("address_id", [False, ""])[1] if emp.get("address_id") else "",
                "phone": emp.get("work_phone", ""),
                "job_id": job["id"] if job else None,
            }

            async with session.post(f"{API_GATEWAY_URL}/employee/", json=emp_payload) as response:
                if response.status == 200:
                    synced_ids.add(emp["id"])
                else:
                    print(f"Failed to sync employee {emp['id']}")