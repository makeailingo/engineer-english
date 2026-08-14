#!/usr/bin/env python3
"""Generate Meetings / Events vocabulary markdown files (129 entries)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from meetings_vocabulary_user_data import USER_ENTRIES

ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = ROOT / "docs" / "vocabulary"
SCENE = "Meetings / Events"
START_ID = 239

DIFFICULTY_ORDER = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}

METADATA: dict[str, dict] = {
    "so far": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/səʊ fɑː/",
        "meaning": "up to now",
        "description": "Report progress or findings confirmed so far in a meeting.",
        "difficulty": "Beginner",
    },
    "still no update": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/stɪl nəʊ ˈʌpdeɪt/",
        "meaning": "still no progress reported",
        "description": "State plainly that expected news or work has not moved forward.",
        "difficulty": "Intermediate",
    },
    "not something unexpected": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/nɒt ˈsʌmθɪŋ ˌʌnɪkˈspektɪd/",
        "meaning": "not surprising",
        "description": "Explain that an issue fits known or expected behavior.",
        "difficulty": "Intermediate",
    },
    "first of all": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/fɜːst əv ɔːl/",
        "meaning": "to begin with",
        "description": "Open a discussion by naming the first topic to cover.",
        "difficulty": "Beginner",
    },
    "provide a diagram to support the discussion": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/prəˈvaɪd ə ˈdaɪəɡræm/",
        "meaning": "to share a diagram for discussion",
        "description": "Offer a diagram or flow chart to clarify a meeting topic.",
        "difficulty": "Intermediate",
    },
    "in the middle of": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/ɪn ðə ˈmɪdl əv/",
        "meaning": "currently doing",
        "description": "Say work is underway and not finished yet.",
        "difficulty": "Beginner",
    },
    "move on to": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/muːv ɒn tuː/",
        "meaning": "to proceed to the next topic",
        "description": "Shift the agenda or work phase to the next item.",
        "difficulty": "Beginner",
    },
    "regarding": {
        "type": "phrase",
        "partOfSpeech": "preposition",
        "pronunciation": "/rɪˈɡɑːdɪŋ/",
        "meaning": "concerning",
        "description": "Introduce a specific topic in a formal meeting update.",
        "difficulty": "Beginner",
    },
    "if I'm not mistaken": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ɪf aɪm nɒt mɪsˈteɪkən/",
        "meaning": "if my memory is correct",
        "description": "Share information while leaving room for correction.",
        "difficulty": "Intermediate",
    },
    "need to confirm": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/niːd tuː kənˈfɜːm/",
        "meaning": "must verify",
        "description": "Say more checking is needed before deciding.",
        "difficulty": "Beginner",
    },
    "at the moment": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/æt ðə ˈməʊmənt/",
        "meaning": "right now",
        "description": "Describe the current temporary situation in a stand-up.",
        "difficulty": "Beginner",
    },
    "we concluded that": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/wiː kənˈkluːdɪd ðæt/",
        "meaning": "we agreed that",
        "description": "Announce the outcome the group reached in discussion.",
        "difficulty": "Intermediate",
    },
    "the reason is because": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ðə ˈriːzn ɪz bɪˈkɒz/",
        "meaning": "the reason is",
        "description": "Start explaining why something is true or needed.",
        "difficulty": "Beginner",
    },
    "ready to release": {
        "type": "phrase",
        "partOfSpeech": "adjective phrase",
        "pronunciation": "/ˈredi tuː rɪˈliːs/",
        "meaning": "ready for release",
        "description": "Report that testing and prep are done enough to ship.",
        "difficulty": "Beginner",
    },
    "plan out": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/plæn aʊt/",
        "meaning": "to plan in detail",
        "description": "Describe breaking work into concrete steps and order.",
        "difficulty": "Intermediate",
    },
    "gradually": {
        "type": "word",
        "partOfSpeech": "adverb",
        "pronunciation": "/ˈɡrædʒuəli/",
        "meaning": "step by step",
        "description": "Say changes will happen in stages, not all at once.",
        "difficulty": "Beginner",
    },
    "from what I understand": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/frɒm wɒt aɪ ˌʌndəˈstænd/",
        "meaning": "as I understand it",
        "description": "Share your understanding while inviting correction.",
        "difficulty": "Intermediate",
    },
    "in the first place": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/ɪn ðə fɜːst pleɪs/",
        "meaning": "to begin with",
        "description": "Return to a root cause or prerequisite in discussion.",
        "difficulty": "Beginner",
    },
    "I was wondering if": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/aɪ wɒz ˈwʌndərɪŋ ɪf/",
        "meaning": "I wanted to ask if",
        "description": "Make a polite suggestion or question in a meeting.",
        "difficulty": "Beginner",
    },
    "I'm not sure how it works": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/aɪm nɒt ʃʊə haʊ ɪt wɜːks/",
        "meaning": "I do not know how it works",
        "description": "Admit uncertainty about behavior and need more investigation.",
        "difficulty": "Beginner",
    },
    "as long as": {
        "type": "phrase",
        "partOfSpeech": "conjunction",
        "pronunciation": "/æz lɒŋ æz/",
        "meaning": "provided that",
        "description": "State a condition that must hold for a plan to work.",
        "difficulty": "Beginner",
    },
    "worth looking into": {
        "type": "phrase",
        "partOfSpeech": "adjective phrase",
        "pronunciation": "/wɜːθ ˈlʊkɪŋ ˈɪntuː/",
        "meaning": "worth investigating",
        "description": "Suggest an option deserves further research.",
        "difficulty": "Intermediate",
    },
    "as time passes": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/æz taɪm ˈpɑːsɪz/",
        "meaning": "over time",
        "description": "Describe expected change over the medium or long term.",
        "difficulty": "Intermediate",
    },
    "bring up one last topic": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/brɪŋ ʌp wʌn lɑːst ˈtɒpɪk/",
        "meaning": "to raise a final topic",
        "description": "Add one more agenda item before closing a meeting.",
        "difficulty": "Intermediate",
    },
    "before we close": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/bɪˈfɔː wiː kləʊz/",
        "meaning": "before we finish",
        "description": "Prompt final checks or comments before ending.",
        "difficulty": "Beginner",
    },
    "what do you guys think?": {
        "type": "phrase",
        "partOfSpeech": "question",
        "pronunciation": "/wɒt duː juː ɡaɪz θɪŋk/",
        "meaning": "what do you all think",
        "description": "Ask the team for open opinions in a casual way.",
        "difficulty": "Beginner",
    },
    "think otherwise": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/θɪŋk ˈʌðəwaɪz/",
        "meaning": "disagree",
        "description": "Check whether anyone holds a different view.",
        "difficulty": "Advanced",
    },
    "what I'm about to mention": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/wɒt aɪm əˈbaʊt tuː ˈmenʃn/",
        "meaning": "what I will say next",
        "description": "Link your upcoming point to the current discussion.",
        "difficulty": "Intermediate",
    },
    "according to the needs": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/əˈkɔːdɪŋ tuː ðə niːdz/",
        "meaning": "based on requirements",
        "description": "Say decisions vary by client or requirement.",
        "difficulty": "Intermediate",
    },
    "that being said": {
        "type": "phrase",
        "partOfSpeech": "discourse marker",
        "pronunciation": "/ðæt ˈbiːɪŋ sed/",
        "meaning": "nevertheless",
        "description": "Acknowledge the prior point, then add a caveat.",
        "difficulty": "Intermediate",
    },
    "separate the concerns": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈseprət ðə kənˈsɜːnz/",
        "meaning": "to split responsibilities",
        "description": "Explain splitting roles or scopes in design discussion.",
        "difficulty": "Intermediate",
    },
    "what I have in mind": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/wɒt aɪ hæv ɪn maɪnd/",
        "meaning": "my idea",
        "description": "Share a draft idea that is not finalized yet.",
        "difficulty": "Beginner",
    },
    "worth considering": {
        "type": "phrase",
        "partOfSpeech": "adjective phrase",
        "pronunciation": "/wɜːθ kənˈsɪdərɪŋ/",
        "meaning": "worth discussing",
        "description": "Suggest an option may be useful under certain conditions.",
        "difficulty": "Intermediate",
    },
    "that's a really good question": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ðæts ə ˈrɪəli ɡʊd ˈkwestʃən/",
        "meaning": "that is a great question",
        "description": "Acknowledge a question positively before answering.",
        "difficulty": "Beginner",
    },
    "just ping me": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/dʒʌst pɪŋ miː/",
        "meaning": "just message me",
        "description": "Invite someone to contact you casually on chat.",
        "difficulty": "Beginner",
    },
    "I plan to raise the topic": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/aɪ plæn tuː reɪz ðə ˈtɒpɪk/",
        "meaning": "I will bring up the topic",
        "description": "Say you will introduce an item in another forum.",
        "difficulty": "Intermediate",
    },
    "in order for that to happen": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ɪn ˈɔːdə fɔː ðæt tuː ˈhæpən/",
        "meaning": "for that to happen",
        "description": "List prerequisites needed to reach a stated goal.",
        "difficulty": "Intermediate",
    },
    "next up": {
        "type": "phrase",
        "partOfSpeech": "discourse marker",
        "pronunciation": "/nekst ʌp/",
        "meaning": "next",
        "description": "Move the meeting to the next agenda item.",
        "difficulty": "Beginner",
    },
    "before that": {
        "type": "phrase",
        "partOfSpeech": "discourse marker",
        "pronunciation": "/bɪˈfɔː ðæt/",
        "meaning": "before that step",
        "description": "Pause to check something before continuing.",
        "difficulty": "Beginner",
    },
    "briefly translate": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈbriːfli trænzˈleɪt/",
        "meaning": "to translate briefly",
        "description": "Introduce a short translation or summary in a meeting.",
        "difficulty": "Intermediate",
    },
    "go with that approach": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɡəʊ wɪð ðæt əˈprəʊtʃ/",
        "meaning": "to adopt that approach",
        "description": "Discuss impact if the team chooses a proposed option.",
        "difficulty": "Intermediate",
    },
    "think what to do if": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/θɪŋk wɒt tuː duː ɪf/",
        "meaning": "to plan for if",
        "description": "Talk through fallback actions for failure cases.",
        "difficulty": "Intermediate",
    },
    "in that case": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/ɪn ðæt keɪs/",
        "meaning": "if so",
        "description": "Give the next decision based on stated conditions.",
        "difficulty": "Beginner",
    },
    "just reiterating": {
        "type": "phrase",
        "partOfSpeech": "discourse marker",
        "pronunciation": "/dʒʌst riːˈɪtəreɪtɪŋ/",
        "meaning": "to restate",
        "description": "Repeat key numbers or settings for clarity.",
        "difficulty": "Advanced",
    },
    "keep an eye on": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/kiːp ən aɪ ɒn/",
        "meaning": "to monitor",
        "description": "Ask someone to watch a risky area over time.",
        "difficulty": "Intermediate",
    },
    "we've got to be cautious": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/wiːv ɡɒt tuː biː ˈkɔːʃəs/",
        "meaning": "we must be careful",
        "description": "Warn that a change needs extra care.",
        "difficulty": "Intermediate",
    },
    "one way is to": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/wʌn weɪ ɪz tuː/",
        "meaning": "one option is to",
        "description": "Offer one possible solution among several.",
        "difficulty": "Beginner",
    },
    "out of office": {
        "type": "phrase",
        "partOfSpeech": "adjective phrase",
        "pronunciation": "/aʊt əv ˈɒfɪs/",
        "meaning": "away from work",
        "description": "Report who is unavailable or on leave today.",
        "difficulty": "Beginner",
    },
    "does anyone have any updates they'd like to talk about?": {
        "type": "phrase",
        "partOfSpeech": "question",
        "pronunciation": "/dʌz ˈeniwʌn hæv ˈeni ʌpdeɪts/",
        "meaning": "any updates to share",
        "description": "Invite voluntary progress updates in a stand-up.",
        "difficulty": "Intermediate",
    },
    "sounds like we can probably skip": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/saʊndz laɪk wiː kæn ˈprɒbəbli skɪp/",
        "meaning": "we can likely skip this",
        "description": "Propose skipping an agenda item to save time.",
        "difficulty": "Intermediate",
    },
    "unless there are any objections": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ənˈles ðeər ɑːr ˈeni əbˈdʒekʃnz/",
        "meaning": "if no one objects",
        "description": "Confirm consensus before moving forward.",
        "difficulty": "Intermediate",
    },
    "I agree with you": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/aɪ əˈɡriː wɪð juː/",
        "meaning": "I agree with you",
        "description": "Express clear agreement with another person's point.",
        "difficulty": "Beginner",
    },
    "talk to you later": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/tɔːk tuː juː ˈleɪtə/",
        "meaning": "see you later",
        "description": "Close a side conversation before leaving.",
        "difficulty": "Beginner",
    },
    "roughly estimate how long it would take": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈrʌfli ˈestɪmeɪt/",
        "meaning": "to give a rough time estimate",
        "description": "Ask for an approximate duration, not exact effort.",
        "difficulty": "Intermediate",
    },
    "by next week": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/baɪ nekst wiːk/",
        "meaning": "before next week ends",
        "description": "Set or accept a deadline around the following week.",
        "difficulty": "Beginner",
    },
    "get the root cause": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɡet ðə ruːt kɔːz/",
        "meaning": "to find the root cause",
        "description": "Commit to investigating the underlying cause.",
        "difficulty": "Intermediate",
    },
    "if anything": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/ɪf ˈeniθɪŋ/",
        "meaning": "if needed",
        "description": "Explain what to do if the situation changes.",
        "difficulty": "Beginner",
    },
    "share briefly": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ʃeə ˈbriːfli/",
        "meaning": "to share briefly",
        "description": "Introduce a short summary before giving details.",
        "difficulty": "Beginner",
    },
    "find out how": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/faɪnd aʊt haʊ/",
        "meaning": "to discover how",
        "description": "Say the method is unknown and needs research.",
        "difficulty": "Beginner",
    },
    "if we were to": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ɪf wiː wɜː tuː/",
        "meaning": "if we were to",
        "description": "Discuss a hypothetical scenario and its impact.",
        "difficulty": "Intermediate",
    },
    "do you have anything else you'd like to share?": {
        "type": "phrase",
        "partOfSpeech": "question",
        "pronunciation": "/duː juː hæv ˈeniθɪŋ els/",
        "meaning": "anything else to share",
        "description": "Check for more input before moving on.",
        "difficulty": "Intermediate",
    },
    "as soon as possible": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/æz suːn æz ˈpɒsəbl/",
        "meaning": "as quickly as possible",
        "description": "Signal urgency for a fix or delivery.",
        "difficulty": "Beginner",
    },
    "as you all know": {
        "type": "phrase",
        "partOfSpeech": "discourse marker",
        "pronunciation": "/æz juː ɔːl nəʊ/",
        "meaning": "as you already know",
        "description": "Build on information the group already has.",
        "difficulty": "Beginner",
    },
    "currently working on": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈkʌrəntli ˈwɜːkɪŋ ɒn/",
        "meaning": "working on now",
        "description": "Share what you are actively doing this sprint.",
        "difficulty": "Beginner",
    },
    "do you happen to know": {
        "type": "phrase",
        "partOfSpeech": "question",
        "pronunciation": "/duː juː ˈhæpən tuː nəʊ/",
        "meaning": "do you by any chance know",
        "description": "Ask politely whether someone has information.",
        "difficulty": "Beginner",
    },
    "take this to Slack later": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/teɪk ðɪs tuː slæk ˈleɪtə/",
        "meaning": "to discuss on Slack later",
        "description": "Move a topic offline when the meeting runs long.",
        "difficulty": "Intermediate",
    },
    "get back to": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɡet bæk tuː/",
        "meaning": "to return to",
        "description": "Say you will resume a paused task or topic.",
        "difficulty": "Beginner",
    },
    "put on hold": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/pʊt ɒn həʊld/",
        "meaning": "to pause",
        "description": "Explain pausing work due to higher priorities.",
        "difficulty": "Beginner",
    },
    "higher-priority tickets": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ˈhaɪə praɪˈɒrəti ˈtɪkɪts/",
        "meaning": "more urgent tickets",
        "description": "Justify delay by citing more urgent work items.",
        "difficulty": "Intermediate",
    },
    "as far as I could tell": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/æz fɑːr æz aɪ kʊd tel/",
        "meaning": "from what I could verify",
        "description": "Share findings limited to what you checked.",
        "difficulty": "Intermediate",
    },
    "as I mentioned": {
        "type": "phrase",
        "partOfSpeech": "discourse marker",
        "pronunciation": "/æz aɪ ˈmenʃnd/",
        "meaning": "as I said earlier",
        "description": "Repeat an earlier point for emphasis.",
        "difficulty": "Beginner",
    },
    "instead of what I proposed": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/ɪnˈsted əv wɒt aɪ prəˈpəʊzd/",
        "meaning": "rather than my proposal",
        "description": "Compare your idea with an alternative option.",
        "difficulty": "Intermediate",
    },
    "source of truth": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/sɔːs əv truːθ/",
        "meaning": "authoritative data source",
        "description": "Name which system holds the canonical data.",
        "difficulty": "Intermediate",
    },
    "make a final decision": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/meɪk ə ˈfaɪnl dɪˈsɪʒn/",
        "meaning": "to decide finally",
        "description": "Refer to the step of making a final call.",
        "difficulty": "Beginner",
    },
    "side note": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/saɪd nəʊt/",
        "meaning": "by the way",
        "description": "Add related information off the main topic.",
        "difficulty": "Beginner",
    },
    "we could do that too": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/wiː kʊd duː ðæt tuː/",
        "meaning": "that is also possible",
        "description": "Accept an option while noting trade-offs.",
        "difficulty": "Beginner",
    },
    "as much as possible": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/æz mʌtʃ æz ˈpɒsəbl/",
        "meaning": "as far as possible",
        "description": "State a goal to minimize or maximize something.",
        "difficulty": "Beginner",
    },
    "Given all that": {
        "type": "phrase",
        "partOfSpeech": "discourse marker",
        "pronunciation": "/ˈɡɪvn ɔːl ðæt/",
        "meaning": "considering all of that",
        "description": "Move to a conclusion after listing context.",
        "difficulty": "Intermediate",
    },
    "I would prefer it that way": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/aɪ wʊd prɪˈfɜː ɪt ðæt weɪ/",
        "meaning": "I would prefer that option",
        "description": "State your preferred choice among alternatives.",
        "difficulty": "Intermediate",
    },
    "if there's no solution": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ɪf ðeəz nəʊ səˈluːʃn/",
        "meaning": "if no solution exists",
        "description": "Define fallback behavior when options are exhausted.",
        "difficulty": "Intermediate",
    },
    "proceed with": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/prəˈsiːd wɪð/",
        "meaning": "to move ahead with",
        "description": "Start execution after agreement is reached.",
        "difficulty": "Beginner",
    },
    "quick update": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/kwɪk ˈʌpdeɪt/",
        "meaning": "brief status update",
        "description": "Introduce a short progress report in a meeting.",
        "difficulty": "Beginner",
    },
    "hopefully by the end of today": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/həʊpfəli baɪ ði end əv təˈdeɪ/",
        "meaning": "hopefully today",
        "description": "Share a target finish time without promising it.",
        "difficulty": "Intermediate",
    },
    "that's all from me": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ðæts ɔːl frɒm miː/",
        "meaning": "that is all from me",
        "description": "Signal the end of your update and hand off.",
        "difficulty": "Beginner",
    },
    "if there is an alternative": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ɪf ðeər ɪz ən ɔːlˈtɜːnətɪv/",
        "meaning": "if another option exists",
        "description": "Ask whether other choices should be compared.",
        "difficulty": "Intermediate",
    },
    "let's wrap things up here": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/lets ræp θɪŋz ʌp hɪə/",
        "meaning": "let us finish here",
        "description": "Close the meeting at a natural stopping point.",
        "difficulty": "Beginner",
    },
    "is English okay with you?": {
        "type": "phrase",
        "partOfSpeech": "question",
        "pronunciation": "/ɪz ˈɪŋɡlɪʃ əˈkeɪ wɪð juː/",
        "meaning": "is English fine for you",
        "description": "Check language preference before starting.",
        "difficulty": "Beginner",
    },
    "that's fine too": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ðæts faɪn tuː/",
        "meaning": "that works too",
        "description": "Accept the other person's preference flexibly.",
        "difficulty": "Beginner",
    },
    "looking into": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈlʊkɪŋ ˈɪntuː/",
        "meaning": "investigating",
        "description": "Report ongoing research into an issue or approach.",
        "difficulty": "Beginner",
    },
    "give that a try": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɡɪv ðæt ə traɪ/",
        "meaning": "to try that",
        "description": "Propose a trial of an idea for one sprint.",
        "difficulty": "Beginner",
    },
    "if it's too complicated": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ɪf ɪts tuː ˌkɒmplɪˈkeɪtɪd/",
        "meaning": "if it is too complex",
        "description": "Suggest a simpler fallback if complexity is high.",
        "difficulty": "Beginner",
    },
    "just fyi": {
        "type": "phrase",
        "partOfSpeech": "discourse marker",
        "pronunciation": "/dʒʌst ef waɪ aɪ/",
        "meaning": "for your information",
        "description": "Share reference info without expecting a reply.",
        "difficulty": "Beginner",
    },
    "straightforward": {
        "type": "word",
        "partOfSpeech": "adjective",
        "pronunciation": "/streɪtˈfɔːwəd/",
        "meaning": "simple and clear",
        "description": "Describe an approach as easy to understand.",
        "difficulty": "Beginner",
    },
    "an important point": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ən ɪmˈpɔːtnt pɔɪnt/",
        "meaning": "an important point",
        "description": "Highlight something the team must not miss.",
        "difficulty": "Beginner",
    },
    "a more conservative approach": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ə mɔː kənˈsɜːvətɪv əˈprəʊtʃ/",
        "meaning": "a safer approach",
        "description": "Offer a lower-risk option in planning.",
        "difficulty": "Intermediate",
    },
    "it depends on": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɪt dɪˈpendz ɒn/",
        "meaning": "it depends on",
        "description": "Say the outcome hinges on other factors.",
        "difficulty": "Beginner",
    },
    "in terms of": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/ɪn tɜːmz əv/",
        "meaning": "with regard to",
        "description": "Frame an opinion around a specific aspect.",
        "difficulty": "Beginner",
    },
    "in advance": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/ɪn ədˈvɑːns/",
        "meaning": "beforehand",
        "description": "Describe preparation done ahead of time.",
        "difficulty": "Beginner",
    },
    "assign this to someone else": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/əˈsaɪn ðɪs tuː ˈsʌmwʌn els/",
        "meaning": "to reassign this task",
        "description": "Move work to another person when needed.",
        "difficulty": "Intermediate",
    },
    "no dedicated": {
        "type": "phrase",
        "partOfSpeech": "adjective phrase",
        "pronunciation": "/nəʊ ˈdedɪkeɪtɪd/",
        "meaning": "no dedicated resource exists",
        "description": "Report that no purpose-built environment exists yet.",
        "difficulty": "Intermediate",
    },
    "take a look at": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/teɪk ə lʊk æt/",
        "meaning": "to review",
        "description": "Suggest checking logs or materials after the meeting.",
        "difficulty": "Beginner",
    },
    "it would be great if": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ɪt wʊd biː ɡreɪt ɪf/",
        "meaning": "it would help if",
        "description": "Politely request a diagram or other help.",
        "difficulty": "Beginner",
    },
    "pick up": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/pɪk ʌp/",
        "meaning": "to take on",
        "description": "Say you will start a task from the backlog.",
        "difficulty": "Beginner",
    },
    "comments so far?": {
        "type": "phrase",
        "partOfSpeech": "question",
        "pronunciation": "/ˈkɒments səʊ fɑː/",
        "meaning": "any comments so far",
        "description": "Check for questions midway through an update.",
        "difficulty": "Beginner",
    },
    "one thing, and the other thing is": {
        "type": "phrase",
        "partOfSpeech": "discourse marker",
        "pronunciation": "/wʌn θɪŋ ænd ði ˈʌðə θɪŋ ɪz/",
        "meaning": "one point and another is",
        "description": "Structure a update with two clear points.",
        "difficulty": "Intermediate",
    },
    "from what I could find out": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/frɒm wɒt aɪ kʊd faɪnd aʊt/",
        "meaning": "from what I found",
        "description": "Report research results with stated limits.",
        "difficulty": "Intermediate",
    },
    "the only difference is": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ði ˈəʊnli ˈdɪfrəns ɪz/",
        "meaning": "the only difference is",
        "description": "Pinpoint the single gap between two options.",
        "difficulty": "Beginner",
    },
    "sounds good": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/saʊndz ɡʊd/",
        "meaning": "that works",
        "description": "Agree quickly to a proposal or answer.",
        "difficulty": "Beginner",
    },
    "do the heavy lifting": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/duː ðə ˈhevi ˈlɪftɪŋ/",
        "meaning": "to do most of the work",
        "description": "Say a framework handles the bulk of the effort.",
        "difficulty": "Advanced",
    },
    "take a look at that when the time comes": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/teɪk ə lʊk æt ðæt/",
        "meaning": "to review it later",
        "description": "Defer review until the right stage arrives.",
        "difficulty": "Intermediate",
    },
    "split things up": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/splɪt θɪŋz ʌp/",
        "meaning": "to divide work",
        "description": "Break a large task so people can work in parallel.",
        "difficulty": "Beginner",
    },
    "take over": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/teɪk ˈəʊvə/",
        "meaning": "to take ownership",
        "description": "Hand off work while someone is away.",
        "difficulty": "Beginner",
    },
    "good to know": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ɡʊd tuː nəʊ/",
        "meaning": "useful to know",
        "description": "Thank someone for helpful information.",
        "difficulty": "Beginner",
    },
    "on my side": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/ɒn maɪ saɪd/",
        "meaning": "on my end",
        "description": "Report status within your own scope or team.",
        "difficulty": "Beginner",
    },
    "my thought process was": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/maɪ θɔːt ˈprəʊses wɒz/",
        "meaning": "my reasoning was",
        "description": "Explain how you reached a design or proposal.",
        "difficulty": "Intermediate",
    },
    "bring that up": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/brɪŋ ðæt ʌp/",
        "meaning": "to raise that topic",
        "description": "Refer to introducing a concern in discussion.",
        "difficulty": "Beginner",
    },
    "I found out later that": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/aɪ faʊnd aʊt ˈleɪtə ðæt/",
        "meaning": "I learned later that",
        "description": "Report a fact discovered after earlier discussion.",
        "difficulty": "Intermediate",
    },
    "the lesson learned here is": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ðə ˈlesn lɜːnd hɪə ɪz/",
        "meaning": "the lesson here is",
        "description": "Share a takeaway from a retrospective or incident.",
        "difficulty": "Advanced",
    },
    "from that angle": {
        "type": "phrase",
        "partOfSpeech": "prepositional phrase",
        "pronunciation": "/frɒm ðæt ˈæŋɡl/",
        "meaning": "from that perspective",
        "description": "Evaluate a decision from a specific viewpoint.",
        "difficulty": "Advanced",
    },
    "set up a guideline": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/set ʌp ə ˈɡaɪdlaɪn/",
        "meaning": "to create a guideline",
        "description": "Propose establishing a team or org standard.",
        "difficulty": "Intermediate",
    },
    "comply with": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/kəmˈplaɪ wɪð/",
        "meaning": "to follow rules",
        "description": "Say teams must follow a policy or guideline.",
        "difficulty": "Intermediate",
    },
    "that requires a slight change to our plan": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ðæt rɪˈkwaɪəz ə slaɪt tʃeɪndʒ/",
        "meaning": "that needs a small plan change",
        "description": "Report a minor schedule adjustment is needed.",
        "difficulty": "Intermediate",
    },
    "the downside is": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ðə ˈdaʊnsaɪd ɪz/",
        "meaning": "the disadvantage is",
        "description": "State a clear drawback of an option.",
        "difficulty": "Intermediate",
    },
    "there shouldn't be any technical reason why": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ðeə ʃʊdnt biː ˈeni ˈteknɪkl ˈriːzn/",
        "meaning": "there should be no technical blocker",
        "description": "Argue nothing technical should prevent the change.",
        "difficulty": "Intermediate",
    },
    "in the meantime": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/ɪn ðə miːnˈtaɪm/",
        "meaning": "meanwhile",
        "description": "Describe interim work until the main fix lands.",
        "difficulty": "Beginner",
    },
    "it's not a rush": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ɪts nɒt ə rʌʃ/",
        "meaning": "it is not urgent",
        "description": "Say the task can wait until after release.",
        "difficulty": "Beginner",
    },
    "I'm not 100% sure": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/aɪm nɒt wʌn ˈhʌndrəd pə ˈsent ʃʊə/",
        "meaning": "I am not completely sure",
        "description": "Flag uncertainty before stating a conclusion.",
        "difficulty": "Beginner",
    },
    "if that doesn't work": {
        "type": "phrase",
        "partOfSpeech": "clause",
        "pronunciation": "/ɪf ðæt ˈdʌznt wɜːk/",
        "meaning": "if that fails",
        "description": "Offer a fallback if the first attempt fails.",
        "difficulty": "Beginner",
    },
    "we're trying to figure out": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/wɪə ˈtraɪɪŋ tuː ˈfɪɡə aʊt/",
        "meaning": "we are working to determine",
        "description": "Say the team is still analyzing an open question.",
        "difficulty": "Beginner",
    },
}

USAGE_EXAMPLE_JA: dict[str, str] = {
    "so far": "現時点では重大な問題は確認されていない。",
    "still no update": "プラットフォームチームからはまだ更新がない。",
    "not something unexpected": "応答遅延は想定外の事象ではない。",
    "first of all": "まず、現在の挙動を説明する。",
    "provide a diagram to support the discussion": "議論の補助として図を提供する。",
    "in the middle of": "設計ドキュメントの更新中である。",
    "move on to": "設計承認後、実装フェーズへ進む。",
    "regarding": "ロールアウトについて、最終承認がまだ必要だ。",
    "if I'm not mistaken": "私の記憶が正しければ、この変更は2エンドポイントに影響する。",
    "need to confirm": "バックエンドチームと正確なスコープを確認する必要がある。",
    "at the moment": "現時点では外部依存によりタスクがブロックされている。",
    "we concluded that": "既存アプローチで当面は十分だという結論に至った。",
    "the reason is because": "理由は環境が他チームと共有されているからだ。",
    "ready to release": "QA承認後、リリース可能な状態になる。",
    "plan out": "どのシナリオを含めるか具体化して計画する必要がある。",
    "gradually": "残りのシナリオは段階的に追加する。",
    "from what I understand": "私の理解では、スキーマは自動生成される。",
    "in the first place": "そもそも、所有権について合意する必要がある。",
    "I was wondering if": "このチェックを自動化できないかと考えていた。",
    "I'm not sure how it works": "高負荷時の動作がよく分からない。",
    "as long as": "契約が安定している限り、この方式で動くはずだ。",
    "worth looking into": "オープンソースツールは調査する価値がある。",
    "as time passes": "時間が経つにつれ、より多くのサービスが新プロトコルを採用する。",
    "bring up one last topic": "終了前に最後の話題を一つ挙げたい。",
    "before we close": "終了前にアクションアイテムを確認しよう。",
    "what do you guys think?": "同じトークンを再利用する件、皆はどう思う？",
    "think otherwise": "異なる見方をする人はいるか？",
    "what I'm about to mention": "これから話す内容に関連している。",
    "according to the needs": "クライアントごとの要件に応じてエンドポイントを作れる。",
    "that being said": "そうは言っても、フォールバック計画は必要だ。",
    "separate the concerns": "機密エンドポイントのみ移すことで関心を分離できる。",
    "what I have in mind": "私が考えている内容を説明する。",
    "worth considering": "性能向上が大きければ検討する価値がある。",
    "that's a really good question": "良い質問だ。依存関係を確認する。",
    "just ping me": "設定が必要なら気軽に連絡してほしい。",
    "I plan to raise the topic": "次回のプラットフォーム会議で話題を取り上げる予定だ。",
    "in order for that to happen": "それを実現するにはネットワークルール変更が必要だ。",
    "next up": "次はデプロイ状況を確認しよう。",
    "before that": "その前に、質問はあるか？",
    "briefly translate": "手短に日本語に訳す。",
    "go with that approach": "その方針で進めるなら追加チェックが必要だ。",
    "think what to do if": "依存が失敗した場合の対応を考える必要がある。",
    "in that case": "その場合は既存リソースを再利用すべきだ。",
    "just reiterating": "要するに、全体として要点を言い換えている。",
    "keep an eye on": "プラン内の削除操作に注意してほしい。",
    "we've got to be cautious": "リソース削除があるプランでは慎重である必要がある。",
    "one way is to": "一つの方法は既存設定を先に確認することだ。",
    "out of office": "今日は数名が不在である。",
    "does anyone have any updates they'd like to talk about?": "この会議で共有したい進捗はあるか？",
    "sounds like we can probably skip": "今日はこのセクションをスキップできそうだ。",
    "unless there are any objections": "異論がなければこの計画で進める。",
    "I agree with you": "同意する。シンプルな方が安全だ。",
    "talk to you later": "後で話そう。また後で。",
    "roughly estimate how long it would take": "修正にどのくらいかかるか概算してもらえるか？",
    "by next week": "来週までに問題を解決したい。",
    "get the root cause": "来週早めに根本原因を突き止める。",
    "if anything": "状況が変われば直接進捗を議論してほしい。",
    "share briefly": "調査内容を簡潔に共有する。",
    "find out how": "古いログの取得方法を調べる必要がある。",
    "if we were to": "古いデータを調査するなら別ストレージ層が必要だ。",
    "do you have anything else you'd like to share?": "他に共有したいことはあるか？",
    "as soon as possible": "修正をできるだけ早くリリースする必要がある。",
    "as you all know": "ご存じの通り、セッション検証フローを変更した。",
    "currently working on": "フォールバック実装に取り組んでいる。",
    "do you happen to know": "このリクエストが失敗する理由をご存じか？",
    "take this to Slack later": "この件は後でSlackで議論する。",
    "get back to": "完了後、セキュリティタスクに戻る。",
    "put on hold": "本番障害対応のためリファクタリングを保留にした。",
    "higher-priority tickets": "優先度の高いチケットを先に対応した。",
    "as far as I could tell": "確認できた限り、技術的ブロッカーはない。",
    "as I mentioned": "先述の通り、KC認証は正の情報源ではない。",
    "instead of what I proposed": "私の提案の代わりにリクエストを再試行できるか？",
    "source of truth": "データベースが正の情報源のままである。",
    "make a final decision": "最終判断の前にメトリクスを集めよう。",
    "side note": "補足：サービスの可用性目標は99.99%だ。",
    "we could do that too": "それも可能だが、運用オーバーヘッドが増える。",
    "as much as possible": "不要な例外はできる限り避けたい。",
    "Given all that": "以上を踏まえると、フォールバックは妥当だと思う。",
    "I would prefer it that way": "社内で対応できるなら、その方法を望む。",
    "if there's no solution": "解決策がなければクライアントにエラーを返す。",
    "proceed with": "フロントエンドが合意すればフォールバックを進める。",
    "quick update": "手短な報告：ダッシュボードは開発環境で準備完了だ。",
    "hopefully by the end of today": "うまくいけば今日中にアラート設定を終えられる。",
    "that's all from me": "私からは以上だ。次の更新に移ろう。",
    "if there is an alternative": "代替案があれば比較できれば助かる。",
    "let's wrap things up here": "もうすぐ昼だから、ここで区切ろう。",
    "is English okay with you?": "始める前に、英語で進めて大丈夫か？",
    "that's fine too": "来週議論する方がよければ、それでも構わない。",
    "looking into": "新しいデプロイ方式を調査している。",
    "give that a try": "1スプリント試してみよう。",
    "if it's too complicated": "複雑すぎるなら現行プロセスを使える。",
    "just fyi": "参考までに、リリースウィンドウは3月だ。",
    "straightforward": "両サービスが同じ方式ならシンプルだ。",
    "an important point": "設計に盛り込むべき重要な点だ。",
    "a more conservative approach": "より慎重な方法は当面両方の選択肢を残すことだ。",
    "it depends on": "トライアル結果次第だ。",
    "in terms of": "デプロイの観点では一貫性を保つべきだ。",
    "in advance": "必要な依存関係を事前に準備する。",
    "assign this to someone else": "多忙なので、他の人に割り当てる。",
    "no dedicated": "現時点では専用環境はまだ存在しない。",
    "take a look at": "会議後にログを確認しよう。",
    "it would be great if": "図を提供してもらえると助かる。",
    "pick up": "次スプリントでこのテストタスクを担当できる。",
    "comments so far?": "ここまでに質問やコメントはあるか？",
    "one thing, and the other thing is": "一つはコスト、もう一つは保守だ。",
    "from what I could find out": "調べた範囲では、このツールは契約テストに対応している。",
    "the only difference is": "唯一の違いはトークン検証方法だ。",
    "sounds good": "了解。シンプルな方で進める。",
    "do the heavy lifting": "基盤フレームワークに重い処理を任せられる。",
    "take a look at that when the time comes": "その段階になったら確認する。",
    "split things up": "並行作業できるよう分割しよう。",
    "take over": "休暇中は別エンジニアが引き継ぐ。",
    "good to know": "参考になった。所有権リストを更新する。",
    "on my side": "私の担当範囲では実装は完了している。",
    "my thought process was": "既存構成を再利用できると考えた。",
    "bring that up": "話題を出してくれてありがたい。妥当な指摘だ。",
    "I found out later that": "後で全サービスが1つの登録を共有していると分かった。",
    "the lesson learned here is": "教訓は認証情報を分離しておくことだ。",
    "from that angle": "その観点から見れば現行構成を維持するのが合理的だ。",
    "set up a guideline": "クロスサービステストのガイドラインを策定する必要がある。",
    "comply with": "全チームがガイドラインに準拠する必要がある。",
    "that requires a slight change to our plan": "来週の計画にわずかな変更が必要になる。",
    "the downside is": "欠点はコードがリポジトリ外で管理されることだ。",
    "there shouldn't be any technical reason why": "スクリプト移設を妨げる技術的理由はないはずだ。",
    "in the meantime": "その間は既存の挙動を維持できる。",
    "it's not a rush": "急ぎではないので、現リリース後に対応できる。",
    "I'm not 100% sure": "完全には確信がないので、フローを確認する。",
    "if that doesn't work": "うまくいかなければ次のウィンドウを使う。",
    "we're trying to figure out": "QAに割り当てるチケットを明確にしようとしている。",
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

