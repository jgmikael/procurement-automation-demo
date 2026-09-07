# WE BUILD Attestation Examples

**W3C Verifiable Credentials with EBWV Vocabulary**

This collection showcases WE BUILD Large Scale Pilot attestation types implemented as W3C Verifiable Credentials using the European Business Wallet Vocabulary (EBWV) as the semantic foundation.

## Live Demo

**https://jgmikael.github.io/procurement-automation-demo/webuild-examples/**

## Overview

- **15+ Attestation Examples** - Complete W3C VC implementations
- **EBWV v0.1 Compliant** - All attributes mapped to official vocabulary
- **JSON-LD Contexts** - Semantic interoperability built-in
- **eIDAS 2.0 Ready** - Aligned with European Digital Identity framework

## Categories

### 🏢 Business Identity & Registration
- **EU Company Certificate (EUCC)** - Complete company registration (QEAA)
- **Company Information** - Extended company profile
- **Legal Entity Identifier (LEI)** - Global LEI
- **EBW Owner ID (EBWOID)** - Wallet owner identifier

### 👤 Representation & Authority
- **EU Power of Attorney** - Formal authorization
- **Authorised Signatories** - Signatory rules and limits
- **Ultimate Beneficial Owner (UBO)** - Ownership transparency

### 💰 Financial & Tax
- **VAT Identification** - Tax registration
- **Tax ID** - National tax number
- **Social Security Contribution** - Compliance verification

### 🌱 ESG & Compliance
- **ESG Certificate** - ISO certifications (9001, 14001, 45001, etc.)
- **Approved Supplier** - Vendor qualification

### 🏗️ Operational & Logistics
- **Site Information** - Facility data with GLN
- **Global Location Number (GLN)** - GS1 identifier

## Technical Details

### Standards Used

- **W3C Verifiable Credentials Data Model v2.0**
- **EBWV (European Business Wallet Vocabulary) v0.1**
- **eIDAS 2.0 Regulation (EU) 2024/1183**
- **JSON-LD for semantic interoperability**
- **SD-JWT VC for selective disclosure** (where applicable)

### EBWV Vocabulary

All examples use the official EBWV vocabulary:
- **Namespace:** `https://w3id.org/ebwv#`
- **Context:** `https://w3id.org/ebwv/v0.1`
- **Documentation:** https://w3id.org/ebwv/

### Example Structure

Each attestation example includes:
1. **Metadata** - Type, issuer, subject, validity
2. **Visual Overview** - Human-readable summary
3. **W3C VC JSON-LD** - Complete credential structure
4. **EBWV Mappings** - Vocabulary references
5. **References** - Links to rulebooks and standards

## Source Rulebooks

All examples are based on official WE BUILD attestation rulebooks:
- **Repository:** https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog
- **Total Rulebooks:** 38+
- **Framework:** WE BUILD Large Scale Pilot

## Usage

### View Online

Browse the examples at: https://jgmikael.github.io/procurement-automation-demo/webuild-examples/

### Local Development

```bash
# Clone the repository
git clone https://github.com/jgmikael/procurement-automation-demo.git

# Open the index
cd procurement-automation-demo/webuild-examples
open index.html  # or your browser
```

### Integration

Use these examples as:
- **Reference implementations** for wallet providers
- **Test data** for verifiers
- **Learning resources** for developers
- **Basis for procurement credentials**

## Key Features

### EBWV Compliance

All attributes map to official EBWV properties:
```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://w3id.org/ebwv/v0.1"
  ],
  "credentialSubject": {
    "@type": "ebwv:Company",
    "ebwv:legalName": "Company Name",
    "ebwv:legalIdentifier": { ... },
    "ebwv:registeredAddress": { ... }
  }
}
```

### eIDAS 2.0 Ready

Examples include:
- **QEAA** (Qualified Electronic Attestation of Attributes)
- **Pub-EAA** (Public Electronic Attestation of Attributes)
- **EAA** (Electronic Attestation of Attributes)

With proper metadata per Annex V/VII of eIDAS 2.0 Regulation.

### Selective Disclosure

Where applicable, examples support SD-JWT VC format for:
- **Privacy-preserving** attribute disclosure
- **Minimal disclosure** principle
- **User control** over shared data

## Procurement Use Cases

These attestations are particularly relevant for:

### Public Procurement
- **Company eligibility** (EUCC, LEI, VAT ID)
- **ESG criteria** (ESG certificates, ISO standards)
- **Financial stability** (Tax compliance, social security)
- **Authority verification** (Power of Attorney, signatories)

### Supplier Onboarding
- **KYC/KYS** (Know Your Supplier)
- **Compliance checks** (AML, sanctions, ownership)
- **Risk assessment** (ESG, certifications)

### Contract Execution
- **Representative authority** (Power of Attorney)
- **Payment details** (Bank accounts, tax IDs)
- **Site verification** (GLN, facility data)

## Contributing

Want to add more examples or improve existing ones?

1. Fork the repository
2. Create examples following the same structure
3. Ensure EBWV v0.1 compliance
4. Submit a pull request

## References

### Official Sources
- **WE BUILD Project:** https://www.webuildconsortium.eu/
- **EBWV Vocabulary:** https://w3id.org/ebwv/
- **WE BUILD Rulebooks:** https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog
- **eIDAS 2.0:** https://eur-lex.europa.eu/eli/reg/2024/1183/oj/eng

### Related Projects
- **Procurement Demo:** https://jgmikael.github.io/procurement-automation-demo/
- **EBWV Semantic Analysis:** https://jgmikael.github.io/ebwv-semantic-analysis/

## License

This project follows the same license as the WE BUILD rulebooks catalog (Apache 2.0).

## Acknowledgments

**WE BUILD Consortium** - Large Scale Pilot co-funded by the European Union

Contributors:
- Member State business registers (PRH, BRREG, KVK, Infogreffe, etc.)
- Certification bodies (Bureau Veritas, TÜV, DNV, etc.)
- Industry partners (SBB, Bosch, etc.)
- WP4 Semantics Group

---

*Generated examples for educational and demonstration purposes.*  
*Not for production use without proper validation and issuer authorization.*
