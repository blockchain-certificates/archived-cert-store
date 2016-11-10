from flask import jsonify



def find_certificate_by_id(uid):
    from cert_store import cert_store
    certificate_json = cert_store.get_certificate_json(uid)
    return jsonify(certificate_json)
