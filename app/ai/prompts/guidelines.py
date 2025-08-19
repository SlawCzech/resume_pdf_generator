GUIDELINES_EXP_EDU = """
SCOPE (THIS CALL):
- Generate ONLY 'experiences' and 'education' per the schema.

METHOD:
- Start from USER_PROFILE. Keep roles/companies/dates exactly as provided; do not create new ones.
- Reorder experiences by relevance to JOB_POSTING, then by recency.
- Where typical responsibilities or outcomes are highly likely AND consistent with USER_PROFILE tech stack, add 0–2 inferred bullets per relevant role.
- Prefer qualitative phrasing ("improved reliability") over numeric claims unless the number exists in USER_PROFILE.
- Education: include only relevant items (highest degree first). Do not infer new degrees.

QUALITY GATES:
- Remove duplicates and buzzword padding.
- No markdown, no extra fields outside the schema.
"""


GUIDELINES_SKL_PROJ_CERT = """
SCOPE (THIS CALL):
- Generate ONLY 'skills', 'projects', and 'certificates' per schema.

METHOD:
- SKILLS:
  - Extract directly from USER_PROFILE.
  - Normalize names (case-insensitive, canonical).
  - Add category if obvious (e.g. backend, frontend, devops, data).
  - Add level if explicitly stated or implied (junior, advanced, expert).
  - Add at most 2 inferred skills per job requirement if strongly implied.

- PROJECTS:
  - Include max 3 most relevant projects for JOB_POSTING.
  - Rewrite description to be concise (<=20 words).
  - Add 1–3 highlights (impact bullets).
  - Keep tech list aligned with profile.
  - If job posting emphasizes a stack and a matching project exists, highlight it.
  - Do not invent new project names.

- CERTIFICATES:
  - Include only those present in USER_PROFILE.
  - Normalize issuer and year.
  - If a job requirement strongly references a certificate (e.g. AWS), and user has relevant training listed but not a named certificate, you MAY add inferred entry with inferred=true, confidence=low, evidence note.

QUALITY GATES:
- No duplicates, no hallucinations.
- No markdown.
- Plain strings only.
- If field not available → leave empty string/null, not invented.
"""


GUIDELINES_SUMMARY = """
TASK:
- Produce a concise professional summary tailored to the JOB_POSTING.
- If USER_PROFILE.summary exists, rewrite and tailor it.
- If USER_PROFILE.summary is null/empty, synthesize a new one using only facts from USER_PROFILE. 
- Do NOT add employers, dates, certificates, or metrics not present in USER_PROFILE.

CONTENT RULES:
- 2 sentences total, 60–100 words.
- Sentence 1: role/seniority, domain focus, core stack aligned to JOB_POSTING (use job keywords that the user actually has).
- Sentence 2: evidence-based impact (qualitative if no numbers), most relevant strengths, and 1–2 technologies or methods directly matching the posting.
- Prefer qualitative phrasing ("improved reliability") over numeric claims unless exact numbers exist in USER_PROFILE.

STYLE:
- ATS-friendly, plain strings, no markdown.
- Confident but factual; no buzzword stuffing.
"""
