# Reducing duplication — refactor patterns

## Decision tree

```
Duplicate block found
├─ Same logic, different data only?
│  └─ Parameterize → one function / map over config
├─ Same UI structure, different labels/handlers?
│  └─ Component + props, or render prop / children
├─ Same validation / parsing in API + client?
│  └─ Shared schema module (Zod, Pydantic, etc.)
├─ Same 3+ line expression repeated in one file?
│  └─ Local helper or const
├─ Copy across layers (controller ↔ service)?
│  └─ Move down stack: one source of truth in domain/service
└─ Similar but different business rules?
   └─ Do NOT merge — document why; optional thin adapter per caller
```

## Patterns by stack

| Situation | Action |
|-----------|--------|
| Repeated fetch + error handling | `async function withApiError(...)` or shared React Query hook |
| Repeated React `useEffect` blocks | Custom hook `useX()` |
| Repeated JSX blocks | Subcomponent; avoid mega-props — use composition |
| Repeated class methods | Base class or mixin only if stable; prefer composition |
| Repeated SQL / ORM queries | Repository function or DB view |
| Repeated constants / magic strings | `constants.ts` or enum |
| Repeated test setup | `beforeEach` helper or factory (`createUser()`) |

## Extract function checklist

1. Name describes **intent**, not mechanics (`parseInvoiceDate` not `handleStuff`).
2. Params = varying parts only; return value explicit.
3. Place file where **all callers** can import without circular deps.
4. Keep diff small: one extraction per cluster first.
5. Add or extend test that covered one copy; delete redundant tests if identical.

## Anti-patterns

- **Wrong abstraction:** forcing unrelated flows into one mega-function with many flags.
- **Premature shared package** for two call sites in one feature folder.
- **Deduplicating tests** until production code is actually shared.

## Measuring success

Re-run scanner with unchanged `--min-lines`. Good outcome:

- Cluster removed or line count below threshold.
- No new clusters from sloppy partial extraction (leftover half-duplicates).
