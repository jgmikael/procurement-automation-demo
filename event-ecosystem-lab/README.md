# Event Ecosystem Lab — procurement scenario

An interactive, self-contained browser simulation for coordinated life and business event services. The first scenario models a public procurement with a public buyer, a Finnish supplier, synthetic issuers, a business wallet, an electronic eligibility service and accountable human decision points.

## Open

Visit `https://jgmikael.github.io/procurement-automation-demo/event-ecosystem-lab/` or open `index.html` locally. There are no build steps or backend dependencies. The optional font request falls back to system fonts offline.

## Explore

- Advance through eight stages from event trigger to buyer review.
- Switch between agent-proposed orchestration and a fixed service portfolio.
- Switch the public buyer between Finland, Sweden and the Netherlands.
- Try expired evidence, a revoked mandate, an untrusted issuer, an unmapped concept and a `NO_INFORMATION` tax status. The run stops at the relevant gate.
- Inspect illustrative JSON-LD and export the simulated process trace as JSON.

## Evidence boundaries

The demo uses synthetic values, fixed strings and deterministic JavaScript. It performs **no** actual LLM reasoning, cryptographic VC verification, SHACL validation, registry query, business-wallet transaction or eligibility-service call. Sample `urn:demo:` semantic identifiers are *illustrative*, not published EBWV terms. Proposed provisions of COM(2026) 590 and COM(2025) 838 are described as proposals. Agent orchestration, Rule APIs, EBWV-aligned profiles and end-to-end extensions are design proposals for a pilot, not requirements already imposed by those acts. The Dubai material is an architectural parallel, not a claim of semantic-stack equivalence.

## Next implementation slices

1. Version an actual EBWV / EU Core / ePO alignment and SHACL profiles, with reviewed URIs and code lists.
2. Replace mock issuers and wallet data with a sandbox, trust lists, status services and evidence protocol adapters.
3. Connect a rule service to machine-readable tender conditions and make the audit trace tamper evident.
4. Add a second event type using the same service catalogue and orchestration contract.

Sources are linked on the page, including the Commission's 9 September 2026 proposal and Digital Dubai's 2026 integrated-services and data-governance announcements.
