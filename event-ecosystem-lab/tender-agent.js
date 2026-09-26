/* Deterministic SME agent demonstration over a synthetic tender feed. */
(function(root){
  function assess(notice,profile){
    const checks=[
      {name:'Catalogue item',points:45,pass:notice.itemId===profile.itemId},
      {name:'Capacity',points:25,pass:notice.quantity<=profile.maxQuantity},
      {name:'Service region',points:15,pass:profile.supportedCountries.includes(notice.buyerCountry)},
      {name:'Submission window',points:15,pass:notice.deadline>notice.announcedOn}
    ];
    const score=checks.reduce((sum,c)=>sum+(c.pass?c.points:0),0);
    return {score,suitable:score>=80,checks};
  }
  function prepareDraft(notice,assessment,credentials){
    if(!assessment.suitable)throw Error('Notice below suitability threshold');
    const required=['registration','tax','social','financial','technical','licence','representation','catalogue'];
    const evidence=required.map(name=>({name,credentialId:credentials[name]?.id||null,available:!!credentials[name]}));
    return {status:'DRAFT_FOR_SUPPLIER_REVIEW',noticeId:notice.id,score:assessment.score,
      proposedItem:notice.itemId,quantity:notice.quantity,buyerCountry:notice.buyerCountry,
      evidence,missing:evidence.filter(x=>!x.available).map(x=>x.name),
      nextActions:['Supplier reviews opportunity and evidence disclosure','Confirm capacity, price and tender-specific conditions','Authorised supplier submits tender'],
      disclaimer:'Synthetic unsigned examples; issuer trust, authority, legal eligibility and tender submission are separate checks.'};
  }
  root.DemoTenderAgent={assess,prepareDraft};
  if(typeof module!=='undefined'&&module.exports)module.exports={assess,prepareDraft};
})(typeof window!=='undefined'?window:globalThis);
