#!/usr/bin/env python3
"""Generate Management vocabulary markdown files (100 entries)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from management_vocabulary_user_data import USER_ENTRIES

ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = ROOT / "docs" / "vocabulary"
SCENE = "Management"
START_ID = 677

DIFFICULTY_ORDER = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}

METADATA: dict[str, dict] = {
    "raise awareness": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/reɪz əˈweənəs/",
        "meaning": "to raise awareness",
        "description": "Share dependency importance so the team understands risks before committing to a timeline.",
        "difficulty": "Intermediate",
    },
    "get everyone on the same page": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɡet ˈevriwʌn ɒn ðə seɪm peɪdʒ/",
        "meaning": "to align everyone's understanding",
        "description": "Align team understanding before assigning owners or making decisions.",
        "difficulty": "Intermediate",
    },
    "tackle different aspects of the same problem": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈtækl ˈdɪfrənt ˈæspekts əv ðə seɪm ˈprɒbləm/",
        "meaning": "to address different facets of one issue",
        "description": "Note two groups work on different facets of one issue and urge coordination.",
        "difficulty": "Advanced",
    },
    "simplify the participation of": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈsɪmplɪfaɪ ðə pɑːtɪsɪˈpeɪʃn əv/",
        "meaning": "to simplify involvement of",
        "description": "Reduce central review involvement to the minimum needed for a pilot.",
        "difficulty": "Intermediate",
    },
    "figure out the details later": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈfɪɡə aʊt ðə ˈdiːteɪlz ˈleɪtə/",
        "meaning": "to defer detailed discussion",
        "description": "Agree on direction first and defer detailed discussion to avoid churn.",
        "difficulty": "Intermediate",
    },
    "come back to this once we have an alpha version": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/kʌm bæk tuː ðɪs wʌns wiː hæv ən ˈælfə ˈvɜːʃn/",
        "meaning": "to revisit after an alpha version exists",
        "description": "Defer governance decisions until an alpha version enables concrete validation.",
        "difficulty": "Advanced",
    },
    "bring the topic to your attention": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/brɪŋ ðə ˈtɒpɪk tuː jɔːr əˈtenʃn/",
        "meaning": "to bring a topic to someone's attention",
        "description": "Escalate an important issue politely before a planning meeting.",
        "difficulty": "Intermediate",
    },
    "intervene as deemed needed": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˌɪntəˈviːn æz diːmd ˈniːdɪd/",
        "meaning": "to intervene when judged necessary",
        "description": "Ask someone to step in at their discretion when support is needed.",
        "difficulty": "Intermediate",
    },
    "increase the priority of": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɪnˈkriːs ðə praɪˈɒrəti əv/",
        "meaning": "to raise the priority of",
        "description": "Explain a reprioritization based on new facts such as a recent incident.",
        "difficulty": "Intermediate",
    },
    "a safety net just in case": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ə ˈseɪfti net dʒʌst ɪn keɪs/",
        "meaning": "a backup safeguard",
        "description": "Describe a secondary review as backup if the primary automated check fails.",
        "difficulty": "Intermediate",
    },
    "the primary ownership still lies in": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ðə ˈpraɪməri ˈəʊnəʃɪp stɪl laɪz ɪn/",
        "meaning": "primary ownership still rests with",
        "description": "Confirm the service team retains primary ownership despite central support.",
        "difficulty": "Intermediate",
    },
    "make sure they are aware of": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/meɪk ʃʊə ðeɪ ɑː əˈweər əv/",
        "meaning": "to ensure they understand",
        "description": "Ensure reviewers understand deadlines and risks, not just receive information.",
        "difficulty": "Intermediate",
    },
    "pay attention to": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/peɪ əˈtenʃn tuː/",
        "meaning": "to pay attention to",
        "description": "Direct focus to items needing close monitoring in management contexts.",
        "difficulty": "Beginner",
    },
    "park this topic for now": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/pɑːk ðɪs ˈtɒpɪk fɔː naʊ/",
        "meaning": "to defer this topic temporarily",
        "description": "Briefly table a topic to prevent meeting drift and return to the agenda.",
        "difficulty": "Intermediate",
    },
    "the priority is to agree on the scope": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ðə praɪˈɒrəti ɪz tuː əˈɡriː ɒn ðə skəʊp/",
        "meaning": "agreeing on scope comes first",
        "description": "Set scope agreement as the first priority before estimating delivery dates.",
        "difficulty": "Intermediate",
    },
    "everything else can come later": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ˈevriθɪŋ els kæn kʌm ˈleɪtə/",
        "meaning": "other items can wait",
        "description": "Separate must-haves from deferrable work to clarify priorities.",
        "difficulty": "Intermediate",
    },
    "with support from": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/wɪð səˈpɔːt frɒm/",
        "meaning": "with support from",
        "description": "Clarify who owns work and which team provides supporting help.",
        "difficulty": "Intermediate",
    },
    "along with a brief explanation": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/əˈlɒŋ wɪð ə briːf ˌekspləˈneɪʃn/",
        "meaning": "together with a short explanation",
        "description": "Ask for risks listed with minimal context needed to judge impact.",
        "difficulty": "Intermediate",
    },
    "ensure that requirements are covered": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɪnˈʃʊə ðæt rɪˈkwaɪəmənts ɑː ˈkʌvəd/",
        "meaning": "to ensure requirements are covered",
        "description": "Assign clear responsibility to verify key requirements before approval.",
        "difficulty": "Intermediate",
    },
    "if applicable": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ɪf ˌæplɪˈkəbl/",
        "meaning": "if applicable",
        "description": "Apply a step conditionally rather than mandating it for everyone.",
        "difficulty": "Beginner",
    },
    "in the long run": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/ɪn ðə lɒŋ rʌn/",
        "meaning": "over the long term",
        "description": "Contrast short-term fixes with a desired future operating model.",
        "difficulty": "Beginner",
    },
    "question the need for": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈkwestʃən ðə niːd fɔː/",
        "meaning": "to question the need for",
        "description": "Prompt reconsideration of a step without directly rejecting it.",
        "difficulty": "Intermediate",
    },
    "add one more layer to maintain": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/æd wʌn mɔː ˈleɪə tuː meɪnˈteɪn/",
        "meaning": "to add another layer to maintain",
        "description": "Highlight ongoing operational cost when a new committee adds complexity.",
        "difficulty": "Intermediate",
    },
    "wonder if that's worth it": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ˈwʌndə ɪf ðæts wɜːθ ɪt/",
        "meaning": "to question whether it is worthwhile",
        "description": "Suggest cost-benefit review without stating firm opposition.",
        "difficulty": "Intermediate",
    },
    "a lot of unknowns": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ə lɒt əv ʌnˈnəʊnz/",
        "meaning": "many uncertainties",
        "description": "Flag uncertainty to keep estimates provisional rather than fixed.",
        "difficulty": "Intermediate",
    },
    "verify our assumptions": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈverɪfaɪ ˈaʊə əˈsʌmpʃnz/",
        "meaning": "to verify our assumptions",
        "description": "State the next validation step before scaling a hypothesis-based decision.",
        "difficulty": "Intermediate",
    },
    "a lighter review process": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ə ˈlaɪtə rɪˈvjuː ˈprəʊses/",
        "meaning": "a lighter review process",
        "description": "Propose lighter reviews to learn faster without lowering quality standards.",
        "difficulty": "Intermediate",
    },
    "favour time to market": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈfeɪvə taɪm tuː ˈmɑːkɪt/",
        "meaning": "to favour time to market",
        "description": "Prioritize speed while keeping critical controls in early stages.",
        "difficulty": "Intermediate",
    },
    "once we get the desired traction": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/wʌns wiː ɡet ðə dɪˈzaɪəd ˈtrækʃn/",
        "meaning": "once desired traction is achieved",
        "description": "Set traction as the condition for investing in stricter process later.",
        "difficulty": "Intermediate",
    },
    "the associated challenges": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ði əˈsəʊʃieɪtɪd ˈtʃælɪndʒɪz/",
        "meaning": "the related challenges",
        "description": "Include accompanying difficulties and risks when adopting a new model.",
        "difficulty": "Intermediate",
    },
    "won't be so straightforward": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/wəʊnt biː səʊ ˌstreɪtˈfɔːwəd/",
        "meaning": "will not be straightforward",
        "description": "Warn that re-architecture gets harder as more teams depend on the service.",
        "difficulty": "Intermediate",
    },
    "deliver with quality and on time": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/dɪˈlɪvə wɪð ˈkwɒləti ænd ɒn taɪm/",
        "meaning": "to deliver with quality and on time",
        "description": "State delivery goals covering both quality and schedule without burnout.",
        "difficulty": "Intermediate",
    },
    "a stricter process": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ə ˈstrɪktə ˈprəʊses/",
        "meaning": "a stricter process",
        "description": "Recommend tighter controls as a service becomes business-critical.",
        "difficulty": "Intermediate",
    },
    "start a discussion between": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/stɑːt ə dɪˈskʌʃn bɪˈtwiːn/",
        "meaning": "to start a discussion between",
        "description": "Begin cross-functional dialogue before scope is finalized.",
        "difficulty": "Intermediate",
    },
    "the appropriate team members": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ði əˈprəʊpriət tiːm ˈmembəz/",
        "meaning": "the appropriate team members",
        "description": "Ask for suitable roles rather than naming specific individuals.",
        "difficulty": "Intermediate",
    },
    "one to follow up, the other to back up": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/wʌn tuː ˈfɒləʊ ʌp ði ˈʌðə tuː bæk ʌp/",
        "meaning": "one follows up, the other backs up",
        "description": "Assign primary and backup coordinators with clear role split.",
        "difficulty": "Advanced",
    },
    "an early heads-up": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ən ˈɜːli hedz ʌp/",
        "meaning": "an early warning",
        "description": "Share advance notice so others can prepare for upcoming capacity changes.",
        "difficulty": "Intermediate",
    },
    "although it is quite early": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ɔːlˈðəʊ ɪt ɪz kwaɪt ˈɜːli/",
        "meaning": "although it is quite early",
        "description": "Acknowledge timing while suggesting proactive preparation or requests.",
        "difficulty": "Intermediate",
    },
    "complete the handover": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/kəmˈpliːt ðə ˈhændəʊvə/",
        "meaning": "to complete the handover",
        "description": "Require handover completion before the current owner goes on leave.",
        "difficulty": "Intermediate",
    },
    "confirm availability": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/kənˈfɜːm əˌveɪləˈbɪləti/",
        "meaning": "to confirm availability",
        "description": "Check actual capacity before assigning people to a milestone.",
        "difficulty": "Intermediate",
    },
    "a development timeline": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ə dɪˈveləpmənt ˈtaɪmlaɪn/",
        "meaning": "a development timeline",
        "description": "Avoid committing to a schedule before main dependencies are clear.",
        "difficulty": "Intermediate",
    },
    "have some bandwidth": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/hæv sʌm ˈbændwɪdθ/",
        "meaning": "to have spare capacity",
        "description": "Ask when a team can realistically take on new work.",
        "difficulty": "Intermediate",
    },
    "feel free to reach out to": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/fiːl friː tuː riːtʃ aʊt tuː/",
        "meaning": "feel free to contact",
        "description": "Lower the barrier to asking for help from a lead or partner team.",
        "difficulty": "Beginner",
    },
    "shift left": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ʃɪft left/",
        "meaning": "to shift left",
        "description": "Move review, testing, or security earlier while requirements stay flexible.",
        "difficulty": "Intermediate",
    },
    "the timeline doesn't align with yours": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ðə ˈtaɪmlaɪn ˈdʌznt əˈlaɪn wɪð jɔːz/",
        "meaning": "the timeline does not match yours",
        "description": "Flag schedule misalignment and discuss interim options.",
        "difficulty": "Intermediate",
    },
    "due to a lack of resources": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/djuː tuː ə læk əv rɪˈsɔːsɪz/",
        "meaning": "because of insufficient resources",
        "description": "Explain delay objectively as an organizational resource shortage.",
        "difficulty": "Intermediate",
    },
    "rely on the solution directly": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/rɪˈlaɪ ɒn ðə səˈluːʃn daɪˈrektli/",
        "meaning": "to rely on the solution directly",
        "description": "Choose direct use of a shared solution instead of a temporary layer.",
        "difficulty": "Intermediate",
    },
    "check whether the team has the bandwidth": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/tʃek ˈweðə ðə tiːm hæz ðə ˈbændwɪdθ/",
        "meaning": "to check team capacity",
        "description": "Verify a team's real capacity before assigning migration support.",
        "difficulty": "Intermediate",
    },
    "address all stakeholder concerns": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/əˈdres ɔːl ˈsteɪkhəʊldə kənˈsɜːnz/",
        "meaning": "to address all stakeholder concerns",
        "description": "Reflect and resolve department concerns before seeking approval.",
        "difficulty": "Intermediate",
    },
    "not have the luxury of": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/nɒt hæv ðə ˈlʌkʃəri əv/",
        "meaning": "to not have the luxury of",
        "description": "Explain practical constraints that rule out an ideal option.",
        "difficulty": "Intermediate",
    },
    "identify the functional owner": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/aɪˈdentɪfaɪ ðə ˈfʌŋkʃənl ˈəʊnə/",
        "meaning": "to identify the functional owner",
        "description": "Clarify who owns a functional area rather than an entire team.",
        "difficulty": "Intermediate",
    },
    "for starters": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/fɔː ˈstɑːtəz/",
        "meaning": "for starters; to begin with",
        "description": "Propose the first small step when facing a large set of tasks.",
        "difficulty": "Beginner",
    },
    "just some ideas, not hard requirements": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/dʒʌst sʌm aɪˈdɪəz nɒt hɑːd rɪˈkwaɪəmənts/",
        "meaning": "ideas only, not strict requirements",
        "description": "Present a draft and invite challenge by lowering the stakes.",
        "difficulty": "Advanced",
    },
    "highlight risk from a project execution angle": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈhaɪlaɪt rɪsk frɒm ə ˈprɒdʒekt ˌeksɪˈkjuːʃn ˈæŋɡl/",
        "meaning": "to highlight execution risk",
        "description": "Focus reviews on delivery risks such as dependencies and progress.",
        "difficulty": "Advanced",
    },
    "get an overview of the ongoing work": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɡet ən ˈəʊvəvjuː əv ði ɒnˈɡəʊɪŋ wɜːk/",
        "meaning": "to get an overview of ongoing work",
        "description": "Help managers see the big picture without diving into every detail.",
        "difficulty": "Intermediate",
    },
    "identify areas that need immediate attention": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/aɪˈdentɪfaɪ ˈeəriəz ðæt niːd ɪˈmiːdiət əˈtenʃn/",
        "meaning": "to identify areas needing immediate attention",
        "description": "Find issues requiring manager intervention, especially blockers.",
        "difficulty": "Advanced",
    },
    "visualise the remaining workload": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈvɪʒuəlaɪz ðə rɪˈmeɪnɪŋ ˈwɜːkləʊd/",
        "meaning": "to visualize remaining workload",
        "description": "Make remaining work visible before accepting another project.",
        "difficulty": "Intermediate",
    },
    "estimate team bandwidth in the short and mid term": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈestɪmeɪt tiːm ˈbændwɪdθ ɪn ðə ʃɔːt ænd mɪd tɜːm/",
        "meaning": "to estimate short- and mid-term team capacity",
        "description": "Estimate load over coming months before changing the roadmap.",
        "difficulty": "Advanced",
    },
    "leverage automation": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈlevərɪdʒ ˌɔːtəˈmeɪʃn/",
        "meaning": "to leverage automation",
        "description": "Automate repetitive updates so people focus on decisions.",
        "difficulty": "Intermediate",
    },
    "agree and clarify company-wide": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/əˈɡriː ænd ˈklærɪfaɪ ˈkʌmpəni waɪd/",
        "meaning": "to agree and clarify company-wide",
        "description": "Establish a shared rule across the company, not just one team.",
        "difficulty": "Intermediate",
    },
    "a written trace we can refer to": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ə ˈrɪtn treɪs wiː kæn rɪˈfɜː tuː/",
        "meaning": "a written record for later reference",
        "description": "Capture decisions in writing instead of relying on verbal agreement.",
        "difficulty": "Intermediate",
    },
    "standardize the testing phases": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈstændədaɪz ðə ˈtestɪŋ feɪzɪz/",
        "meaning": "to standardize testing phases",
        "description": "Unify phase names, scope, and owners across teams.",
        "difficulty": "Intermediate",
    },
    "before answering, let me share some assumptions": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/bɪˈfɔːr ˈɑːnsərɪŋ let miː ʃeə sʌm əˈsʌmpʃnz/",
        "meaning": "before answering, let me share assumptions",
        "description": "Disclose assumptions upfront to prevent misunderstanding.",
        "difficulty": "Advanced",
    },
    "minimize the process changes": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈmɪnɪmaɪz ðə ˈprəʊses ˈtʃeɪndʒɪz/",
        "meaning": "to minimize process changes",
        "description": "Limit process change for this release and document longer-term fixes.",
        "difficulty": "Intermediate",
    },
    "a huge shift": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ə hjuːdʒ ʃɪft/",
        "meaning": "a major change",
        "description": "Stress broad impact on organization, mindset, and operations.",
        "difficulty": "Intermediate",
    },
    "keep in mind that a proper solution will be required": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/kiːp ɪn maɪnd ðæt ə ˈprɒpə səˈluːʃn wɪl biː rɪˈkwaɪəd/",
        "meaning": "remember a proper solution will be needed",
        "description": "Use a workaround now while noting a permanent fix is still required.",
        "difficulty": "Advanced",
    },
    "not a huge fan of": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/nɒt ə hjuːdʒ fæn əv/",
        "meaning": "not very enthusiastic about",
        "description": "Express concern softly without outright rejecting a proposal.",
        "difficulty": "Intermediate",
    },
    "easier to monitor": {
        "type": "phrase",
        "partOfSpeech": "adjective phrase",
        "pronunciation": "/ˈiːziə tuː ˈmɒnɪtə/",
        "meaning": "easier to monitor",
        "description": "Recommend daytime rollouts for easier monitoring and faster response.",
        "difficulty": "Intermediate",
    },
    "treat all releases as equal": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/triːt ɔːl rɪˈliːsɪz æz ˈiːkwəl/",
        "meaning": "to treat all releases equally",
        "description": "Apply one standard to all releases until classification is reliable.",
        "difficulty": "Intermediate",
    },
    "assign the same amount of attention": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/əˈsaɪn ðə seɪm əˈmaʊnt əv əˈtenʃn/",
        "meaning": "to give equal attention",
        "description": "Ensure critical handoffs get consistent attention across teams.",
        "difficulty": "Intermediate",
    },
    "not a bad thing": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/nɒt ə bæd θɪŋ/",
        "meaning": "not a bad thing; worth considering",
        "description": "Offer mild approval of an idea without full endorsement.",
        "difficulty": "Intermediate",
    },
    "focus on applications first": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈfəʊkəs ɒn ˌæplɪˈkeɪʃnz fɜːst/",
        "meaning": "to focus on applications first",
        "description": "Narrow scope to applications before broader model discussions.",
        "difficulty": "Intermediate",
    },
    "provide time-limited access": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/prəˈvaɪd ˈtaɪm ˌlɪmɪtɪd ˈækses/",
        "meaning": "to provide time-limited access",
        "description": "Grant temporary access instead of permanent privileges.",
        "difficulty": "Intermediate",
    },
    "consider this high priority": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/kənˈsɪdə ðɪs haɪ praɪˈɒrəti/",
        "meaning": "to consider this high priority",
        "description": "State priority based on impact scope or urgency.",
        "difficulty": "Intermediate",
    },
    "there is a concern regarding": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ðeər ɪz ə kənˈsɜːn rɪˈɡɑːdɪŋ/",
        "meaning": "there is a concern regarding",
        "description": "Raise an issue objectively without blaming individuals.",
        "difficulty": "Intermediate",
    },
    "save migration cost": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/seɪv maɪˈɡreɪʃn kɒst/",
        "meaning": "to save migration cost",
        "description": "Justify long-term investment by comparing upfront and migration costs.",
        "difficulty": "Intermediate",
    },
    "keep it simple for now": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/kiːp ɪt ˈsɪmpl fɔː naʊ/",
        "meaning": "to keep it simple for now",
        "description": "Avoid over-engineering early and add controls as the process matures.",
        "difficulty": "Intermediate",
    },
    "bare minimum documentation": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/beə ˈmɪnɪməm ˌdɒkjumenˈteɪʃn/",
        "meaning": "bare minimum documentation",
        "description": "Require only essential docs before pilot to reduce writing burden.",
        "difficulty": "Intermediate",
    },
    "tackle both at the same time": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈtækl bəʊθ æt ðə seɪm taɪm/",
        "meaning": "to handle both simultaneously",
        "description": "Raise doubt about parallel work given current capacity limits.",
        "difficulty": "Intermediate",
    },
    "a requirement regarding the delivery timing": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ə rɪˈkwaɪəmənt rɪˈɡɑːdɪŋ ðə dɪˈlɪvəri ˈtaɪmɪŋ/",
        "meaning": "a requirement about delivery timing",
        "description": "Check whether delivery timing is fixed or the quarter can move.",
        "difficulty": "Intermediate",
    },
    "prioritize user experience over security": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/praɪˈɒrətaɪz ˈjuːzər ɪkˈspɪəriəns ˈəʊvə sɪˈkjʊərəti/",
        "meaning": "to prioritize UX over security",
        "description": "State a trade-off and document accepted risk if UX wins.",
        "difficulty": "Advanced",
    },
    "keep in mind the risks": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/kiːp ɪn maɪnd ðə rɪsks/",
        "meaning": "to keep the risks in mind",
        "description": "Accept a workaround while reminding stakeholders of operational risks.",
        "difficulty": "Intermediate",
    },
    "leave the final decisions to whoever implements this": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/liːv ðə ˈfaɪnl dɪˈsɪʒnz tuː huːˈevə ˈɪmplɪments ðɪs/",
        "meaning": "leave final decisions to implementers",
        "description": "Suggest direction but defer final calls to the people doing the work.",
        "difficulty": "Advanced",
    },
    "broaden the topic": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈbrɔːdn ðə ˈtɒpɪk/",
        "meaning": "to broaden the topic",
        "description": "Expand discussion from one issue to related support or compliance areas.",
        "difficulty": "Intermediate",
    },
    "give everyone a chance to participate": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɡɪv ˈevriwʌn ə tʃɑːns tuː pɑːˈtɪsɪpeɪt/",
        "meaning": "to give everyone a chance to participate",
        "description": "Share proposals widely to offer fair opportunity to join in.",
        "difficulty": "Intermediate",
    },
    "suggest the following steps": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/səˈdʒest ðə ˈfɒləʊɪŋ steps/",
        "meaning": "to suggest the following steps",
        "description": "Propose concrete next steps when discussion is unclear.",
        "difficulty": "Intermediate",
    },
    "avoid putting everything on one person's shoulders": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/əˈvɔɪd ˈpʊtɪŋ ˈevriθɪŋ ɒn wʌn ˈpɜːsnz ˈʃəʊldəz/",
        "meaning": "to avoid overloading one person",
        "description": "Split roles to spread load and reduce single-point dependency.",
        "difficulty": "Advanced",
    },
    "count on you and your team": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/kaʊnt ɒn juː ænd jɔː tiːm/",
        "meaning": "to count on you and your team",
        "description": "Ask directly for a commitment of support from a partner team.",
        "difficulty": "Intermediate",
    },
    "see if it complies with": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/siː ɪf ɪt kəmˈplaɪz wɪð/",
        "meaning": "to see if it complies with",
        "description": "Check policy compliance with compliance before proceeding.",
        "difficulty": "Intermediate",
    },
    "make sure we have a scale-up plan": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/meɪk ʃʊə wiː hæv ə ˈskeɪl ʌp plæn/",
        "meaning": "to ensure a scale-up plan exists",
        "description": "Verify readiness for traffic growth before a peak period.",
        "difficulty": "Intermediate",
    },
    "in my stead": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/ɪn maɪ sted/",
        "meaning": "on my behalf",
        "description": "Ask someone to present or act on your behalf when unavailable.",
        "difficulty": "Intermediate",
    },
    "keep members informed": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/kiːp ˈmembəz ɪnˈfɔːmd/",
        "meaning": "to keep members informed",
        "description": "Promise ongoing updates to affected people during an investigation.",
        "difficulty": "Intermediate",
    },
    "secure resources to officially start the project": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/sɪˈkjʊə rɪˈsɔːsɪz tuː əˈfɪʃəli stɑːt ðə ˈprɒdʒekt/",
        "meaning": "to secure resources to start the project",
        "description": "Secure people or budget needed to move from idea to execution.",
        "difficulty": "Advanced",
    },
    "no need to hurry": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/nəʊ niːd tuː ˈhʌri/",
        "meaning": "no need to hurry",
        "description": "Discourage rushing until owner and funding are confirmed.",
        "difficulty": "Beginner",
    },
    "for visibility": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/fɔː ˌvɪzəˈbɪləti/",
        "meaning": "for visibility",
        "description": "Add someone for awareness without requiring immediate action.",
        "difficulty": "Beginner",
    },
    "my two cents on this": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/maɪ tuː sens ɒn ðɪs/",
        "meaning": "my personal opinion on this",
        "description": "Offer a modest, constructive opinion without overstating authority.",
        "difficulty": "Intermediate",
    },
    "concerned that it might look bloated": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/kənˈsɜːnd ðæt ɪt maɪt lʊk ˈbləʊtɪd/",
        "meaning": "concerned it may look bloated",
        "description": "Flag report bloat to reduce meeting burden and improve clarity.",
        "difficulty": "Advanced",
    },
    "make upcoming changes more predictable and controlled": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/meɪk ʌpˈkʌmɪŋ ˈtʃeɪndʒɪz mɔː prɪˈdɪktəbl ænd kənˈtrəʊld/",
        "meaning": "to make upcoming changes predictable and controlled",
        "description": "Explain process goals in terms of stable, predictable operations.",
        "difficulty": "Advanced",
    },
    "focus on technical sanity": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈfəʊkəs ɒn ˈteknɪkl ˈsænəti/",
        "meaning": "to focus on technical sanity",
        "description": "Keep engineering review on design soundness while PM handles coordination.",
        "difficulty": "Intermediate",
    },
    "break it down into smaller PRs": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/breɪk ɪt daʊn ˈɪntuː ˈsmɔːlə piː ɑːz/",
        "meaning": "to break into smaller pull requests",
        "description": "Split large changes into smaller PRs to simplify review and risk.",
        "difficulty": "Intermediate",
    },
}

USAGE_EXAMPLE_JA: dict[str, str] = {
    "raise awareness": "タイムライン確定前に、依存関係の認識を高めたい。",
    "get everyone on the same page": "担当者を決める前に、全員の認識を揃えよう。",
    "tackle different aspects of the same problem": "2グループが同一課題の別側面に取り組んでいるので、連携すべきだ。",
    "simplify the participation of": "パイロットでは、中央レビューチームの関与を簡素化しよう。",
    "figure out the details later": "方針に合意し、詳細は後で詰めよう。",
    "come back to this once we have an alpha version": "アルファ版ができたら、ガバナンスモデルに戻ろう。",
    "bring the topic to your attention": "計画会議前に、人員リスクを共有したい。",
    "intervene as deemed needed": "状況を確認し、必要と判断したら介入してください。",
    "increase the priority of": "最近のインシデントで、監視改善の優先度が上がった。",
    "a safety net just in case": "2次レビューは、自動チェック漏れに備えた安全装置だ。",
    "the primary ownership still lies in": "中央支援があっても、主導的責任はサービスチームにある。",
    "make sure they are aware of": "レビュアーが期限と残リスクを認識していることを確認して。",
    "pay attention to": "次スプリントでは引き継ぎ遅延に注意すべきだ。",
    "park this topic for now": "この話題はいったん保留にし、人員決定に戻ろう。",
    "the priority is to agree on the scope": "納期見積もり前に、スコープ合意が優先だ。",
    "everything else can come later": "まずオーナーシップを確立し、他は後回しでよい。",
    "with support from": "1チームが提案を所有し、プラットフォームが支援する。",
    "along with a brief explanation": "リスクと影響の簡単な説明を添えて一覧にして。",
    "ensure that requirements are covered": "PMは承認前に主要要件が網羅されていることを確認すべきだ。",
    "if applicable": "該当する場合は、法務とセキュリティにも関与して。",
    "in the long run": "長期的には、各ドメインに明確な責任者が必要だ。",
    "question the need for": "承認段階追加で、別レビュー委員会の必要性を問い直した。",
    "add one more layer to maintain": "別委員会は、明確な利益なく保守層を増やす。",
    "wonder if that's worth it": "場所コストを考えると、一時的プロセスに見合うか疑問だ。",
    "a lot of unknowns": "不確実性が多いので、見積もりは暫定のままにすべきだ。",
    "verify our assumptions": "スケール前に、ユーザーで前提を検証すべきだ。",
    "a lighter review process": "実験では、より軽量なレビューで学習を速くできる。",
    "favour time to market": "この段階では、重要統制を保ちつつ市場投入を優先すべきだ。",
    "once we get the desired traction": "期待する手応えが得られたら、より厳格なプロセスに投資できる。",
    "the associated challenges": "新運用モデル採用前に、それに伴う課題を認識すべきだ。",
    "won't be so straightforward": "多くのチームが依存すると、再構成は直球にいかない。",
    "deliver with quality and on time": "目標は、チームを燃え尽きさせず品質と期限を両立することだ。",
    "a stricter process": "サービスが事業クリティカルになれば、より厳格なプロセスが必要だ。",
    "start a discussion between": "スコープ確定前に、Product・QA・Engineering間で議論を始めよう。",
    "the appropriate team members": "セキュリティレビューに適切なチームメンバーを含めて。",
    "one to follow up, the other to back up": "2名のコーディネーターを割り当て、一人がフォロー、もう一人が支援する。",
    "an early heads-up": "来月、キャパシティが下がる可能性がある事前案内だ。",
    "although it is quite early": "まだ早い段階だが、レビュアーの可用性確認は有用だ。",
    "complete the handover": "現オーナー休暇前に、引き継ぎを完了して。",
    "confirm availability": "次マイルストーンに対応可能か、チームの可用性を確認して。",
    "a development timeline": "主要依存が明確になるまで、開発スケジュールを確約すべきでない。",
    "have some bandwidth": "この作業に対応余力がある時期を教えて。",
    "feel free to reach out to": "ブロッカー解消に困ったら、プラットフォームリードに遠慮なく連絡して。",
    "shift left": "要件が柔軟なうちにQAを関与させ、左シフトしよう。",
    "the timeline doesn't align with yours": "プラットフォームのスケジュールが合わなければ、暫定案が必要だ。",
    "due to a lack of resources": "所有チームのリソース不足のため、作業が遅れた。",
    "rely on the solution directly": "一時レイヤーではなく、共有ソリューションを直接利用した。",
    "check whether the team has the bandwidth": "今四半期、移行支援の余力があるか確認して。",
    "address all stakeholder concerns": "承認前に、提案は全関係者の懸念に対応すべきだ。",
    "not have the luxury of": "今四半期、専任コーディネーターを追加する余裕はない。",
    "identify the functional owner": "各ドメインをチームに割り当てれば、機能上の責任者を特定できる。",
    "for starters": "まず手始めに、現オーナーと未決事項を文書化しよう。",
    "just some ideas, not hard requirements": "あくまでアイデアなので、遠慮なく修正してください。",
    "highlight risk from a project execution angle": "週次レビューでは、進行観点のリスクを明確にすべきだ。",
    "get an overview of the ongoing work": "ダッシュボードで、進行中作業の概要を把握できるはずだ。",
    "identify areas that need immediate attention": "レビューで、特に未解決ブロッカーなど即対応領域を特定して。",
    "visualise the remaining workload": "新案件受入前に、残作業量を可視化する必要がある。",
    "estimate team bandwidth in the short and mid term": "ロードマップ変更前に、短期・中期のチーム余力を見積もろう。",
    "leverage automation": "ステータス更新は自動化し、人間は判断に集中すべきだ。",
    "agree and clarify company-wide": "アーキテクチャレビュー要否を全社的に合意・明確化すべきだ。",
    "a written trace we can refer to": "後から参照できるよう、決定を文書で記録して。",
    "standardize the testing phases": "テスト工程のスコープとオーナーを含め標準化すべきだ。",
    "before answering, let me share some assumptions": "回答前に、キャパシティと納期リスクの前提を共有する。",
    "minimize the process changes": "このリリースではプロセス変更を最小限に抑えよう。",
    "a huge shift": "ドメイン別オーナーシップへの移行は、複数チームにとって大転換だ。",
    "keep in mind that a proper solution will be required": "暫定策は使えるが、恒久策が必要な点は忘れないで。",
    "not a huge fan of": "明確なリスク低減なしに承認追加にはあまり乗り気ではない。",
    "easier to monitor": "日中ロールアウトの方が監視しやすく、対応人員も増える。",
    "treat all releases as equal": "分類が信頼できるまで、すべてのリリースを同等に扱うべきだ。",
    "assign the same amount of attention": "重要な引き継ぎは、チーム間で同程度の注意を向けるべきだ。",
    "not a bad thing": "軽量に保てば、定期計画チェックポイントは悪くない。",
    "focus on applications first": "広いモデルも重要だが、まずアプリケーションに集中したい。",
    "provide time-limited access": "例外的運用には、期間限定アクセスを提供できる。",
    "consider this high priority": "複数チームに影響するため、これは高優先度と判断する。",
    "there is a concern regarding": "ローンチ後のサポートキャパシティについて懸念がある。",
    "save migration cost": "共有プラットフォームは初期費用こそ高いが、移行コストを抑えられる。",
    "keep it simple for now": "今はシンプルに保ち、プロセス成熟に合わせ統制を追加しよう。",
    "bare minimum documentation": "パイロット開始前に、必要最小限の文書が必要だ。",
    "tackle both at the same time": "現キャパシティでは、両方を同時に処理できるか不明だ。",
    "a requirement regarding the delivery timing": "納期要件は固定か、四半期調整は可能か？",
    "prioritize user experience over security": "UXを優先するなら、受容リスクを文書化すべきだ。",
    "keep in mind the risks": "暫定策は受け入れられるが、運用リスクは念頭に置こう。",
    "leave the final decisions to whoever implements this": "方向は示せるが、最終判断は実装担当者に委ねる。",
    "broaden the topic": "サポートとコンプライアンスの影響も含め、議論を広げよう。",
    "give everyone a chance to participate": "広いチャンネルで提案を共有し、全員に参加機会を与える。",
    "suggest the following steps": "未解決点が多いので、以下のステップを提案する。",
    "avoid putting everything on one person's shoulders": "役割を分け、一人にすべてを背負わせないようにしよう。",
    "count on you and your team": "インフラ支援が必要なら、あなたとチームを頼れるか？",
    "see if it complies with": "計画をコンプライアンスに伝え、方針適合を確認しよう。",
    "make sure we have a scale-up plan": "トラフィックピーク前に、スケールアップ計画を確認して。",
    "in my stead": "文脈を把握しているので、代理で発表できるはずだ。",
    "keep members informed": "調査中、影響メンバーに随時情報共有して。",
    "secure resources to officially start the project": "来四半期の正式開始に必要なリソースを確保する必要がある。",
    "no need to hurry": "オーナーと資金が確定するまで、急ぐ必要はない。",
    "for visibility": "可視化のためサポートリードを追加する。まだ対応不要。",
    "my two cents on this": "私見だが、更新は簡潔にし詳細レポートへリンクして。",
    "concerned that it might look bloated": "週次レポートが情報過多に見えるのではと懸念している。",
    "make upcoming changes more predictable and controlled": "リリースウィンドウ標準化で、今後の変更を予測可能にできる。",
    "focus on technical sanity": "PMが調整を担い、エンジニアリングレビューは技術健全性に集中すべきだ。",
    "break it down into smaller PRs": "レビューとリスク低減のため、小さなPRに分割する。",
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
