#!/usr/bin/env python3
"""Generate Career / Interview vocabulary markdown files (114 entries)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from career_vocabulary_user_data import USER_ENTRIES

ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = ROOT / "docs" / "vocabulary"
SCENE = "Career / Interview"

DIFFICULTY_ORDER = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}

METADATA: dict[str, dict] = {
    "accelerate delivery": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/əkˈseləreɪt dɪˈlɪvəri/",
        "meaning": "to deliver work faster",
        "description": "Speed up delivery while keeping quality and safety acceptable.",
        "difficulty": "Intermediate",
    },
    "account for work in the plan": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/əˈkaʊnt fɔː wɜːk ɪn ðə plæn/",
        "meaning": "to include work in a plan",
        "description": "Include necessary tasks such as testing or rollback in planning.",
        "difficulty": "Intermediate",
    },
    "action items": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ˈækʃn ˈaɪtəmz/",
        "meaning": "specific tasks assigned after a meeting",
        "description": "Turn discussion outcomes into tasks with owners and deadlines.",
        "difficulty": "Beginner",
    },
    "adapt to changes": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/əˈdæpt tuː ˈtʃeɪndʒɪz/",
        "meaning": "to adjust when conditions change",
        "description": "Adjust plans when priorities, risks, or constraints shift.",
        "difficulty": "Intermediate",
    },
    "address issues": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/əˈdres ˈɪʃuːz/",
        "meaning": "to deal with problems",
        "description": "Take action on problems affecting delivery, quality, or reliability.",
        "difficulty": "Beginner",
    },
    "align on": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/əˈlaɪn ɒn/",
        "meaning": "to agree on a specific point",
        "description": "Reach shared agreement on a specific topic before starting work.",
        "difficulty": "Beginner",
    },
    "align on common goals": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/əˈlaɪn ɒn ˈkɒmən ɡəʊlz/",
        "meaning": "to agree on shared objectives",
        "description": "Agree on shared objectives before debating implementation details.",
        "difficulty": "Intermediate",
    },
    "align stakeholders": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/əˈlaɪn ˈsteɪkhəʊldəz/",
        "meaning": "to get stakeholders to agree",
        "description": "Build agreement among people affected by a decision or rollout.",
        "difficulty": "Intermediate",
    },
    "align with": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/əˈlaɪn wɪð/",
        "meaning": "to match or agree with something",
        "description": "Match your approach with another team, policy, or direction.",
        "difficulty": "Beginner",
    },
    "allow time for learning and investigation": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/əˈlaʊ taɪm fɔː ˈlɜːnɪŋ ænd ɪnˌvestɪˈɡeɪʃn/",
        "meaning": "to reserve time for learning before delivery",
        "description": "Budget time for unknown domains before committing to delivery dates.",
        "difficulty": "Advanced",
    },
    "as a result": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/æz ə rɪˈzʌlt/",
        "meaning": "because of something that happened",
        "description": "Connect an action to its outcome in interview storytelling.",
        "difficulty": "Beginner",
    },
    "assess the risk": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/əˈses ðə rɪsk/",
        "meaning": "to judge how risky something is",
        "description": "Evaluate potential harm before a release or major change.",
        "difficulty": "Intermediate",
    },
    "automate daily work processes": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈɔːtəmeɪt ˈdeɪli wɜːk ˈprəʊsesɪz/",
        "meaning": "to automate routine daily work",
        "description": "Replace repetitive manual steps with automation to save time.",
        "difficulty": "Advanced",
    },
    "best approach": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/best əˈprəʊtʃ/",
        "meaning": "the most suitable way to do something",
        "description": "Recommend the option that best fits constraints and goals.",
        "difficulty": "Intermediate",
    },
    "clarify requirements": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈklærɪfaɪ rɪˈkwaɪəmənts/",
        "meaning": "to make requirements clear",
        "description": "Remove ambiguity in scope, acceptance criteria, or business rules.",
        "difficulty": "Beginner",
    },
    "clear goal": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/klɪə ɡəʊl/",
        "meaning": "a specific and understandable target",
        "description": "Set a specific, measurable target for a project or improvement.",
        "difficulty": "Beginner",
    },
    "collaborate with": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/kəˈlæbəreɪt wɪð/",
        "meaning": "to work jointly with others",
        "description": "Work jointly with others toward a shared engineering goal.",
        "difficulty": "Beginner",
    },
    "contribute to": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/kənˈtrɪbjuːt tuː/",
        "meaning": "to help cause or achieve something",
        "description": "Help achieve a shared outcome through your work or ideas.",
        "difficulty": "Beginner",
    },
    "coordinate with": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/kəʊˈɔːdɪneɪt wɪð/",
        "meaning": "to organize activities with others",
        "description": "Align plans and timing with other teams or stakeholders.",
        "difficulty": "Beginner",
    },
    "cross-functional scope": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/krɒs ˈfʌŋkʃənl skəʊp/",
        "meaning": "work involving multiple functions or teams",
        "description": "Describe work spanning multiple roles, teams, or disciplines.",
        "difficulty": "Advanced",
    },
    "current situation": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ˈkʌrənt ˌsɪtʃuˈeɪʃn/",
        "meaning": "the present state of affairs",
        "description": "Describe the starting context before explaining actions taken.",
        "difficulty": "Beginner",
    },
    "current understanding": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ˈkʌrənt ˌʌndəˈstændɪŋ/",
        "meaning": "what you currently believe is true",
        "description": "Summarize what you know and confirm it with the team.",
        "difficulty": "Intermediate",
    },
    "decided to": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/dɪˈsaɪdɪd tuː/",
        "meaning": "chose to do something after consideration",
        "description": "State a deliberate choice made after reviewing options.",
        "difficulty": "Beginner",
    },
    "define the scope": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/dɪˈfaɪn ðə skəʊp/",
        "meaning": "to set the limits of work",
        "description": "Set boundaries early to prevent uncontrolled scope expansion.",
        "difficulty": "Beginner",
    },
    "delegate tasks": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈdelɪɡeɪt tɑːsks/",
        "meaning": "to assign work to others",
        "description": "Assign work based on skills while staying accountable for results.",
        "difficulty": "Intermediate",
    },
    "design details": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/dɪˈzaɪn ˈdiːteɪlz/",
        "meaning": "specific elements of a design",
        "description": "Fill in concrete design specifics before handoff to implementation.",
        "difficulty": "Intermediate",
    },
    "desired outcome": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/dɪˈzaɪəd ˈaʊtkʌm/",
        "meaning": "the result you want to reach",
        "description": "Clarify the ideal end state before comparing implementation options.",
        "difficulty": "Beginner",
    },
    "drive the project": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/draɪv ðə ˈprɒdʒekt/",
        "meaning": "to actively push a project forward",
        "description": "Act as a central force moving a project toward completion.",
        "difficulty": "Intermediate",
    },
    "drive the transformation forward": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/draɪv ðə ˌtrænsfəˈmeɪʃn ˈfɔːwəd/",
        "meaning": "to push a major change forward",
        "description": "Turn broad organizational goals into executable milestones.",
        "difficulty": "Advanced",
    },
    "end-to-end": {
        "type": "phrase",
        "partOfSpeech": "adjective",
        "pronunciation": "/end tuː end/",
        "meaning": "covering the whole process",
        "description": "Cover an entire workflow from design through production operation.",
        "difficulty": "Beginner",
    },
    "ensure consistency": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɪnˈʃʊə kənˈsɪstənsi/",
        "meaning": "to make things uniform across teams",
        "description": "Standardize practices so teams produce uniform quality and behavior.",
        "difficulty": "Intermediate",
    },
    "evaluate the impact": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɪˈvæljueɪt ði ˈɪmpækt/",
        "meaning": "to judge the effect of something",
        "description": "Measure how a change affected metrics, users, or operations.",
        "difficulty": "Intermediate",
    },
    "execute in a phased manner": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈeksɪkjuːt ɪn ə feɪzd ˈmænə/",
        "meaning": "to carry out work in planned stages",
        "description": "Roll out changes in stages to control operational risk.",
        "difficulty": "Advanced",
    },
    "execute without unnecessary delay": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈeksɪkjuːt wɪˈðaʊt ʌnˈnesəsəri dɪˈleɪ/",
        "meaning": "to act promptly without wasted waiting",
        "description": "Move quickly once scope and risks are understood.",
        "difficulty": "Advanced",
    },
    "expected behavior": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ɪkˈspektɪd bɪˈheɪvjə/",
        "meaning": "the behavior something should show",
        "description": "Define correct system behavior when investigating bugs or incidents.",
        "difficulty": "Beginner",
    },
    "expected outcome": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ɪkˈspektɪd ˈaʊtkʌm/",
        "meaning": "the result you plan to achieve",
        "description": "Define the result you aim to achieve before choosing an approach.",
        "difficulty": "Beginner",
    },
    "experience with": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ɪkˈspɪəriəns wɪð/",
        "meaning": "practical knowledge gained from doing something",
        "description": "State practical background with tools, domains, or responsibilities.",
        "difficulty": "Beginner",
    },
    "final scope": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ˈfaɪnl skəʊp/",
        "meaning": "the agreed range of work",
        "description": "Refer to the agreed delivery boundary after scope discussions.",
        "difficulty": "Beginner",
    },
    "focus on": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈfəʊkəs ɒn/",
        "meaning": "to give most attention to something",
        "description": "Direct attention or effort toward a specific goal, task, or area.",
        "difficulty": "Beginner",
    },
    "follow through on": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈfɒləʊ θruː ɒn/",
        "meaning": "to complete something you promised",
        "description": "Complete agreed actions reliably through to verification.",
        "difficulty": "Beginner",
    },
    "from scratch": {
        "type": "phrase",
        "partOfSpeech": "adverb phrase",
        "pronunciation": "/frɒm skrætʃ/",
        "meaning": "starting with nothing existing",
        "description": "Build something new without relying on an existing implementation.",
        "difficulty": "Beginner",
    },
    "identify common pain points": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/aɪˈdentɪfaɪ ˈkɒmən peɪn pɔɪnts/",
        "meaning": "to find shared recurring problems",
        "description": "Find recurring problems shared across teams or workflows.",
        "difficulty": "Intermediate",
    },
    "identify the root cause": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/aɪˈdentɪfaɪ ðə ruːt kɔːz/",
        "meaning": "to find the basic cause of a problem",
        "description": "Find the underlying cause of a problem, not just its symptoms.",
        "difficulty": "Intermediate",
    },
    "improve future outcomes": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɪmˈpruːv ˈfjuːtʃə ˈaʊtkʌmz/",
        "meaning": "to make later results better",
        "description": "Use retrospectives or feedback to improve later results.",
        "difficulty": "Intermediate",
    },
    "improve monitoring coverage": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɪmˈpruːv ˈmɒnɪtərɪŋ ˈkʌvərɪdʒ/",
        "meaning": "to broaden what systems are monitored",
        "description": "Expand alerts and dashboards so issues are detected sooner.",
        "difficulty": "Advanced",
    },
    "improve your skills": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɪmˈpruːv jɔː skɪlz/",
        "meaning": "to become better at your work",
        "description": "Show continuous growth through practice, study, and real incidents.",
        "difficulty": "Beginner",
    },
    "interested in": {
        "type": "phrase",
        "partOfSpeech": "adjective phrase",
        "pronunciation": "/ˈɪntrəstɪd ɪn/",
        "meaning": "wanting to know or learn about something",
        "description": "Express genuine interest in a role, domain, or type of work.",
        "difficulty": "Beginner",
    },
    "investigate the issue": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ɪnˈvestɪɡeɪt ði ˈɪʃuː/",
        "meaning": "to examine a problem carefully",
        "description": "Lead or perform structured analysis to understand a problem.",
        "difficulty": "Beginner",
    },
    "keep communication transparent": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/kiːp kəˌmjuːnɪˈkeɪʃn trænsˈpeərənt/",
        "meaning": "to share information openly",
        "description": "Share progress, risks, and decisions openly with stakeholders.",
        "difficulty": "Intermediate",
    },
    "keep discussions solution-oriented": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/kiːp dɪˈskʌʃnz səˈluːʃn ˈɔːrientɪd/",
        "meaning": "to focus talks on solving problems",
        "description": "Guide disagreements toward constructive outcomes and shared goals.",
        "difficulty": "Advanced",
    },
    "learn from others": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/lɜːn frɒm ˈʌðəz/",
        "meaning": "to gain knowledge from other people",
        "description": "Improve your work by adopting practices from experienced colleagues.",
        "difficulty": "Beginner",
    },
    "look into": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/lʊk ˈɪntuː/",
        "meaning": "to investigate or examine something",
        "description": "Investigate a problem, option, or request in more detail.",
        "difficulty": "Beginner",
    },
    "make a decision": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/meɪk ə dɪˈsɪʒn/",
        "meaning": "to choose what to do",
        "description": "Choose a direction after weighing facts, risks, and constraints.",
        "difficulty": "Beginner",
    },
    "make a measurable impact": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/meɪk ə ˈmeʒərəbl ˈɪmpækt/",
        "meaning": "to create results that can be measured",
        "description": "Show results that can be quantified with metrics or numbers.",
        "difficulty": "Intermediate",
    },
    "make a technical decision": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/meɪk ə ˈteknɪkl dɪˈsɪʒn/",
        "meaning": "to choose a technical approach",
        "description": "Choose architecture or technology based on engineering trade-offs.",
        "difficulty": "Intermediate",
    },
    "make an informed decision": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/meɪk ən ɪnˈfɔːmd dɪˈsɪʒn/",
        "meaning": "to decide based on good information",
        "description": "Decide after gathering relevant data, constraints, and input.",
        "difficulty": "Intermediate",
    },
    "make progress": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/meɪk ˈprəʊɡres/",
        "meaning": "to advance toward a goal",
        "description": "Show measurable advancement toward resolving a problem or goal.",
        "difficulty": "Beginner",
    },
    "make sense": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/meɪk sens/",
        "meaning": "to be reasonable or logical",
        "description": "Explain why a choice or design is reasonable in context.",
        "difficulty": "Beginner",
    },
    "make sure": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/meɪk ʃʊə/",
        "meaning": "to check or ensure something",
        "description": "Confirm that something is true, done, or safe before proceeding.",
        "difficulty": "Beginner",
    },
    "meet expectations": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/miːt ˌekspekˈteɪʃnz/",
        "meaning": "to satisfy what people expect",
        "description": "Deliver work that satisfies agreed standards or stakeholder needs.",
        "difficulty": "Beginner",
    },
    "miss out on": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/mɪs aʊt ɒn/",
        "meaning": "to fail to get something useful",
        "description": "Warn that a process may lose useful input or opportunities.",
        "difficulty": "Intermediate",
    },
    "move forward": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/muːv ˈfɔːwəd/",
        "meaning": "to continue or proceed with something",
        "description": "Proceed to the next stage after agreement or preparation.",
        "difficulty": "Beginner",
    },
    "move things forward": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/muːv θɪŋz ˈfɔːwəd/",
        "meaning": "to make progress on stalled work",
        "description": "Break stalemates and push stalled work toward concrete next steps.",
        "difficulty": "Beginner",
    },
    "next steps": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/nekst steps/",
        "meaning": "actions planned after the current stage",
        "description": "Name follow-up actions after a decision or discussion.",
        "difficulty": "Beginner",
    },
    "operational gaps": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ˌɒpəˈreɪʃənl ɡæps/",
        "meaning": "weaknesses in operational processes",
        "description": "Identify missing monitoring, runbooks, or response practices.",
        "difficulty": "Advanced",
    },
    "opportunity to": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ˌɒpəˈtjuːnəti tuː/",
        "meaning": "a chance to do something",
        "description": "Describe a chance to take on meaningful work or growth.",
        "difficulty": "Beginner",
    },
    "positive impact": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ˈpɒzətɪv ˈɪmpækt/",
        "meaning": "a beneficial effect",
        "description": "Describe beneficial effects your work had on teams or systems.",
        "difficulty": "Beginner",
    },
    "preventive measures": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/prɪˈventɪv ˈmeʒəz/",
        "meaning": "actions taken to stop recurrence",
        "description": "Introduce safeguards to stop a problem from happening again.",
        "difficulty": "Intermediate",
    },
    "prioritize this work": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/praɪˈɒrətaɪz ðɪs wɜːk/",
        "meaning": "to treat this work as more urgent",
        "description": "Raise urgency for work that affects critical outcomes.",
        "difficulty": "Intermediate",
    },
    "proactively enhance": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/prəʊˈæktɪvli ɪnˈhɑːns/",
        "meaning": "to improve something before being asked",
        "description": "Improve systems or processes before problems force reactive work.",
        "difficulty": "Advanced",
    },
    "proactively onboard new members": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/prəʊˈæktɪvli ˈɒnbɔːd njuː ˈmembəz/",
        "meaning": "to help new members start effectively early",
        "description": "Prepare docs and pairing so newcomers become productive quickly.",
        "difficulty": "Advanced",
    },
    "project priorities": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ˈprɒdʒekt praɪˈɒrətiz/",
        "meaning": "the most important tasks for a project",
        "description": "Adjust plans when the team's focus or urgency changes.",
        "difficulty": "Intermediate",
    },
    "promote continuous improvement": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/prəˈməʊt kənˌtɪnjuəs ˌɪmˈpruːvmənt/",
        "meaning": "to encourage ongoing improvement",
        "description": "Build habits and rituals that keep improving team practices.",
        "difficulty": "Advanced",
    },
    "provide guidance": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/prəˈvaɪd ˈɡaɪdns/",
        "meaning": "to give helpful advice or direction",
        "description": "Advise less experienced engineers during design or delivery.",
        "difficulty": "Intermediate",
    },
    "provide knowledge transfer": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/prəˈvaɪd ˈnɒlɪdʒ ˈtrænsfɜː/",
        "meaning": "to share expertise so others can take over",
        "description": "Hand off expertise so another team can operate the system independently.",
        "difficulty": "Intermediate",
    },
    "provide support": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/prəˈvaɪd səˈpɔːt/",
        "meaning": "to give practical help",
        "description": "Offer hands-on help during migrations, releases, or incidents.",
        "difficulty": "Beginner",
    },
    "provide timelines": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/prəˈvaɪd ˈtaɪmlaɪnz/",
        "meaning": "to give expected schedules",
        "description": "Share schedule estimates with assumptions and known risks.",
        "difficulty": "Beginner",
    },
    "provide visibility into": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/prəˈvaɪd ˌvɪzəˈbɪləti ˈɪntuː/",
        "meaning": "to make something easier to see or understand",
        "description": "Make hidden operational or technical state observable to others.",
        "difficulty": "Advanced",
    },
    "reach out to": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/riːtʃ aʊt tuː/",
        "meaning": "to contact someone",
        "description": "Contact someone proactively for help, input, or coordination.",
        "difficulty": "Beginner",
    },
    "reduce friction": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/rɪˈdjuːs ˈfrɪkʃn/",
        "meaning": "to make work easier and smoother",
        "description": "Remove obstacles that slow onboarding, development, or collaboration.",
        "difficulty": "Intermediate",
    },
    "resolve the issue": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/rɪˈzɒlv ði ˈɪʃuː/",
        "meaning": "to fix or settle a problem",
        "description": "Fix a problem with a concrete solution, not just analysis.",
        "difficulty": "Beginner",
    },
    "resulted in": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/rɪˈzʌltɪd ɪn/",
        "meaning": "caused a particular outcome",
        "description": "State the concrete outcome caused by your work or change.",
        "difficulty": "Beginner",
    },
    "review the requirements": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/rɪˈvjuː ðə rɪˈkwaɪəmənts/",
        "meaning": "to examine requirements carefully",
        "description": "Check requirements with stakeholders before estimating or building.",
        "difficulty": "Beginner",
    },
    "risk assessment": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/rɪsk əˈsesmənt/",
        "meaning": "a formal review of risks",
        "description": "Refer to a structured review of risks affecting a decision.",
        "difficulty": "Intermediate",
    },
    "roll out": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/rəʊl aʊt/",
        "meaning": "to introduce something gradually",
        "description": "Release or deploy a change gradually to users or environments.",
        "difficulty": "Beginner",
    },
    "scope and complexity": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/skəʊp ænd kəmˈpleksəti/",
        "meaning": "the size and difficulty of work",
        "description": "Explain estimates using both breadth of work and technical difficulty.",
        "difficulty": "Intermediate",
    },
    "share knowledge": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ʃeə ˈnɒlɪdʒ/",
        "meaning": "to pass useful information to others",
        "description": "Spread what you learned so others can work more effectively.",
        "difficulty": "Beginner",
    },
    "short-term and long-term": {
        "type": "phrase",
        "partOfSpeech": "adjective phrase",
        "pronunciation": "/ʃɔːt tɜːm ænd lɒŋ tɜːm/",
        "meaning": "covering both immediate and future time frames",
        "description": "Separate immediate fixes from durable improvements in planning.",
        "difficulty": "Intermediate",
    },
    "short-term solution": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ʃɔːt tɜːm səˈluːʃn/",
        "meaning": "a temporary fix for a problem",
        "description": "Propose a temporary fix while planning a sustainable long-term approach.",
        "difficulty": "Beginner",
    },
    "solve complex problems": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/sɒlv ˈkɒmpleks ˈprɒbləmz/",
        "meaning": "to resolve difficult issues",
        "description": "Handle difficult issues needing deep analysis and coordination.",
        "difficulty": "Intermediate",
    },
    "started the analysis": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈstɑːtɪd ði əˈnæləsɪs/",
        "meaning": "to begin examining a problem systematically",
        "description": "Describe how you began structured analysis in a STAR Action section.",
        "difficulty": "Intermediate",
    },
    "stay on schedule": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/steɪ ɒn ˈʃedjuːl/",
        "meaning": "to finish work on time",
        "description": "Keep delivery on track through scope or priority trade-offs.",
        "difficulty": "Intermediate",
    },
    "step up when the team needs you": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/step ʌp wen ðə tiːm niːdz juː/",
        "meaning": "to help when the team is in need",
        "description": "Take responsibility voluntarily during gaps or urgent moments.",
        "difficulty": "Intermediate",
    },
    "streamline routine tasks": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/ˈstriːmlaɪn ruːˈtiːn tɑːsks/",
        "meaning": "to make regular work more efficient",
        "description": "Simplify repetitive work so the team can focus on higher-value tasks.",
        "difficulty": "Intermediate",
    },
    "strike a better balance": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/straɪk ə ˈbetə ˈbæləns/",
        "meaning": "to find a better compromise",
        "description": "Find a workable compromise between competing priorities.",
        "difficulty": "Intermediate",
    },
    "successfully completed": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/səkˈsesfli kəmˈpliːtɪd/",
        "meaning": "finished something with success",
        "description": "Report finishing a project or milestone without major issues.",
        "difficulty": "Beginner",
    },
    "support the team": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/səˈpɔːt ðə tiːm/",
        "meaning": "to help a team succeed",
        "description": "Help teammates succeed through reviews, unblocking, or guidance.",
        "difficulty": "Beginner",
    },
    "take a data-driven approach": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/teɪk ə ˈdeɪtə ˈdrɪvn əˈprəʊtʃ/",
        "meaning": "to decide using data and evidence",
        "description": "Use metrics and evidence rather than intuition alone.",
        "difficulty": "Intermediate",
    },
    "take action": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/teɪk ˈækʃn/",
        "meaning": "to do something in response to a situation",
        "description": "Act on a problem or risk instead of only observing it.",
        "difficulty": "Beginner",
    },
    "take constraints into consideration": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/teɪk kənˈstreɪnts ˌɪntuː kənˌsɪdəˈreɪʃn/",
        "meaning": "to include limits when deciding",
        "description": "Factor security, cost, and schedule limits into decisions.",
        "difficulty": "Intermediate",
    },
    "take ownership of": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/teɪk əʊnəʃɪp ɒv/",
        "meaning": "to accept responsibility for something",
        "description": "Accept responsibility and drive work proactively beyond your lane.",
        "difficulty": "Intermediate",
    },
    "take the lead": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/teɪk ði liːd/",
        "meaning": "to be the main person driving something",
        "description": "Lead an initiative even without a formal leadership title.",
        "difficulty": "Beginner",
    },
    "targeted fix": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ˈtɑːɡɪtɪd fɪks/",
        "meaning": "a precise fix for a specific cause",
        "description": "Apply a precise correction aimed at the actual cause.",
        "difficulty": "Intermediate",
    },
    "the outcome": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ðiː ˈaʊtkʌm/",
        "meaning": "the final result of an action or project",
        "description": "State the final measurable result of your actions in STAR interviews.",
        "difficulty": "Beginner",
    },
    "track progress": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/træk ˈprəʊɡres/",
        "meaning": "to monitor how work is advancing",
        "description": "Monitor milestones and raise blockers early during delivery.",
        "difficulty": "Beginner",
    },
    "trade-off": {
        "type": "word",
        "partOfSpeech": "noun",
        "pronunciation": "/ˈtreɪd ɒf/",
        "meaning": "a balance between two competing factors",
        "description": "Explain a balance where improving one factor sacrifices another.",
        "difficulty": "Beginner",
    },
    "valuable feedback": {
        "type": "phrase",
        "partOfSpeech": "noun phrase",
        "pronunciation": "/ˈvæljuəbl ˈfiːdbæk/",
        "meaning": "useful comments or advice",
        "description": "Acknowledge useful input from others and act on it.",
        "difficulty": "Beginner",
    },
    "weigh the pros and cons": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/weɪ ðə prəʊz ænd kɒnz/",
        "meaning": "to compare advantages and disadvantages",
        "description": "Compare advantages and disadvantages before recommending a path.",
        "difficulty": "Intermediate",
    },
    "work alongside the team": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/wɜːk əˈlɒŋsaɪd ðə tiːm/",
        "meaning": "to work together with a team closely",
        "description": "Partner closely with a team for a period rather than directing remotely.",
        "difficulty": "Intermediate",
    },
    "work closely with": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/wɜːk ˈkləʊsli wɪð/",
        "meaning": "to collaborate intensively with someone",
        "description": "Collaborate intensively with another role or team on shared goals.",
        "difficulty": "Beginner",
    },
    "work independently": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/wɜːk ˌɪndɪˈpendəntli/",
        "meaning": "to work without close supervision",
        "description": "Progress work with minimal supervision while keeping others informed.",
        "difficulty": "Beginner",
    },
    "work toward a goal": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/wɜːk təˈwɔːd ə ɡəʊl/",
        "meaning": "to make effort to reach a goal",
        "description": "Describe sustained effort aligned toward a shared objective.",
        "difficulty": "Beginner",
    },
    "work with limited bandwidth": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/wɜːk wɪð ˈlɪmɪtɪd ˈbændwɪdθ/",
        "meaning": "to work with little available capacity",
        "description": "Deliver results despite tight time or staffing constraints.",
        "difficulty": "Intermediate",
    },
    "work within the scope": {
        "type": "phrase",
        "partOfSpeech": "verb phrase",
        "pronunciation": "/wɜːk wɪˈðɪn ðə skəʊp/",
        "meaning": "to stay inside agreed boundaries",
        "description": "Deliver agreed work and defer extra requests appropriately.",
        "difficulty": "Intermediate",
    },
}

USAGE_EXAMPLE_JA: dict[str, str] = {
    "accelerate delivery": "検証を自動化し、品質を保ちながら提供速度を上げた。",
    "account for work in the plan": "移行テストとロールバック準備を提供計画に盛り込んだ。",
    "action items": "議論を担当者と期限付きアクション項目に落とし込んだ。",
    "adapt to changes": "優先度変更に合わせ計画とテスト工数を再配分した。",
    "address issues": "リリース遅延のビルドパイプライン課題に対応した。",
    "align on": "実装前に命名規則について認識を合わせた。",
    "align on common goals": "実装詳細の前に共通目標でチームを揃えた。",
    "align stakeholders": "共通展開計画と成功基準で関係者を揃えた。",
    "align with": "認証フロー変更前にセキュリティチームと整合を取った。",
    "allow time for learning and investigation": "未知領域のため、見積もりに学習・調査時間を確保した。",
    "as a result": "その結果、リリース準備時間が2日から3時間に短縮した。",
    "assess the risk": "リリース前にリスクを評価し段階展開を提案した。",
    "automate daily work processes": "日常業務を自動化し、チームの週あたり数時間を削減した。",
    "best approach": "3案を評価し、制約に最適な手法を提案した。",
    "clarify requirements": "ビジネスチームと要件と受入基準を明確化した。",
    "clear goal": "復旧時間を20%以上短縮する明確な目標を設定した。",
    "collaborate with": "基盤エンジニアと協働し保守しやすいデプロイ手順を設計した。",
    "contribute to": "デプロイ基盤の改善でプラットフォームに貢献した。",
    "coordinate with": "セキュリティ・運用と調整し展開計画を確定した。",
    "cross-functional scope": "エンジニアリング・セキュリティ・運用横断の範囲だった。",
    "current situation": "現状と既存設計の制約を説明することから始めた。",
    "current understanding": "現時点の理解を整理し、チームに確認を求めた。",
    "decided to": "新機能より信頼性を優先することを決めた。",
    "define the scope": "早期にスコープを定義し、計画外の拡大を防いだ。",
    "delegate tasks": "専門性に応じて委任し、成果には責任を持った。",
    "design details": "実装チームへ引き渡す前に不足していた設計詳細を補完した。",
    "desired outcome": "目指す成果を明確にし、逆算で最善策を導いた。",
    "drive the project": "依存関係を解消し関係者を揃えてプロジェクトを推進した。",
    "drive the transformation forward": "大きな目標を実行可能なマイルストーンに落とし変革を推進した。",
    "end-to-end": "設計から本番監視まで機能を一貫して担当した。",
    "ensure consistency": "共通テンプレで全サービスの一貫性を確保した。",
    "evaluate the impact": "CV率・レイテンシ・問合せ件数で影響を評価した。",
    "execute in a phased manner": "運用リスクを抑え段階的に移行を実行した。",
    "execute without unnecessary delay": "スコープ確定後、遅延なく復旧計画を実行した。",
    "expected behavior": "期待動作を文書化し、本番ログと比較した。",
    "expected outcome": "技術方針決定前に期待成果を定義した。",
    "experience with": "分散システムとクラウド基盤で5年の実務経験がある。",
    "final scope": "最終スコープ合意後、現実的な提供計画を作成した。",
    "focus on": "高リスク箇所から優先して対応した。",
    "follow through on": "全アクションを完遂し、本番で修正を確認した。",
    "from scratch": "パイプラインを一から構築し、チーム向けに文書化した。",
    "identify common pain points": "複数チームへヒアリングしデプロイの共通課題を特定した。",
    "identify the root cause": "ログ解析と再現で根本原因を特定した。",
    "improve future outcomes": "FBを活かし今後の成果とプログラムを改善した。",
    "improve monitoring coverage": "不足アラートとダッシュボード追加で監視範囲を改善した。",
    "improve your skills": "障害対応と障害パターン分析で可用性スキルを向上させた。",
    "interested in": "プラットフォームエンジニアリングと開発生産性に関心がある。",
    "investigate the issue": "リクエスト経路全体の権限を追跡し問題を調査した。",
    "keep communication transparent": "毎週リスクと進捗を共有し透明なコミュニケーションを保った。",
    "keep discussions solution-oriented": "対立時も解決志向で共通目標に議論を集中させた。",
    "learn from others": "先輩エンジニアからレビュー手法を学び取り入れた。",
    "look into": "間欠障害を調査し、競合状態を発見した。",
    "make a decision": "両案の運用コストと信頼性を比較し意思決定した。",
    "make a measurable impact": "デプロイ時間40%短縮という測定可能な成果を出した。",
    "make a technical decision": "スケール要件に基づきサービス分割を技術決定した。",
    "make an informed decision": "利用データとセキュリティ要件を収集し、十分な情報で判断した。",
    "make progress": "応急修正と再設計を分離し前進させた。",
    "make sense": "同一ライフサイクルのため、部品統合は合理的だった。",
    "make sure": "データ整合性を保つ自動チェックを追加した。",
    "meet expectations": "セキュリティを損なわず関係者の期待に応える実装に調整した。",
    "miss out on": "共有レビューがなければ他チームの有用な知見を逃す。",
    "move forward": "合意後、実装へ前進させた。",
    "move things forward": "チームが対立した際、集中議論を設定し前進させた。",
    "next steps": "決定を整理し、各チームの次アクションを明確にした。",
    "operational gaps": "レビューで監視と障害対応の運用上の不足を特定した。",
    "opportunity to": "部門横断移行プロジェクトを率いる機会を活かした。",
    "positive impact": "変更は信頼性と開発生産性の両方に良い影響を与えた。",
    "preventive measures": "自動検証と手順書整備など再発防止策を導入した。",
    "prioritize this work": "重要なカスタマージャーニーに影響するため優先した。",
    "proactively enhance": "重要フェーズ前にテスト基盤を先回り強化した。",
    "proactively onboard new members": "資料準備と初回スプリントのペアリングで新メンバーを先回り支援した。",
    "project priorities": "プロジェクト優先度の変更に合わせ計画を見直した。",
    "promote continuous improvement": "定例振り返りで継続的改善を推進した。",
    "provide guidance": "設計・レビュー段階でジュニアエンジニアへ指導した。",
    "provide knowledge transfer": "運用チームが独立保守できるよう知識引き継ぎを行った。",
    "provide support": "移行中、変更レビューとエスカレーション対応で支援した。",
    "provide timelines": "要件確認後、前提とリスク付きスケジュールを提示した。",
    "provide visibility into": "ダッシュボードでデプロイ健全性とリソース使用を可視化した。",
    "reach out to": "要件が不明確な際、専門家に相談した。",
    "reduce friction": "セットアップ標準化で参画エンジニアの摩擦を減らした。",
    "resolve the issue": "設定修正と回帰テスト追加で課題を解決した。",
    "resulted in": "最適化によりレイテンシ低下とタイムアウト減少を実現した。",
    "review the requirements": "見積前に関係者と要件を確認した。",
    "risk assessment": "セキュリティ・可用性・運用コストのリスク評価を実施した。",
    "roll out": "全量リリース前に小規模ユーザーグループへ展開した。",
    "scope and complexity": "移行の範囲と複雑さからスケジュールを見積もった。",
    "share knowledge": "設計レビューと技術勉強会で知識を共有した。",
    "short-term and long-term": "改善を短期・長期アクションに分けた。",
    "short-term solution": "恒久設計と並行し短期対応を提案した。",
    "solve complex problems": "技術深度と関係者調整が要る複雑課題の解決が好きだ。",
    "started the analysis": "環境横断の障害パターン整理から分析を開始した。",
    "stay on schedule": "重要品質を保ち予定通り進めるため初期スコープを調整した。",
    "step up when the team needs you": "重要リリース時、暫定テックリードとして主導した。",
    "streamline routine tasks": "定型業務を効率化し、高付加価値作業へ集中させた。",
    "strike a better balance": "自律性と一貫性のバランスを取るハイブリッド戦略を提案した。",
    "successfully completed": "顧客影響なしで移行を完了した。",
    "support the team": "設計レビューと技術的障害の除去でチームを支援した。",
    "take a data-driven approach": "データに基づき、顧客影響の大きい障害を優先した。",
    "take action": "リスク確認後、本番影響前に行動を起こした。",
    "take constraints into consideration": "アーキテクチャ選定前にセキュリティ・コスト・納期制約を考慮した。",
    "take ownership of": "移行を主体的に担い、3チーム横断の展開を調整した。",
    "take the lead": "再設計を主導し、実装までチームを支援した。",
    "targeted fix": "広範な回避策ではなく的確な修正を実装した。",
    "the outcome": "結果としてデプロイ失敗が30%減少した。",
    "track progress": "週次マイルストーンで進捗を追い、障害を早期に共有した。",
    "trade-off": "主なトレードオフは提供速度と長期保守性だった。",
    "valuable feedback": "貴重なFBを集め、設計の簡素化に活かした。",
    "weigh the pros and cons": "サービス集約の長所短所を比較し提案した。",
    "work alongside the team": "2スプリント伴走し新しい自動化の定着を支援した。",
    "work closely with": "PMと密に連携し、顧客ニーズを技術要件に落とし込んだ。",
    "work independently": "調査は自律的に進めつつ、チームへ状況を共有した。",
    "work toward a goal": "安全なサービス復旧という共通目標に取り組んだ。",
    "work with limited bandwidth": "余力が限られる中、高リスクシナリオを優先した。",
    "work within the scope": "合意スコープ内で作業し、追加要望は次フェーズ用に記録した。",
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

    for idx, entry in enumerate(entries, start=1):
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
