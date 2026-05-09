# Model Routing: customer-email-reply-agent

## Routing

Routine classification and sensitive-data detection use deterministic rules plus a low-cost model. Grounded draft writing uses the standard model with policy snippets. Legal, security, refund exception, privacy, policy conflict, or low confidence cases route to frontier review or human handoff.

## Fallback

If schema validation fails, repair once with the same model. If retrieval fails or confidence remains low, fail closed to handoff. Budget exceed events use reduced-context fallback and require human review.
