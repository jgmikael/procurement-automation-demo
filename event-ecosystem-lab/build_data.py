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
CONTEXT = ['https://www.w3.org/ns/credentials/v2', {
    'ebwv': 'https://w3id.org/ebwv#',
    'epo': 'http://data.europa.eu/a4g/ontology#',
    'elig': BASE + 'eligibility.ttl#',
    'trade': BASE + 'trade.ttl#',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
    'elig:asOf': {'@type': 'xsd:date'},
    'elig:periodStart': {'@type': 'xsd:date'},
    'elig:periodEnd': {'@type': 'xsd:date'},
    'trade:issueDate': {'@type': 'xsd:date'},
    'trade:deliveryDate': {'@type': 'xsd:date'},
    'trade:currency': {'@type': '@id'},
    'trade:precedes': {'@type': '@id'},
    'elig:appliesToLot': {'@type': '@id'},
    'trade:appliesToLot': {'@type': '@id'},
    'trade:sourceDocument': {'@type': '@id'},
    'trade:responseTo': {'@type': '@id'},
    'elig:annualTurnover': {'@type': 'xsd:decimal'},
    'elig:insuranceLimit': {'@type': 'xsd:decimal'},
    'elig:deliveredValue': {'@type': 'xsd:decimal'},
    'trade:unitPrice': {'@type': 'xsd:decimal'},
    'trade:payableAmount': {'@type': 'xsd:decimal'},
    'trade:quantity': {'@type': 'xsd:integer'},
    'trade:receivedQuantity': {'@type': 'xsd:integer'},
}]
LOT = 'urn:demo:procurement:lot-1'
CO = 'urn:demo:operator:aalto-timber'
BUYER = 'urn:demo:buyer:harbour-city'

