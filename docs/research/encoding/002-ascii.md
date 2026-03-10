<!-- docs/research/encoding/002-ascii.md -->
# ASCII Encoding Rationale

Date: 2026-03-09
Status: Research complete
Author: Tracer

---

## Purpose

Why *.workflow.list uses printable ASCII only.

---

## Core Constraint

Allowed: 0x20-0x7E (space through tilde)
Excluded: Control characters, Unicode, extended ASCII

---

## Information Theory Perspective

### Entropy Minimization

Printable ASCII: 95 characters
Log2(95) ≈ 6.57 bits per character

Full Unicode: 1,114,112 code points
Log2(1,114,112) ≈ 20.09 bits per character

ASCII reduces encoding uncertainty by approximately 67 percent.

---

### Set Theory: Bounded Domain

Smaller domain = simpler validation.

ASCII domain: x where 0x20 <= x <= 0x7E

Validation: Single range check.

---

## Security Considerations

### Injection Attack Surface

Unicode vulnerabilities:
- Homoglyph attacks (Cyrillic vs Latin)
- Zero-width characters (invisible injection)
- Bidirectional override characters

ASCII advantage:
- No homoglyphs in printable range
- No zero-width characters
- No bidirectional text

---

### Parsing Ambiguity

Unicode normalization forms: NFC, NFD, NFKC, NFKD

Same visual character, different byte sequences.

ASCII: No normalization needed. Byte-equality = semantic-equality.

---

### Cross-Platform Consistency

Unicode pitfalls:
- Different default encodings
- Line ending variations
- Locale-specific collation

ASCII:
- Single encoding (UTF-8 compatible)
- Consistent across all platforms
- Locale-independent

---

## Encoding Compatibility

### Universal Decodability

ASCII property: Valid UTF-8, UTF-16, UTF-32, Latin-1, 7-bit ASCII.

Any system can read *.workflow.list without encoding detection.

---

### Transmission Safety

Safe channels:
- Email (SMTP 7-bit clean)
- URLs (no percent-encoding)
- JSON (no escape sequences)
- Shell arguments (minimal quoting)

---

## Readability Trade-offs

### What We Lose

- International language support
- Special symbols (arrows, boxes, math)
- Visual richness

### What We Gain

- Universal readability
- Parsing simplicity
- Security (reduced injection surface)
- Tooling compatibility

---

## Design Decision

DECISION: 2026-03-09 — Printable ASCII only.

WHY:
- Security over visual richness
- Compatibility over internationalization
- Simplicity over expressiveness

---

## Validation Rules

```
printable_ascii = 0x20-0x7E
workflow_char = printable_ascii | newline
workflow_file = { workflow_char }
```

---

## Open Questions

- Should we allow tab (0x09) for indentation?
- Should we allow carriage return (0x0D) for Windows?
- Legitimate Unicode use cases that outweigh risks?

---

REFERENCE: ../../design/security/005-layers.md — Security layers
REFERENCE: ../../design/overview/001-principles.md — Design principles

---

Last Updated: 2026-03-09
