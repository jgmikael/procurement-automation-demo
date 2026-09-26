# Procurement data profile

Synthetic W3C VC 2.0 examples and OWL/SHACL demonstration profile. Browse the [visual data layer](../data-layer.html).

## EU Company Certificate

`registration.vc.json` follows the [WE BUILD EUCC rulebook](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/blob/main/rulebooks/rb-eucc/README.md), sections 2 and 3.3, for a Finnish limited liability company. It is synthetic and unsigned. The `credentialSubject` is the company itself (`ebwv:LimitedLiabilityCompany`). The example uses the draft EBWV properties `legalName`, `legalIdentifier` (synthetic EUID), `legalForm`, `jurisdiction`, `registeredAddress`, `dateOfRegistration`, `legalStatus`, `activity` (NACE Rev 2.1), and `legalRepresentative`. The address and two natural-person representatives are nested nodes. Both representatives have `ebwv:scopeOfAuthorization = ebwv:Jointly`; the local properties `elig:jointSignatureCount = 2` and `elig:signatoryGroup` make the `joint_two` rule unambiguous. The rulebook references `ebwv:legalRepresentativeId`, which is absent from the examined EBWV Turtle; this optional identifier is omitted, not invented.

The VC envelope contains `ebwv:attestationLegalCategory = ebwv:Pub-EAA`, a demo public-sector issuer with jurisdiction FI and `validUntil`. Its illustrative lifetime is below 24 hours; no fictional revocation endpoint or proof is supplied. It is not an issued EUCC or a claim that this pilot profile is the Commission's final EUCC definition. The EUCC is reusable evidence and has no procurement-lot field.

`eligibility.ttl` declares only demo extension terms. `shapes.ttl` checks the EUCC subject's required fields, typed EUID, nested address, representative cases and joint-rule details. It does not perform cryptographic or issuer-trust checks. Date-of-registration-before-issuance and country/EUID consistency are additional cross-envelope integrity checks for a production validator.
