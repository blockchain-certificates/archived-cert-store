import json


def find_certificate_by_id(uid):
    from cert_store import cert_store_connection
    cert_raw = cert_store_connection.get_certificate(uid)
    cert_string = cert_raw.decode('utf-8')
    return json.loads(cert_string)


