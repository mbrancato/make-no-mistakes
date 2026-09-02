---
id: security-configuration
title: Security, Configuration, and Secure Boundaries
summary: Safe configuration, secrets, encoding, and secure boundary design.
category: guidance
render: body
---

# Security, Configuration, and Secure Boundaries

Keep configuration explicit, validate it at startup where possible, and separate it from code.

- Never commit secrets.
- Never log secret values.
- Do not require production credentials for local development or tests.

At system boundaries:

- Validate untrusted input.
- Preserve useful diagnostic context without exposing credentials, tokens, or sensitive personal
  data.
- Keep sensitive values out of logs, test fixtures, examples, and generated documentation.

# Secure Boundaries

Keep untrusted data separate from executable structure. Prefer structured interfaces that preserve
that separation, and apply context-specific encoding at the boundary where data is consumed.

- Treat untrusted input as data, never as executable syntax or an untrusted structural fragment.
- Prefer parameterized queries, typed formatting APIs, argument-vector process execution,
  serializers, and auto-escaping templates over string interpolation.
- Use the encoder for the actual target context, such as HTML text, HTML attributes, JavaScript,
  CSS, URLs, SQL, LDAP, shell arguments, XML, or another interpreted format.
- Do not use generic escaping as a substitute for context-specific encoding.
- Validate structural values such as table names, column names, sort directions, command names, and
  protocol fields against an explicit allowlist.
- Avoid dynamic evaluation, string-built commands, query concatenation, and unsafe rendering sinks.
- Preserve the intended character encoding and avoid accidental double encoding or decode/re-encode
  confusion.

Test injection boundaries with delimiters, metacharacters, Unicode, and other values relevant to the
target context. Verify that untrusted values remain data and cannot change command, query, markup,
or protocol structure.
