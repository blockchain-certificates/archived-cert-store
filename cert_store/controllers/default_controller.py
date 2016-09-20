

def find_certificate_by_id(uid):
    from cert_store import cert_store_connection
    return cert_store_connection.get_certificate(uid)


