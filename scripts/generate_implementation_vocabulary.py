#!/usr/bin/env python3
"""Generate Implementation / Review vocabulary markdown files (124 entries)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from implementation_vocabulary_user_data import USER_ENTRIES

ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = ROOT / "docs" / "vocabulary"
SCENE = "Implementation / Review"
START_ID = 115

DIFFICULTY_ORDER = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}

METADATA: dict[str, dict] = {
    "introduce a new API": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02cc\u026antr\u0259\u02c8dju\u02d0s \u0259 nju\u02d0 \u02cce\u026a pi\u02d0 \u02c8a\u026a/",
        "meaning": "to add a new API",
        "description": "Add a new API endpoint or contract in a PR or design note.",
        "difficulty": "Intermediate"
    },
    "enable seamless transitions": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u026a\u02c8ne\u026abl \u02c8si\u02d0ml\u0259s tr\u00e6n\u02c8z\u026a\u0283nz/",
        "meaning": "to allow smooth transitions",
        "description": "Allow users or data to move between apps or states without friction.",
        "difficulty": "Intermediate"
    },
    "leverage A for persistence": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02c8lev\u0259r\u026ad\u0292 f\u0254\u02d0 p\u0259\u02c8s\u026ast\u0259ns/",
        "meaning": "to use A for storing data",
        "description": "Use a component or store to persist state in implementation reviews.",
        "difficulty": "Intermediate"
    },
    "include robust error handling": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u026an\u02c8klu\u02d0d r\u0259\u028a\u02c8b\u028cst \u02c8er\u0259 \u02c8h\u00e6ndl\u026a\u014b/",
        "meaning": "to include strong error handling",
        "description": "Handle malformed or unexpected upstream responses safely in code.",
        "difficulty": "Intermediate"
    },
    "implement an endpoint": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02c8\u026ampl\u026ament \u0259n \u02c8endp\u0254\u026ant/",
        "meaning": "to build an API endpoint",
        "description": "Describe adding a concrete HTTP endpoint in a pull request.",
        "difficulty": "Beginner"
    },
    "support two estimate types": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/s\u0259\u02c8p\u0254\u02d0t tu\u02d0 \u02c8est\u026am\u0259t ta\u026aps/",
        "meaning": "to support two calculation modes",
        "description": "Explain that an endpoint handles two calculation modes via a parameter.",
        "difficulty": "Intermediate"
    },
    "refactor A to simplify and standardize B": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ri\u02d0\u02c8f\u00e6kt\u0259 tu\u02d0 \u02c8s\u026ampl\u026afa\u026a \u00e6nd \u02c8st\u00e6nd\u0259da\u026az/",
        "meaning": "to refactor A to simplify B",
        "description": "Restructure code so setup or logic is simpler and more consistent.",
        "difficulty": "Intermediate"
    },
    "reduce duplication and improve readability": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/r\u026a\u02c8dju\u02d0s \u02ccdju\u02d0pl\u026a\u02c8ke\u026a\u0283n \u00e6nd \u026am\u02c8pru\u02d0v \u02ccri\u02d0d\u0259\u02c8b\u026al\u0259ti/",
        "meaning": "to cut duplication and improve clarity",
        "description": "Use shared helpers to remove repeated code and clarify tests.",
        "difficulty": "Intermediate"
    },
    "streamline the internal data structures": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02c8stri\u02d0mla\u026an \u00f0i \u026an\u02c8t\u025c\u02d0nl \u02c8de\u026at\u0259 \u02c8str\u028ckt\u0283\u0259z/",
        "meaning": "to simplify internal data structures",
        "description": "Remove wrappers or fields so internal models are leaner.",
        "difficulty": "Intermediate"
    },
    "eliminate an unused field": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u026a\u02c8l\u026am\u026ane\u026at \u0259n \u028cn\u02c8ju\u02d0zd fi\u02d0ld/",
        "meaning": "to remove an unused field",
        "description": "Drop a field no longer needed from responses or models.",
        "difficulty": "Intermediate"
    },
    "remove references throughout the codebase": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/r\u026a\u02c8mu\u02d0v \u02c8refr\u0259ns\u026az \u03b8ru\u02d0\u02c8a\u028at \u00f0\u0259 \u02c8k\u0259\u028adbe\u026as/",
        "meaning": "to delete references across the codebase",
        "description": "Delete all usages of a deprecated flag or symbol repo-wide.",
        "difficulty": "Intermediate"
    },
    "match the response schema": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/m\u00e6t\u0283 \u00f0\u0259 r\u026a\u02c8sp\u0252ns \u02c8ski\u02d0m\u0259/",
        "meaning": "to align with the response schema",
        "description": "Update mapping so runtime output matches the defined schema.",
        "difficulty": "Intermediate"
    },
    "reflect the new response shape": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/r\u026a\u02c8flekt \u00f0\u0259 nju\u02d0 r\u026a\u02c8sp\u0252ns \u0283e\u026ap/",
        "meaning": "to show the new response structure",
        "description": "Update docs or code to match the new response structure.",
        "difficulty": "Intermediate"
    },
    "align the implementation with the API contract": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u0259\u02c8la\u026an \u00f0i \u02cc\u026ampl\u026amen\u02c8te\u026a\u0283n w\u026a\u00f0 \u00f0i \u02cce\u026a pi\u02d0 \u02c8a\u026a \u02c8k\u0252ntr\u00e6kt/",
        "meaning": "to match the published API contract",
        "description": "Close gaps between published API specs and running code.",
        "difficulty": "Intermediate"
    },
    "resolve a schema mismatch": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/r\u026a\u02c8z\u0252lv \u0259 \u02c8ski\u02d0m\u0259 \u02c8m\u026asm\u00e6t\u0283/",
        "meaning": "to fix a schema mismatch",
        "description": "Fix differences between generated code, types, and runtime models.",
        "difficulty": "Intermediate"
    },
    "have a mismatch between A and B": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/h\u00e6v \u0259 \u02c8m\u026asm\u00e6t\u0283 b\u026a\u02c8twi\u02d0n/",
        "meaning": "to have a mismatch between two things",
        "description": "Describe inconsistency between a spec and a runtime model.",
        "difficulty": "Intermediate"
    },
    "avoid A being interpreted as B": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u0259\u02c8v\u0254\u026ad \u02c8bi\u02d0\u026a\u014b \u026an\u02c8t\u025c\u02d0pr\u026at\u026ad \u00e6z/",
        "meaning": "to prevent A from being read as B",
        "description": "Rename or restructure code so tools do not misread intent.",
        "difficulty": "Advanced"
    },
    "cause A to appear incorrectly": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/k\u0254\u02d0z tu\u02d0 \u0259\u02c8p\u026a\u0259 \u02cc\u026ank\u0259\u02c8rektli/",
        "meaning": "to make A show up incorrectly",
        "description": "Explain a misconfiguration that made a property display wrongly.",
        "difficulty": "Intermediate"
    },
    "correctly expose the allowed values": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/k\u0259\u02c8rektli \u026ak\u02c8sp\u0259\u028az \u00f0i \u0259\u02c8la\u028ad \u02c8v\u00e6lju\u02d0z/",
        "meaning": "to show allowed values correctly",
        "description": "Ensure enums or constraints appear correctly in generated schemas.",
        "difficulty": "Intermediate"
    },
    "introduce a breaking response contract change": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02cc\u026antr\u0259\u02c8dju\u02d0s \u0259 \u02c8bre\u026ak\u026a\u014b r\u026a\u02c8sp\u0252ns \u02c8k\u0252ntr\u00e6kt t\u0283e\u026and\u0292/",
        "meaning": "to make a breaking response change",
        "description": "Flag a response change that breaks existing client expectations.",
        "difficulty": "Intermediate"
    },
    "be backward-compatible": {
        "type": "phrase",
        "partOfSpeech": "adjective phrase",
        "pronunciation": "/bi \u02ccb\u00e6kw\u0259d k\u0259m\u02c8p\u00e6t\u0259bl/",
        "meaning": "to remain compatible with older clients",
        "description": "State that existing clients can keep working after a change.",
        "difficulty": "Intermediate"
    },
    "support both the new and old formats": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/s\u0259\u02c8p\u0254\u02d0t b\u0259\u028a\u03b8 \u00f0\u0259 nju\u02d0 \u00e6nd \u0259\u028ald \u02c8f\u0254\u02d0m\u00e6ts/",
        "meaning": "to accept new and old formats",
        "description": "Keep both payload formats during a migration period.",
        "difficulty": "Intermediate"
    },
    "remove the deprecated fields": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/r\u026a\u02c8mu\u02d0v \u00f0\u0259 d\u026a\u02c8preke\u026at\u026ad fi\u02d0ldz/",
        "meaning": "to delete deprecated fields",
        "description": "Plan cleanup of deprecated fields after clients migrate.",
        "difficulty": "Intermediate"
    },
    "be carried out in the following steps": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/bi \u02c8k\u00e6rid a\u028at \u026an \u00f0\u0259 \u02c8f\u0252l\u0259\u028a\u026a\u014b steps/",
        "meaning": "to be done in listed steps",
        "description": "Outline a staged rollout across services or environments.",
        "difficulty": "Intermediate"
    },
    "be followed by the client release": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/bi \u02c8f\u0252l\u0259\u028ad ba\u026a \u00f0\u0259 \u02c8kla\u026a\u0259nt r\u026a\u02c8li\u02d0s/",
        "meaning": "to come before the client release",
        "description": "State release order when backend must ship before frontend.",
        "difficulty": "Intermediate"
    },
    "add A back if B does not cover it": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u00e6d b\u00e6k \u026af d\u028cz n\u0252t \u02c8k\u028cv\u0259/",
        "meaning": "to restore A if B is insufficient",
        "description": "Plan to restore a field if a new model misses a case.",
        "difficulty": "Intermediate"
    },
    "following a suggestion": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/\u02c8f\u0252l\u0259\u028a\u026a\u014b \u0259 s\u0259\u02c8d\u0292est\u0283n/",
        "meaning": "after receiving a suggestion",
        "description": "Note that a review suggestion drove a code change.",
        "difficulty": "Beginner"
    },
    "it was pointed out that": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/\u026at w\u0252z \u02c8p\u0254\u026ant\u026ad a\u028at \u00f0\u00e6t/",
        "meaning": "someone noted that",
        "description": "Record feedback received during review or discussion.",
        "difficulty": "Beginner"
    },
    "rename A for better clarity": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ri\u02d0\u02c8ne\u026am f\u0254\u02d0 \u02c8bet\u0259 \u02c8kl\u00e6r\u0259ti/",
        "meaning": "to rename A for clarity",
        "description": "Rename a symbol so its purpose is clearer to reviewers.",
        "difficulty": "Beginner"
    },
    "migrate away from A": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ma\u026a\u02c8\u0261re\u026at \u0259\u02c8we\u026a fr\u0252m/",
        "meaning": "to move off A gradually",
        "description": "Describe moving off an old integration or library.",
        "difficulty": "Intermediate"
    },
    "instead of relying on a A": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/\u026an\u02c8sted \u0252v r\u026a\u02c8la\u026a\u026a\u014b \u0252n/",
        "meaning": "rather than depending on A",
        "description": "Explain an architecture change away from a dependency.",
        "difficulty": "Intermediate"
    },
    "have more control": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/h\u00e6v m\u0254\u02d0 k\u0259n\u02c8tr\u0259\u028al/",
        "meaning": "to gain finer control",
        "description": "Justify direct calls to control retries, timeouts, or behavior.",
        "difficulty": "Beginner"
    },
    "handle non-JSON responses properly": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02c8h\u00e6ndl n\u0252n \u02c8d\u0292e\u026as\u0252n r\u026a\u02c8sp\u0252ns\u026az \u02c8pr\u0252p\u0259li/",
        "meaning": "to handle non-JSON responses correctly",
        "description": "Handle unexpected upstream response formats without crashing.",
        "difficulty": "Intermediate"
    },
    "cannot migrate everything at once": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02c8k\u00e6n\u0252t ma\u026a\u02c8\u0261re\u026at \u02c8evri\u03b8\u026a\u014b \u00e6t w\u028cns/",
        "meaning": "cannot migrate all at once",
        "description": "Explain why both formats must coexist during migration.",
        "difficulty": "Intermediate"
    },
    "improvement might be limited unless": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/\u026am\u02c8pru\u02d0vm\u0259nt ma\u026at bi\u02d0 \u02c8l\u026am\u026at\u026ad \u028cn\u02c8les/",
        "meaning": "gains may be small unless",
        "description": "Point out that local optimization needs broader changes too.",
        "difficulty": "Advanced"
    },
    "be a laborious task": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/bi \u0259 l\u0259\u02c8b\u0254\u02d0ri\u0259s t\u0251\u02d0sk/",
        "meaning": "to be very time-consuming work",
        "description": "Argue for scoping down work that would touch every call site.",
        "difficulty": "Advanced"
    },
    "put a task on hold": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/p\u028at \u0259 t\u0251\u02d0sk \u0252n h\u0259\u028ald/",
        "meaning": "to pause a task",
        "description": "Defer cleanup until another dependency finishes.",
        "difficulty": "Beginner"
    },
    "plan to migrate to": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/pl\u00e6n tu\u02d0 ma\u026a\u02c8\u0261re\u026at tu\u02d0/",
        "meaning": "to intend to move to",
        "description": "State a future migration target or schedule.",
        "difficulty": "Intermediate"
    },
    "add A temporarily": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u00e6d \u02c8temp\u0259r\u0259rili/",
        "meaning": "to add A for a limited time",
        "description": "Mark code as temporary for migration or tracking.",
        "difficulty": "Intermediate"
    },
    "fall back to the most recently updated entry": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/f\u0254\u02d0l b\u00e6k tu\u02d0 \u00f0\u0259 m\u0259\u028ast \u02c8ri\u02d0sntli \u02c8\u028cpde\u026at\u026ad \u02c8entri/",
        "meaning": "to use the latest updated entry",
        "description": "Describe fallback logic when a preferred value is missing.",
        "difficulty": "Intermediate"
    },
    "support partial updates": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/s\u0259\u02c8p\u0254\u02d0t \u02c8p\u0251\u02d0\u0283l \u02c8\u028cpde\u026ats/",
        "meaning": "to allow partial updates",
        "description": "Switch to PATCH or similar to update only some fields.",
        "difficulty": "Intermediate"
    },
    "handle both active and terminated accounts": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02c8h\u00e6ndl b\u0259\u028a\u03b8 \u02c8\u00e6kt\u026av \u00e6nd \u02c8t\u025c\u02d0m\u026ane\u026at\u026ad \u0259\u02c8ka\u028ants/",
        "meaning": "to handle active and closed accounts",
        "description": "Explain that multiple account states are handled together.",
        "difficulty": "Intermediate"
    },
    "have no equivalent call for A": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/h\u00e6v n\u0259\u028a \u026a\u02c8kw\u026av\u0259l\u0259nt k\u0254\u02d0l f\u0254\u02d0/",
        "meaning": "to lack a matching API call",
        "description": "Point out API gaps between legacy and new services.",
        "difficulty": "Intermediate"
    },
    "create an isolated disposable branch": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/kri\u02c8e\u026at \u0259n \u02c8a\u026as\u0259le\u026at\u026ad d\u026a\u02c8sp\u0259\u028az\u0259bl br\u0251\u02d0nt\u0283/",
        "meaning": "to create a throwaway branch",
        "description": "Use a temporary branch for safe integration testing.",
        "difficulty": "Intermediate"
    },
    "the safest way to verify": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/\u00f0\u0259 \u02c8se\u026af\u026ast we\u026a tu\u02d0 \u02c8ver\u026afa\u026a/",
        "meaning": "the safest verification method",
        "description": "Explain why a chosen verification approach is low risk.",
        "difficulty": "Beginner"
    },
    "not be treated as the canonical implementation": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/n\u0252t bi \u02c8tri\u02d0t\u026ad \u00e6z \u00f0\u0259 k\u0259\u02c8n\u0252n\u026akl \u02cc\u026ampl\u026amen\u02c8te\u026a\u0283n/",
        "meaning": "not to be treated as canonical",
        "description": "Warn that a patch is temporary, not the official design.",
        "difficulty": "Advanced"
    },
    "leave the original history unchanged": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/li\u02d0v \u00f0i \u0259\u02c8r\u026ad\u0292\u0259nl \u02c8h\u026ast\u0259ri \u028cn\u02c8t\u0283e\u026and\u0292d/",
        "meaning": "to keep original history intact",
        "description": "Verify changes without rewriting branch history.",
        "difficulty": "Intermediate"
    },
    "be decided separately": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/bi d\u026a\u02c8sa\u026ad\u026ad \u02c8sepr\u0259tli/",
        "meaning": "to be decided later",
        "description": "Defer a decision to a follow-up after validation.",
        "difficulty": "Beginner"
    },
    "reproduce an error": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02ccri\u02d0pr\u0259\u02c8dju\u02d0s \u0259n \u02c8er\u0259/",
        "meaning": "to reproduce an error",
        "description": "Set up stubs or data to reproduce a bug reliably.",
        "difficulty": "Beginner"
    },
    "verify an edge case in integration tests": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02c8ver\u026afa\u026a \u0259n ed\u0292 ke\u026as \u026an \u02cc\u026ant\u026a\u02c8\u0261re\u026a\u0283n tests/",
        "meaning": "to verify an edge case in integration tests",
        "description": "Show edge-case coverage in integration tests.",
        "difficulty": "Intermediate"
    },
    "cover the happy path and the failure path": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02c8k\u028cv \u00f0\u0259 \u02c8h\u00e6pi p\u0251\u02d0\u03b8 \u00e6nd \u00f0\u0259 \u02c8fe\u026alj\u0259 p\u0251\u02d0\u03b8/",
        "meaning": "to cover success and failure cases",
        "description": "Argue tests cover both success and downstream failure paths.",
        "difficulty": "Intermediate"
    },
    "increase branch coverage": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u026an\u02c8kri\u02d0s br\u0251\u02d0nt\u0283 \u02c8k\u028cv\u0259r\u026ad\u0292/",
        "meaning": "to raise branch coverage",
        "description": "Add tests to cover more conditional branches.",
        "difficulty": "Intermediate"
    },
    "be covered by unit and integration tests": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/bi \u02c8k\u028cv\u0259d ba\u026a \u02c8ju\u02d0n\u026at \u00e6nd \u02cc\u026ant\u026a\u02c8\u0261re\u026a\u0283n tests/",
        "meaning": "to be covered by unit and integration tests",
        "description": "State that behavior is protected by existing tests.",
        "difficulty": "Intermediate"
    },
    "consider it passed if the build succeeds": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/k\u0259n\u02c8s\u026ad\u0259r \u026at p\u0251\u02d0st \u026af \u00f0\u0259 b\u026ald s\u0259k\u02c8si\u02d0dz/",
        "meaning": "to treat a green build as pass",
        "description": "Accept CI build success as sufficient for low-risk changes.",
        "difficulty": "Intermediate"
    },
    "CI passed": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/si\u02d0 a\u026a p\u0251\u02d0st/",
        "meaning": "continuous integration succeeded",
        "description": "Report that CI completed successfully.",
        "difficulty": "Beginner"
    },
    "no production code changed": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/n\u0259\u028a pr\u0259\u02c8d\u028ck\u0283n k\u0259\u028ad t\u0283e\u026and\u0292d/",
        "meaning": "production code was not changed",
        "description": "Clarify a PR changes only tests or non-runtime files.",
        "difficulty": "Intermediate"
    },
    "be documentation-only": {
        "type": "phrase",
        "partOfSpeech": "adjective phrase",
        "pronunciation": "/bi \u02ccd\u0252kjumen\u02c8te\u026a\u0283n \u02c8\u0259\u028anli/",
        "meaning": "to change only documentation",
        "description": "State a PR updates docs without affecting runtime behavior.",
        "difficulty": "Intermediate"
    },
    "have no runtime, API, or configuration changes": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/h\u00e6v n\u0259\u028a \u02c8r\u028cnta\u026am \u02cce\u026a pi\u02d0 \u02c8a\u026a \u0254\u02d0 \u02cck\u0252nf\u026a\u0261\u0259\u02c8re\u026a\u0283n \u02c8t\u0283e\u026and\u0292\u026az/",
        "meaning": "to have no runtime, API, or config changes",
        "description": "Assure reviewers there is no production impact.",
        "difficulty": "Intermediate"
    },
    "establish a standard way to": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u026a\u02c8st\u00e6bl\u026a\u0283 \u0259 \u02c8st\u00e6nd\u0259d we\u026a tu\u02d0/",
        "meaning": "to establish a standard approach",
        "description": "Introduce a shared pattern or guideline for a workflow.",
        "difficulty": "Intermediate"
    },
    "provide examples that reviewers can follow": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/pr\u0259\u02c8va\u026ad \u026a\u0261\u02c8z\u0251\u02d0mplz \u00f0\u00e6t r\u026a\u02c8vju\u02d0\u0259z k\u00e6n \u02c8f\u0252l\u0259\u028a/",
        "meaning": "to give examples for reviewers",
        "description": "Include sample steps reviewers can reuse later.",
        "difficulty": "Intermediate"
    },
    "keep A as the source while making B primary": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ki\u02d0p \u00e6z \u00f0\u0259 s\u0254\u02d0s wa\u026al \u02c8me\u026ak\u026a\u014b \u02c8pra\u026am\u0259ri/",
        "meaning": "to keep A as source and B as primary",
        "description": "Describe dual documentation roles during a transition.",
        "difficulty": "Advanced"
    },
    "avoid inventing unsupported details": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u0259\u02c8v\u0254\u026ad \u026an\u02c8vent\u026a\u014b \u02cc\u028cns\u0259\u02c8p\u0254\u02d0t\u026ad \u02c8di\u02d0te\u026alz/",
        "meaning": "to avoid adding unsupported details",
        "description": "Stick to the spec instead of adding nonstandard behavior.",
        "difficulty": "Advanced"
    },
    "the root cause was that": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/\u00f0\u0259 ru\u02d0t k\u0254\u02d0z w\u0252z \u00f0\u00e6t/",
        "meaning": "the root cause was",
        "description": "State the direct cause found during debugging.",
        "difficulty": "Beginner"
    },
    "perform A before validating B": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/p\u0259\u02c8f\u0254\u02d0m b\u026a\u02c8f\u0254\u02d0 \u02c8v\u00e6l\u026ade\u026at\u026a\u014b/",
        "meaning": "to run A before validating B",
        "description": "Describe a ordering bug where work runs before validation.",
        "difficulty": "Intermediate"
    },
    "exceed the supported format boundary": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u026ak\u02c8si\u02d0d \u00f0\u0259 s\u0259\u02c8p\u0254\u02d0t\u026ad \u02c8f\u0254\u02d0m\u00e6t \u02c8ba\u028andri/",
        "meaning": "to go beyond supported format limits",
        "description": "Explain input exceeded allowed format or length.",
        "difficulty": "Advanced"
    },
    "return the standard not-found response": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/r\u026a\u02c8t\u025c\u02d0n \u00f0\u0259 \u02c8st\u00e6nd\u0259d n\u0252t fa\u028and r\u026a\u02c8sp\u0252ns/",
        "meaning": "to return the standard 404 response",
        "description": "Return a unified not-found response for missing records.",
        "difficulty": "Intermediate"
    },
    "surface an upstream error as a server error": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02c8s\u025c\u02d0f\u026as \u0259n \u02c8\u028cpstri\u02d0m \u02c8er\u0259r \u00e6z \u0259 \u02c8s\u025c\u02d0v\u0259 \u02c8er\u0259/",
        "meaning": "to expose upstream errors as 5xx",
        "description": "Describe incorrect error mapping from upstream failures.",
        "difficulty": "Advanced"
    },
    "leave the cached value state or incomplete": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/li\u02d0v \u00f0\u0259 k\u00e6\u0283t \u02c8v\u00e6lju\u02d0 ste\u026at \u0254\u02d0r \u02cc\u026ank\u0259m\u02c8pli\u02d0t/",
        "meaning": "to leave cache stale or incomplete",
        "description": "Warn that failed updates can leave cache inconsistent.",
        "difficulty": "Advanced"
    },
    "on every request instead of using the cache": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/\u0252n \u02c8evri r\u026a\u02c8kwest \u026an\u02c8sted \u0252v \u02c8ju\u02d0z\u026a\u014b \u00f0\u0259 k\u00e6\u0283/",
        "meaning": "on every request rather than cache",
        "description": "Fetch fresh data each request instead of using cache.",
        "difficulty": "Intermediate"
    },
    "prevent confusion": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/pr\u026a\u02c8vent k\u0259n\u02c8fju\u02d0\u0292n/",
        "meaning": "to prevent confusion",
        "description": "Rename or clarify to avoid misunderstanding.",
        "difficulty": "Beginner"
    },
    "prevent an overly large value from being stored": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/pr\u026a\u02c8vent \u0259n \u02c8\u0259\u028av\u0259li l\u0251\u02d0d\u0292 \u02c8v\u00e6lju\u02d0 fr\u0252m \u02c8bi\u02d0\u026a\u014b st\u0254\u02d0d/",
        "meaning": "to block storing oversized values",
        "description": "Validate inputs so storage limits are not exceeded.",
        "difficulty": "Intermediate"
    },
    "prevent an unnecessary call": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/pr\u026a\u02c8vent \u0259n \u028cn\u02c8nes\u0259s\u0259ri k\u0254\u02d0l/",
        "meaning": "to avoid an unnecessary call",
        "description": "Add guards to skip redundant downstream calls.",
        "difficulty": "Intermediate"
    },
    "avoid an unnecessary client error": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u0259\u02c8v\u0254\u026ad \u0259n \u028cn\u02c8nes\u0259s\u0259ri \u02c8kla\u026a\u0259nt \u02c8er\u0259/",
        "meaning": "to avoid unnecessary client errors",
        "description": "Change responses so clients do not error unnecessarily.",
        "difficulty": "Intermediate"
    },
    "avoid static-analysis false positives": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u0259\u02c8v\u0254\u026ad \u02ccst\u00e6t\u026ak \u0259\u02c8n\u00e6l\u0259s\u026as f\u0254\u02d0ls \u02c8p\u0252z\u0259t\u026avz/",
        "meaning": "to avoid static-analysis false positives",
        "description": "Exclude generated code from tools that flag false issues.",
        "difficulty": "Advanced"
    },
    "return an empty list instead of an error": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/r\u026a\u02c8t\u025c\u02d0n \u0259n \u02c8empti l\u026ast \u026an\u02c8sted \u0252v \u0259n \u02c8er\u0259/",
        "meaning": "to return an empty list, not an error",
        "description": "Treat missing upstream data as an empty list, not failure.",
        "difficulty": "Intermediate"
    },
    "avoid sending the app to the error page": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u0259\u02c8v\u0254\u026ad \u02c8send\u026a\u014b \u00f0i \u00e6p tu\u02d0 \u00f0i \u02c8er\u0259 pe\u026ad\u0292/",
        "meaning": "to keep the app off the error page",
        "description": "Adjust backend responses to prevent client error screens.",
        "difficulty": "Intermediate"
    },
    "treat A as a non-error response": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/tri\u02d0t \u00e6z \u0259 n\u0252n \u02c8er\u0259 r\u026a\u02c8sp\u0252ns/",
        "meaning": "to treat A as a normal response",
        "description": "Classify a business state as success, not an error.",
        "difficulty": "Intermediate"
    },
    "mask sensitive paths in logs": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/m\u0251\u02d0sk \u02c8sens\u0259t\u026av p\u0251\u02d0\u03b8z \u026an l\u0252\u0261z/",
        "meaning": "to mask sensitive paths in logs",
        "description": "Redact sensitive paths before logs are exported.",
        "difficulty": "Intermediate"
    },
    "ensure correct masking behavior": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u026an\u02c8\u0283\u028a\u0259 k\u0259\u02c8rekt \u02c8m\u0251\u02d0sk\u026a\u014b b\u026a\u02c8he\u026avj\u0259/",
        "meaning": "to ensure masking works correctly",
        "description": "Add tests that verify log masking on protected routes.",
        "difficulty": "Intermediate"
    },
    "improve privacy and security in Logging": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u026am\u02c8pru\u02d0v \u02c8pr\u026av\u0259si \u00e6nd s\u026a\u02c8kj\u028a\u0259r\u0259ti \u026an \u02c8l\u0252\u0261\u026a\u014b/",
        "meaning": "to improve logging privacy and security",
        "description": "Strengthen log redaction to reduce sensitive data exposure.",
        "difficulty": "Intermediate"
    },
    "verify that unrelated endpoints are unaffected": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02c8ver\u026afa\u026a \u00f0\u00e6t \u028cnr\u026a\u02c8le\u026at\u026ad \u02c8endp\u0254\u026ants \u0251\u02d0r \u028cn\u0259\u02c8fekt\u026ad/",
        "meaning": "to verify unrelated endpoints are safe",
        "description": "Show shared changes did not affect other endpoints.",
        "difficulty": "Intermediate"
    },
    "have the potential of leaking A": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/h\u00e6v \u00f0\u0259 p\u0259\u02c8ten\u0283l \u0252v \u02c8li\u02d0k\u026a\u014b/",
        "meaning": "to risk leaking A",
        "description": "Describe a security risk before a fix.",
        "difficulty": "Advanced"
    },
    "be consistently masked in logs": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/bi k\u0259n\u02c8s\u026ast\u0259ntli m\u0251\u02d0skt \u026an l\u0252\u0261z/",
        "meaning": "to be consistently masked in logs",
        "description": "Report that sensitive values are always redacted in logs.",
        "difficulty": "Intermediate"
    },
    "store a hash instead of the whole token": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/st\u0254\u02d0r \u0259 h\u00e6\u0283 \u026an\u02c8sted \u0252v \u00f0\u0259 h\u0259\u028al \u02c8t\u0259\u028ak\u0259n/",
        "meaning": "to store a hash, not the full token",
        "description": "Store only a hash of tokens for better security.",
        "difficulty": "Intermediate"
    },
    "save memory": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/se\u026av \u02c8mem\u0259ri/",
        "meaning": "to reduce memory use",
        "description": "Lighten stored data to reduce memory consumption.",
        "difficulty": "Beginner"
    },
    "be unable to make use of exposed records": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/bi \u028cn\u02c8e\u026abl tu\u02d0 me\u026ak ju\u02d0s \u0252v \u026ak\u02c8sp\u0259\u028azd \u02c8rek\u0254\u02d0dz/",
        "meaning": "to be unable to abuse exposed records",
        "description": "Argue hashed records are useless if leaked.",
        "difficulty": "Advanced"
    },
    "only merge when": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/\u02c8\u0259\u028anli m\u025c\u02d0d\u0292 wen/",
        "meaning": "merge only when",
        "description": "Set conditional merge rules based on environment readiness.",
        "difficulty": "Beginner"
    },
    "as part of the response to a security review": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/\u00e6z p\u0251\u02d0t \u0252v \u00f0\u0259 r\u026a\u02c8sp\u0252ns tu\u02d0 \u0259 s\u026a\u02c8kj\u028a\u0259r\u0259ti r\u026a\u02c8vju\u02d0/",
        "meaning": "as part of a security review response",
        "description": "Note a change addresses security review findings.",
        "difficulty": "Intermediate"
    },
    "add an additional authentication check": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u00e6d \u0259n \u0259\u02c8d\u026a\u0283\u0259nl \u0254\u02d0\u02cc\u03b8ent\u026a\u02c8ke\u026a\u0283n t\u0283ek/",
        "meaning": "to add another auth check",
        "description": "Harden sensitive endpoints with extra authentication.",
        "difficulty": "Intermediate"
    },
    "catch failures and latencies": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/k\u00e6t\u0283 \u02c8fe\u026alj\u0259z \u00e6nd \u02c8le\u026at\u0259nsiz/",
        "meaning": "to detect failures and latency",
        "description": "Use thresholds or metrics to catch errors and slow paths.",
        "difficulty": "Intermediate"
    },
    "track performance by scenario": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/tr\u00e6k p\u0259\u02c8f\u0254\u02d0m\u0259ns ba\u026a s\u026a\u02c8n\u0251\u02d0ri\u0259\u028a/",
        "meaning": "to track performance per scenario",
        "description": "Split reports so each scenario has its own metrics.",
        "difficulty": "Intermediate"
    },
    "reflect real latency": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/r\u026a\u02c8flekt r\u026a\u0259l \u02c8le\u026at\u0259nsi/",
        "meaning": "to reflect actual latency",
        "description": "Adjust histogram bounds to match production latency.",
        "difficulty": "Intermediate"
    },
    "make the metrics inaccurate": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/me\u026ak \u00f0\u0259 \u02c8metr\u026aks \u026an\u02c8\u00e6kj\u0259r\u0259t/",
        "meaning": "to make metrics inaccurate",
        "description": "Explain how bad settings distort monitoring data.",
        "difficulty": "Intermediate"
    },
    "increase the load considerably": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u026an\u02c8kri\u02d0s \u00f0\u0259 l\u0259\u028ad k\u0259n\u02c8s\u026ad\u0259r\u0259bli/",
        "meaning": "to increase load significantly",
        "description": "Warn that a design choice may heavily load downstream services.",
        "difficulty": "Intermediate"
    },
    "cause high latency": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/k\u0254\u02d0z ha\u026a \u02c8le\u026at\u0259nsi/",
        "meaning": "to cause high latency",
        "description": "Report latency caused by a code path or design.",
        "difficulty": "Intermediate"
    },
    "optimize A not to call B": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02c8\u0252pt\u026ama\u026az n\u0252t tu\u02d0 k\u0254\u02d0l/",
        "meaning": "to optimize A to avoid calling B",
        "description": "Remove unnecessary downstream calls from a hot path.",
        "difficulty": "Intermediate"
    },
    "reduce the number of lines for manageability": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/r\u026a\u02c8dju\u02d0s \u00f0\u0259 \u02c8n\u028cmb\u0259r \u0252v la\u026anz f\u0254\u02d0 \u02ccm\u00e6n\u026ad\u0292\u0259\u02c8b\u026al\u0259ti/",
        "meaning": "to reduce line count for manageability",
        "description": "Split or refactor large files to improve maintainability.",
        "difficulty": "Intermediate"
    },
    "let us focus on the relevant code": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/let \u0259s \u02c8f\u0259\u028ak\u0259s \u0252n \u00f0\u0259 \u02c8rel\u0259v\u0259nt k\u0259\u028ad/",
        "meaning": "to let reviewers focus on relevant code",
        "description": "Use helpers so reviews focus on the important changes.",
        "difficulty": "Beginner"
    },
    "ensure compatibility with the latest frameworks": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u026an\u02c8\u0283\u028a\u0259 k\u0259m\u02ccp\u00e6t\u0259\u02c8b\u026al\u0259ti w\u026a\u00f0 \u00f0\u0259 \u02c8le\u026at\u026ast \u02c8fre\u026amw\u025c\u02d0ks/",
        "meaning": "to ensure latest framework compatibility",
        "description": "Upgrade dependencies to stay compatible with supported frameworks.",
        "difficulty": "Intermediate"
    },
    "resolve a production issue": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/r\u026a\u02c8z\u0252lv \u0259 pr\u0259\u02c8d\u028ck\u0283n \u02c8\u026a\u0283u\u02d0/",
        "meaning": "to fix a production issue",
        "description": "Describe a hotfix for an active production problem.",
        "difficulty": "Beginner"
    },
    "preserve a URI template": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/pr\u026a\u02c8z\u025c\u02d0v \u0259 \u02ccju\u02d0 \u0251\u02d0r \u02c8a\u026a \u02c8templ\u0259t/",
        "meaning": "to keep a URI template intact",
        "description": "Keep route templates so metrics labels stay stable.",
        "difficulty": "Advanced"
    },
    "result in high cardinality": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/r\u026a\u02c8z\u028clt \u026an ha\u026a \u02cck\u0251\u02d0d\u026a\u02c8n\u00e6l\u0259ti/",
        "meaning": "to cause high metric cardinality",
        "description": "Warn that dynamic labels can explode metric cardinality.",
        "difficulty": "Advanced"
    },
    "keep metric cardinality low": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ki\u02d0p \u02c8metr\u026ak \u02cck\u0251\u02d0d\u026a\u02c8n\u00e6l\u0259ti l\u0259\u028a/",
        "meaning": "to keep metric cardinality low",
        "description": "Use route templates to limit unique metric label values.",
        "difficulty": "Advanced"
    },
    "avoid the same issue when copying and pasting code": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u0259\u02c8v\u0254\u026ad \u00f0\u0259 se\u026am \u02c8\u026a\u0283u\u02d0 wen \u02c8k\u0252pi\u026a\u014b \u00e6nd \u02c8pe\u026ast\u026a\u014b k\u0259\u028ad/",
        "meaning": "to avoid repeat issues from copy-paste",
        "description": "Fix other call sites to prevent copy-paste bugs spreading.",
        "difficulty": "Intermediate"
    },
    "prioritize user experience": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/pra\u026a\u02c8\u0252r\u0259ta\u026az \u02c8ju\u02d0z\u0259r \u026ak\u02c8sp\u026a\u0259ri\u0259ns/",
        "meaning": "to prioritize user experience",
        "description": "Choose fallbacks that keep UX smooth during brief failures.",
        "difficulty": "Beginner"
    },
    "have a limited period of negative impact": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/h\u00e6v \u0259 \u02c8l\u026am\u026at\u026ad \u02c8p\u026a\u0259ri\u0259d \u0252v \u02c8ne\u0261\u0259t\u026av \u02c8\u026amp\u00e6kt/",
        "meaning": "to have limited negative impact",
        "description": "Explain harm is temporary and expires naturally.",
        "difficulty": "Advanced"
    },
    "follow the single-responsibility principle": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02c8f\u0252l\u0259\u028a \u00f0\u0259 \u02ccs\u026a\u014b\u0261l r\u026a\u02ccsp\u0252ns\u0259\u02c8b\u026al\u0259ti \u02c8pr\u026ans\u0259pl/",
        "meaning": "to follow single responsibility",
        "description": "Split layers to give each component one clear job.",
        "difficulty": "Intermediate"
    },
    "separate service-level and repository-level tests": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u02c8sepr\u0259t \u02c8s\u025c\u02d0v\u026as lev\u0259l \u00e6nd r\u026a\u02c8p\u0252z\u026at\u0259ri lev\u0259l tests/",
        "meaning": "to separate service and repository tests",
        "description": "Organize tests by layer for clearer coverage.",
        "difficulty": "Advanced"
    },
    "be too tightly coupled to a specific use case": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/bi tu\u02d0 \u02c8ta\u026atli \u02c8k\u028cpld tu\u02d0 \u0259 sp\u0259\u02c8s\u026af\u026ak ju\u02d0s ke\u026as/",
        "meaning": "to be too tied to one use case",
        "description": "Explain a helper is not reusable across flows.",
        "difficulty": "Advanced"
    },
    "move the read path to a dedicated resource": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/mu\u02d0v \u00f0\u0259 ri\u02d0d p\u0251\u02d0\u03b8 tu\u02d0 \u0259 \u02c8ded\u026ake\u026at\u026ad r\u026a\u02c8s\u0254\u02d0s/",
        "meaning": "to move reads to a dedicated resource",
        "description": "Separate read paths for clearer ownership or CQRS.",
        "difficulty": "Advanced"
    },
    "reuse it across multiple surfaces": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ri\u02d0\u02c8ju\u02d0z \u026at \u0259\u02c8kr\u0252s \u02c8m\u028clt\u026apl \u02c8s\u025c\u02d0f\u026as\u026az/",
        "meaning": "to reuse across multiple UIs",
        "description": "Share responses or components across screens without duplication.",
        "difficulty": "Advanced"
    },
    "conduct a size impact analysis": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/k\u0259n\u02c8d\u028ckt \u0259 sa\u026az \u02c8\u026amp\u00e6kt \u0259\u02c8n\u00e6l\u0259s\u026as/",
        "meaning": "to analyze size impact",
        "description": "Analyze capacity impact before storing new data in cache.",
        "difficulty": "Advanced"
    },
    "have a minimal impact on": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/h\u00e6v \u0259 \u02c8m\u026an\u026aml \u02c8\u026amp\u00e6kt \u0252n/",
        "meaning": "to have very little impact on",
        "description": "State resource or side effects are negligible.",
        "difficulty": "Intermediate"
    },
    "not move the needle much": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/n\u0252t mu\u02d0v \u00f0\u0259 \u02c8ni\u02d0dl m\u028ct\u0283/",
        "meaning": "to make little overall difference",
        "description": "Say further optimization would barely help at this scale.",
        "difficulty": "Advanced"
    },
    "add a standalone validation and transformation layer": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u00e6d \u0259 \u02c8st\u00e6nd\u0259\u02ccl\u0259\u028an \u02ccv\u00e6l\u026a\u02c8de\u026a\u0283n \u00e6nd \u02cctr\u00e6nsf\u0259\u02c8me\u026a\u0283n \u02c8le\u026a\u0259/",
        "meaning": "to add a validation and transform layer",
        "description": "Modularize validation and transformation in its own layer.",
        "difficulty": "Advanced"
    },
    "transform flat keys into a nested structure": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/tr\u00e6ns\u02c8f\u0254\u02d0m fl\u00e6t ki\u02d0z \u02c8\u026antu\u02d0 \u0259 \u02c8nest\u026ad \u02c8str\u028ckt\u0283\u0259/",
        "meaning": "to nest flat keys",
        "description": "Convert flat keys into nested structures clients expect.",
        "difficulty": "Intermediate"
    },
    "check that paired values are complete": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/t\u0283ek \u00f0\u00e6t pe\u0259d \u02c8v\u00e6lju\u02d0z \u0251\u02d0 k\u0259m\u02c8pli\u02d0t/",
        "meaning": "to verify paired values are complete",
        "description": "Validate related fields exist together before transforming.",
        "difficulty": "Intermediate"
    },
    "restrict A to a supported subset": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/r\u026a\u02c8str\u026akt tu\u02d0 \u0259 s\u0259\u02c8p\u0254\u02d0t\u026ad \u02c8s\u028cbset/",
        "meaning": "to limit A to a supported subset",
        "description": "Filter inputs or features to an allowed subset.",
        "difficulty": "Intermediate"
    },
    "confirm that there have been no requests for a period": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/k\u0259n\u02c8f\u025c\u02d0m \u00f0\u00e6t \u00f0e\u0259 h\u00e6v bi\u02d0n n\u0259\u028a r\u026a\u02c8kwests f\u0254\u02d0r \u0259 \u02c8p\u026a\u0259ri\u0259d/",
        "meaning": "to confirm zero traffic for a period",
        "description": "Verify an endpoint had no traffic before removal.",
        "difficulty": "Advanced"
    },
    "force tests to be updated when properties change": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/f\u0254\u02d0s tests tu\u02d0 bi\u02d0 \u02c8\u028cpde\u026at\u026ad wen \u02c8pr\u0252p\u0259tiz t\u0283e\u026and\u0292/",
        "meaning": "to force test updates on property changes",
        "description": "Use strict assertions so tests break when responses change.",
        "difficulty": "Intermediate"
    },
    "ensure consistent handling across the workflow": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u026an\u02c8\u0283\u028a\u0259 k\u0259n\u02c8s\u026ast\u0259nt \u02c8h\u00e6ndl\u026a\u014b \u0259\u02c8kr\u0252s \u00f0\u0259 \u02c8w\u025c\u02d0kfl\u0259\u028a/",
        "meaning": "to ensure consistent handling",
        "description": "Use shared models so identifiers are handled uniformly.",
        "difficulty": "Intermediate"
    },
    "ensure that tests reflect the new requirements": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u026an\u02c8\u0283\u028a\u0259 \u00f0\u00e6t tests r\u026a\u02c8flekt \u00f0\u0259 nju\u02d0 r\u026a\u02c8kwa\u026a\u0259m\u0259nts/",
        "meaning": "to ensure tests match new requirements",
        "description": "Update fixtures when specs or data requirements change.",
        "difficulty": "Intermediate"
    },
    "make the response easier for the client to consume": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/me\u026ak \u00f0\u0259 r\u026a\u02c8sp\u0252ns \u02c8i\u02d0zi\u0259 f\u0254\u02d0 \u00f0\u0259 \u02c8kla\u026a\u0259nt tu\u02d0 k\u0259n\u02c8sju\u02d0m/",
        "meaning": "to make responses easier for clients",
        "description": "Shape API responses for simpler client consumption.",
        "difficulty": "Intermediate"
    },
    "align the public contract with the actual semantics": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/\u0259\u02c8la\u026an \u00f0\u0259 \u02c8p\u028cbl\u026ak \u02c8k\u0252ntr\u00e6kt w\u026a\u00f0 \u00f0i \u02c8\u00e6kt\u0283u\u0259l s\u026a\u02c8m\u00e6nt\u026aks/",
        "meaning": "to align contract with actual semantics",
        "description": "Match public API definitions to real business state meaning.",
        "difficulty": "Advanced"
    },
}

USAGE_EXAMPLE_JA: dict[str, str] = {
    "introduce a new API": "\u3053\u306ePR\u306f\u30e6\u30fc\u30b6\u30fc\u901a\u77e5\u8a2d\u5b9a\u53d6\u5f97\u7528\u306e\u65b0API\u3092\u5c0e\u5165\u3059\u308b\u3002",
    "enable seamless transitions": "\u5171\u6709\u30b3\u30f3\u30c6\u30ad\u30b9\u30c8\u306b\u3088\u308a2\u30a2\u30d7\u30ea\u9593\u306e\u30b7\u30fc\u30e0\u30ec\u30b9\u306a\u9077\u79fb\u3092\u53ef\u80fd\u306b\u3059\u308b\u3002",
    "leverage A for persistence": "\u77ed\u671f\u72b6\u614b\u306e\u6c38\u7d9a\u5316\u306b\u30ad\u30fc\u30d0\u30ea\u30e5\u30fc\u30b9\u30c8\u30a2\u3092\u6d3b\u7528\u3059\u308b\u3002",
    "include robust error handling": "\u4e0d\u6b63\u306a\u4e0a\u6d41\u30ec\u30b9\u30dd\u30f3\u30b9\u5411\u3051\u306b\u5805\u7262\u306a\u30a8\u30e9\u30fc\u30cf\u30f3\u30c9\u30ea\u30f3\u30b0\u3092\u542b\u3081\u308b\u3002",
    "implement an endpoint": "\u3053\u306ePR\u306f\u30c1\u30e5\u30fc\u30c8\u30ea\u30a2\u30eb\u9032\u6357\u66f4\u65b0\u7528\u30a8\u30f3\u30c9\u30dd\u30a4\u30f3\u30c8\u3092\u5b9f\u88c5\u3059\u308b\u3002",
    "support two estimate types": "\u30a8\u30f3\u30c9\u30dd\u30a4\u30f3\u30c8\u306f\u30ea\u30af\u30a8\u30b9\u30c8\u30d1\u30e9\u30e1\u30fc\u30bf\u30672\u7a2e\u985e\u306e\u8a08\u7b97\u65b9\u5f0f\u306b\u5bfe\u5fdc\u3059\u308b\u3002",
    "refactor A to simplify and standardize B": "\u8a8d\u8a3c\u8a2d\u5b9a\u3092\u7c21\u7d20\u5316\u30fb\u6a19\u6e96\u5316\u3059\u308b\u305f\u3081\u30c6\u30b9\u30c8\u3092\u30ea\u30d5\u30a1\u30af\u30bf\u30ea\u30f3\u30b0\u3057\u305f\u3002",
    "reduce duplication and improve readability": "\u5171\u901a\u30d8\u30eb\u30d1\u30fc\u3067\u91cd\u8907\u3092\u6e1b\u3089\u3057\u3001\u30c6\u30b9\u30c8\u5168\u4f53\u306e\u53ef\u8aad\u6027\u3092\u5411\u4e0a\u3055\u305b\u305f\u3002",
    "streamline the internal data structures": "\u672a\u4f7f\u7528\u30e9\u30c3\u30d1\u30fc\u524a\u9664\u3067\u5185\u90e8\u30c7\u30fc\u30bf\u69cb\u9020\u3092\u5408\u7406\u5316\u3057\u305f\u3002",
    "eliminate an unused field": "\u30ea\u30d5\u30a1\u30af\u30bf\u30ea\u30f3\u30b0\u3067\u516c\u958b\u30ec\u30b9\u30dd\u30f3\u30b9\u304b\u3089\u672a\u4f7f\u7528\u30d5\u30a3\u30fc\u30eb\u30c9\u3092\u9664\u53bb\u3057\u305f\u3002",
    "remove references throughout the codebase": "\u975e\u63a8\u5968\u30d5\u30e9\u30b0\u3078\u306e\u53c2\u7167\u3092\u30b3\u30fc\u30c9\u30d9\u30fc\u30b9\u5168\u4f53\u304b\u3089\u524a\u9664\u3057\u305f\u3002",
    "match the response schema": "\u30b5\u30fc\u30d3\u30b9\u30de\u30c3\u30d4\u30f3\u30b0\u3092\u7c21\u7d20\u5316\u3055\u308c\u305f\u30ec\u30b9\u30dd\u30f3\u30b9\u30b9\u30ad\u30fc\u30de\u306b\u5408\u308f\u305b\u305f\u3002",
    "reflect the new response shape": "API\u30c9\u30ad\u30e5\u30e1\u30f3\u30c8\u3092\u65b0\u3057\u3044\u30ec\u30b9\u30dd\u30f3\u30b9\u5f62\u5f0f\u306b\u5408\u308f\u305b\u3066\u66f4\u65b0\u3057\u305f\u3002",
    "align the implementation with the API contract": "\u3053\u306ePR\u306f\u5b9f\u88c5\u3092\u516c\u958bAPI\u5951\u7d04\u306b\u9069\u5408\u3055\u305b\u308b\u3002",
    "resolve a schema mismatch": "\u751f\u6210\u5217\u6319\u5024\u306e\u30b9\u30ad\u30fc\u30de\u4e0d\u4e00\u81f4\u3092\u89e3\u6d88\u3057\u305f\u3002",
    "have a mismatch between A and B": "\u4ed5\u69d8\u3068\u5b9f\u884c\u6642\u30e2\u30c7\u30eb\u306e\u9593\u306b\u4e0d\u4e00\u81f4\u304c\u3042\u3063\u305f\u3002",
    "avoid A being interpreted as B": "\u547d\u540d\u5909\u66f4\u3067\u30d5\u30a3\u30fc\u30eb\u30c9\u304c\u30b7\u30ea\u30a2\u30e9\u30a4\u30ba\u5c5e\u6027\u3068\u8aa4\u89e3\u3055\u308c\u306a\u3044\u3088\u3046\u306b\u3057\u305f\u3002",
    "cause A to appear incorrectly": "\u8a2d\u5b9a\u30df\u30b9\u3067\u30d7\u30ed\u30d1\u30c6\u30a3\u304c\u30b9\u30ad\u30fc\u30de\u4e0a\u8aa4\u3063\u3066\u8868\u793a\u3055\u308c\u3066\u3044\u305f\u3002",
    "correctly expose the allowed values": "\u751f\u6210\u30b9\u30ad\u30fc\u30de\u304c\u8a31\u53ef\u5024\u3092\u6b63\u3057\u304f\u516c\u958b\u3059\u308b\u3088\u3046\u306b\u306a\u3063\u305f\u3002",
    "introduce a breaking response contract change": "\u3053\u306e\u30d7\u30ed\u30d1\u30c6\u30a3\u524a\u9664\u306f\u4e92\u63db\u6027\u306e\u306a\u3044\u30ec\u30b9\u30dd\u30f3\u30b9\u5909\u66f4\u3092\u5c0e\u5165\u3059\u308b\u3002",
    "be backward-compatible": "\u65b0\u30d5\u30a3\u30fc\u30eb\u30c9\u306f\u4efb\u610f\u306e\u305f\u3081\u5909\u66f4\u306f\u5f8c\u65b9\u4e92\u63db\u6027\u304c\u3042\u308b\u3002",
    "support both the new and old formats": "\u30b5\u30fc\u30d0\u30fc\u306f\u79fb\u884c\u671f\u9593\u4e2d\u3001\u65b0\u65e7\u4e21\u65b9\u306e\u30da\u30a4\u30ed\u30fc\u30c9\u5f62\u5f0f\u306b\u5bfe\u5fdc\u3059\u308b\u3002",
    "remove the deprecated fields": "\u5168\u30af\u30e9\u30a4\u30a2\u30f3\u30c8\u79fb\u884c\u5f8c\u306b\u975e\u63a8\u5968\u30d5\u30a3\u30fc\u30eb\u30c9\u3092\u524a\u9664\u3059\u308b\u3002",
    "be carried out in the following steps": "\u5c55\u958b\u306f\u6b21\u306e\u624b\u9806\u3067\u6bb5\u968e\u7684\u306b\u5b9f\u65bd\u3055\u308c\u308b\u3002",
    "be followed by the client release": "\u30d0\u30c3\u30af\u30a8\u30f3\u30c9\u30ea\u30ea\u30fc\u30b9\u306e\u5f8c\u306b\u30af\u30e9\u30a4\u30a2\u30f3\u30c8\u5074\u3092\u30ea\u30ea\u30fc\u30b9\u3059\u308b\u3002",
    "add A back if B does not cover it": "\u65b0\u30e2\u30c7\u30eb\u3067\u30ab\u30d0\u30fc\u3067\u304d\u306a\u3051\u308c\u3070\u30d5\u30a3\u30fc\u30eb\u30c9\u3092\u623b\u3059\u5fc5\u8981\u304c\u3042\u308b\u3002",
    "following a suggestion": "API\u30ec\u30d3\u30e5\u30fc\u306e\u63d0\u6848\u3092\u53d7\u3051\u3001\u30d5\u30a3\u30fc\u30eb\u30c9\u3092boolean\u306b\u5909\u66f4\u3057\u305f\u3002",
    "it was pointed out that": "\u5143\u306e\u540d\u524d\u304c\u66d6\u6627\u3067\u3042\u308b\u3068\u6307\u6458\u3055\u308c\u305f\u3002",
    "rename A for better clarity": "\u660e\u78ba\u5316\u306e\u305f\u3081`isNameOverlimit`\u306b\u30ea\u30cd\u30fc\u30e0\u3057\u305f\u3002",
    "migrate away from A": "\u30d7\u30ed\u30ad\u30b7\u9023\u643a\u304b\u3089\u6bb5\u968e\u7684\u306b\u79fb\u884c\u3059\u308b\u5fc5\u8981\u304c\u3042\u308b\u3002",
    "instead of relying on a A": "\u30b5\u30a4\u30c9\u30ab\u30fc\u306b\u983c\u3089\u305a\u30b5\u30fc\u30d3\u30b9\u30ea\u30af\u30a8\u30b9\u30c8\u3092\u76f4\u63a5\u547c\u3073\u51fa\u3059\u3002",
    "have more control": "\u76f4\u63a5\u547c\u3073\u51fa\u3057\u3067\u30ea\u30c8\u30e9\u30a4\u3068\u30bf\u30a4\u30e0\u30a2\u30a6\u30c8\u3092\u3088\u308a\u7d30\u304b\u304f\u5236\u5fa1\u3067\u304d\u308b\u3002",
    "handle non-JSON responses properly": "\u66f4\u65b0\u30ed\u30b8\u30c3\u30af\u306fJSON\u4ee5\u5916\u306e\u30ec\u30b9\u30dd\u30f3\u30b9\u3082\u9069\u5207\u306b\u51e6\u7406\u3067\u304d\u308b\u3002",
    "cannot migrate everything at once": "\u5168\u30af\u30e9\u30a4\u30a2\u30f3\u30c8\u3092\u4e00\u5ea6\u306b\u79fb\u884c\u3067\u304d\u306a\u3044\u305f\u3081\u4e21\u5f62\u5f0f\u304c\u5171\u5b58\u3059\u308b\u3002",
    "improvement might be limited unless": "\u4e0b\u6d41\u547c\u3073\u51fa\u3057\u3082\u975e\u30d6\u30ed\u30c3\u30ad\u30f3\u30b0\u3067\u306a\u3051\u308c\u3070\u6027\u80fd\u6539\u5584\u306f\u9650\u5b9a\u7684\u304b\u3082\u3057\u308c\u306a\u3044\u3002",
    "be a laborious task": "\u5168\u547c\u3073\u51fa\u3057\u7b87\u6240\u30921PR\u3067\u79fb\u884c\u3059\u308b\u306e\u306f\u624b\u9593\u306e\u304b\u304b\u308b\u4f5c\u696d\u3060\u3002",
    "put a task on hold": "\u30af\u30e9\u30a4\u30a2\u30f3\u30c8\u79fb\u884c\u5b8c\u4e86\u307e\u3067\u30af\u30ea\u30fc\u30f3\u30a2\u30c3\u30d7\u30bf\u30b9\u30af\u3092\u4fdd\u7559\u306b\u3059\u308b\u3002",
    "plan to migrate to": "\u6b21\u30ea\u30ea\u30fc\u30b9\u3067\u30d0\u30fc\u30b8\u30e7\u30f3\u4ed8\u304d\u30a8\u30f3\u30c9\u30dd\u30a4\u30f3\u30c8\u3078\u79fb\u884c\u4e88\u5b9a\u3060\u3002",
    "add A temporarily": "\u3053\u306ePR\u306f\u79fb\u884c\u8ffd\u8de1\u7528\u306b\u8b58\u5225\u5b50\u3092\u4e00\u6642\u7684\u306b\u8ffd\u52a0\u3059\u308b\u3002",
    "fall back to the most recently updated entry": "\u512a\u5148\u5024\u304c\u306a\u3051\u308c\u3070\u6700\u7d42\u66f4\u65b0\u30a8\u30f3\u30c8\u30ea\u306b\u30d5\u30a9\u30fc\u30eb\u30d0\u30c3\u30af\u3059\u308b\u3002",
    "support partial updates": "\u90e8\u5206\u66f4\u65b0\u5bfe\u5fdc\u306e\u305f\u3081\u30e1\u30bd\u30c3\u30c9\u3092PATCH\u306b\u5909\u66f4\u3057\u305f\u3002",
    "handle both active and terminated accounts": "\u4e0b\u6d41API\u306f\u6709\u52b9\u30fb\u89e3\u7d04\u6e08\u307f\u30a2\u30ab\u30a6\u30f3\u30c8\u53cc\u65b9\u3092\u5185\u90e8\u51e6\u7406\u3059\u308b\u3002",
    "have no equivalent call for A": "\u30ec\u30ac\u30b7\u30fc\u30b5\u30fc\u30d3\u30b9\u306b\u306f\u3053\u306e\u30ea\u30bd\u30fc\u30b9\u76f8\u5f53\u306e\u547c\u3073\u51fa\u3057\u304c\u306a\u3044\u3002",
    "create an isolated disposable branch": "\u7d50\u5408\u30c6\u30b9\u30c8\u7528\u306b\u9694\u96e2\u3055\u308c\u305f\u4f7f\u3044\u6368\u3066\u30d6\u30e9\u30f3\u30c1\u3092\u4f5c\u6210\u3057\u305f\u3002",
    "the safest way to verify": "\u5909\u66f4\u691c\u8a3c\u306e\u6700\u3082\u5b89\u5168\u306a\u65b9\u6cd5\u306f\u73fe\u884c\u7d50\u5408\u30d6\u30e9\u30f3\u30c1\u3067\u30c6\u30b9\u30c8\u3059\u308b\u3053\u3068\u3060\u3063\u305f\u3002",
    "not be treated as the canonical implementation": "\u3053\u306e\u66ab\u5b9a\u30d1\u30c3\u30c1\u306f\u6b63\u5f0f\u306a\u5b9f\u88c5\u3068\u3057\u3066\u6271\u3046\u3079\u304d\u3067\u306f\u306a\u3044\u3002",
    "leave the original history unchanged": "\u691c\u8a3c\u624b\u9806\u306f\u5143\u30d6\u30e9\u30f3\u30c1\u306e\u5c65\u6b74\u3092\u5909\u66f4\u305b\u305a\u306b\u6b8b\u3059\u3002",
    "be decided separately": "\u30af\u30ea\u30fc\u30f3\u30a2\u30c3\u30d7\u65b9\u91dd\u306f\u691c\u8a3c\u5f8c\u306b\u5225\u9014\u6c7a\u5b9a\u3059\u308b\u3002",
    "reproduce an error": "\u30b9\u30bf\u30d6\u3067\u958b\u767a\u74b0\u5883\u3067\u30a8\u30e9\u30fc\u3092\u4e00\u8cab\u3057\u3066\u518d\u73fe\u3067\u304d\u308b\u3002",
    "verify an edge case in integration tests": "\u7d50\u5408\u30c6\u30b9\u30c8\u3067\u3053\u306e\u5883\u754c\u6761\u4ef6\u3092\u78ba\u8a8d\u3057\u305f\u3002",
    "cover the happy path and the failure path": "\u30c6\u30b9\u30c8\u306f\u6b63\u5e38\u7cfb\u3068\u4e0b\u6d41\u5931\u6557\u7cfb\u306e\u4e21\u65b9\u3092\u30ab\u30d0\u30fc\u3059\u308b\u3002",
    "increase branch coverage": "\u8ffd\u52a0\u30c6\u30b9\u30c8\u3067\u30d5\u30a9\u30fc\u30eb\u30d0\u30c3\u30af\u30ed\u30b8\u30c3\u30af\u306e\u5206\u5c90\u30ab\u30d0\u30ec\u30c3\u30b8\u3092\u9ad8\u3081\u305f\u3002",
    "be covered by unit and integration tests": "\u3053\u306e\u6319\u52d5\u306f\u5358\u4f53\u30fb\u7d50\u5408\u30c6\u30b9\u30c8\u3067\u30ab\u30d0\u30fc\u3055\u308c\u3066\u3044\u308b\u3002",
    "consider it passed if the build succeeds": "\u5185\u90e8\u5909\u66f4\u306fCI\u30d3\u30eb\u30c9\u6210\u529f\u3092\u3082\u3063\u3066\u5408\u683c\u3068\u307f\u306a\u3057\u3066\u3088\u3044\u3002",
    "CI passed": "CI\u306f\u5168\u5358\u4f53\u30fb\u7d50\u5408\u30c6\u30b9\u30c8\u6709\u52b9\u3067\u6210\u529f\u3057\u305f\u3002",
    "no production code changed": "\u30d7\u30ed\u30c0\u30af\u30b7\u30e7\u30f3\u30b3\u30fc\u30c9\u306b\u5909\u66f4\u306f\u306a\u304f\u3001\u30c6\u30b9\u30c8\u306e\u307f\u66f4\u65b0\u3057\u305f\u3002",
    "be documentation-only": "\u3053\u306ePR\u306f\u30c9\u30ad\u30e5\u30e1\u30f3\u30c8\u306e\u307f\u306e\u5909\u66f4\u3067\u5b9f\u884c\u6642\u6319\u52d5\u306b\u5f71\u97ff\u3057\u306a\u3044\u3002",
    "have no runtime, API, or configuration changes": "\u4eca\u56de\u306e\u66f4\u65b0\u306b\u5b9f\u884c\u6642\u30fbAPI\u30fb\u8a2d\u5b9a\u3078\u306e\u5909\u66f4\u306f\u306a\u3044\u3002",
    "establish a standard way to": "\u3053\u306ePR\u306f\u30b5\u30fc\u30d3\u30b9\u9023\u643a\u3092\u6587\u66f8\u5316\u3059\u308b\u6a19\u6e96\u7684\u65b9\u6cd5\u3092\u78ba\u7acb\u3059\u308b\u3002",
    "provide examples that reviewers can follow": "\u6587\u66f8\u306f\u4eca\u5f8c\u306e\u79fb\u884c\u3067\u30ec\u30d3\u30e5\u30fc\u62c5\u5f53\u8005\u304c\u53c2\u8003\u306b\u3067\u304d\u308b\u4f8b\u3092\u793a\u3059\u3002",
    "keep A as the source while making B primary": "PlantUML\u3092\u4fdd\u7ba1\u5143\u3068\u3057\u3064\u3064TDD\u3092\u4e3b\u8a2d\u8a08\u8cc7\u6599\u3068\u3059\u308b\u3002",
    "avoid inventing unsupported details": "\u5909\u63db\u30eb\u30fc\u30eb\u306f\u672a\u30b5\u30dd\u30fc\u30c8\u306e\u5b9f\u88c5\u8a73\u7d30\u3092\u72ec\u81ea\u306b\u4f5c\u3089\u306a\u3044\u3002",
    "the root cause was that": "\u6839\u672c\u539f\u56e0\u306f\u6240\u6709\u6a29\u30eb\u30c3\u30af\u30a2\u30c3\u30d7\u304c\u5165\u529b\u691c\u8a3c\u3088\u308a\u5148\u306b\u8d70\u3063\u3066\u3044\u305f\u3053\u3068\u3060\u3063\u305f\u3002",
    "perform A before validating B": "\u65e7\u30d5\u30ed\u30fc\u306f\u8b58\u5225\u5b50\u691c\u8a3c\u524d\u306bDB\u30eb\u30c3\u30af\u30a2\u30c3\u30d7\u3092\u5b9f\u884c\u3057\u3066\u3044\u305f\u3002",
    "exceed the supported format boundary": "\u8b58\u5225\u5b50\u304c\u30b5\u30dd\u30fc\u30c8\u5f62\u5f0f\u306e\u5883\u754c\u3092\u8d85\u3048\u305f\u3068\u304d\u306b\u30a8\u30e9\u30fc\u304c\u8d77\u304d\u305f\u3002",
    "return the standard not-found response": "\u65b0\u691c\u8a3c\u306f\u4e0d\u5728\u30ec\u30b3\u30fc\u30c9\u306b\u6a19\u6e96404\u30ec\u30b9\u30dd\u30f3\u30b9\u3092\u8fd4\u3059\u3002",
    "surface an upstream error as a server error": "\u65e7\u5b9f\u88c5\u306f\u4e0a\u6d41\u691c\u8a3c\u30a8\u30e9\u30fc\u3092\u30b5\u30fc\u30d0\u30fc\u30a8\u30e9\u30fc\u3068\u3057\u3066\u9732\u51fa\u3055\u305b\u3066\u3044\u305f\u3002",
    "leave the cached value state or incomplete": "\u66f4\u65b0\u5931\u6557\u3067\u30ad\u30e3\u30c3\u30b7\u30e5\u30de\u30c3\u30d4\u30f3\u30b0\u304c\u53e4\u3044\u304b\u4e0d\u5b8c\u5168\u306a\u72b6\u614b\u306b\u6b8b\u308b\u3002",
    "on every request instead of using the cache": "\u30ad\u30e3\u30c3\u30b7\u30e5\u3092\u4f7f\u308f\u305a\u30ea\u30af\u30a8\u30b9\u30c8\u3054\u3068\u306b\u6700\u65b0\u30de\u30c3\u30d4\u30f3\u30b0\u3092\u53d6\u5f97\u3059\u308b\u3002",
    "prevent confusion": "\u30d3\u30b8\u30cd\u30b9\u610f\u5473\u306e\u6df7\u4e71\u3092\u9632\u3050\u305f\u3081\u5217\u6319\u578b\u3092\u30ea\u30cd\u30fc\u30e0\u3057\u305f\u3002",
    "prevent an overly large value from being stored": "\u691c\u8a3c\u3067\u904e\u5927\u306a\u6709\u52b9\u671f\u9650\u5024\u304c\u4fdd\u5b58\u3055\u308c\u308b\u306e\u3092\u9632\u3050\u3002",
    "prevent an unnecessary call": "\u7a7a\u72b6\u614b\u30c1\u30a7\u30c3\u30af\u3067\u4e0d\u8981\u306a\u4e0b\u6d41\u547c\u3073\u51fa\u3057\u3092\u9632\u3050\u3002",
    "avoid an unnecessary client error": "\u671f\u9650\u5207\u308c\u30c7\u30fc\u30bf\u3067\u4e0d\u8981\u306a\u30af\u30e9\u30a4\u30a2\u30f3\u30c8\u30a8\u30e9\u30fc\u3092\u907f\u3051\u308b\u305f\u3081\u7a7a\u5fdc\u7b54\u3092\u8fd4\u3059\u3002",
    "avoid static-analysis false positives": "\u751f\u6210\u30ea\u30dd\u30b8\u30c8\u30ea\u3092\u9664\u5916\u3057\u9759\u7684\u89e3\u6790\u306e\u8aa4\u691c\u77e5\u3092\u907f\u3051\u308b\u3002",
    "return an empty list instead of an error": "\u4e0a\u6d41\u30dc\u30c7\u30a3\u304cnull\u306e\u3068\u304d\u30a8\u30e9\u30fc\u3067\u306f\u306a\u304f\u7a7a\u30ea\u30b9\u30c8\u3092\u8fd4\u3059\u3002",
    "avoid sending the app to the error page": "\u7a7a\u30ec\u30b9\u30dd\u30f3\u30b9\u3067\u3053\u306e\u6761\u4ef6\u6642\u306b\u30a2\u30d7\u30ea\u304c\u30a8\u30e9\u30fc\u30da\u30fc\u30b8\u3078\u9077\u79fb\u3059\u308b\u306e\u3092\u9632\u3050\u3002",
    "treat A as a non-error response": "\u505c\u6b62\u30a2\u30ab\u30a6\u30f3\u30c8\u306f\u30a8\u30e9\u30fc\u3067\u306f\u306a\u304f\u5229\u7528\u4e0d\u53ef\u306e\u6b63\u5e38\u30ec\u30b9\u30dd\u30f3\u30b9\u3068\u3057\u3066\u6271\u3046\u3002",
    "mask sensitive paths in logs": "\u30d5\u30a3\u30eb\u30bf\u30fc\u306f\u30a8\u30af\u30b9\u30dd\u30fc\u30c8\u524d\u306b\u30ed\u30b0\u5185\u306e\u6a5f\u5bc6\u30d1\u30b9\u3092\u30de\u30b9\u30ad\u30f3\u30b0\u3059\u308b\u3002",
    "ensure correct masking behavior": "\u30c6\u30b9\u30c8\u30b1\u30fc\u30b9\u3067\u5168\u4fdd\u8b77\u30eb\u30fc\u30c8\u306e\u6b63\u3057\u3044\u30de\u30b9\u30ad\u30f3\u30b0\u52d5\u4f5c\u3092\u4fdd\u8a3c\u3059\u308b\u3002",
    "improve privacy and security in Logging": "\u30de\u30b9\u30ad\u30f3\u30b0\u30eb\u30fc\u30eb\u3067\u30ed\u30b0\u306e\u30d7\u30e9\u30a4\u30d0\u30b7\u30fc\u3068\u30bb\u30ad\u30e5\u30ea\u30c6\u30a3\u3092\u5411\u4e0a\u3055\u305b\u305f\u3002",
    "verify that unrelated endpoints are unaffected": "\u30c6\u30b9\u30c8\u3067\u7121\u95a2\u4fc2\u30a8\u30f3\u30c9\u30dd\u30a4\u30f3\u30c8\u304c\u30de\u30b9\u30ad\u30f3\u30b0\u898f\u5247\u306e\u5f71\u97ff\u3092\u53d7\u3051\u306a\u3044\u3053\u3068\u3092\u78ba\u8a8d\u3057\u305f\u3002",
    "have the potential of leaking A": "\u751f\u30d1\u30b9\u30ea\u30af\u30a8\u30b9\u30c8\u306f\u8a8d\u8a3c\u60c5\u5831\u6f0f\u6d29\u306e\u53ef\u80fd\u6027\u304c\u3042\u3063\u305f\u3002",
    "be consistently masked in logs": "\u6a5f\u5bc6\u8b58\u5225\u5b50\u306f\u30ed\u30b0\u5185\u3067\u4e00\u8cab\u3057\u3066\u30de\u30b9\u30ad\u30f3\u30b0\u3055\u308c\u308b\u3002",
    "store a hash instead of the whole token": "\u30c8\u30fc\u30af\u30f3\u5168\u4f53\u3067\u306f\u306a\u304f\u30cf\u30c3\u30b7\u30e5\u306e\u307f\u3092\u4fdd\u5b58\u3059\u308b\u3002",
    "save memory": "JME\u30c8\u30fc\u30af\u30f3\u5024\u306e\u307f\u4fdd\u5b58\u3057\u30e1\u30e2\u30ea\u3092\u7bc0\u7d04\u3059\u308b\u3002",
    "be unable to make use of exposed records": "\u653b\u6483\u8005\u306f\u6f0f\u6d29\u3057\u305f\u30cf\u30c3\u30b7\u30e5\u8a18\u9332\u3092\u60aa\u7528\u3067\u304d\u306a\u3044\u3002",
    "only merge when": "\u4e21\u30b9\u30c6\u30fc\u30b8\u30f3\u30b0\u74b0\u5883\u304c\u65b0\u30ad\u30fc\u3092\u53d7\u3051\u5165\u308c\u305f\u5834\u5408\u306e\u307f\u30de\u30fc\u30b8\u3059\u308b\u3002",
    "as part of the response to a security review": "\u30c8\u30fc\u30af\u30f3\u6697\u53f7\u5316\u306f\u30bb\u30ad\u30e5\u30ea\u30c6\u30a3\u30ec\u30d3\u30e5\u30fc\u5bfe\u5fdc\u306e\u4e00\u74b0\u3068\u3057\u3066\u66f4\u65b0\u3057\u305f\u3002",
    "add an additional authentication check": "\u3053\u306ePR\u306f\u6a5f\u5bc6\u30a8\u30f3\u30c9\u30dd\u30a4\u30f3\u30c8\u306b\u8ffd\u52a0\u8a8d\u8a3c\u30c1\u30a7\u30c3\u30af\u3092\u52a0\u3048\u308b\u3002",
    "catch failures and latencies": "\u6027\u80fd\u95be\u5024\u304c\u30ea\u30ea\u30fc\u30b9\u524d\u306b\u5931\u6557\u3068\u9045\u5ef6\u3092\u691c\u77e5\u3059\u308b\u3002",
    "track performance by scenario": "\u30ec\u30dd\u30fc\u30c8\u3092\u5206\u5272\u3057\u30b7\u30ca\u30ea\u30aa\u5225\u306b\u6027\u80fd\u3092\u8ffd\u8de1\u3067\u304d\u308b\u3002",
    "reflect real latency": "\u672c\u756a\u30ec\u30a4\u30c6\u30f3\u30b7\u3092\u53cd\u6620\u3059\u308b\u305f\u3081\u30d2\u30b9\u30c8\u30b0\u30e9\u30e0\u4e0a\u9650\u3092\u5f15\u304d\u4e0a\u3052\u305f\u3002",
    "make the metrics inaccurate": "\u30d2\u30b9\u30c8\u30b0\u30e9\u30e0\u4e0a\u9650\u304c\u4f4e\u3059\u304e\u308b\u3068\u30e1\u30c8\u30ea\u30af\u30b9\u304c\u4e0d\u6b63\u78ba\u306b\u306a\u308b\u3002",
    "increase the load considerably": "\u7121\u95a2\u4fc2\u5c5e\u6027\u53d6\u5f97\u306f\u4e0b\u6d41\u30b5\u30fc\u30d3\u30b9\u306e\u8ca0\u8377\u3092\u5927\u5e45\u306b\u5897\u52a0\u3055\u305b\u308b\u53ef\u80fd\u6027\u304c\u3042\u308b\u3002",
    "cause high latency": "\u3053\u306e\u30d1\u30b9\u306e\u7121\u95a2\u4fc2\u5c5e\u6027\u304c\u9ad8\u30ec\u30a4\u30c6\u30f3\u30b7\u3092\u5f15\u304d\u8d77\u3053\u3057\u3066\u3044\u305f\u3002",
    "optimize A not to call B": "\u30b5\u30de\u30ea\u30fc\u30a8\u30f3\u30c9\u30dd\u30a4\u30f3\u30c8\u304c2\u3064\u306e\u4e0b\u6d41\u3092\u547c\u3070\u306a\u3044\u3088\u3046\u6700\u9069\u5316\u3057\u305f\u3002",
    "reduce the number of lines for manageability": "\u7ba1\u7406\u3057\u3084\u3059\u304f\u3059\u308b\u305f\u3081\u30ed\u30b8\u30c3\u30af\u3092\u8907\u6570\u30d5\u30a1\u30a4\u30eb\u306b\u5206\u5272\u3057\u305f\u3002",
    "let us focus on the relevant code": "\u30d8\u30eb\u30d1\u30fc\u306b\u3088\u308a\u30ec\u30d3\u30e5\u30fc\u6642\u306b\u30af\u30e9\u30a4\u30a2\u30f3\u30c8\u30b3\u30fc\u30c9\u3078\u96c6\u4e2d\u3067\u304d\u308b\u3002",
    "ensure compatibility with the latest frameworks": "\u66f4\u65b0\u306f\u6700\u65b0\u30b5\u30dd\u30fc\u30c8\u30d5\u30ec\u30fc\u30e0\u30ef\u30fc\u30af\u3068\u306e\u4e92\u63db\u6027\u3092\u78ba\u4fdd\u3059\u308b\u3002",
    "resolve a production issue": "\u3053\u306e\u30db\u30c3\u30c8\u30d5\u30a3\u30c3\u30af\u30b9\u306f\u30a2\u30c3\u30d7\u30b0\u30ec\u30fc\u30c9\u6e08\u307f\u30a2\u30ab\u30a6\u30f3\u30c8\u306e\u672c\u756a\u4e0d\u5177\u5408\u3092\u89e3\u6d88\u3059\u308b\u3002",
    "preserve a URI template": "\u30eb\u30fc\u30bf\u30fc\u306f\u30e1\u30c8\u30ea\u30af\u30b9\u7528\u306bURI\u30c6\u30f3\u30d7\u30ec\u30fc\u30c8\u3092\u4fdd\u6301\u3059\u308b\u3002",
    "result in high cardinality": "\u30e1\u30c8\u30ea\u30af\u30b9\u30e9\u30d9\u30eb\u306b\u5c55\u958b\u8b58\u5225\u5b50\u3092\u4f7f\u3046\u3068\u9ad8\u30ab\u30fc\u30c7\u30a3\u30ca\u30ea\u30c6\u30a3\u306b\u306a\u308b\u3002",
    "keep metric cardinality low": "\u30eb\u30fc\u30c8\u30c6\u30f3\u30d7\u30ec\u30fc\u30c8\u3067\u52d5\u7684\u30ea\u30af\u30a8\u30b9\u30c8\u306e\u30e1\u30c8\u30ea\u30af\u30b9\u30ab\u30fc\u30c7\u30a3\u30ca\u30ea\u30c6\u30a3\u3092\u4f4e\u304f\u4fdd\u3064\u3002",
    "avoid the same issue when copying and pasting code": "\u30b3\u30d4\u30da\u3067\u540c\u554f\u984c\u304c\u8d77\u304d\u306a\u3044\u3088\u3046\u4ed6\u547c\u3073\u51fa\u3057\u7b87\u6240\u3082\u66f4\u65b0\u3057\u305f\u3002",
    "prioritize user experience": "\u77ed\u6642\u9593\u969c\u5bb3\u3067\u306fUX\u512a\u5148\u3067\u5b89\u5168\u306a\u30d5\u30a9\u30fc\u30eb\u30d0\u30c3\u30af\u3092\u7d9a\u884c\u3059\u308b\u3002",
    "have a limited period of negative impact": "\u72b6\u614b\u5024\u306f\u3059\u3050\u5931\u52b9\u3059\u308b\u305f\u3081\u60aa\u5f71\u97ff\u671f\u9593\u306f\u9650\u5b9a\u7684\u3060\u3002",
    "follow the single-responsibility principle": "\u5358\u4e00\u8cac\u4efb\u539f\u5247\u306b\u5f93\u3044\u30ea\u30dd\u30b8\u30c8\u30ea\u3092\u30b5\u30fc\u30d3\u30b9\u304b\u3089\u5206\u96e2\u3057\u305f\u3002",
    "separate service-level and repository-level tests": "\u7d50\u5408\u30b9\u30a4\u30fc\u30c8\u306f\u30b5\u30fc\u30d3\u30b9\u5c64\u3068\u30ea\u30dd\u30b8\u30c8\u30ea\u5c64\u306e\u30c6\u30b9\u30c8\u3092\u5206\u96e2\u3059\u308b\u3002",
    "be too tightly coupled to a specific use case": "\u5171\u6709\u30d8\u30eb\u30d1\u30fc\u306f\u7279\u5b9a\u753b\u9762\u30d5\u30ed\u30fc\u306b\u5bc6\u7d50\u5408\u3057\u3059\u304e\u3066\u3044\u305f\u3002",
    "move the read path to a dedicated resource": "\u8aad\u307f\u53d6\u308a\u30d1\u30b9\u3092\u6240\u6709\u6a29\u304c\u660e\u78ba\u306a\u5c02\u7528\u30ea\u30bd\u30fc\u30b9\u3078\u79fb\u3057\u305f\u3002",
    "reuse it across multiple surfaces": "\u30ec\u30b9\u30dd\u30f3\u30b9\u3092\u8907\u6570\u753b\u9762\u3067\u91cd\u8907\u30ea\u30af\u30a8\u30b9\u30c8\u306a\u304f\u518d\u5229\u7528\u3067\u304d\u308b\u3002",
    "conduct a size impact analysis": "\u65e2\u5b58\u30ad\u30e3\u30c3\u30b7\u30e5\u3078\u65b0\u30b3\u30f3\u30c6\u30ad\u30b9\u30c8\u4fdd\u5b58\u524d\u306b\u30b5\u30a4\u30ba\u5f71\u97ff\u5206\u6790\u3092\u5b9f\u65bd\u3057\u305f\u3002",
    "have a minimal impact on": "\u8ffd\u52a0\u30a8\u30f3\u30c8\u30ea\u306f\u30ad\u30e3\u30c3\u30b7\u30e5\u5bb9\u91cf\u3078\u306e\u5f71\u97ff\u304c\u6975\u3081\u3066\u5c0f\u3055\u3044\u3002",
    "not move the needle much": "\u3053\u306e\u898f\u6a21\u3067\u306f\u30ad\u30fc\u3092\u3055\u3089\u306b\u77ed\u304f\u3057\u3066\u3082\u5927\u3057\u305f\u5dee\u306f\u751f\u307e\u308c\u306a\u3044\u3002",
    "add a standalone validation and transformation layer": "\u5916\u90e8\u30e1\u30bf\u30c7\u30fc\u30bf\u7528\u306b\u72ec\u7acb\u3057\u305f\u691c\u8a3c\u30fb\u5909\u63db\u5c64\u3092\u8ffd\u52a0\u3057\u305f\u3002",
    "transform flat keys into a nested structure": "\u30a2\u30c0\u30d7\u30bf\u30fc\u304c\u30d5\u30e9\u30c3\u30c8\u30ad\u30fc\u3092\u30af\u30e9\u30a4\u30a2\u30f3\u30c8\u671f\u5f85\u306e\u5165\u308c\u5b50\u69cb\u9020\u3078\u5909\u63db\u3059\u308b\u3002",
    "check that paired values are complete": "\u5909\u63db\u524d\u306b\u30da\u30a2\u306elocate\u5024\u304c\u63c3\u3063\u3066\u3044\u308b\u3053\u3068\u3092\u30d0\u30ea\u30c7\u30fc\u30bf\u304c\u78ba\u8a8d\u3059\u308b\u3002",
    "restrict A to a supported subset": "\u30ec\u30f3\u30c0\u30e9\u30fc\u306fMarkdown\u3092\u30b5\u30dd\u30fc\u30c8\u5bfe\u8c61\u306e\u66f8\u5f0f\u6a5f\u80fd\u306b\u5236\u9650\u3059\u308b\u3002",
    "confirm that there have been no requests for a period": "\u30a8\u30f3\u30c9\u30dd\u30a4\u30f3\u30c8\u524a\u9664\u524d\u306b30\u65e5\u9593\u30ea\u30af\u30a8\u30b9\u30c8\u304c\u306a\u304b\u3063\u305f\u3053\u3068\u3092\u78ba\u8a8d\u3057\u305f\u3002",
    "force tests to be updated when properties change": "\u53b3\u5bc6\u6bd4\u8f03\u3067\u30ec\u30b9\u30dd\u30f3\u30b9\u30d7\u30ed\u30d1\u30c6\u30a3\u5909\u66f4\u6642\u306b\u30c6\u30b9\u30c8\u66f4\u65b0\u3092\u5f37\u8981\u3059\u308b\u3002",
    "ensure consistent handling across the workflow": "\u5171\u6709\u30e2\u30c7\u30eb\u3067\u30ef\u30fc\u30af\u30d5\u30ed\u30fc\u5168\u4f53\u306e\u8b58\u5225\u5b50\u51e6\u7406\u3092\u4e00\u8cab\u3055\u305b\u308b\u3002",
    "ensure that tests reflect the new requirements": "\u65b0\u30c7\u30fc\u30bf\u8981\u4ef6\u3092\u53cd\u6620\u3059\u308b\u305f\u3081\u30d5\u30a3\u30af\u30b9\u30c1\u30e3\u3092\u66f4\u65b0\u3057\u305f\u3002",
    "make the response easier for the client to consume": "boolean\u3092enum\u306b\u7f6e\u304d\u63db\u3048\u30af\u30e9\u30a4\u30a2\u30f3\u30c8\u304c\u6271\u3044\u3084\u3059\u3044\u30ec\u30b9\u30dd\u30f3\u30b9\u306b\u3057\u305f\u3002",
    "align the public contract with the actual semantics": "enum\u3067\u516c\u958b\u5951\u7d04\u3092\u5b9f\u969b\u306e\u72b6\u614b\u610f\u5473\u8ad6\u306b\u9069\u5408\u3055\u305b\u308b\u3002",
}

def slug(term: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")


def word_count(text: str) -> int:
    return len(text.split())


def merge_entries() -> list[dict]:
    merged: list[dict] = []
    for user_index, user in enumerate(USER_ENTRIES):
        term = user["term"]
        if term not in METADATA:
            raise KeyError(f"Missing METADATA for term: {term}")
        if term not in USAGE_EXAMPLE_JA:
            raise KeyError(f"Missing USAGE_EXAMPLE_JA for term: {term}")
        entry = {**METADATA[term], **user}
        entry["usageExampleJa"] = USAGE_EXAMPLE_JA[term]
        entry["scene"] = SCENE
        entry["_user_index"] = user_index
        merged.append(entry)
    merged.sort(
        key=lambda e: (
            DIFFICULTY_ORDER[e["difficulty"]],
            e["_user_index"],
        )
    )
    for entry in merged:
        del entry["_user_index"]
    return merged


def validate(entry: dict, entry_id: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    term = entry["term"]
    if len(entry["description"]) > 120:
        errors.append(f"{entry_id} {term}: description > 120 chars ({len(entry['description'])})")
    if len(entry["descriptionJa"]) > 80:
        warnings.append(f"{entry_id} {term}: descriptionJa > 80 chars ({len(entry['descriptionJa'])})")
    if word_count(entry["usageExample"]) > 25:
        errors.append(
            f"{entry_id} {term}: usageExample > 25 words ({word_count(entry['usageExample'])})"
        )
    if len(entry["usageExampleJa"]) > 80:
        errors.append(
            f"{entry_id} {term}: usageExampleJa > 80 chars ({len(entry['usageExampleJa'])})"
        )
    return errors, warnings


def render(entry: dict, entry_id: str) -> str:
    return (
        "---\n"
        f'id: "{entry_id}"\n'
        f'term: "{entry["term"]}"\n'
        f'type: "{entry["type"]}"\n'
        f'partOfSpeech: "{entry["partOfSpeech"]}"\n'
        f'pronunciation: "{entry["pronunciation"]}"\n'
        f'description: "{entry["description"]}"\n'
        f'descriptionJa: "{entry["descriptionJa"]}"\n'
        f'meaning: "{entry["meaning"]}"\n'
        f'meaningJa: "{entry["meaningJa"]}"\n'
        f'usageExample: "{entry["usageExample"]}"\n'
        f'usageExampleJa: "{entry["usageExampleJa"]}"\n'
        f'difficulty: "{entry["difficulty"]}"\n'
        f'scene: "{SCENE}"\n'
        "---\n"
    )


def main() -> int:
    entries = merge_entries()
    VOCAB_DIR.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    all_errors: list[str] = []
    all_warnings: list[str] = []
    counts = {"Beginner": 0, "Intermediate": 0, "Advanced": 0}

    for idx, entry in enumerate(entries, start=START_ID):
        term = entry["term"]
        if term in seen:
            all_errors.append(f"Duplicate term: {term}")
            continue
        seen.add(term)
        counts[entry["difficulty"]] += 1
        entry_id = f"{idx:04d}"
        errs, warns = validate(entry, entry_id)
        all_errors.extend(errs)
        all_warnings.extend(warns)
        path = VOCAB_DIR / f"{entry_id}_{slug(term)}.md"
        path.write_text(render(entry, entry_id), encoding="utf-8")

    print(f"Wrote {len(entries)} vocabulary files to {VOCAB_DIR}")
    print(
        "Difficulty counts: "
        f"Beginner={counts['Beginner']}, "
        f"Intermediate={counts['Intermediate']}, "
        f"Advanced={counts['Advanced']}"
    )
    if all_warnings:
        print(f"Warnings ({len(all_warnings)}):")
        for warn in all_warnings:
            print(f"  - {warn}")
    if all_errors:
        print(f"Validation failures ({len(all_errors)}):")
        for err in all_errors:
            print(f"  - {err}")
        return 1
    print("All validations passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
