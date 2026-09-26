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

`data/` contains 19 synthetic, unsigned W3C VC 2.0 examples: 10 eligibility attestations and 1 ePO procurement award decision and 8 UBL trade and logistics documents. The company registration credential follows the [WE BUILD EUCC rulebook](https://github.com/webuild-consortium/webuild-attestation-rulebooks-catalog/blob/main/rulebooks/rb-eucc/README.md) limited liability company variant, with a synthetic EUID, registered address, NACE activity, legal representatives and an explicit joint signature group. The eligibility extension is grounded in the draft EBWV and ePO; a small OWL trade vocabulary defines UBL 2.4 document roots and reuses selected components from the Finnish busdoc Turtle export (which references UBL 2.2). `data/shapes.ttl` contains 19 SHACL shapes for the credential subjects. The OWL and SHACL files describe the fixtures but do not establish signature validity, XML conformance or legal eligibility.

Regenerate the files with `python event-ecosystem-lab/build_data.py` from the repository root. Use `rdflib` and `pyshacl` to parse the Turtle and validate the JSON-LD credential subjects against `data/shapes.ttl`. The generator writes the manifest consumed by `data-layer.js`.

The local extension no longer redefines `busdoc:lineItem_` or `busdoc:orderReference_`. The EUCC credential subject is an `ebwv:LimitedLiabilityCompany`, while the credential has its own EUCC type. The award uses ePO's `hasAwardDecisionDate` (`xsd:dateTime`).

## Executable Rule API examples

At the Evidence, Mandate, Present, Verify and Invoice steps, select **Run rule**. `rule-api.js` evaluates five versioned examples: issuer trust/freshness, authority and purpose, approved semantic mapping, tax/social eligibility, and order–receipt–invoice reconciliation. Each button displays an illustrative `POST /rules/v1/{ruleId}:evaluate` request, a PASS/FAIL/REVIEW response and individual reasons. The next transition waits for PASS. Select a fault to see a failed or indeterminate decision, then download the trace to inspect all executed calls. The inputs come from the linked sample credentials with explicit scenario overrides (trust-list membership, validity date, revocation, mapping, unknown status or invoice mismatch). The route is an **API contract illustration** evaluated locally in JavaScript; there is no HTTP endpoint or cryptographic verifier.

## SME tender discovery agent

At the Discover step, click **Start tender watcher**. A synthetic tender announcement arrives after the watcher starts. `tender-agent.js` scores the notice against the supplier's catalogue item, capacity, service region and submission window, then autonomously fetches eight linked sample documents and prepares an inspectable bid draft. The trace includes each agent action. Supplier review remains required for capacity, pricing, disclosure and submission. The sources are a **synthetic event feed**, not live tender portals; the rule-based scorer is not an LLM and the collected VCs remain unsigned.

## DID presentation request and W3C VP

At Mandate, the buyer constructs an illustrative OpenID4VP Authorization Request payload. Its `client_id` uses the `decentralized_identifier:` prefix with the buyer's fictional DID; `dcql_query` asks for the registration, tax, social-contribution and representation W3C VCs in `ldp_vc` format. At Present, the supplier approves the disclosure and the EBW builds a W3C VC Data Model 2.0 `VerifiablePresentation` embedding those four credential examples. Verify displays a structural match and the rule result. The same fixed example is available as `data/presentation-request.json` and `data/wallet-presentation.vp.json`.

The dynamic request uses a fresh random nonce and state. A real OpenID4VP request using a DID client identifier **must be signed** using a key associated with the DID. A real holder presentation needs a cryptographic proof binding its challenge to that nonce and its domain to the verifier's client identifier. The demonstration has neither signing keys nor a live response URI; its static fixtures have deliberately fixed demo nonce/state values. The sample VCs and VP have no proofs. Structural matching here never means cryptographic or legal verification. No alternative credential format is used.

## Evidence boundaries

The 12-step browser simulation links each process stage to its relevant W3C VC example in the data layer, from catalogue and eligibility evidence through award, order, delivery and invoice. Each linked VC is a synthetic, unsigned sample; requested profiles at the requirements stage are examples rather than already-issued credentials. The browser uses synthetic values, fixed strings and deterministic JavaScript. It performs **no** LLM reasoning, cryptographic VC verification, live SHACL validation, registry query, business-wallet transaction or eligibility-service call. The `urn:demo:` instance identifiers are fictional; the EBWV, ePO and busdoc vocabulary URIs are real, while `elig:` and `trade:` are published demo extensions. COM(2026) 590 and COM(2025) 838 are proposals. Agent orchestration and VC profiles are design choices for a pilot, not requirements already imposed by those proposals.

## Next implementation slices

1. Review EBWV / ePO alignments, issuer authority, controlled URIs and code lists with domain experts.
2. Replace mock issuers and wallet data with a sandbox, trust lists, status services and evidence protocol adapters.
3. Connect a rule service to machine-readable tender conditions and make the audit trace tamper evident.
4. Add a second event type using the same service catalogue and orchestration contract.

Sources are linked on the page, including the Commission's 9 September 2026 proposal and Digital Dubai's 2026 integrated-services and data-governance announcements.

The generated VCs use compact, per-credential JSON-LD contexts; unused semantic prefixes and coercions are omitted while keeping the W3C base context and issuer, type, subject, identifier and validity metadata.
