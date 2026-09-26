"""Generate the synthetic VC fixtures and their human-readable manifest.

Run from the repository root: python event-ecosystem-lab/build_data.py
The vocabulary and SHACL profile are deliberately small teaching artifacts.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'data'
OUT.mkdir(exist_ok=True)
BASE = 'https://jgmikael.github.io/procurement-automation-demo/event-ecosystem-lab/data/'
# Keep the required W3C context first. Add only terms used by the particular
# credential; duplicating every profile term in all 19 files obscures the subject.
VC_CONTEXT = 'https://www.w3.org/ns/credentials/v2'
NAMESPACES = {
    'ebwv': 'https://w3id.org/ebwv#',
    'epo': 'http://data.europa.eu/a4g/ontology#',
    'elig': BASE + 'eligibility.ttl#',
    'trade': BASE + 'trade.ttl#',
    'busdoc': 'https://iri.suomi.fi/model/busdoc/',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
}
COERCIONS = {
    'elig:asOf': {'@type': 'xsd:date'},
    'elig:periodStart': {'@type': 'xsd:date'},
    'elig:periodEnd': {'@type': 'xsd:date'},
    'elig:appliesToLot': {'@type': '@id'},
    'elig:annualTurnover': {'@type': 'xsd:decimal'},
    'elig:insuranceLimit': {'@type': 'xsd:decimal'},
    'elig:deliveredValue': {'@type': 'xsd:decimal'},
    'busdoc:issueDate': {'@type': 'xsd:date'},
    'busdoc:quantity': {'@type': 'xsd:decimal'},
    'busdoc:deliveredQuantity': {'@type': 'xsd:decimal'},
    'busdoc:receivedQuantity': {'@type': 'xsd:decimal'},
    'busdoc:priceAmount': {'@type': 'xsd:decimal'},
    'busdoc:payableAmount': {'@type': 'xsd:decimal'},
    'epo:hasAwardDecisionDate': {'@type': 'xsd:dateTime'},
    'elig:decisionFor': {'@type': '@id'},
    'ebwv:legalIdentifier': {'@id': 'ebwv:legalIdentifier', '@type': 'ebwv:Euid'},
    'ebwv:dateOfRegistration': {'@type': 'xsd:date'},
    'ebwv:dateOfBirth': {'@type': 'xsd:date'},
    'ebwv:activity': {'@type': 'ebwv:Nace21'},
    'ebwv:scopeOfAuthorization': {'@type': '@id'},
    'ebwv:attestationLegalCategory': {'@type': '@id'},
    'elig:jointSignatureCount': {'@type': 'xsd:integer'},
    'elig:signatoryGroup': {'@type': '@id'},
}

def credential_context(credential):
    keys, values = set(), set()
    def collect(node):
        if isinstance(node, dict):
            for key, value in node.items():
                keys.add(key)
                collect(value)
        elif isinstance(node, list):
            for value in node: collect(value)
        elif isinstance(node, str):
            values.add(node)
    collect(credential)
    terms = {term: definition for term, definition in COERCIONS.items() if term in keys}
    # Include namespace dependencies from identifiers and datatype declarations.
    for definition in terms.values(): collect(definition)
    used = {token.split(':',1)[0] for token in keys | values if ':' in token}
    local = {prefix: iri for prefix, iri in NAMESPACES.items() if prefix in used}
    local.update(terms)
    return [VC_CONTEXT, local]

LOT = 'urn:demo:procurement:lot-1'
CO = 'urn:demo:operator:aalto-timber'
BUYER = 'urn:demo:buyer:harbour-city'
EUID = 'FI-PRH-3141592-6' # Synthetic EUID: country + example register code + example Business ID.
EUCC_RULEBOOK = 'https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/blob/main/rulebooks/rb-eucc/README.md'

EUCC_COMPANY = {
 'ebwv:legalName':'Aalto Timber Services Oy',
 'ebwv:legalIdentifier':EUID,
 'ebwv:legalForm':'Oy',
 'ebwv:jurisdiction':'FI',
 'ebwv:registeredAddress':{'id':'urn:demo:address:aalto','type':'ebwv:Address',
                           'ebwv:fullAddress':'Example Street 12; 00100 Helsinki; FI',
                           'ebwv:postCode':'00100','ebwv:postName':'Helsinki','ebwv:adminUnitL1':'FI'},
 'ebwv:dateOfRegistration':'2017-05-16',
 'ebwv:legalStatus':'active',
 'ebwv:activity':'31.00',
 'ebwv:legalRepresentative':[
     {'id':'urn:demo:person:mira','type':['ebwv:LegalRepresentative','ebwv:Person'],
      'ebwv:fullName':'Mira Example','ebwv:dateOfBirth':'1985-04-12',
      'ebwv:scopeOfAuthorization':'ebwv:Jointly','elig:jointSignatureCount':'2',
      'elig:signatoryGroup':'urn:demo:signatory-group:board-reps-1'},
     {'id':'urn:demo:person:oskar','type':['ebwv:LegalRepresentative','ebwv:Person'],
      'ebwv:fullName':'Oskar Example','ebwv:dateOfBirth':'1987-08-03',
      'ebwv:scopeOfAuthorization':'ebwv:Jointly','elig:jointSignatureCount':'2',
      'elig:signatoryGroup':'urn:demo:signatory-group:board-reps-1'}],
}

ELIG = [
 ('registration','EU Company Certificate','CompanyRegistration', 'Demo Finnish Trade Register issuer', EUCC_COMPANY, 'WE BUILD EUCC rulebook §2 and §3.3; limited liability company; joint signatures of two'),
 ('representation','Representative authority','RepresentationAuthority','Finnish Trade Register',{'elig:representativeName':'Mira Example','elig:scope':'Submit eligibility evidence and tender for LOT-1','elig:authorityStatus':'ACTIVE','elig:asOf':'2026-09-26'}, 'Authorised action in the wallet; agent governance design'),
 ('tax','Tax compliance','TaxCompliance','Finnish Tax Administration',{'elig:complianceStatus':'CLEAR','elig:jurisdiction':'FI','elig:asOf':'2026-09-26'}, 'Exclusion proof; Arts. 25–26, 28'),
 ('social','Social security contributions','SocialSecurityCompliance','Finnish Social Insurance Institution',{'ebwv:complianceStatus':'CLEAR','elig:jurisdiction':'FI','elig:asOf':'2026-09-26'}, 'Exclusion proof; Arts. 25–26, 28'),
 ('insolvency','Insolvency status','InsolvencyStatus','Finnish Insolvency Register',{'elig:proceedingStatus':'NO_RELEVANT_PROCEEDING','elig:asOf':'2026-09-26'}, 'Exclusion proof; Arts. 25–26, 28'),
 ('exclusion','Exclusion grounds check','ExclusionCheck','Competent judicial evidence service',{'elig:scope':'Applicable mandatory exclusion grounds for LOT-1','elig:checkOutcome':'NO_RELEVANT_GROUND_REPORTED','elig:asOf':'2026-09-26'}, 'Exclusion proof; Arts. 25–26, 28; scoped outcome only'),
 ('financial','Financial capacity','FinancialCapacity','Licensed financial statement register',{'elig:annualTurnover':'2100000.00','elig:currencyCode':'EUR','elig:periodStart':'2025-01-01','elig:periodEnd':'2025-12-31','elig:insuranceLimit':'1000000.00'}, 'Economic and financial standing; Art. 27(1)(c)'),
 ('licence','Professional authorisation','ProfessionalAuthorisation','Professional licensing authority',{'elig:registerName':'FI Works Provider Register','elig:licenceIdentifier':'FI-WORKS-2026-0042','elig:licenceStatus':'ACTIVE','elig:asOf':'2026-09-26'}, 'Trade register/licence where applicable; Art. 27(1)(a)'),
 ('technical','Technical capacity','TechnicalCapacity','Qualified reference verifier',{'elig:referenceProject':'Municipal furniture supply 2024–2025','elig:deliveredValue':'780000.00','elig:currencyCode':'EUR','elig:qualificationStatus':'CONFIRMED'}, 'Technical and professional ability; Art. 27(1)(b)'),
 ('origin','Operator origin','OperatorOrigin','Finnish Trade Register',{'elig:establishmentCountry':'FI','elig:asOf':'2026-09-26'}, 'Origin information where procedure requires it; Art. 133'),
]
# The busdoc export is a component library (its prefix maps to UBL 2.2); these
# deliberately small examples select terms that still have UBL 2.4 counterparts.
# UBL document roots are defined locally because busdoc has no such root classes.
def party(identifier, kind):
    return {'id': identifier, 'type': f'busdoc:{kind}'}

def item_line(kind, identifier, quantity, price=None):
    line = {'id': f'urn:demo:line:{kind.lower()}-1', 'type': f'busdoc:{kind}',
            'busdoc:iD': '1', 'busdoc:item_': {'id': 'urn:demo:item:birch-desk',
                'type': 'busdoc:Item', 'busdoc:name': 'Modular birch desk'}}
    if quantity is not None:
        line['busdoc:invoicedQuantity' if kind == 'InvoiceLine' else
             'busdoc:receivedQuantity' if kind == 'ReceiptLine' else
             'busdoc:deliveredQuantity' if kind == 'DespatchLine' else 'busdoc:quantity'] = str(quantity)
    if price is not None:
        line['busdoc:price_'] = {'id': f'urn:demo:price:{kind.lower()}-1',
                                'type': 'busdoc:Price', 'busdoc:priceAmount': str(price)}
    return line

TRADING_PARTIES = {'busdoc:sellerSupplierParty': party(CO, 'SupplierParty'),
                   'busdoc:buyerCustomerParty': party(BUYER, 'CustomerParty')}
def document(identifier, day, **extra):
    return {'busdoc:iD': identifier, 'busdoc:issueDate': day, **extra}

TRADE = [
 ('catalogue','Supplier catalogue','Catalogue','OASIS UBL 2.4 Catalogue',
  document('CAT-2026-001','2026-09-22',**TRADING_PARTIES,
           **{'busdoc:catalogueLine_':{
               **item_line('CatalogueLine','1',None),
               'busdoc:requiredItemLocationQuantity':{'id':'urn:demo:location-quantity:1',
                   'type':'busdoc:ItemLocationQuantity',
                   'busdoc:price_':{'id':'urn:demo:price:catalogue-1','type':'busdoc:Price',
                                    'busdoc:priceAmount':'320.00'}}}}),
  'Supplier publishes a catalogue line'),
 ('offer','Supplier offer / quotation','Quotation','OASIS UBL 2.4 Quotation',
  document('QUO-2026-011','2026-09-26',**TRADING_PARTIES,
           **{'trade:quotationLine':{'id':'urn:demo:line:quotation-1',
                  'type':'busdoc:QuotationLine','busdoc:iD':'1',
                  'busdoc:lineItem_':item_line('LineItem','1',200,310)}}),
  'Commercial quotation; procurement tender remains distinct'),
 ('award','Buyer award decision','AwardDecision','ePO AwardDecision (outside UBL)',
  {'elig:decisionID':'AWD-2026-012','epo:hasAwardDecisionDate':'2026-10-08T00:00:00Z',
   'elig:appliesToLot':LOT,'elig:decisionFor':BASE+'offer.vc.json',
   'elig:decisionOutcome':'AWARDED'},
  'Procurement award governed by ePO, outside the UBL trade vocabulary'),
 ('acceptance','Seller order acceptance','OrderResponse','OASIS UBL 2.4 OrderResponse',
  document('AGR-2026-012','2026-10-10',**TRADING_PARTIES,
           **{'busdoc:orderReference_':{'id':BASE+'order.vc.json',
                   'type':'busdoc:OrderReference','busdoc:iD':'ORD-2026-014'},
              'trade:orderResponseCode':'ACCEPTED'}),
  'Seller responds to the buyer order; distinct from award'),
 ('order','Purchase order','Order','OASIS UBL 2.4 Order',
  document('ORD-2026-014','2026-10-09',**TRADING_PARTIES,
           **{'busdoc:orderLine_':{'id':'urn:demo:line:order-1','type':'busdoc:OrderLine',
                'busdoc:lineItem_':item_line('LineItem','1',200,310)}}),
  'Buyer places an order after award'),
 ('invoice','Supplier invoice','Invoice','OASIS UBL 2.4 Invoice',
  document('INV-2026-009','2026-11-02',**TRADING_PARTIES,
           **{'busdoc:documentCurrencyCode':'EUR',
              'busdoc:legalMonetaryTotal':{'id':'urn:demo:monetary-total:invoice-1',
                  'type':'busdoc:MonetaryTotal','busdoc:payableAmount':'62000.00'},
              'busdoc:invoiceLine_':item_line('InvoiceLine','1',200,310),
              'busdoc:orderDocumentReference_':{'id':BASE+'order.vc.json',
                   'type':'busdoc:DocumentReference','busdoc:iD':'ORD-2026-014'}}),
  'Supplier requests payment'),
 ('despatch','Despatch advice','DespatchAdvice','OASIS UBL 2.4 DespatchAdvice',
  document('DES-2026-027','2026-10-25',**TRADING_PARTIES,
           **{'trade:despatchLine':item_line('DespatchLine','1',200),
              'busdoc:orderDocumentReference_':{'id':BASE+'order.vc.json',
                   'type':'busdoc:DocumentReference','busdoc:iD':'ORD-2026-014'}}),
  'Supplier announces dispatched goods'),
 ('receipt','Receipt advice','ReceiptAdvice','OASIS UBL 2.4 ReceiptAdvice',
  document('REC-2026-028','2026-10-29',**TRADING_PARTIES,
           **{'trade:receiptLine':item_line('ReceiptLine','1',200),
              'busdoc:despatchDocumentReference':{'id':BASE+'despatch.vc.json',
                   'type':'busdoc:DocumentReference','busdoc:iD':'DES-2026-027'}}),
  'Buyer acknowledges receipt'),
 ('waybill','Waybill','Waybill','OASIS UBL 2.4 Waybill',
  document('WAY-2026-030','2026-10-25',
           **{'busdoc:carrierParty':party('urn:demo:carrier:baltic-logistics','Party'),
              'busdoc:shipment_':{'id':'urn:demo:shipment:1','type':'busdoc:Shipment',
                                  'busdoc:iD':'BDL-003145'}}),
  'Carrier records the shipment'),
]

def credential(name, category, cls, issuer, fields):
    if name == 'registration':
        # EUCC is reusable company evidence, independent of a particular procurement lot.
        subject={'id':CO,'type':'ebwv:LimitedLiabilityCompany',**fields}
    else:
        subject = {'id': f'urn:demo:{category}:{name}-2026',
                   'type': ('epo:AwardDecision' if name == 'award' else f'{"elig" if category == "eligibility" else "trade"}:{cls}')}
        if category == 'eligibility':
            subject.update({'elig:economicOperator':{'id':CO,'type':'ebwv:Company','ebwv:legalName':'Aalto Timber Services Oy','ebwv:legalIdentifier':EUID},'elig:appliesToLot':LOT})
            if name == 'social': subject['type'] = ['ebwv:SocialSecurityContribution','elig:SocialSecurityCompliance']
        subject.update(fields)
    issuer_id=(BUYER if name in ('award','order','receipt') else
               'urn:demo:carrier:baltic-logistics' if name=='waybill' else
               CO if category=='trade' else f'urn:demo:issuer:{name}')
    start=(fields.get('busdoc:issueDate') or fields.get('epo:hasAwardDecisionDate') or
           fields.get('elig:asOf') or '2026-09-26')[:10]
    vc={'@context':None,'type':['VerifiableCredential',f'{"elig" if category == "eligibility" or name == "award" else "trade"}:{cls}Credential'],
        'issuer':issuer_id,'credentialSubject':subject,
        'id':BASE+name+'.vc.json','validFrom':start+'T00:00:00Z'}
    if name=='registration':
        vc['type'].append('ebwv:ElectronicAttestationOfAttributes')
        vc['issuer']={'id':issuer_id,'type':'ebwv:PublicSectorBody',
                      'ebwv:legalName':'Demo Finnish Trade Register issuer','ebwv:jurisdiction':'FI'}
        vc['ebwv:attestationLegalCategory']='ebwv:Pub-EAA'
        # Short illustrative lifetime avoids inventing a non-working revocation service.
        vc['validUntil']='2026-09-26T23:00:00Z'
    vc['@context']=credential_context(vc)
    return vc

MANIFEST=[]
for category, rows in [('eligibility',ELIG),('trade',TRADE)]:
    for name,label,cls,issuer,fields,note in rows:
        vc=credential(name,category,cls,issuer,fields)
        (OUT/(name+'.vc.json')).write_text(json.dumps(vc,ensure_ascii=False,indent=2)+'\n')
        MANIFEST.append({'name':name,'label':label,'category':category,'class':cls,'basis':issuer,'note':note,'file':'data/'+name+'.vc.json'})
(OUT/'manifest.json').write_text(json.dumps(MANIFEST,ensure_ascii=False,indent=2)+'\n')

# Static teaching fixtures for the DID-identified OpenID4VP request payload and
# W3C VP response. Neither contains a cryptographic signature or usable endpoint.
requested = {'registration':'CompanyRegistration','tax':'TaxCompliance',
             'social':'SocialSecurityCompliance','representation':'RepresentationAuthority'}
sample_request = {
 'client_id':'decentralized_identifier:did:example:harbour-city-buyer',
 'response_type':'vp_token','response_mode':'direct_post',
 'response_uri':'https://buyer.example.invalid/oid4vp/callback',
 'nonce':'DEMO-FIXED-NONCE-NOT-FOR-PRODUCTION','state':'DEMO-STATE-NOT-FOR-PRODUCTION',
 'dcql_query':{'credentials':[
   {'id':name,'format':'ldp_vc','meta':{'type_values':[[BASE+'eligibility.ttl#'+cls+'Credential']]}}
   for name,cls in requested.items()]},
 'client_metadata':{'vp_formats_supported':{'ldp_vc':{'proof_type_values':['DataIntegrityProof']}}}
}
sample_vp = {
 'state':sample_request['state'],
 'vp_token':{'@context':[VC_CONTEXT],'type':['VerifiablePresentation'],
             'holder':'did:example:aalto-timber-ebw',
             'verifiableCredential':[json.loads((OUT/(name+'.vc.json')).read_text()) for name in requested]}
}
(OUT/'presentation-request.json').write_text(json.dumps(sample_request,ensure_ascii=False,indent=2)+'\n')
(OUT/'wallet-presentation.vp.json').write_text(json.dumps(sample_vp,ensure_ascii=False,indent=2)+'\n')

PREFIXES = '''@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ebwv: <https://w3id.org/ebwv#> .
@prefix epo: <http://data.europa.eu/a4g/ontology#> .
@prefix elig: '''+ '<'+BASE+'eligibility.ttl#> .\n'+'''@prefix trade: '''+ '<'+BASE+'trade.ttl#> .\n'+'@prefix busdoc: <https://iri.suomi.fi/model/busdoc/> .\n\n'
ELIG_LINKS = {
 'TaxCompliance':'epo:ExclusionGround',
 'SocialSecurityCompliance':'epo:ExclusionGround','InsolvencyStatus':'epo:ExclusionGround',
 'ExclusionCheck':'epo:ExclusionGround','FinancialCapacity':'epo:SelectionCriterion',
 'ProfessionalAuthorisation':'epo:SelectionCriterion','TechnicalCapacity':'epo:SelectionCriterion'}
ELIG_FIELDS = sorted({k for _,_,_,_,fields,_ in ELIG for k in fields if k.startswith('elig:')})
DATE_FIELDS = {'asOf','periodStart','periodEnd','issueDate','deliveryDate'}
DECIMAL_FIELDS = {'annualTurnover','insuranceLimit','deliveredValue','unitPrice','payableAmount'}
INTEGER_FIELDS = {'quantity','receivedQuantity'}
IRI_FIELDS = {'appliesToLot','sourceDocument','responseTo'}

def property_owl(term):
    local=term.split(':')[1]
    kind='owl:ObjectProperty' if local in IRI_FIELDS or local=='economicOperator' else 'owl:DatatypeProperty'
    rng=('rdfs:Resource' if kind=='owl:ObjectProperty' else
         'xsd:date' if local in DATE_FIELDS else 'xsd:decimal' if local in DECIMAL_FIELDS else
         'xsd:integer' if local in INTEGER_FIELDS else 'xsd:string')
    return f'{term} a {kind} ; rdfs:label "{local}"@en ; rdfs:range {rng} .\n'

def vocabulary(category,rows,fields):
    ns='elig'
    doc=PREFIXES+f'<{BASE}eligibility.ttl> a owl:Ontology ;\n'
    doc+=f'  rdfs:label "Event Ecosystem Lab {category} extension profile v0.1"@en ;\n'
    doc+=f'  rdfs:comment "Synthetic demonstration extension; EBWV, ePO, Peppol and UBL terms are independently governed."@en .\n\n'
    for name,label,cls,issuer,props,note in rows:
        if cls!='CompanyRegistration':
            doc+=f'{ns}:{cls} a owl:Class ; rdfs:label "{label}"@en'
            if category=='eligibility' and cls in ELIG_LINKS:
                doc+=f' ; rdfs:seeAlso {ELIG_LINKS[cls]}'
            doc+=' .\n'
        doc+=f'{ns}:{cls}Credential a owl:Class ; rdfs:label "{label} VC type"@en .\n'
        if cls=='CompanyRegistration':
            doc+=f'elig:CompanyRegistrationCredential rdfs:seeAlso <{EUCC_RULEBOOK}> .\n'
    doc+='\n'
    if category=='eligibility':
        doc+='elig:economicOperator a owl:ObjectProperty ; rdfs:range ebwv:EconomicOperator ; rdfs:label "economic operator"@en .\n'
        doc+='elig:appliesToLot a owl:ObjectProperty ; rdfs:range epo:Lot ; rdfs:label "applies to lot"@en .\n'
        doc+='elig:jointSignatureCount a owl:DatatypeProperty ; rdfs:domain ebwv:LegalRepresentative ; rdfs:range xsd:integer ; rdfs:label "joint signature count"@en ; rdfs:comment "Demo extension for the EUCC rulebook joint_two rule, which is more specific than ebwv:Jointly."@en .\n'
        doc+='elig:signatoryGroup a owl:ObjectProperty ; rdfs:domain ebwv:LegalRepresentative ; rdfs:range rdfs:Resource ; rdfs:label "signatory group"@en ; rdfs:comment "Identifies which representatives belong to the same joint-signature rule."@en .\n'
    for f in fields:
        if f=='elig:appliesToLot': continue
        doc+=property_owl(f)
    return doc

(OUT/'eligibility.ttl').write_text(vocabulary('eligibility',ELIG,ELIG_FIELDS) + "\n".join(["elig:AwardDecisionCredential a owl:Class .","elig:decisionID a owl:DatatypeProperty ; rdfs:range xsd:string .","elig:decisionFor a owl:ObjectProperty .","elig:decisionOutcome a owl:DatatypeProperty ; rdfs:range xsd:string ."]))
UBL_DOCUMENTS = ('Catalogue','Quotation','OrderResponse','Order','Invoice',
                 'DespatchAdvice','ReceiptAdvice','Waybill')
# busdoc exports components but not UBL document roots. Use UBL 2.4 schema
# namespaces for provenance, without asserting OWL equivalence to XML Schema.
trade_owl = PREFIXES + f'<{BASE}trade.ttl> a owl:Ontology ; rdfs:label "UBL 2.4 trade document profile"@en ; rdfs:seeAlso <https://iri.suomi.fi/model/busdoc/> .\n'
for cls in UBL_DOCUMENTS:
    trade_owl += (f'trade:{cls} a owl:Class ; rdfs:label "UBL {cls}"@en ; '
                  f'rdfs:seeAlso <https://docs.oasis-open.org/ubl/os-UBL-2.4/xsd/maindoc/UBL-{cls}-2.4.xsd> .\n'
                  f'trade:{cls}Credential a owl:Class .\n')
for cls in ('CatalogueLine','QuotationLine','OrderLine','OrderReference','LineItem','InvoiceLine','DespatchLine','ReceiptLine','ItemLocationQuantity','MonetaryTotal','DocumentReference','Item','Price','SupplierParty','CustomerParty','Party','Shipment'):
    trade_owl += f'busdoc:{cls} rdfs:isDefinedBy <https://iri.suomi.fi/model/busdoc/> .\n'
for prop in ('iD','issueDate','sellerSupplierParty','buyerCustomerParty','catalogueLine_','requiredItemLocationQuantity','orderLine_','lineItem_','invoiceLine_','orderDocumentReference_','orderReference_','despatchDocumentReference','documentCurrencyCode','legalMonetaryTotal','payableAmount','carrierParty','shipment_','item_','price_','name','quantity','invoicedQuantity','deliveredQuantity','receivedQuantity','priceAmount'):
    trade_owl += f'busdoc:{prop} rdfs:isDefinedBy <https://iri.suomi.fi/model/busdoc/> .\n'
# UBL elements missing from the incomplete busdoc export are declared locally.
for prop,domain,range_ in [('quotationLine','Quotation','busdoc:QuotationLine'),('despatchLine','DespatchAdvice','busdoc:DespatchLine'),('receiptLine','ReceiptAdvice','busdoc:ReceiptLine')]:
    trade_owl += f'trade:{prop} a owl:ObjectProperty ; rdfs:label "{prop}"@en ; rdfs:domain {"busdoc" if domain == "QuotationLine" else "trade"}:{domain} ; rdfs:range {range_} .\n'
trade_owl += 'trade:orderResponseCode a owl:DatatypeProperty ; rdfs:domain trade:OrderResponse ; rdfs:range xsd:string .\n'
(OUT/'trade.ttl').write_text(trade_owl)

def path_shape(prop):
    local=prop.split(':')[-1]
    constraints=('sh:nodeKind sh:IRI' if local in IRI_FIELDS else
                 'sh:datatype xsd:date' if local in DATE_FIELDS else
                 'sh:datatype xsd:decimal' if local in DECIMAL_FIELDS else
                 'sh:datatype xsd:integer' if local in INTEGER_FIELDS else
                 'sh:datatype xsd:string')
    if local in ('complianceStatus','registrationStatus','authorityStatus','licenceStatus'):
        constraints+=' ; sh:in ( "CLEAR" "ACTIVE" "NOT_CLEAR" "UNKNOWN" )' if local=='complianceStatus' else ' ; sh:in ( "ACTIVE" "INACTIVE" "UNKNOWN" )'
    if local=='responseCode': constraints+=' ; sh:in ( "ACCEPTED" "REJECTED" "CHANGED" )'
    return f'    sh:property [ sh:path {prop} ; sh:minCount 1 ; sh:maxCount 1 ; {constraints} ]'

SHAPES=PREFIXES+f'''# Validate the credentialSubject RDF node after JSON-LD expansion.
# These shapes do not check signatures, trust, legal eligibility or Peppol XML conformance.
< {BASE}shapes.ttl > a owl:Ontology ; rdfs:label "Synthetic VC subject shapes v0.1"@en .

elig:OperatorShape a sh:NodeShape ; sh:class ebwv:Company ;
    sh:property [ sh:path ebwv:legalName ; sh:minCount 1 ; sh:maxCount 1 ; sh:datatype xsd:string ] ;
    sh:property [ sh:path ebwv:legalIdentifier ; sh:minCount 1 ; sh:maxCount 1 ] .

# EUCC limited liability company profile (WE BUILD rb-eucc, sections 2 and 3.3).
# EUCC's legalRepresentativeId semantic reference is absent from current EBWV;
# no such EBWV term is invented here. Synthetic persons omit optional identifiers.
elig:EUCCAddressShape a sh:NodeShape ; sh:class ebwv:Address ;
    sh:property [ sh:path ebwv:fullAddress ; sh:minCount 1 ; sh:maxCount 1 ; sh:datatype xsd:string ] .

elig:EUCCRepresentativeShape a sh:NodeShape ; sh:class ebwv:LegalRepresentative ;
    sh:property [ sh:path ebwv:scopeOfAuthorization ; sh:minCount 1 ; sh:maxCount 1 ;
                  sh:nodeKind sh:IRI ; sh:in ( ebwv:Alone ebwv:Jointly ) ] ;
    sh:or ( [ sh:property [ sh:path ebwv:scopeOfAuthorization ; sh:hasValue ebwv:Alone ] ]
            [ sh:property [ sh:path ebwv:scopeOfAuthorization ; sh:hasValue ebwv:Jointly ] ;
              sh:property [ sh:path elig:jointSignatureCount ; sh:minCount 1 ;
                            sh:datatype xsd:integer ; sh:minInclusive 2 ] ;
              sh:property [ sh:path elig:signatoryGroup ; sh:minCount 1 ; sh:nodeKind sh:IRI ] ] ) ;
    sh:or ( [ sh:class ebwv:Person ;
              sh:property [ sh:path ebwv:fullName ; sh:minCount 1 ; sh:datatype xsd:string ] ;
              sh:property [ sh:path ebwv:dateOfBirth ; sh:minCount 1 ; sh:datatype xsd:date ] ]
            [ sh:class ebwv:EconomicOperator ;
              sh:property [ sh:path ebwv:legalName ; sh:minCount 1 ] ;
              sh:property [ sh:path ebwv:legalIdentifier ; sh:minCount 1 ] ;
              sh:property [ sh:path ebwv:legalForm ; sh:minCount 1 ] ] ) .

elig:CompanyRegistrationShape a sh:NodeShape ; sh:targetClass ebwv:LimitedLiabilityCompany ;
    sh:class ebwv:LimitedLiabilityCompany ;
    sh:property [ sh:path ebwv:legalName ; sh:minCount 1 ; sh:maxCount 1 ; sh:datatype xsd:string ] ;
    sh:property [ sh:path ebwv:legalIdentifier ; sh:minCount 1 ; sh:maxCount 1 ;
                  sh:datatype ebwv:Euid ; sh:pattern "^[A-Z]{{2}}-[A-Z0-9]+-[A-Z0-9-]+$" ] ;
    sh:property [ sh:path ebwv:legalForm ; sh:minCount 1 ; sh:datatype xsd:string ] ;
    sh:property [ sh:path ebwv:jurisdiction ; sh:minCount 1 ; sh:pattern "^[A-Z]{{2}}$" ] ;
    sh:property [ sh:path ebwv:registeredAddress ; sh:minCount 1 ; sh:node elig:EUCCAddressShape ] ;
    sh:property [ sh:path ebwv:dateOfRegistration ; sh:minCount 1 ; sh:datatype xsd:date ] ;
    sh:property [ sh:path ebwv:legalStatus ; sh:minCount 1 ; sh:datatype xsd:string ] ;
    sh:property [ sh:path ebwv:activity ; sh:minCount 1 ; sh:datatype ebwv:Nace21 ] ;
    sh:property [ sh:path ebwv:legalRepresentative ; sh:minCount 1 ; sh:node elig:EUCCRepresentativeShape ] .

'''.replace('< '+BASE+'shapes.ttl >','<'+BASE+'shapes.ttl>')
for name,label,cls,issuer,fields,note in ELIG:
    if name=='registration': continue
    paths=[p for p in fields if p!='elig:appliesToLot']
    SHAPES+=f'elig:{cls}Shape a sh:NodeShape ; sh:targetClass elig:{cls} ;\n'
    SHAPES+='    sh:property [ sh:path elig:economicOperator ; sh:minCount 1 ; sh:maxCount 1 ; sh:node elig:OperatorShape ] ;\n'
    SHAPES+='    sh:property [ sh:path elig:appliesToLot ; sh:minCount 1 ; sh:maxCount 1 ; sh:nodeKind sh:IRI ] ;\n'
    SHAPES+=' ;\n'.join(path_shape(p) for p in paths)+' .\n\n'
SHAPES += ('trade:DocumentShape a sh:NodeShape ; '
           'sh:property [ sh:path busdoc:iD ; sh:minCount 1 ; sh:datatype xsd:string ] ; '
           'sh:property [ sh:path busdoc:issueDate ; sh:minCount 1 ; sh:datatype xsd:date ] .\n'
           'trade:ItemShape a sh:NodeShape ; sh:class busdoc:Item ; '
           'sh:property [ sh:path busdoc:name ; sh:minCount 1 ; sh:datatype xsd:string ] .\n\n')
for name,label,cls,issuer,fields,note in TRADE:
    if name=='award':
        SHAPES += ('elig:AwardDecisionShape a sh:NodeShape ; sh:targetClass epo:AwardDecision ; '
                   'sh:property [ sh:path elig:decisionID ; sh:minCount 1 ] ; '
                   'sh:property [ sh:path epo:hasAwardDecisionDate ; sh:minCount 1 ; sh:datatype xsd:dateTime ] ; '
                   'sh:property [ sh:path elig:decisionFor ; sh:minCount 1 ; sh:nodeKind sh:IRI ] ; '
                   'sh:property [ sh:path elig:appliesToLot ; sh:minCount 1 ; sh:nodeKind sh:IRI ] ; '
                   'sh:property [ sh:path elig:decisionOutcome ; sh:hasValue "AWARDED" ] .\n\n')
        continue
    SHAPES+=f'trade:{cls}Shape a sh:NodeShape ; sh:targetClass trade:{cls} ; sh:node trade:DocumentShape'
    if name!='waybill':
        SHAPES+=' ; sh:property [ sh:path busdoc:sellerSupplierParty ; sh:minCount 1 ; sh:class busdoc:SupplierParty ]'
        SHAPES+=' ; sh:property [ sh:path busdoc:buyerCustomerParty ; sh:minCount 1 ; sh:class busdoc:CustomerParty ]'
    line_path={'catalogue':'busdoc:catalogueLine_','offer':'trade:quotationLine',
               'order':'busdoc:orderLine_','invoice':'busdoc:invoiceLine_',
               'despatch':'trade:despatchLine','receipt':'trade:receiptLine'}.get(name)
    if line_path:
        line_class={'catalogue':'CatalogueLine','offer':'QuotationLine','order':'OrderLine',
                    'invoice':'InvoiceLine','despatch':'DespatchLine','receipt':'ReceiptLine'}[name]
        SHAPES+=f' ; sh:property [ sh:path {line_path} ; sh:minCount 1 ; sh:class busdoc:{line_class}'
        if name=='catalogue':
            SHAPES+=' ; sh:property [ sh:path busdoc:item_ ; sh:minCount 1 ; sh:node trade:ItemShape ]'
            SHAPES+=' ; sh:property [ sh:path busdoc:requiredItemLocationQuantity ; sh:minCount 1 ; sh:class busdoc:ItemLocationQuantity ; sh:property [ sh:path busdoc:price_ ; sh:minCount 1 ; sh:class busdoc:Price ] ]'
        elif name=='offer':
            SHAPES+=' ; sh:property [ sh:path busdoc:lineItem_ ; sh:minCount 1 ; sh:class busdoc:LineItem ; sh:property [ sh:path busdoc:item_ ; sh:minCount 1 ; sh:node trade:ItemShape ] ; sh:property [ sh:path busdoc:quantity ; sh:minCount 1 ; sh:datatype xsd:decimal ] ]'
        elif name!='order':
            SHAPES+=' ; sh:property [ sh:path busdoc:item_ ; sh:minCount 1 ; sh:node trade:ItemShape ]'
            quantity_prop={'invoice':'busdoc:invoicedQuantity','despatch':'busdoc:deliveredQuantity','receipt':'busdoc:receivedQuantity'}.get(name)
            if quantity_prop:
                dtype='xsd:string' if name=='invoice' else 'xsd:decimal'
                SHAPES+=f' ; sh:property [ sh:path {quantity_prop} ; sh:minCount 1 ; sh:datatype {dtype} ]'
        else:
            SHAPES+=' ; sh:property [ sh:path busdoc:lineItem_ ; sh:minCount 1 ; sh:class busdoc:LineItem ]'
        SHAPES+=' ]'
    if name=='invoice': SHAPES+=' ; sh:property [ sh:path busdoc:legalMonetaryTotal ; sh:minCount 1 ; sh:class busdoc:MonetaryTotal ; sh:property [ sh:path busdoc:payableAmount ; sh:minCount 1 ; sh:datatype xsd:decimal ] ]'
    if name=='acceptance':
        SHAPES+=' ; sh:property [ sh:path busdoc:orderReference_ ; sh:minCount 1 ; sh:class busdoc:OrderReference ; sh:property [ sh:path busdoc:iD ; sh:minCount 1 ] ]'
        SHAPES+=' ; sh:property [ sh:path trade:orderResponseCode ; sh:hasValue "ACCEPTED" ]'
    if name=='waybill':
        SHAPES+=' ; sh:property [ sh:path busdoc:carrierParty ; sh:minCount 1 ]'
        SHAPES+=' ; sh:property [ sh:path busdoc:shipment_ ; sh:minCount 1 ; sh:class busdoc:Shipment ]'
    SHAPES+=' .\n\n'
(OUT/'shapes.ttl').write_text(SHAPES)
print(f'Generated {len(MANIFEST)} credentials and manifest')
