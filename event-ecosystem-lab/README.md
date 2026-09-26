# Event Ecosystem Lab — procurement scenario

An interactive, self-contained browser simulation for coordinated life and business event services. The first scenario models a public procurement with a public buyer, a Finnish supplier, synthetic issuers, a business wallet, an electronic eligibility service and accountable human decision points.

## Open

Visit the [simulation](https://jgmikael.github.io/procurement-automation-demo/event-ecosystem-lab/) and the [data layer browser](https://jgmikael.github.io/procurement-automation-demo/event-ecosystem-lab/data-layer.html). GitHub Pages serves the static files. To use the browsers locally, serve this folder with a local HTTP server so JavaScript can fetch the JSON fixtures.

## Explore

- Advance through eight stages from event trigger to buyer review.
- Switch between agent-proposed orchestration and a fixed service portfolio.
- Switch the public buyer between Finland, Sweden and the Netherlands.
- Try expired evidence, a revoked mandate, an untrusted issuer, an unmapped concept and a `NO_INFORMATION` tax status. The run stops at the relevant gate.
- Inspect a W3C VC 2.0 JSON-LD tax attestation and export the simulated process trace as JSON.

## Data layer

`data/` contains 19 synthetic, unsigned W3C VC 2.0 examples: 10 eligibility attestations and 9 procurement, commercial and logistics documents. The company registration credential follows the [WE BUILD EUCC rulebook](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/blob/main/rulebooks/rb-eucc/README.md) limited liability company variant, with a synthetic EUID, registered address, NACE activity, legal representatives and an explicit joint signature group. The eligibility extension is grounded in the draft EBWV and ePO; a small OWL trade vocabulary records links to Peppol BIS and UBL source definitions. `data/shapes.ttl` contains 19 SHACL shapes for the credential subjects. The OWL and SHACL files describe the fixtures but do not establish signature validity, XML conformance or legal eligibility.

Regenerate the files with `python event-ecosystem-lab/build_data.py` from the repository root. Use `rdflib` and `pyshacl` to parse the Turtle and validate the JSON-LD credential subjects against `data/shapes.ttl`. The generator writes the manifest consumed by `data-layer.js`.

## Evidence boundaries

The browser uses synthetic values, fixed strings and deterministic JavaScript. It performs **no** LLM reasoning, cryptographic VC verification, live SHACL validation, registry query, business-wallet transaction or eligibility-service call. The `urn:demo:` instance identifiers are fictional; the EBWV and ePO vocabulary URIs are real, while `elig:` and `trade:` are published demo extensions. COM(2026) 590 and COM(2025) 838 are proposals. Agent orchestration and VC profiles are design choices for a pilot, not requirements already imposed by those proposals.

## Next implementation slices

1. Review EBWV / ePO alignments, issuer authority, controlled URIs and code lists with domain experts.
2. Replace mock issuers and wallet data with a sandbox, trust lists, status services and evidence protocol adapters.
3. Connect a rule service to machine-readable tender conditions and make the audit trace tamper evident.
4. Add a second event type using the same service catalogue and orchestration contract.

Sources are linked on the page, including the Commission's 9 September 2026 proposal and Digital Dubai's 2026 integrated-services and data-governance announcements.
