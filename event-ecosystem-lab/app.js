/* Deterministic, browser-only simulation. No real AI, registry, wallet, VC or SHACL engine. */
const $ = id => document.getElementById(id);
const STEPS = [
  {short:'Trigger', title:'An opportunity becomes an event', actor:'Procurement platform', basis:'Event + catalogue', description:'A public buyer needs 200 modular birch desks for a public facility. The event links buyer and supplier services.', heading:'Machine-readable opportunity', bullets:['Fictional buyer publishes the intent and target goods.','The supplier catalogue is an illustrative product input, not the public tender notice.','No agent is allowed to infer a legal procurement route on its own.'], agent:'Identify candidate services and suggest a plan. The service portfolio mode follows a fixed sequence.', control:'Buyer remains responsible for the published need and procedure.'},
  {short:'Requirements', title:'Approve structured requirements', actor:'Public buyer', basis:'COM(2026) 590 · scenario', description:'The buyer agent suggests evidence types and procedure-specific conditions for expert review.', heading:'Requirements proposed for the fictional tender', bullets:['Company registration and an authorised representative.','Tax and social contribution status as of the reference date.','Financial capability and professional qualification.','The buyer publishes only conditions a procurement expert has approved.'], agent:'Propose evidence profiles and flag missing or ambiguous conditions; cannot publish the call.', control:'Human gate: the buyer approves the conditions and publication.'},
  {short:'Discover', title:'The supplier agent finds the tender', actor:'Supplier', basis:'Scoped discovery', description:'A Finnish SME’s agent matches the opportunity against its declared capabilities.', heading:'Opportunity matched to company profile', bullets:['Synthetic Finnish supplier: Aalto Timber Services Oy.','Tender location and evidence requirements are read from the structured notice.','The agent suggests participation and lists required attestations.'], agent:'Search approved procurement feeds and recommend a match; cannot commit the business to bid.', control:'The supplier can decline participation or stop its agent.'},
  {short:'Evidence', title:'Assemble current evidence', actor:'Issuers + authentic sources', basis:'Issuer + status checks', description:'The issuer side supplies synthetic facts; the wallet holds evidence for selective presentation.', heading:'Three distinct responsibilities', bullets:['Authentic source supplies synthetic company and compliance facts.','Issuer applies a versioned profile and supplies a sample credential record.','Status, freshness and trusted issuer checks are separate from the meaning of a field.'], agent:'Coordinate permitted requests and explain a missing record; cannot invent facts or signatures.', control:'Issuer controls what it attests. A simulated failure stops progress here.'},
  {short:'Mandate', title:'Check who may act for the supplier', actor:'Supplier wallet', basis:'Mandate + purpose', description:'The wallet checks representation authority before anything is presented.', heading:'A narrow mandate for this procedure', bullets:['Person: Mira Example; organization: Aalto Timber Services Oy.','Scope: prepare and present eligibility evidence for this tender.','A revoked or insufficient mandate blocks the presentation.'], agent:'Prepare the minimum disclosure request; cannot bypass mandate or approve its own authority.', control:'Human gate: an authorised supplier representative approves disclosure.'},
  {short:'Present', title:'Present an agreed evidence profile', actor:'Wallet → eligibility service', basis:'URI + profile v0.1', description:'Fields are matched to governed identifiers and code lists, not labels in Finnish, Swedish or Dutch.', heading:'Semantic matching across borders', bullets:['National labels are mapped to a shared concept in an approved profile.','The profile fixes date, obligation, status code and required fields.','An unknown mapping is escalated; an LLM translation cannot silently approve equivalence.'], agent:'Find the applicable profile and explain discrepancies; cannot authorise a new semantic mapping.', control:'Human gate: the supplier submits its binding tender after reviewing the disclosure.'},
  {short:'Verify', title:'Run evidence and rule checks', actor:'Eligibility service + verifier', basis:'Deterministic rules', description:'Trust, profile validity and the buyer’s eligibility conditions are evaluated independently.', heading:'Evidence check, then procedure-specific decision support', bullets:['Illustrative checks: issuer trusted; status current; mandate valid; profile mapped.','Tax status is CLEAR as of the reference date. UNKNOWN is never treated as CLEAR.','The result includes an evidence trace and identifies exceptions for human review.'], agent:'Summarise verified results and exceptions. The demo uses fixed templates, no LLM.', control:'The procurement buyer retains responsibility for legal assessment.'},
  {short:'Decision', title:'The buyer reviews the outcome', actor:'Public buyer', basis:'Accountable decision', description:'The buyer receives the rule results and source trace; the award is never made by the agent.', heading:'A reviewable case file', bullets:['Eligibility evidence is separate from tender quality and price.','The buyer considers any legal and qualitative assessments.','A later status change can trigger a new evidence check when required.'], agent:'Prepare a concise case summary; cannot make or sign an award decision.', control:'Human gate: a responsible public buyer makes the consequential decision.'},
  {short:'Order', title:'The buyer places an order', actor:'Public buyer', basis:'UBL Order', description:'After the fictional award, the buyer orders the 200 modular desks.', heading:'From award to purchase order', bullets:['The award decision and purchase order have different legal and process roles.','The buyer references the agreed quotation and issues a sample UBL-based order credential.','An agent can prepare the order for the responsible buyer to review.'], agent:'Draft and reconcile the order against the award and quotation; cannot commit the buyer to an unapproved order.', control:'Buyer approves the synthetic order.'},
  {short:'Accept', title:'The supplier responds to the order', actor:'Supplier', basis:'UBL OrderResponse', description:'The supplier acknowledges the buyer’s order in a separate commercial response.', heading:'Seller response, not procurement award', bullets:['The order response identifies the buyer order.','The sample response code indicates acceptance of the order.','The buyer’s earlier award decision remains a separate procurement document.'], agent:'Check the order against capacity and prepare a response for supplier approval.', control:'Supplier approves the synthetic order response.'},
  {short:'Deliver', title:'Ship and acknowledge the goods', actor:'Supplier + carrier + buyer', basis:'UBL logistics documents', description:'The supplier dispatches the desks, the carrier records transport and the buyer acknowledges receipt.', heading:'A linked delivery chain', bullets:['Despatch advice tells the buyer what was sent.','Waybill records the carrier’s shipment.','Receipt advice records the buyer’s received quantity.'], agent:'Track document references and surface discrepancies; cannot invent proof of delivery.', control:'Each actor is responsible for its own logistics record.'},
  {short:'Invoice', title:'Invoice the received goods', actor:'Supplier', basis:'UBL Invoice', description:'The supplier issues the sample invoice referencing the buyer’s order.', heading:'Close the commercial document chain', bullets:['The invoice contains a monetary total and one sample item line.','The buyer can compare order, despatch, receipt and invoice.','Payment is outside this demo; no transaction is executed.'], agent:'Prepare a document comparison for finance review; cannot authorise payment.', control:'Supplier issues the synthetic invoice; the buyer retains payment controls.'}
];
// The values are manifest names. Each button opens the matching example in
// the data layer; a requested profile is not an issued document at that stage.
const STEP_DOCUMENTS = [
  [{name:'catalogue',role:'Input'}],
  [{name:'registration',role:'Requested profile'},{name:'tax',role:'Requested profile'},{name:'social',role:'Requested profile'},{name:'financial',role:'Requested profile'},{name:'licence',role:'Requested profile'}],
  [{name:'catalogue',role:'Input'},{name:'registration',role:'Company profile'},{name:'technical',role:'Capability'}],
  [{name:'registration',role:'Evidence'},{name:'tax',role:'Evidence'},{name:'social',role:'Evidence'},{name:'insolvency',role:'Evidence'},{name:'exclusion',role:'Evidence'},{name:'financial',role:'Evidence'},{name:'licence',role:'Evidence'},{name:'technical',role:'Evidence'},{name:'origin',role:'Evidence'}],
  [{name:'representation',role:'Authority'}],
  [{name:'offer',role:'Tender offer'},{name:'registration',role:'Disclosed evidence'},{name:'tax',role:'Disclosed evidence'},{name:'social',role:'Disclosed evidence'}],
  [{name:'tax',role:'Checked evidence'},{name:'social',role:'Checked evidence'},{name:'exclusion',role:'Checked evidence'},{name:'financial',role:'Checked evidence'},{name:'technical',role:'Checked evidence'}],
  [{name:'offer',role:'Reviewed tender'},{name:'award',role:'Buyer decision'}],
  [{name:'order',role:'Buyer document'}],
  [{name:'acceptance',role:'Supplier response'}],
  [{name:'despatch',role:'Supplier document'},{name:'waybill',role:'Carrier document'},{name:'receipt',role:'Buyer document'}],
  [{name:'invoice',role:'Supplier document'}]
];
const DOCUMENT_LABELS = Object.fromEntries([
  ['catalogue','Supplier catalogue'],['registration','EU Company Certificate'],['tax','Tax compliance'],['social','Social security contributions'],
  ['financial','Financial capacity'],['licence','Professional authorisation'],['technical','Technical capacity'],['insolvency','Insolvency status'],
  ['exclusion','Exclusion grounds check'],['origin','Operator origin'],['representation','Representative authority'],
  ['offer','Supplier offer / quotation'],['award','Buyer award decision'],['order','Purchase order'],
  ['acceptance','Seller order acceptance'],['despatch','Despatch advice'],['waybill','Waybill'],
  ['receipt','Receipt advice'],['invoice','Supplier invoice']
]);
const COUNTRIES = {
  FI:{name:'Finland',label:'verovelkatilanne',source:'Synthetic Finnish Tax Administration source',code:'FI: CLEAR',buyer:'Finnish municipality'},
  SE:{name:'Sweden',label:'skatteskuldstatus',source:'Synthetic Finnish issuer → Swedish buyer',code:'SE: CLEAR',buyer:'Swedish public buyer'},
  NL:{name:'Netherlands',label:'status belastingschuld',source:'Synthetic Finnish issuer → Dutch buyer',code:'NL: CLEAR',buyer:'Dutch public buyer'}
};
const FAULTS = {
  expired:{at:3,title:'Credential expired',detail:'The synthetic tax credential is past its validity date. Request a new issuance before presentation.'},
  untrusted:{at:3,title:'Issuer not trusted',detail:'The issuer is absent from the simulated trust list. A fresh record alone cannot fix this.'},
  revoked:{at:4,title:'Mandate revoked',detail:'The representative no longer has a valid authorisation for this procedure. Stop disclosure.'},
  unmapped:{at:5,title:'Semantic mapping missing',detail:'The national status field has no approved mapping to the shared profile. Escalate it to semantic governance.'},
  unknown:{at:6,title:'Status unknown',detail:'The source returned NO_INFORMATION. The eligibility rule must not convert that to CLEAR.'},
  invoiceMismatch:{at:11,title:'Invoice mismatch',detail:'The invoice total differs from the order and received goods; reconcile before closing the case.'}
};
const RULE_AT_STEP={3:'credential-integrity',4:'representation',5:'semantic-profile',6:'tax-eligibility',11:'invoice-reconciliation'};
const RULE_FILES={'credential-integrity':['tax'],'representation':['representation'],'semantic-profile':['tax'],'tax-eligibility':['tax','social'],'invoice-reconciliation':['order','receipt','invoice']};
let state={step:0,completed:false,trace:[],run:1,ruleResults:{}};
const currentCountry=()=>COUNTRIES[$('country').value];
const currentFault=()=>FAULTS[$('fault').value];
const mode=()=>document.querySelector('input[name="mode"]:checked').value;
const record=(owner,action,kind='ok')=>state.trace.push({seq:state.trace.length+1,owner,action,kind,step:state.step});
function reset(){state={step:0,completed:false,trace:[],run:state.run+1,ruleResults:{}};record('System',`New synthetic ${currentCountry().name} scenario · ${mode()==='adaptive'?'agent proposed plan':'defined service portfolio'}`);render();}
function resultStatus(key,step){let f=currentFault();if(f&&f.at===step&&((key==='Tax status'&&['expired','unknown','untrusted'].includes($('fault').value))||(key==='Mandate'&&$('fault').value==='revoked')||(key==='Profile mapping'&&$('fault').value==='unmapped')))return 'Issue';return step<=state.step?'Sample OK':'Pending';}
function render(){let n=state.step,s=STEPS[n],f=currentFault(),blocked=f&&f.at===n;
  $('run-number').textContent='#'+String(state.run).padStart(3,'0');$('step-title').textContent=s.title;$('step-description').textContent=s.description;
  $('actor-label').textContent=s.actor;$('basis-label').textContent=s.basis;
  $('stage-badge').textContent=state.completed?'RUN COMPLETE':blocked?'ACTION REQUIRED':n===0?'READY':n===7?'HUMAN REVIEW':'IN PROGRESS';$('stage-badge').classList.toggle('warning',!!blocked||n===7&&!state.completed);
  $('progress').innerHTML=STEPS.map((x,i)=>`<button class="step-tab ${i===n?'active':i<n?'done':''}" type="button" data-step="${i}" ${i>n?'disabled':''} aria-current="${i===n?'step':'false'}"><span class="step-n">${String(i+1).padStart(2,'0')}</span>${x.short}</button>`).join('');
  $('stage-detail').innerHTML=`<h4>${s.heading}</h4><ul>${s.bullets.map(b=>`<li>${b}</li>`).join('')}</ul>`;
  const links=$('step-document-links');links.replaceChildren();
  for(const {name,role} of STEP_DOCUMENTS[n]){
    const link=document.createElement('a');link.className='document-link';
    link.href=`./data-layer.html?doc=${encodeURIComponent(name)}#credentials`;
    link.target='_blank';link.rel='noopener';
    const kind=document.createElement('span');kind.className='document-role';kind.textContent=role;
    const label=document.createElement('strong');label.textContent=DOCUMENT_LABELS[name];
    const arrow=document.createElement('span');arrow.setAttribute('aria-hidden','true');arrow.textContent='↗';
    link.append(kind,label,arrow);links.append(link);
  }
  const ruleId=RULE_AT_STEP[n],run=state.ruleResults[n];
  $('rule-panel-title').textContent=ruleId?DemoRules.definitions[ruleId].label:'Rules are called at designated steps';
  $('rule-intro').textContent=ruleId?`POST /rules/v1/${ruleId}:evaluate · version 1.0 · simulated locally. Click to inspect the request and decision.`:'Continue to a step with a rule to execute and inspect its request and result.';
  $('run-rule').hidden=!ruleId;$('run-rule').disabled=false;
  $('rule-result').replaceChildren();
  if(run){const status=document.createElement('strong');status.className='rule-status '+run.response.decision.toLowerCase();status.textContent=run.response.decision;
    const checks=document.createElement('ul');for(const x of run.response.checks){const li=document.createElement('li');li.textContent=`${x.pass?'✓':'×'} ${x.name}: ${x.detail}`;checks.append(li)}
    const details=document.createElement('details');const summary=document.createElement('summary');summary.textContent='Inspect request and response JSON';const pre=document.createElement('pre');pre.textContent=JSON.stringify({request:run.request,response:run.response},null,2);details.append(summary,pre);
    $('rule-result').append(status,checks,details);
  } else if(ruleId){$('rule-result').textContent='Rule not run yet. The next transition waits for its result.';}
  $('issue-box').textContent=blocked?`${f.title}. ${f.detail} Select a healthy evidence chain or reset to run another case.`:'';
  $('advance').disabled=!!blocked||state.completed||!!ruleId&&run?.response.decision!=='PASS';$('advance').textContent=state.completed?'Completed ✓':n===7?'Record buyer decision →':n===STEPS.length-1?'Finish process →':n===1?'Buyer approves & continues →':n===4?'Approve disclosure →':n===5?'Submit tender →':'Run next step →';$('back').disabled=n===0;
  $('agent-text').textContent=mode()==='adaptive'?s.agent:`A predefined service portfolio fixes this task's position: ${s.short}. Conditions, authority and checks remain the same.`;$('control-text').textContent=s.control;
  $('evidence-list').innerHTML=[['Company identity',2],['Tax status',3],['Social contributions',3],['Mandate',4],['Profile mapping',5]].map(([key,at])=>{let v=resultStatus(key,at);return `<div class="evidence-item"><span>${key}</span><b class="${v==='Issue'?'bad':''}">${n>=at?v:'Pending'}</b></div>`}).join('');
  $('trace').innerHTML=state.trace.map(e=>`<li><time>T+${String(e.seq-1).padStart(2,'0')}</time><span><strong>${e.owner}</strong> · ${e.action}</span></li>`).join('');
  renderSemantics();
}
function advance(){let n=state.step,f=currentFault();if(state.completed||f&&f.at===n||RULE_AT_STEP[n]&&state.ruleResults[n]?.response.decision!=='PASS')return;
  if(n===STEPS.length-1){record('Supplier','Synthetic invoice recorded; simulation ended (no payment).','gate');state.completed=true;render();return;}
  const actions=['Event registered; scoped service catalogue loaded.','Procurement expert approved synthetic criteria.','Supplier agent suggested participation; supplier remained in control.','Synthetic records checked: source, issuer, status and profile are distinct.','Representative approved procedure-specific evidence disclosure.','Tender presentation authorised; labels aligned via the approved semantic profile.','Rule check returned an explained, procedure-specific result.','Public buyer recorded a synthetic award decision after human review.','Buyer recorded a synthetic purchase order.','Supplier recorded a synthetic order response.','Supplier, carrier and buyer recorded dispatch, waybill and receipt.'];
  record(STEPS[n].actor,actions[n],[1,4,5,7,8,9].includes(n)?'gate':'ok');state.step=n+1;
  let issue=currentFault();if(issue&&issue.at===state.step)record('Exception control',`${issue.title}: ${issue.detail}`,'issue');
  render();
}
async function runRule(){const step=state.step,ruleId=RULE_AT_STEP[step];if(!ruleId)return;
  const button=$('run-rule');button.disabled=true;$('rule-result').textContent='Loading sample credentials…';
  try{
    const documents=Object.fromEntries(await Promise.all(RULE_FILES[ruleId].map(async name=>{const response=await fetch(`./data/${name}.vc.json?v=7`);if(!response.ok)throw Error(`Could not load ${name}: ${response.status}`);return [name,await response.json()]})));
    const fault=$('fault').value,referenceDate='2026-09-26',tax=documents.tax?.credentialSubject;
    let input;
    if(ruleId==='credential-integrity')input={credentialId:documents.tax.id,issuer:documents.tax.issuer,trustedIssuers:fault==='untrusted'?[]:[documents.tax.issuer],credentialStatus:'active',referenceDate,validUntil:fault==='expired'?'2026-09-25':'2026-10-01'};
    else if(ruleId==='representation'){const mandate=documents.representation.credentialSubject;input={credentialId:documents.representation.id,authorityStatus:fault==='revoked'?'REVOKED':mandate['elig:authorityStatus'],scope:mandate['elig:scope'],procedure:'LOT-1',operatorId:mandate['elig:economicOperator'].id,expectedOperatorId:'urn:demo:operator:aalto-timber'};}
    else if(ruleId==='semantic-profile')input={credentialId:documents.tax.id,localLabel:currentCountry().label,mappedConcept:fault==='unmapped'?null:'https://jgmikael.github.io/procurement-automation-demo/event-ecosystem-lab/data/eligibility.ttl#complianceStatus',approvedConcept:'https://jgmikael.github.io/procurement-automation-demo/event-ecosystem-lab/data/eligibility.ttl#complianceStatus',profileVersion:'0.1'};
    else if(ruleId==='tax-eligibility')input={taxCredentialId:documents.tax.id,socialCredentialId:documents.social.id,taxOperatorId:tax['elig:economicOperator'].id,socialOperatorId:documents.social.credentialSubject['elig:economicOperator'].id,taxStatus:fault==='unknown'?'UNKNOWN':tax['elig:complianceStatus'],socialStatus:documents.social.credentialSubject['ebwv:complianceStatus'],taxAsOf:tax['elig:asOf'],referenceDate};
    else {const order=documents.order.credentialSubject,receipt=documents.receipt.credentialSubject,invoice=documents.invoice.credentialSubject;const orderLine=order['busdoc:orderLine_']['busdoc:lineItem_'],invoiceLine=invoice['busdoc:invoiceLine_'];input={orderCredentialId:documents.order.id,receiptCredentialId:documents.receipt.id,invoiceCredentialId:documents.invoice.id,orderId:order['busdoc:iD'],invoiceOrderId:invoice['busdoc:orderDocumentReference_']['busdoc:iD'],orderItemId:orderLine['busdoc:item_'].id,invoiceItemId:invoiceLine['busdoc:item_'].id,receivedQuantity:Number(receipt['trade:receiptLine']['busdoc:receivedQuantity']),invoiceQuantity:Number(invoiceLine['busdoc:invoicedQuantity']),orderUnitPrice:Number(orderLine['busdoc:price_']['busdoc:priceAmount']),invoiceUnitPrice:Number(invoiceLine['busdoc:price_']['busdoc:priceAmount']),invoiceAmount:Number(invoice['busdoc:legalMonetaryTotal']['busdoc:payableAmount'])+(fault==='invoiceMismatch'?100:0),currency:invoice['busdoc:documentCurrencyCode']};}
    const request={method:'POST',path:`/rules/v1/${ruleId}:evaluate`,ruleVersion:DemoRules.definitions[ruleId].version,inputs:input};
    const response=DemoRules.evaluate(ruleId,input);
    state.ruleResults[step]={request,response};record('Rule API',`${ruleId} v${response.version}: ${response.decision} · ${response.checks.filter(x=>x.pass).length}/${response.checks.length} checks passed`,response.decision==='PASS'?'ok':'issue');render();
  }catch(error){$('rule-result').textContent=`Rule not executed: ${error.message}`;button.disabled=false;}
}
$('run-rule').addEventListener('click',runRule);
let taxCredential=null;
fetch('./data/tax.vc.json?v=6').then(r=>r.ok?r.json():Promise.reject(Error(r.status))).then(vc=>{taxCredential=vc;renderSemantics()}).catch(()=>{});
function renderSemantics(){let c=currentCountry(),fault=$('fault').value,concept='https://jgmikael.github.io/procurement-automation-demo/event-ecosystem-lab/data/eligibility.ttl#complianceStatus',mapped=fault!=='unmapped',status=fault==='unknown'?'UNKNOWN':'CLEAR';
  $('mapping-demo').innerHTML=`<div class="mapping-row"><span>Local label</span><strong>${c.label} (${c.name})</strong></div><div class="mapping-row"><span>Common concept</span><strong><code>${mapped?concept:'UNMAPPED · expert review'}</code></strong></div><div class="mapping-row"><span>Value code</span><strong>${status}</strong></div><div class="mapping-row"><span>Profile</span><strong>elig:TaxComplianceShape · as of 2026-09-26</strong></div><div class="mapping-row"><span>Rule</span><strong>${mapped?'Tax status must be CLEAR on the specified date.':'No rule evaluation until the mapping is governed.'}</strong></div>`;
  if(taxCredential){const payload=JSON.parse(JSON.stringify(taxCredential));payload.credentialSubject['elig:complianceStatus']=status;$('json-preview').textContent=JSON.stringify(payload,null,2)}else $('json-preview').textContent='Loading W3C VC example…';
}
document.addEventListener('click',e=>{let tab=e.target.closest('[data-step]');if(tab){let n=Number(tab.dataset.step);if(n<=state.step){state.step=n;state.completed=false;record('Presenter',`Returned to ${STEPS[n].short} for inspection.`);render();}}});
$('advance').addEventListener('click',advance);$('back').addEventListener('click',()=>{if(state.step>0){state.step--;state.completed=false;record('Presenter',`Returned to ${STEPS[state.step].short} for inspection.`);render();}});
['country','fault'].forEach(id=>$(id).addEventListener('change',reset));document.querySelectorAll('input[name="mode"]').forEach(x=>x.addEventListener('change',reset));$('reset').addEventListener('click',reset);
$('download').addEventListener('click',()=>{let out={disclaimer:'Synthetic browser simulation; local rule examples, no live credentials or legal decision',country:$('country').value,mode:mode(),fault:$('fault').value,completed:state.completed,ruleCalls:state.ruleResults,entries:state.trace};let url=URL.createObjectURL(new Blob([JSON.stringify(out,null,2)],{type:'application/json'}));let a=document.createElement('a');a.href=url;a.download='event-ecosystem-trace.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
$('copy-json').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('json-preview').textContent);$('copy-json').textContent='Copied ✓';setTimeout(()=>$('copy-json').textContent='Copy JSON',1800)}catch{$('copy-json').textContent='Select text to copy';}});
state.run=0;reset();
