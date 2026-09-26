/* W3C VC/VP JSON-LD payloads with an illustrative OpenID4VP request payload.
   No Request Object signature, VC proof, VP proof, DID resolution or transport. */
(function(root){
  const base='https://jgmikael.github.io/procurement-automation-demo/event-ecosystem-lab/data/';
  const buyerDid='did:example:harbour-city-buyer';
  const walletDid='did:example:aalto-timber-ebw';
  const types={registration:'CompanyRegistration',tax:'TaxCompliance',social:'SocialSecurityCompliance',representation:'RepresentationAuthority'};
  function request(nonce,state){
    return {client_id:`decentralized_identifier:${buyerDid}`,response_type:'vp_token',response_mode:'direct_post',
      response_uri:'https://buyer.example.invalid/oid4vp/callback',nonce,state,
      dcql_query:{credentials:Object.entries(types).map(([id,type])=>({id,format:'ldp_vc',meta:{type_values:[[base+'eligibility.ttl#'+type+'Credential']]}}))},
      client_metadata:{vp_formats_supported:{ldp_vc:{proof_type_values:['DataIntegrityProof']}}}};
  }
  function response(requestPayload,credentials){
    const names=Object.keys(types);
    for(const name of names){if(!credentials[name]?.type?.includes('elig:'+types[name]+'Credential'))throw Error(`Missing matching ${name} VC`)}
    const presentation={'@context':['https://www.w3.org/ns/credentials/v2'],
      type:['VerifiablePresentation'],holder:walletDid,
      verifiableCredential:names.map(name=>credentials[name])};
    return {state:requestPayload.state,vp_token:presentation};
  }
  function inspect(requestPayload,responsePayload){
    if(!requestPayload||!responsePayload)return {structuralMatch:false,reason:'Missing request or presentation'};
    const vp=responsePayload.vp_token,credentialTypes=(vp?.verifiableCredential||[]).flatMap(vc=>vc.type||[]);
    const structuralMatch=responsePayload.state===requestPayload.state&&vp?.holder===walletDid&&
      vp?.type?.includes('VerifiablePresentation')&&Object.values(types).every(t=>credentialTypes.includes('elig:'+t+'Credential'));
    return {structuralMatch,credentialCount:vp?.verifiableCredential?.length||0,
      cryptographicVerification:'NOT_PERFORMED',
      reason:structuralMatch?'Response state, holder label and requested VC types match. Request signature, holder binding, nonce and issuer proofs remain unverified.':'Response state, holder or requested VC types do not match.'};
  }
  root.DemoWalletExchange={request,response,inspect,buyerDid,walletDid,types};
  if(typeof module!=='undefined'&&module.exports)module.exports={request,response,inspect,buyerDid,walletDid,types};
})(typeof window!=='undefined'?window:globalThis);
