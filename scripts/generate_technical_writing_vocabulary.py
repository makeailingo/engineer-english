#!/usr/bin/env python3
"""Generate Technical Writing vocabulary markdown files (107 entries)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from technical_writing_vocabulary_user_data import USER_ENTRIES

ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = ROOT / "docs" / "vocabulary"
SCENE = "Technical Writing"
START_ID = 570

DIFFICULTY_ORDER = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}

METADATA: dict[str, dict] = {
    'be called to retrieve': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/biː kɔːld tuː rɪˈtriːv/',
        "meaning": 'to be called to retrieve data',
        "description": 'Describe an endpoint invoked synchronously to fetch data such as user settings.',
        "difficulty": 'Intermediate',
    },
    'given a post code': {
        "type": 'phrase',
        "partOfSpeech": 'prepositional phrase',
        "pronunciation": '/ˈɡɪvn ə pəʊst kəʊd/',
        "meaning": 'given a post code',
        "description": 'State an input condition used to return matching results such as addresses.',
        "difficulty": 'Intermediate',
    },
    'during the signup flow': {
        "type": 'phrase',
        "partOfSpeech": 'prepositional phrase',
        "pronunciation": '/ˈdjʊərɪŋ ðə ˈsaɪnʌp fləʊ/',
        "meaning": 'during the signup flow',
        "description": 'Pinpoint when an error or behavior occurs within registration steps.',
        "difficulty": 'Intermediate',
    },
    'have a couple of': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/hæv ə ˈkʌpl əv/',
        "meaning": 'to have a few',
        "description": 'Report a small number of concerns or issues that need attention.',
        "difficulty": 'Intermediate',
    },
    'get rid of': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/ɡet rɪd əv/',
        "meaning": 'to remove or eliminate',
        "description": 'Propose removing an unnecessary layer, field, or component.',
        "difficulty": 'Intermediate',
    },
    'place ... instead': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/pleɪs ɪnˈsted/',
        "meaning": 'to place something elsewhere instead',
        "description": 'Suggest moving validation or logic to a different layer or location.',
        "difficulty": 'Intermediate',
    },
    'here is a list of': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/hɪər ɪz ə lɪst əv/',
        "meaning": 'here is a list of',
        "description": 'Introduce an enumerated list of fields, endpoints, or requirements.',
        "difficulty": 'Intermediate',
    },
    'be ideally required': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/biː aɪˈdiːəli rɪˈkwaɪəd/',
        "meaning": 'to ideally be required',
        "description": 'Propose fields or rules that should ideally be mandatory in a schema.',
        "difficulty": 'Intermediate',
    },
    'if there is a reason': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/ɪf ðeər ɪz ə ˈriːzn/',
        "meaning": 'if there is a reason',
        "description": 'Ask for documentation when an exception or non-standard behavior is kept.',
        "difficulty": 'Intermediate',
    },
    'cannot be required': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/ˈkænɒt biː rɪˈkwaɪəd/',
        "meaning": 'cannot be required',
        "description": 'Ask why a field cannot be mandatory due to a spec or system constraint.',
        "difficulty": 'Intermediate',
    },
    'the following is': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/ðə ˈfɒləʊɪŋ ɪz/',
        "meaning": 'the following is',
        "description": 'Introduce an expected format, example, or specification detail.',
        "difficulty": 'Intermediate',
    },
    'previously classified as out of scope': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/ˈpriːviəsli ˈklæsɪfaɪd æz aʊt əv skəʊp/',
        "meaning": 'previously classified as out of scope',
        "description": 'Contrast a past scope decision with a current change or reconsideration.',
        "difficulty": 'Advanced',
    },
    'be required for': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/biː rɪˈkwaɪəd fɔː/',
        "meaning": 'to be required for',
        "description": 'State that a change is needed for a release, bug fix, or dependency.',
        "difficulty": 'Intermediate',
    },
    'provide detail about': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/prəˈvaɪd ˈdiːteɪl əˈbaʊt/',
        "meaning": 'to provide detail about',
        "description": 'Request detailed explanation of failure conditions or root causes.',
        "difficulty": 'Intermediate',
    },
    'where it is used': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/weər ɪt ɪz juːzd/',
        "meaning": 'where it is used',
        "description": 'Ask which screens, services, or components use a field or property.',
        "difficulty": 'Intermediate',
    },
    'seem to be': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/siːm tuː biː/',
        "meaning": 'to seem to be',
        "description": 'Share a tentative conclusion while investigation is still underway.',
        "difficulty": 'Intermediate',
    },
    'be called when': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/biː kɔːld wen/',
        "meaning": 'to be called when',
        "description": 'Specify the trigger event or user action that invokes an API.',
        "difficulty": 'Intermediate',
    },
    'in addition to': {
        "type": 'phrase',
        "partOfSpeech": 'prepositional phrase',
        "pronunciation": '/ɪn əˈdɪʃn tuː/',
        "meaning": 'in addition to',
        "description": 'Add another issue, requirement, or observation alongside an existing one.',
        "difficulty": 'Intermediate',
    },
    're-raise': {
        "type": 'phrase',
        "partOfSpeech": 'verb',
        "pronunciation": '/riː reɪz/',
        "meaning": 'to re-raise',
        "description": 'Bring up a previously discussed requirement again before implementation.',
        "difficulty": 'Intermediate',
    },
    'be relevant to': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/biː ˈreləvənt tuː/',
        "meaning": 'to be relevant to',
        "description": 'Point out topics tied to a specific feature, flow, or area.',
        "difficulty": 'Intermediate',
    },
    'still out of scope': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/stɪl aʊt əv skəʊp/',
        "meaning": 'still out of scope',
        "description": 'Ask whether a scenario remains excluded from the current scope.',
        "difficulty": 'Intermediate',
    },
    'be used in some screens': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/biː juːzd ɪn sʌm skriːnz/',
        "meaning": 'to be used in some screens',
        "description": 'Indicate a status or field appears across multiple UI screens.',
        "difficulty": 'Intermediate',
    },
    'return a URL string': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/rɪˈtɜːn ə juː ɑːr el strɪŋ/',
        "meaning": 'to return a URL string',
        "description": 'Describe an endpoint response type and its purpose for next steps.',
        "difficulty": 'Intermediate',
    },
    'be opened in a webview': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/biː ˈəʊpənd ɪn ə ˈwebvjuː/',
        "meaning": 'to be opened in a webview',
        "description": 'Explain how the client should display a returned URL.',
        "difficulty": 'Intermediate',
    },
    'this issue is to create': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/ðɪs ˈɪʃuː ɪz tuː kriˈeɪt/',
        "meaning": 'this issue is to create',
        "description": 'State the goal of an issue, such as adding a new endpoint.',
        "difficulty": 'Intermediate',
    },
    'the steps are': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/ðə steps ɑː/',
        "meaning": 'the steps are',
        "description": 'Begin documenting a procedure, flow, or reproduction sequence.',
        "difficulty": 'Intermediate',
    },
    'send a POST request': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/send ə pəʊst rɪˈkwest/',
        "meaning": 'to send a POST request',
        "description": 'Describe client behavior using a specific HTTP method.',
        "difficulty": 'Intermediate',
    },
    'generate random values': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/ˈdʒenəreɪt ˈrændəm ˈvæljuːz/',
        "meaning": 'to generate random values',
        "description": 'Explain security or validation behavior that creates random values.',
        "difficulty": 'Intermediate',
    },
    'open a modal': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/ˈəʊpən ə ˈməʊdl/',
        "meaning": 'to open a modal',
        "description": 'Specify UI behavior such as opening a modal for external auth.',
        "difficulty": 'Intermediate',
    },
    'redirect URL': {
        "type": 'phrase',
        "partOfSpeech": 'noun phrase',
        "pronunciation": '/ˌriːdəˈrekt juː ɑːr el/',
        "meaning": 'redirect URL',
        "description": 'Refer to the callback or return URL used after external verification.',
        "difficulty": 'Intermediate',
    },
    'with data in query parameters': {
        "type": 'phrase',
        "partOfSpeech": 'prepositional phrase',
        "pronunciation": '/wɪð ˈdeɪtə ɪn ˈkwɪəri pəˈræmɪtəz/',
        "meaning": 'with data in query parameters',
        "description": 'Describe passing result data via URL query parameters.',
        "difficulty": 'Intermediate',
    },
    'call the following endpoints': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/kɔːl ðə ˈfɒləʊɪŋ ˈendpɔɪnts/',
        "meaning": 'to call the following endpoints',
        "description": 'List subsequent API calls the client should make in order.',
        "difficulty": 'Intermediate',
    },
    'be combined into one': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/biː kəmˈbaɪnd ˈɪntuː wʌn/',
        "meaning": 'to be combined into one',
        "description": 'Propose merging multiple checks or requests into a single call.',
        "difficulty": 'Intermediate',
    },
    'using this algorithm': {
        "type": 'phrase',
        "partOfSpeech": 'prepositional phrase',
        "pronunciation": '/ˈjuːzɪŋ ðɪs ˈælɡərɪðəm/',
        "meaning": 'using this algorithm',
        "description": 'Refer to a specific validation or processing algorithm in specs.',
        "difficulty": 'Intermediate',
    },
    'for the scope of': {
        "type": 'phrase',
        "partOfSpeech": 'prepositional phrase',
        "pronunciation": '/fɔː ðə skəʊp əv/',
        "meaning": 'for the scope of',
        "description": 'Limit what is supported or in scope for a release or document.',
        "difficulty": 'Intermediate',
    },
    'need to pass through': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/niːd tuː pɑːs θruː/',
        "meaning": 'to need to pass through',
        "description": 'Instruct a BFF or proxy to forward headers or values upstream.',
        "difficulty": 'Intermediate',
    },
    'create tasks for': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/kriˈeɪt tɑːsks fɔː/',
        "meaning": 'to create tasks for',
        "description": 'Break work into follow-up tasks for contract and implementation updates.',
        "difficulty": 'Intermediate',
    },
    'update the specification': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/ˈʌpdeɪt ðə ˌspesɪfɪˈkeɪʃn/',
        "meaning": 'to update the specification',
        "description": 'Direct changes to OpenAPI, contract, or design documents before coding.',
        "difficulty": 'Intermediate',
    },
    'the actual implementation': {
        "type": 'phrase',
        "partOfSpeech": 'noun phrase',
        "pronunciation": '/ði ˈæktʃuəl ˌɪmplɪmenˈteɪʃn/',
        "meaning": 'the actual implementation',
        "description": 'Contrast written specification with what the code actually does.',
        "difficulty": 'Intermediate',
    },
    'revise the implementation': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/rɪˈvaɪz ði ˌɪmplɪmenˈteɪʃn/',
        "meaning": 'to revise the implementation',
        "description": 'Ask for code changes such as adopting a shared client library.',
        "difficulty": 'Intermediate',
    },
    'support ... with ...': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/səˈpɔːt wɪð/',
        "meaning": 'to support something with something',
        "description": 'Require shared defaults alongside per-case configuration or handlers.',
        "difficulty": 'Intermediate',
    },
    'make a few requests related to': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/meɪk ə fjuː rɪˈkwests rɪˈleɪtɪd tuː/',
        "meaning": 'to make a few requests related to',
        "description": 'Politely introduce several change requests about one API or area.',
        "difficulty": 'Intermediate',
    },
    'make ... the same as': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/meɪk ðə seɪm æz/',
        "meaning": 'to make the same as',
        "description": 'Ask to align schemas or properties with an existing definition.',
        "difficulty": 'Intermediate',
    },
    'have the same meaning as': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/hæv ðə seɪm ˈmiːnɪŋ æz/',
        "meaning": 'to have the same meaning as',
        "description": 'Explain that two fields or tags represent the same concept.',
        "difficulty": 'Intermediate',
    },
    'perform logic related to': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/pəˈfɔːm ˈlɒdʒɪk rɪˈleɪtɪd tuː/',
        "meaning": 'to perform logic related to',
        "description": 'Direct backend work on business rules such as eligibility checks.',
        "difficulty": 'Intermediate',
    },
    'rename ... to ...': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/riːˈneɪm tuː/',
        "meaning": 'to rename to',
        "description": 'Propose renaming a field to better reflect its actual meaning.',
        "difficulty": 'Intermediate',
    },
    'fill ... using': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/fɪl ˈjuːzɪŋ/',
        "meaning": 'to fill using',
        "description": 'Describe populating a field from an upstream response or source.',
        "difficulty": 'Intermediate',
    },
    'on the backend side': {
        "type": 'phrase',
        "partOfSpeech": 'prepositional phrase',
        "pronunciation": '/ɒn ðə ˈbækend saɪd/',
        "meaning": 'on the backend side',
        "description": 'Clarify that validation or processing should happen server-side.',
        "difficulty": 'Intermediate',
    },
    'only necessary to': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/ˈəʊnli ˈnesəsəri tuː/',
        "meaning": 'only necessary to',
        "description": 'State the minimum action required, such as setting a field on create.',
        "difficulty": 'Intermediate',
    },
    'not during': {
        "type": 'phrase',
        "partOfSpeech": 'prepositional phrase',
        "pronunciation": '/nɒt ˈdjʊərɪŋ/',
        "meaning": 'not during',
        "description": 'Restrict when a rule applies, such as excluding partial updates.',
        "difficulty": 'Intermediate',
    },
    'partial updates': {
        "type": 'phrase',
        "partOfSpeech": 'noun phrase',
        "pronunciation": '/ˈpɑːʃl ˈʌpdeɪts/',
        "meaning": 'partial updates',
        "description": 'Refer to PATCH-style updates that change only some fields.',
        "difficulty": 'Intermediate',
    },
    'replace ... with ...': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/rɪˈpleɪs wɪð/',
        "meaning": 'to replace with',
        "description": 'Propose swapping a response payload or behavior for another.',
        "difficulty": 'Intermediate',
    },
    'no-content status': {
        "type": 'phrase',
        "partOfSpeech": 'noun phrase',
        "pronunciation": '/nəʊ ˈkɒntent ˈsteɪtəs/',
        "meaning": 'no-content status',
        "description": 'Recommend a 204-style response when no body should be returned.',
        "difficulty": 'Intermediate',
    },
    "returning ... isn't meaningful": {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/rɪˈtɜːnɪŋ ˈɪznt ˈmiːnɪŋfl/',
        "meaning": 'returning is not meaningful',
        "description": 'Argue against returning an empty or useless success payload.',
        "difficulty": 'Advanced',
    },
    'thus': {
        "type": 'phrase',
        "partOfSpeech": 'adverb',
        "pronunciation": '/ðʌs/',
        "meaning": 'thus; therefore',
        "description": 'Draw a formal logical conclusion from a prior statement in specs.',
        "difficulty": 'Beginner',
    },
    'be suitable': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/biː ˈsuːtəbl/',
        "meaning": 'to be suitable',
        "description": 'Say a proposed response type or approach fits the requirements.',
        "difficulty": 'Intermediate',
    },
    'required endpoints': {
        "type": 'phrase',
        "partOfSpeech": 'noun phrase',
        "pronunciation": '/rɪˈkwaɪəd ˈendpɔɪnts/',
        "meaning": 'required endpoints',
        "description": 'Introduce the list of endpoints that must be implemented.',
        "difficulty": 'Intermediate',
    },
    'current flow': {
        "type": 'phrase',
        "partOfSpeech": 'noun phrase',
        "pronunciation": '/ˈkʌrənt fləʊ/',
        "meaning": 'current flow',
        "description": 'Describe how the system works today before proposing changes.',
        "difficulty": 'Intermediate',
    },
    'check if ... is available': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/tʃek ɪf ɪz əˈveɪləbl/',
        "meaning": 'to check if available',
        "description": 'Require a precondition check on an external service or feature.',
        "difficulty": 'Intermediate',
    },
    'not undergoing maintenance': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/nɒt ˌʌndəˈɡəʊɪŋ ˈmeɪntənəns/',
        "meaning": 'not undergoing maintenance',
        "description": 'State that requests proceed only when the service is not in maintenance.',
        "difficulty": 'Intermediate',
    },
    'encrypt ... using ...': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/ɪnˈkrɪpt ˈjuːzɪŋ/',
        "meaning": 'to encrypt using',
        "description": 'Specify encryption of a value with a named or configured key.',
        "difficulty": 'Intermediate',
    },
    'log in ... using ...': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/lɒɡ ɪn ˈjuːzɪŋ/',
        "meaning": 'to log in using',
        "description": 'Describe authenticating to an external provider with a credential.',
        "difficulty": 'Intermediate',
    },
    'update records with': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/ˈʌpdeɪt ˈrekɔːdz wɪð/',
        "meaning": 'to update records with',
        "description": 'Instruct updating stored records using returned identifiers or data.',
        "difficulty": 'Intermediate',
    },
    'response body is ignored': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/rɪˈspɒns ˈbɒdi ɪz ɪɡˈnɔːd/',
        "meaning": 'response body is ignored',
        "description": 'Note that only the status code matters and the body is discarded.',
        "difficulty": 'Intermediate',
    },
    'even though': {
        "type": 'phrase',
        "partOfSpeech": 'conjunction',
        "pronunciation": '/ˈiːvn ðəʊ/',
        "meaning": 'even though',
        "description": 'Highlight behavior that contradicts an expected convention.',
        "difficulty": 'Intermediate',
    },
    'user might need to': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/ˈjuːzə maɪt niːd tuː/',
        "meaning": 'user might need to',
        "description": 'Warn about a possible user action such as re-authentication.',
        "difficulty": 'Intermediate',
    },
    'through a third-party page': {
        "type": 'phrase',
        "partOfSpeech": 'prepositional phrase',
        "pronunciation": '/θruː ə ˌθɜːd ˈpɑːti peɪdʒ/',
        "meaning": 'through a third-party page',
        "description": 'Explain authentication completed via an external provider page.',
        "difficulty": 'Intermediate',
    },
    'must consent to': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/mʌst kənˈsent tuː/',
        "meaning": 'must consent to',
        "description": 'Require user consent before continuing a sensitive flow.',
        "difficulty": 'Intermediate',
    },
    'validate ... against ...': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/ˈvælɪdeɪt əˈɡenst/',
        "meaning": 'to validate against',
        "description": 'Direct comparing submitted data with verified or reference data.',
        "difficulty": 'Intermediate',
    },
    'be sent': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/biː sent/',
        "meaning": 'to be sent',
        "description": 'Describe delivery of a code or message to the user automatically.',
        "difficulty": 'Intermediate',
    },
    'finalize': {
        "type": 'phrase',
        "partOfSpeech": 'verb',
        "pronunciation": '/ˈfaɪnəlaɪz/',
        "meaning": 'to finalize',
        "description": 'Complete the last step of a process such as account linkage.',
        "difficulty": 'Beginner',
    },
    'for the first step': {
        "type": 'phrase',
        "partOfSpeech": 'prepositional phrase',
        "pronunciation": '/fɔː ðə fɜːst step/',
        "meaning": 'for the first step',
        "description": 'Set conditions or behavior for the initial stage of a multi-step flow.',
        "difficulty": 'Intermediate',
    },
    'provide a fallback': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/prəˈvaɪd ə ˈfɔːlbæk/',
        "meaning": 'to provide a fallback',
        "description": 'Require an alternate path when a primary value or service is missing.',
        "difficulty": 'Intermediate',
    },
    'if available': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/ɪf əˈveɪləbl/',
        "meaning": 'if available',
        "description": 'Apply optional data or behavior only when the value exists.',
        "difficulty": 'Beginner',
    },
    'not ... but a request for ...': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/nɒt bət ə rɪˈkwest fɔː/',
        "meaning": 'not but a request for',
        "description": 'Clarify an issue is a platform request rather than a backend bug.',
        "difficulty": 'Advanced',
    },
    'when performing': {
        "type": 'phrase',
        "partOfSpeech": 'prepositional phrase',
        "pronunciation": '/wen pəˈfɔːmɪŋ/',
        "meaning": 'when performing',
        "description": 'Scope a requirement to a specific operation such as account linkage.',
        "difficulty": 'Intermediate',
    },
    'redirect back to': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/ˌriːdəˈrekt bæk tuː/',
        "meaning": 'to redirect back to',
        "description": 'Describe returning the user to a callback or original page after auth.',
        "difficulty": 'Intermediate',
    },
    'however': {
        "type": 'phrase',
        "partOfSpeech": 'adverb',
        "pronunciation": '/haʊˈevə/',
        "meaning": 'however',
        "description": 'Introduce a contrast or problem that contradicts a prior statement.',
        "difficulty": 'Beginner',
    },
    'the true target is': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/ðə truː ˈtɑːɡɪt ɪz/',
        "meaning": 'the true target is',
        "description": 'Contrast the apparent destination with the correct navigation target.',
        "difficulty": 'Intermediate',
    },
    'with an extra action before': {
        "type": 'phrase',
        "partOfSpeech": 'prepositional phrase',
        "pronunciation": '/wɪð ən ˈekstrə ˈækʃn bɪˈfɔː/',
        "meaning": 'with an extra action before',
        "description": 'Describe an additional step required before redirection occurs.',
        "difficulty": 'Intermediate',
    },
    'easy to set up': {
        "type": 'phrase',
        "partOfSpeech": 'adjective phrase',
        "pronunciation": '/ˈiːzi tuː set ʌp/',
        "meaning": 'easy to set up',
        "description": 'Note that a redirect or integration is straightforward to configure.',
        "difficulty": 'Intermediate',
    },
    'lose some information': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/luːz sʌm ˌɪnfəˈmeɪʃn/',
        "meaning": 'to lose some information',
        "description": 'Explain data lost during redirection or migration without a parameter.',
        "difficulty": 'Intermediate',
    },
    'it would be nice if': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/ɪt wʊd biː naɪs ɪf/',
        "meaning": 'it would be nice if',
        "description": 'Express a non-blocking improvement wish in specs or reviews.',
        "difficulty": 'Intermediate',
    },
    'include ... in ...': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/ɪnˈkluːd ɪn/',
        "meaning": 'to include in',
        "description": 'Direct adding an identifier or value to launch or request parameters.',
        "difficulty": 'Intermediate',
    },
    'solve this minor problem': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/sɒlv ðɪs ˈmaɪnə ˈprɒbləm/',
        "meaning": 'to solve this minor problem',
        "description": 'Propose a small fix that addresses a low-impact issue.',
        "difficulty": 'Intermediate',
    },
    'caused by': {
        "type": 'phrase',
        "partOfSpeech": 'prepositional phrase',
        "pronunciation": '/kɔːzd baɪ/',
        "meaning": 'caused by',
        "description": 'State the root cause of a regression or failure clearly.',
        "difficulty": 'Beginner',
    },
    'missing required non-nullable field': {
        "type": 'phrase',
        "partOfSpeech": 'noun phrase',
        "pronunciation": '/ˈmɪsɪŋ rɪˈkwaɪəd nɒn ˈnʌləbl fiːld/',
        "meaning": 'missing required non-nullable field',
        "description": 'Name a schema mismatch where a required non-null field is absent.',
        "difficulty": 'Advanced',
    },
    'be thrown': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/biː θrəʊn/',
        "meaning": 'to be thrown',
        "description": 'Describe an exception raised during deserialization or processing.',
        "difficulty": 'Intermediate',
    },
    'apparently': {
        "type": 'phrase',
        "partOfSpeech": 'adverb',
        "pronunciation": '/əˈpærəntli/',
        "meaning": 'apparently',
        "description": 'Share an observed behavior that is not yet fully confirmed.',
        "difficulty": 'Beginner',
    },
    're-throw ... as ...': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/riː θrəʊ æz/',
        "meaning": 'to re-throw as',
        "description": 'Explain converting one exception into another generic type.',
        "difficulty": 'Advanced',
    },
    'cause ... to be ...': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/kɔːz tuː biː/',
        "meaning": 'to cause to be',
        "description": 'Describe how a mapping or change leads to a misleading result.',
        "difficulty": 'Intermediate',
    },
    'the request succeeded': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/ðə rɪˈkwest səkˈsiːdɪd/',
        "meaning": 'the request succeeded',
        "description": 'Separate HTTP success from a later parsing or handling failure.',
        "difficulty": 'Intermediate',
    },
    'the caller is expecting': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/ðə ˈkɔːlər ɪz ɪkˈspektɪŋ/',
        "meaning": 'the caller is expecting',
        "description": 'Highlight mismatch between client expectations and provider behavior.',
        "difficulty": 'Intermediate',
    },
    'not provided by upstream anymore': {
        "type": 'phrase',
        "partOfSpeech": 'clause',
        "pronunciation": '/nɒt prəˈvaɪdɪd baɪ ˈʌpstr iːm ˈeni mɔː/',
        "meaning": 'not provided by upstream anymore',
        "description": 'Note upstream no longer returns fields the client still expects.',
        "difficulty": 'Intermediate',
    },
    'slightly misleading': {
        "type": 'phrase',
        "partOfSpeech": 'adjective phrase',
        "pronunciation": '/ˈslaɪtli mɪsˈliːdɪŋ/',
        "meaning": 'slightly misleading',
        "description": 'Point out an error message that is not fully wrong but confusing.',
        "difficulty": 'Intermediate',
    },
    'detect ... was caused by ...': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/dɪˈtekt wɒz kɔːzd baɪ/',
        "meaning": 'to detect was caused by',
        "description": 'Require detecting whether a failure stemmed from a specific root cause.',
        "difficulty": 'Advanced',
    },
    'identify this issue': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/aɪˈdentɪfaɪ ðɪs ˈɪʃuː/',
        "meaning": 'to identify this issue',
        "description": 'Explain how a changeset or investigation surfaced the problem.',
        "difficulty": 'Intermediate',
    },
    'be missing from': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/biː ˈmɪsɪŋ frɒm/',
        "meaning": 'to be missing from',
        "description": 'State that an expected property is absent from a schema or payload.',
        "difficulty": 'Intermediate',
    },
    'expect ... in a request': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/ɪkˈspekt ɪn ə rɪˈkwest/',
        "meaning": 'to expect in a request',
        "description": 'Describe a field or status the API definition requires in requests.',
        "difficulty": 'Intermediate',
    },
    'as seen here': {
        "type": 'phrase',
        "partOfSpeech": 'adverbial phrase',
        "pronunciation": '/æz siːn hɪər/',
        "meaning": 'as seen here',
        "description": 'Point to code or an example as evidence for a requirement.',
        "difficulty": 'Intermediate',
    },
    'in the request schema': {
        "type": 'phrase',
        "partOfSpeech": 'prepositional phrase',
        "pronunciation": '/ɪn ðə rɪˈkwest ˈskiːmə/',
        "meaning": 'in the request schema',
        "description": 'Ground a statement in how the request schema defines a property.',
        "difficulty": 'Intermediate',
    },
    'be defined': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/biː dɪˈfaɪnd/',
        "meaning": 'to be defined',
        "description": 'Confirm a field exists in the specification or schema.',
        "difficulty": 'Intermediate',
    },
    'reference another schema': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/ˈrefrəns əˈnʌðə ˈskiːmə/',
        "meaning": 'to reference another schema',
        "description": 'Explain schema reuse or dependency between OpenAPI components.',
        "difficulty": 'Intermediate',
    },
    'add the property': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/æd ðə ˈprɒpəti/',
        "meaning": 'to add the property',
        "description": 'Propose adding a missing property to a shared schema.',
        "difficulty": 'Intermediate',
    },
    'resolve this issue': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/rɪˈzɒlv ðɪs ˈɪʃuː/',
        "meaning": 'to resolve this issue',
        "description": 'Link a proposed change directly to fixing the reported problem.',
        "difficulty": 'Intermediate',
    },
    'improve test coverage': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/ɪmˈpruːv test ˈkʌvərɪdʒ/',
        "meaning": 'to improve test coverage',
        "description": 'State a goal to add tests, often for error handling paths.',
        "difficulty": 'Intermediate',
    },
    'leverage the power of': {
        "type": 'phrase',
        "partOfSpeech": 'verb phrase',
        "pronunciation": '/ˈlevərɪdʒ ðə ˈpaʊər əv/',
        "meaning": 'to leverage the power of',
        "description": 'Propose using a tool or mechanism such as generated tests effectively.',
        "difficulty": 'Intermediate',
    },
}

USAGE_EXAMPLE_JA: dict[str, str] = {
    'be called to retrieve': 'このエンドポイントはユーザーの現在の設定を取得するために呼び出される。',
    'given a post code': 'サービスは郵便番号を指定して住所候補を返す。',
    'during the signup flow': 'エラーは登録フロー中に発生する。',
    'have a couple of': '対応が必要な互換性の懸念がいくつかある。',
    'get rid of': '冗長な変換レイヤーを取り除きたい。',
    'place ... instead': 'このバリデーションは代わりにバックエンドに置くべきだ。',
    'here is a list of': '以下が検証が必要なフィールドの一覧です。',
    'be ideally required': 'これらのフィールドはスキーマ上、理想的には必須である。',
    'if there is a reason': 'この挙動を残す理由がある場合は、文書化してください。',
    'cannot be required': 'このフィールドを必須にできない理由を説明してください。',
    'the following is': '以下が期待されるレスポンス形式です。',
    'previously classified as out of scope': 'この処理は以前は対象外と分類されていた。',
    'be required for': 'この変更は次のリリースに必要である。',
    'provide detail about': '文書は障害条件について詳細を提供すべきだ。',
    'where it is used': '文書はどこで使用されているかを説明すべきだ。',
    'seem to be': '問題は移行済みアカウントに限定されているようだ。',
    'be called when': 'APIはユーザーが変更を確認したときに呼び出される。',
    'in addition to': 'タイムアウトに加えて、重複リクエストも観測した。',
    're-raise': '実装開始前に、この要件を再度提起したい。',
    'be relevant to': 'これらの点はアカウント復旧フローに関連している。',
    'still out of scope': 'このシナリオがまだ対象外なら、確認してください。',
    'be used in some screens': 'このステータスはいくつかの画面でナビゲーション制御に使われる。',
    'return a URL string': 'エンドポイントは次のステップ用にURL文字列を返す。',
    'be opened in a webview': '返されたURLはWebViewで開かれる。',
    'this issue is to create': 'このIssueの目的はアカウント復旧用エンドポイントを作成することです。',
    'the steps are': '手順は以下のとおりです。',
    'send a POST request': 'クライアントはユーザー確認後にPOSTリクエストを送信する。',
    'generate random values': 'システムはリクエスト検証用に2つのランダム値を生成する。',
    'open a modal': 'アプリは外部認証用のモーダルを開く。',
    'redirect URL': 'プロバイダーはリダイレクトURL経由で結果を返す。',
    'with data in query parameters': 'プロバイダーはクエリパラメータにデータを含めて結果を送る。',
    'call the following endpoints': 'クライアントは続けて以下のエンドポイントを呼び出す。',
    'be combined into one': 'この2つのチェックは1つのリクエストに統合できる。',
    'using this algorithm': 'このアルゴリズムを使ってデータを検証すべきだ。',
    'for the scope of': 'このリリースのスコープでは、新フローのみがサポートされる。',
    'need to pass through': 'BFFは相関ヘッダーを上流サービスへそのまま通過させる必要がある。',
    'create tasks for': '契約と実装更新のタスクを作成すべきだ。',
    'update the specification': '実装前に仕様書を更新する必要がある。',
    'the actual implementation': '仕様と実際の実装は一致したままでなければならない。',
    'revise the implementation': '共有クライアントを使うよう実装を見直してください。',
    'support ... with ...': 'クライアントは個別エラーハンドラ付きの共有設定をサポートすべきだ。',
    'make a few requests related to': '登録APIに関していくつか要望を出したい。',
    'make ... the same as': 'このスキーマを既存リクエストスキーマと同じにできますか？',
    'have the same meaning as': 'このタグは既存のステータスフィールドと同じ意味を持つ。',
    'perform logic related to': 'バックエンドはキャンペーン適格性に関連するロジックを実行する必要がある。',
    'rename ... to ...': '実際の意味を反映するようこのフィールド名を変更できますか？',
    'fill ... using': '上流レスポンスを使ってこのフィールドを設定できる。',
    'on the backend side': 'バリデーションはバックエンド側で実行すべきだ。',
    'only necessary to': '作成時にこのフィールドを設定するだけでよい。',
    'not during': '作成時に値を設定するが、部分更新時には設定しない。',
    'partial updates': '部分更新をサポートするPATCHエンドポイントを追加する。',
    'replace ... with ...': '成功ペイロードを本文なしレスポンスに置き換える。',
    'no-content status': 'レスポンスにペイロードがない場合、本文なしステータスが適切だ。',
    "returning ... isn't meaningful": '空の成功メッセージを返すのは意味がない。',
    'thus': 'レスポンスに本文がない。したがって本文なしステータスが適切だ。',
    'be suitable': '本文なしレスポンスはこの操作に適切だ。',
    'required endpoints': '必要なエンドポイントは以下に示す。',
    'current flow': '現在のフローでは上流呼び出しが3回必要だ。',
    'check if ... is available': '外部サービスが利用可能か確認する。',
    'not undergoing maintenance': 'サービスがメンテナンス中でない場合のみリクエストが進む。',
    'encrypt ... using ...': '設定されたキーを使って識別子を暗号化する。',
    'log in ... using ...': '暗号化した識別子を使ってプロバイダーにログインする。',
    'update records with': '返された識別子で認証レコードを更新する。',
    'response body is ignored': 'ステータスコードのみ必要なため、レスポンス本文は無視される。',
    'even though': 'POSTを使うにもかかわらず、エンドポイントはデータを取得する。',
    'user might need to': '移行後、ユーザーは再認証が必要になるかもしれない。',
    'through a third-party page': '認証は外部ページを介して完了する。',
    'must consent to': '続行する前に、ユーザーは情報共有に同意しなければならない。',
    'validate ... against ...': '提出プロフィールを検証済み本人データと照合する。',
    'be sent': 'ユーザーにはワンタイム認可コードが送信される。',
    'finalize': '検証成功後、アカウント連携を完了させる。',
    'for the first step': '最初のステップでは、クライアントはキャッシュ識別子を再利用すべきだ。',
    'provide a fallback': '主要な値がない場合、クライアントは代替手段を提供すべきだ。',
    'if available': '利用可能であればキャッシュ識別子を使う。',
    'not ... but a request for ...': 'これはバックエンド不具合ではなく、プラットフォーム支援の要請だ。',
    'when performing': 'アカウント連携を行う際は、元のstate値を保持する。',
    'redirect back to': 'プロバイダーはユーザーをコールバックページへリダイレクトして戻す。',
    'however': 'しかし、新アプリにはコールバックパスが存在しない。',
    'the true target is': '実際の遷移先はアカウント設定ページである。',
    'with an extra action before': '同じページだが、リダイレクト前に追加アクションがある。',
    'easy to set up': 'クライアントサービスではリダイレクト設定が簡単だ。',
    'lose some information': 'このパラメータがないと、リダイレクト中に一部情報が失われる。',
    'it would be nice if': 'リダイレクトが元のアクションを保持できればよい。',
    'include ... in ...': '起動パラメータにソース識別子を含める。',
    'solve this minor problem': '追加パラメータでこの軽微な問題を解決できる。',
    'caused by': 'リグレッションは契約変更によって引き起こされた。',
    'missing required non-nullable field': 'レスポンスに必須のnull不可フィールドの欠落がある。',
    'be thrown': 'この場合、デシリアライズ例外がスローされる。',
    'apparently': 'クライアントはどうやら元の例外をラップしている。',
    're-throw ... as ...': 'クライアントはパースエラーを汎用例外として再スローする。',
    'cause ... to be ...': 'このマッピングによりエラーメッセージが誤解を招く結果になる。',
    'the request succeeded': 'リクエストは成功したが、レスポンス解析に失敗した。',
    'the caller is expecting': '呼び出し側はプロバイダーが返さなくなったフィールドを期待している。',
    'not provided by upstream anymore': 'これらのフィールドは上流からはもう提供されていない。',
    'slightly misleading': '現在のエラーメッセージはやや誤解を招く。',
    'detect ... was caused by ...': '障害がデータ欠落によって起きたか検出すべきだ。',
    'identify this issue': '変更セットがこの問題の特定に役立った。',
    'be missing from': '必須プロパティがリクエストスキーマから欠落している。',
    'expect ... in a request': 'APIはリクエストにこのステータスを要求する。',
    'as seen here': 'ここで確認できるように、ハンドラはこのフィールドを要求する。',
    'in the request schema': 'リクエストスキーマでは、このプロパティは必須とマークされている。',
    'be defined': 'フィールドはリクエストスキーマで定義されている。',
    'reference another schema': 'このスキーマは共有フィールド用に別スキーマを参照する。',
    'add the property': '共有スキーマにそのプロパティを追加できますか？',
    'resolve this issue': '不足フィールドを追加してこの問題を解決する。',
    'improve test coverage': 'エラーハンドリングのテストカバレッジを改善したい。',
    'leverage the power of': '生成テストの力を活用してエッジケースをカバーできる。',
}

def slug(term: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")


def word_count(text: str) -> int:
    return len(text.split())


def load_existing_terms() -> set[str]:
    terms: set[str] = set()
    if not VOCAB_DIR.exists():
        return terms
    term_re = re.compile(r'^term:\s*"(.*)"\s*$')
    for path in VOCAB_DIR.glob("*.md"):
        for line in path.read_text(encoding="utf-8").splitlines():
            match = term_re.match(line)
            if match:
                terms.add(match.group(1))
                break
    return terms


def merge_entries() -> tuple[list[dict], list[str]]:
    existing = load_existing_terms()
    skipped: list[str] = []
    merged: list[dict] = []
    for user_index, user in enumerate(USER_ENTRIES):
        term = user["term"]
        if term in existing:
            skipped.append(term)
            continue
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
    return merged, skipped


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
    entries, skipped = merge_entries()
    VOCAB_DIR.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    all_errors: list[str] = []
    all_warnings: list[str] = []
    counts = {"Beginner": 0, "Intermediate": 0, "Advanced": 0}

    if skipped:
        print(f"Skipped duplicates ({len(skipped)}):")
        for term in skipped:
            print(f"  - {term}")

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