ELIG = [
 ('registration','Company registration','CompanyRegistration', 'Finnish Trade Register', {'elig:registrationStatus':'ACTIVE','elig:asOf':'2026-09-26'}, 'Legal and professional standing; Art. 27(1)(a)'),
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
TRADE = [
 ('catalogue','Supplier catalogue','Catalogue','Peppol BIS Catalogue / UBL Catalogue',{'trade:documentNumber':'CAT-2026-001','trade:issueDate':'2026-09-22','trade:seller':CO,'trade:buyer':BUYER,'trade:itemName':'Modular birch desk','trade:quantity':'200','trade:unitPrice':'320.00','trade:currencyCode':'EUR'}, 'Supplier publishes catalogue entries'),
 ('offer','Supplier offer / quotation','Quotation','OASIS UBL Quotation; ePO Tender is procurement context',{'trade:documentNumber':'QUO-2026-011','trade:issueDate':'2026-09-26','trade:seller':CO,'trade:buyer':BUYER,'trade:itemName':'Modular birch desk','trade:quantity':'200','trade:unitPrice':'310.00','trade:currencyCode':'EUR','trade:appliesToLot':LOT,'trade:sourceDocument':BASE+'catalogue.vc.json'}, 'Commercial offer; procurement tender remains distinct'),
 ('award','Buyer award / offer acceptance','AwardDecision','ePO AwardDecision; procurement-specific decision',{'trade:documentNumber':'AWD-2026-012','trade:issueDate':'2026-10-08','trade:seller':CO,'trade:buyer':BUYER,'trade:responseCode':'ACCEPTED','trade:responseTo':BASE+'offer.vc.json','trade:appliesToLot':LOT}, 'Buyer accepts tender through a separate award decision; ePO semantics'),
 ('acceptance','Seller order acceptance','OrderAgreement','Peppol BIS Order Agreement / UBL OrderResponse',{'trade:documentNumber':'AGR-2026-012','trade:issueDate':'2026-10-10','trade:seller':CO,'trade:buyer':BUYER,'trade:responseCode':'ACCEPTED','trade:responseTo':BASE+'order.vc.json'}, 'Seller accepts buyer order; distinct from the award'),
 ('order','Purchase order','Order','Peppol BIS Ordering / UBL Order',{'trade:documentNumber':'ORD-2026-014','trade:issueDate':'2026-10-09','trade:seller':CO,'trade:buyer':BUYER,'trade:itemName':'Modular birch desk','trade:quantity':'200','trade:unitPrice':'310.00','trade:currencyCode':'EUR','trade:sourceDocument':BASE+'offer.vc.json'}, 'Buyer places order after separate award decision'),
 ('invoice','Supplier invoice','Invoice','Peppol BIS Billing / UBL Invoice',{'trade:documentNumber':'INV-2026-009','trade:issueDate':'2026-11-02','trade:seller':CO,'trade:buyer':BUYER,'trade:payableAmount':'62000.00','trade:currencyCode':'EUR','trade:sourceDocument':BASE+'order.vc.json'}, 'Supplier requests payment'),
 ('despatch','Despatch advice','DespatchAdvice','Peppol BIS Despatch Advice / UBL DespatchAdvice',{'trade:documentNumber':'DES-2026-027','trade:issueDate':'2026-10-25','trade:seller':CO,'trade:buyer':BUYER,'trade:itemName':'Modular birch desk','trade:quantity':'200','trade:sourceDocument':BASE+'order.vc.json'}, 'Supplier announces shipped goods'),
 ('receipt','Receipt advice','ReceiptAdvice','OASIS UBL ReceiptAdvice; no Peppol BIS claimed',{'trade:documentNumber':'REC-2026-028','trade:issueDate':'2026-10-29','trade:seller':CO,'trade:buyer':BUYER,'trade:receivedQuantity':'200','trade:sourceDocument':BASE+'despatch.vc.json'}, 'Buyer acknowledges receipt'),
 ('waybill','Waybill','Waybill','OASIS UBL Waybill; no Peppol BIS claimed',{'trade:documentNumber':'WAY-2026-030','trade:issueDate':'2026-10-25','trade:carrierName':'Baltic Demo Logistics','trade:trackingIdentifier':'BDL-003145','trade:deliveryDate':'2026-10-29','trade:sourceDocument':BASE+'despatch.vc.json'}, 'Carrier records transport movement'),
]

def credential(name, category, cls, issuer, fields):
    subject = {'id': f'urn:demo:{category}:{name}-2026', 'type': f'{"elig" if category == "eligibility" else "trade"}:{cls}'}
    if category == 'eligibility':
        subject.update({'elig:economicOperator':{'id':CO,'type':'ebwv:Company','ebwv:legalName':'Aalto Timber Services Oy','ebwv:legalIdentifier':'FI-3141592-6'},'elig:appliesToLot':LOT})
        if name == 'social': subject['type'] = ['ebwv:SocialSecurityContribution','elig:SocialSecurityCompliance']
    subject.update(fields)
    issuer_id=(BUYER if name in ('award','order','receipt') else
               'urn:demo:carrier:baltic-logistics' if name=='waybill' else
               CO if category=='trade' else f'urn:demo:issuer:{name}')
    start=fields.get('trade:issueDate') or fields.get('elig:asOf') or '2026-09-26'
    return {'@context':CONTEXT,'id':BASE+name+'.vc.json','type':['VerifiableCredential',f'{"elig" if category == "eligibility" else "trade"}:{cls}Credential'],
            'issuer':issuer_id,'validFrom':start+'T00:00:00Z',
            'credentialSubject':subject}

MANIFEST=[]
for category, rows in [('eligibility',ELIG),('trade',TRADE)]:
    for name,label,cls,issuer,fields,note in rows:
        vc=credential(name,category,cls,issuer,fields)
        (OUT/(name+'.vc.json')).write_text(json.dumps(vc,ensure_ascii=False,indent=2)+'\n')
        MANIFEST.append({'name':name,'label':label,'category':category,'class':cls,'basis':issuer,'note':note,'file':'data/'+name+'.vc.json'})
(OUT/'manifest.json').write_text(json.dumps(MANIFEST,ensure_ascii=False,indent=2)+'\n')

PREFIXES = '''@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ebwv: <https://w3id.org/ebwv#> .
@prefix epo: <http://data.europa.eu/a4g/ontology#> .
@prefix elig: '''+ '<'+BASE+'eligibility.ttl#> .\n'+'''@prefix trade: '''+ '<'+BASE+'trade.ttl#> .\n\n'
ELIG_LINKS = {
 'CompanyRegistration':'epo:SelectionCriterion','TaxCompliance':'epo:ExclusionGround',
 'SocialSecurityCompliance':'epo:ExclusionGround','InsolvencyStatus':'epo:ExclusionGround',
 'ExclusionCheck':'epo:ExclusionGround','FinancialCapacity':'epo:SelectionCriterion',
 'ProfessionalAuthorisation':'epo:SelectionCriterion','TechnicalCapacity':'epo:SelectionCriterion'}
TRADE_LINKS = {
 'Catalogue':'https://docs.peppol.eu/poacc/upgrade-3/syntax/Catalogue/',
 'Quotation':'https://docs.oasis-open.org/ubl/os-UBL-2.4/mod/summary/reports/UBL-Quotation-2.4.html',
 'AwardDecision':'http://data.europa.eu/a4g/ontology#AwardDecision',
 'OrderAgreement':'https://docs.peppol.eu/poacc/upgrade-3/profiles/42-orderagreement/',
 'Order':'https://docs.peppol.eu/poacc/upgrade-3/syntax/Order/',
 'Invoice':'https://docs.peppol.eu/poacc/upgrade-3/syntax/Invoice/',
 'DespatchAdvice':'https://docs.peppol.eu/poacc/upgrade-3/syntax/DespatchAdvice/',
 'ReceiptAdvice':'https://docs.oasis-open.org/ubl/os-UBL-2.4/mod/summary/reports/UBL-ReceiptAdvice-2.4.html',
 'Waybill':'https://docs.oasis-open.org/ubl/os-UBL-2.4/mod/summary/reports/UBL-Waybill-2.4.html'}
ELIG_FIELDS = sorted({k for _,_,_,_,fields,_ in ELIG for k in fields if k.startswith('elig:')})
TRADE_FIELDS = sorted({k for _,_,_,_,fields,_ in TRADE for k in fields})
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
    ns='elig' if category=='eligibility' else 'trade'
    doc=PREFIXES+f'<{BASE}{"eligibility" if ns=="elig" else "trade"}.ttl> a owl:Ontology ;\n'
    doc+=f'  rdfs:label "Event Ecosystem Lab {category} extension profile v0.1"@en ;\n'
    doc+=f'  rdfs:comment "Synthetic demonstration extension; EBWV, ePO, Peppol and UBL terms are independently governed."@en .\n\n'
    for name,label,cls,issuer,props,note in rows:
        doc+=f'{ns}:{cls} a owl:Class ; rdfs:label "{label}"@en'
        if category=='eligibility' and cls in ELIG_LINKS:
            doc+=f' ; rdfs:seeAlso {ELIG_LINKS[cls]}'
        if category=='trade': doc+=f' ; rdfs:seeAlso <{TRADE_LINKS[cls]}>'
        doc+=' .\n'
        doc+=f'{ns}:{cls}Credential a owl:Class ; rdfs:label "{label} VC type"@en .\n'
    doc+='\n'
    if category=='eligibility':
        doc+='elig:economicOperator a owl:ObjectProperty ; rdfs:range ebwv:EconomicOperator ; rdfs:label "economic operator"@en .\n'
        doc+='elig:appliesToLot a owl:ObjectProperty ; rdfs:range epo:Lot ; rdfs:label "applies to lot"@en .\n'
    for f in fields:
        if f=='elig:appliesToLot': continue
        doc+=property_owl(f)
    return doc

(OUT/'eligibility.ttl').write_text(vocabulary('eligibility',ELIG,ELIG_FIELDS))
(OUT/'trade.ttl').write_text(vocabulary('trade',TRADE,TRADE_FIELDS))

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

'''.replace('< '+BASE+'shapes.ttl >','<'+BASE+'shapes.ttl>')
for category,rows in [('eligibility',ELIG),('trade',TRADE)]:
    ns='elig' if category=='eligibility' else 'trade'
    for name,label,cls,issuer,fields,note in rows:
        paths=list(fields)
        if category=='eligibility': paths=[p for p in paths if p!='elig:appliesToLot']
        SHAPES+=f'{ns}:{cls}Shape a sh:NodeShape ; sh:targetClass {ns}:{cls} ;\n'
        if category=='eligibility':
            SHAPES+='    sh:property [ sh:path elig:economicOperator ; sh:minCount 1 ; sh:maxCount 1 ; sh:node elig:OperatorShape ] ;\n'
            SHAPES+='    sh:property [ sh:path elig:appliesToLot ; sh:minCount 1 ; sh:maxCount 1 ; sh:nodeKind sh:IRI ] ;\n'
        SHAPES+=' ;\n'.join(path_shape(p) for p in paths)+' .\n\n'
(OUT/'shapes.ttl').write_text(SHAPES)
print(f'Generated {len(MANIFEST)} credentials and manifest')
