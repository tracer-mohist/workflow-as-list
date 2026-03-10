<!-- docs/research/theory/004-derivation.md -->
# Effective Context Square Root Formula: Derivation

Date: 2026-03-09
Status: Finalized
Authors: sha_dow, Tracer, DeepSeek

---

## Purpose

Mathematical derivation of k = √N from Six Degrees of Separation.

---

## Named Formula

Formal Name: Effective Context Square Root Formula

Formula:
```
TaskToken_range = [√(N × 0.618), √N]

Where:
  N = Context_max
  0.618 = Golden ratio
```

For 128k models:
- TaskToken_min = √(128,000 × 0.618) ≈ 281 tokens
- TaskToken_max = √128,000 ≈ 358 tokens
- Recommended range: 282-358 tokens

---

## Base Formula: Six Degrees of Separation

```
L = ln(N) / ln(k)
```

Original context (Milgram, 1967):
- N = Population size
- k = Average acquaintances per person
- L = Average separation degrees (famously ≈ 6)

Our adaptation:
- N = Context window size (tokens)
- k = Hub tokens needed (summary size)
- L = Inference steps from hub to any token

---

## Derivation History

### Phase 1: Initial Question

Question: How many tokens (k) cover N tokens?

Initial assumption (flawed): k = 2 (possibilities per token)

Result: L = log2(N) ≈ 16.97 (for N = 128,000)

Problem: Computes L, not k — wrong variable.

---

### Phase 2: Error Identification

Critical insight: Formula reversed mapping between L and k.

Error analysis:

| Aspect | Correct | Flawed |
|--------|---------|--------|
| Question | Solve for k | Solved for L |
| Given | L < 2 | Assumed k = 2 |
| Result | k = √N | L = log2(N) |

Why k = 2 is wrong:
- k = average degree (connections per node)
- k ≠ possibilities per token

---

### Phase 3: Correct Derivation

Constraint: L < 2 (two-step coverage)

```
L = ln(N) / ln(k)

Apply L < 2:
  ln(N) / ln(k) < 2

Multiply by ln(k):
  ln(N) < 2 · ln(k)

Logarithm identity:
  ln(N) < ln(k²)

Exponentiate:
  N < k²

Solve for k:
  k > √N

Boundary:
  k = √N
```

Result: k = √N (for N = 128,000: k ≈ 358 tokens)

---

### Phase 4: Golden Ratio Integration

Additional constraint: Effective context = N × 0.618

Rationale:
- 61.8% is golden ratio conjugate
- Safety margin before 80% performance cliff
- Accounts for transmission imprecision

Complete formula:
```
TaskToken_min = √(N × 0.618)
TaskToken_max = √N

Range: [√(N × 0.618), √N]
```

---

## Logical Structure

### Necessary Condition

For L < 2:
```
ln(N) / ln(k) < 2
k > √N

Therefore k > √N is necessary for two-step coverage
```

### Sufficient Condition

With k = √N:
```
L = ln(N) / ln(√N)
L = ln(N) / (0.5 · ln(N))
L = 2

Therefore k = √N is sufficient for exactly L = 2
```

---

## Physical Interpretation

### Network Structure

```
Hub Layer (k = √N tokens)
    /    |    \
Token groups (N/k tokens each)

Total: k × (N/k) = N tokens
Max path: Token → Hub → Token = 2 hops
```

### LLM Inference

```
Step 1: LLM reads hub tokens (282-358 tokens)
         ↓
Step 2: LLM infers any part of full context (128k tokens)

Inference distance: L = 2 steps
```

---

## Lessons Learned

### Question-Answer Alignment

Always verify: Solving for right variable?
- Question asks for k → Solve for k
- Don't fix k and solve for L

### Variable Interpretation

Always verify: What does variable mean?
- k = hub size, NOT possibilities per token
- L = inference distance, NOT information depth

### Constraint Identification

Always verify: What is given vs. to find?
- Given: L < 2
- Find: k

### Mathematical Intuition

Trust but verify: Intuition valuable, requires formal verification.

---

## Authorship

Contributors:
- sha_dow (Primary theorist): Initial question, error identification, golden ratio integration
- Tracer (Formal verifier): Mathematical derivation, error analysis
- DeepSeek (Collaborative validator): Derivation verification

---

REFERENCE: 003-limits.md — Application and enforcement
REFERENCE: ../../design/security/005-layers.md — Security application

---

Last Updated: 2026-03-09
