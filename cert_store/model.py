class BlockcertVersion:
    V1_1 = 0
    V1_2 = 1


def detect_version(certificate_json):
    # assumes it's a certificate. Maybe add some schema validation
    if not '@context' in certificate_json:
        return BlockcertVersion.V1_1
    context = certificate_json['@context']
    version_marker = context.rfind('/')
    version = context[version_marker + 1:]
    if version == 'v1':
        return BlockcertVersion.V1_2
    raise Exception('Unknown Blockchain Certificate version')


class V1_2_BlockchainCertificate(object):
    def __init__(self, json_certificate):
        self.version = BlockcertVersion.V1_2
        document = json_certificate['document']
        certificate = document['certificate']
        assertion = document['assertion']
        recipient = document['recipient']
        receipt = json_certificate['receipt']
        txid = receipt['anchors'][0]['sourceId']
        self.uid = assertion['uid']
        self.logo_image = certificate['issuer']['image']
        self.recipient_given_name = recipient['givenName']
        self.recipient_family_name = recipient['familyName']
        self.recipient_public_key = recipient['publicKey']
        self.title = certificate['name']
        self.organization = certificate['issuer']['name']
        self.description = certificate['description']
        self.issuer_id = certificate['issuer']['id']
        self.transaction_id = txid
        self.issued_on = assertion['issuedOn']

        if 'image:signature' in assertion:
            self.signature_image = assertion['image:signature']
        else:
            self.signature_image = None

        if 'subtitle' in certificate:
            self.subtitle = certificate['subtitle']
        else:
            self.subtitle = None


class V1_1_BlockchainCertificate(object):
    def __init__(self, json_certificate, txid, certificate_bytes):
        self.version = BlockcertVersion.V1_1
        self.uid = json_certificate['assertion']['uid']
        self.logo_image = json_certificate['certificate']['issuer']['image']
        self.recipient_given_name = json_certificate['recipient']['givenName']
        self.recipient_family_name = json_certificate['recipient']['familyName']
        self.recipient_public_key = json_certificate['recipient']['pubkey']
        self.title = json_certificate['certificate']['title']
        self.organization = json_certificate['certificate']['issuer']['name']
        self.description = json_certificate['certificate']['description']
        self.signature_image = json_certificate['assertion']['image:signature']
        self.issuer_id = json_certificate['certificate']['issuer']['id']
        self.transaction_id = txid
        self.issued_on = json_certificate['assertion']['issuedOn']

        subtitle = json_certificate['certificate']['subtitle']['content']
        display_subtitle = json_certificate['certificate']['subtitle']['display']
        if display_subtitle in ['true', 'True', 'TRUE']:
            self.subtitle = subtitle
        else:
            self.subtitle = None

        self.certificate_bytes = certificate_bytes


def to_certificate_model(certificate_json, txid=None, certificate_bytes=None):
    version = detect_version(certificate_json)
    if version == BlockcertVersion.V1_1:
        if not txid or not certificate_bytes:
            raise Exception('V1.1 Blockchain Certificates require a transaction id and raw bytes')
        return V1_1_BlockchainCertificate(certificate_json, txid, certificate_bytes)
    elif version == BlockcertVersion.V1_2:
        return V1_2_BlockchainCertificate(certificate_json)
    else:
        raise Exception('Unknown Blockchain Certificate version')
