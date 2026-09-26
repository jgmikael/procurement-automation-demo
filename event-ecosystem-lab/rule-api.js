/* Executable, deterministic Rule API examples. No HTTP service or VC signature verification. */
(function (root) {
  const definitions = {
    'credential-integrity': {label:'Issuer, status and freshness', version:'1.0', step:3},
    'representation': {label:'Mandate and permitted purpose', version:'1.0', step:4},
    'semantic-profile': {label:'Approved semantic mapping', version:'1.0', step:5},
    'tax-eligibility': {label:'Tax and social eligibility', version:'1.0', step:6},
    'invoice-reconciliation': {label:'Order, receipt and invoice', version:'1.0', step:11}
  };
  function evaluate(ruleId, input) {
    if (!definitions[ruleId]) throw new Error('Unknown rule: '+ruleId);
    const checks=[];
    const check=(name,pass,detail)=>checks.push({name,pass,detail});
    if(ruleId==='credential-integrity'){
      check('Trusted issuer',input.trustedIssuers.includes(input.issuer),`Issuer ${input.issuer} ${input.trustedIssuers.includes(input.issuer)?'is':'is not'} on the sample trust list.`);
      check('Credential status',input.credentialStatus==='active',`Synthetic status: ${input.credentialStatus}.`);
      check('Freshness',input.referenceDate<=input.validUntil,`Reference date ${input.referenceDate}; scenario valid until ${input.validUntil}.`);
    } else if(ruleId==='representation'){
      check('Mandate active',input.authorityStatus==='ACTIVE',`Authority status: ${input.authorityStatus}.`);
      check('Procedure in scope',input.scope.includes(input.procedure),`Mandate scope: ${input.scope}.`);
      check('Matching company',input.operatorId===input.expectedOperatorId,`Representative acts for ${input.operatorId}.`);
    } else if(ruleId==='semantic-profile'){
      check('Approved concept URI',input.mappedConcept===input.approvedConcept,`Mapped: ${input.mappedConcept||'none'}; required: ${input.approvedConcept}.`);
      check('Profile version',input.profileVersion==='0.1',`Profile version: ${input.profileVersion}.`);
    } else if(ruleId==='tax-eligibility'){
      check('Company identity',input.taxOperatorId===input.socialOperatorId,`Tax and social evidence concern ${input.taxOperatorId} and ${input.socialOperatorId}.`);
      check('Tax status CLEAR',input.taxStatus==='CLEAR',`Tax status: ${input.taxStatus}. UNKNOWN is not CLEAR.`);
      check('Social status CLEAR',input.socialStatus==='CLEAR',`Social status: ${input.socialStatus}.`);
      check('Reference date',input.taxAsOf===input.referenceDate,`Tax evidence as of ${input.taxAsOf}; required ${input.referenceDate}.`);
    } else {
      check('Order reference',input.invoiceOrderId===input.orderId,`Invoice references ${input.invoiceOrderId}; order ${input.orderId}.`);
      check('Same item',input.orderItemId===input.invoiceItemId,`Order item ${input.orderItemId}; invoice item ${input.invoiceItemId}.`);
      check('Quantity received',input.invoiceQuantity<=input.receivedQuantity,`Invoiced ${input.invoiceQuantity}; received ${input.receivedQuantity}.`);
      check('Unit price',input.invoiceUnitPrice===input.orderUnitPrice,`Invoice unit price ${input.invoiceUnitPrice}; order unit price ${input.orderUnitPrice}.`);
      check('Amount agrees',input.invoiceAmount===input.invoiceQuantity*input.invoiceUnitPrice,`Invoice ${input.invoiceAmount} ${input.currency}; line calculation ${input.invoiceQuantity*input.invoiceUnitPrice} ${input.currency}.`);
    }
    const decision=checks.every(x=>x.pass)?'PASS':ruleId==='tax-eligibility'&&input.taxStatus==='UNKNOWN'?'REVIEW':'FAIL';
    return {ruleId,version:definitions[ruleId].version,decision,checks};
  }
  root.DemoRules={definitions,evaluate};
  if(typeof module!=='undefined'&&module.exports)module.exports={definitions,evaluate};
})(typeof window!=='undefined'?window:globalThis);
