#!/usr/bin/env python3
"""Generate Incident Response vocabulary markdown files (99 entries)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from incident_vocabulary_user_data import USER_ENTRIES

ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = ROOT / "docs" / "vocabulary"
SCENE = "Incident Response"
START_ID = 471

DIFFICULTY_ORDER = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}

METADATA: dict[str, dict] = {'notice the status had changed': {'type': 'phrase',
                                   'partOfSpeech': 'verb phrase',
                                   'pronunciation': '/ˈnəʊtɪs ðə ˈsteɪtəs hæd tʃeɪndʒd/',
                                   'meaning': 'to notice the status changed',
                                   'description': 'Report that an incident status changed, such as '
                                                  'to Resolved.',
                                   'difficulty': 'Intermediate'},
 'An alert occurred in this thread as well': {'type': 'phrase',
                                              'partOfSpeech': 'clause',
                                              'pronunciation': '/ən əˈlɜːt əˈkɜːd ɪn ðɪs θred æz '
                                                               'wel/',
                                              'meaning': 'an alert also fired in this thread',
                                              'description': 'Report that the same alert channel '
                                                             'or thread saw another alert.',
                                              'difficulty': 'Intermediate'},
 'The alert keeps getting triggered': {'type': 'phrase',
                                       'partOfSpeech': 'clause',
                                       'pronunciation': '/ði əˈlɜːt kiːps ˈɡetɪŋ ˈtrɪɡəd/',
                                       'meaning': 'the alert keeps firing',
                                       'description': 'Share that alerts are repeating at short '
                                                      'intervals during an incident.',
                                       'difficulty': 'Intermediate'},
 'alerts suddenly started firing frequently': {'type': 'phrase',
                                               'partOfSpeech': 'clause',
                                               'pronunciation': '/əˈlɜːts ˈsʌdnli ˈstɑːtɪd '
                                                                'ˈfaɪərɪŋ ˈfriːkwəntli/',
                                               'meaning': 'alerts suddenly began firing often',
                                               'description': 'Report a sudden increase in alert '
                                                              'frequency during an incident.',
                                               'difficulty': 'Intermediate'},
 'Is the alert still active?': {'type': 'phrase',
                                'partOfSpeech': 'clause',
                                'pronunciation': '/ɪz ði əˈlɜːt stɪl ˈæktɪv/',
                                'meaning': 'is the alert still firing',
                                'description': 'Ask whether an alert is still open or was '
                                               'auto-resolved.',
                                'difficulty': 'Beginner'},
 'CPU usage briefly spiked again': {'type': 'phrase',
                                    'partOfSpeech': 'clause',
                                    'pronunciation': '/ˌsiː piː ˈjuːsɪdʒ ˈbriːfli spaɪkt əˈɡen/',
                                    'meaning': 'CPU usage spiked again briefly',
                                    'description': 'Report a short CPU spike and note whether it '
                                                   'is easing.',
                                    'difficulty': 'Intermediate'},
 'seeing lots of ... in the logs': {'type': 'phrase',
                                    'partOfSpeech': 'verb phrase',
                                    'pronunciation': '/ˈsiːɪŋ lɒts əv ɪn ðə lɒɡz/',
                                    'meaning': 'seeing many occurrences in logs',
                                    'description': 'Share that logs show many instances of a '
                                                   'specific error pattern.',
                                    'difficulty': 'Intermediate'},
 'usage is gradually increasing': {'type': 'phrase',
                                   'partOfSpeech': 'clause',
                                   'pronunciation': '/ˈjuːsɪdʒ ɪz ˈɡrædʒuəli ɪŋˈkriːsɪŋ/',
                                   'meaning': 'usage is slowly rising',
                                   'description': 'Report gradual resource growth rather than a '
                                                  'sudden spike.',
                                   'difficulty': 'Intermediate'},
 'successful requests have dropped to zero': {'type': 'phrase',
                                              'partOfSpeech': 'clause',
                                              'pronunciation': '/səkˈsesfl rɪˈkwests hæv drɒpt tuː '
                                                               'ˈzɪərəʊ/',
                                              'meaning': 'successful requests fell to zero',
                                              'description': 'Report zero successful requests as a '
                                                             'severe customer impact signal.',
                                              'difficulty': 'Intermediate'},
 'The error started again': {'type': 'phrase',
                             'partOfSpeech': 'clause',
                             'pronunciation': '/ði ˈerə ˈstɑːtɪd əˈɡen/',
                             'meaning': 'the error recurred',
                             'description': 'Report that an error has started happening again and '
                                            'when.',
                             'difficulty': 'Beginner'},
 'Be quickly auto-resolved': {'type': 'phrase',
                              'partOfSpeech': 'verb phrase',
                              'pronunciation': '/biː ˈkwɪkli ˌɔːtəʊ rɪˈzɒlvd/',
                              'meaning': 'to be auto-resolved quickly',
                              'description': 'Note alerts cleared quickly, suggesting a brief or '
                                             'false-positive spike.',
                              'difficulty': 'Intermediate'},
 'Might be worth checking what happened': {'type': 'phrase',
                                           'partOfSpeech': 'clause',
                                           'pronunciation': '/maɪt biː wɜːθ ˈtʃekɪŋ wɒt ˈhæpənd/',
                                           'meaning': 'worth investigating what happened',
                                           'description': 'Suggest checking events during a spike '
                                                          'even if impact seems low.',
                                           'difficulty': 'Intermediate'},
 'check if there is any impact': {'type': 'phrase',
                                  'partOfSpeech': 'verb phrase',
                                  'pronunciation': '/tʃek ɪf ðeər ɪz ˈeni ˈɪmpækt/',
                                  'meaning': 'to check for any impact',
                                  'description': 'Verify whether production traffic or users are '
                                                 'affected.',
                                  'difficulty': 'Beginner'},
 'should not affect ... but let me verify': {'type': 'phrase',
                                             'partOfSpeech': 'clause',
                                             'pronunciation': '/ʃʊd nɒt əˈfekt bət let miː '
                                                              'ˈverɪfaɪ/',
                                             'meaning': 'likely no impact but verifying',
                                             'description': 'State low expected impact while '
                                                            'confirming production safety.',
                                             'difficulty': 'Intermediate'},
 'should not impact the user experience': {'type': 'phrase',
                                           'partOfSpeech': 'clause',
                                           'pronunciation': '/ʃʊd nɒt ˈɪmpækt ðə ˈjuːzə '
                                                            'ɪkˈspɪəriəns/',
                                           'meaning': 'should not affect user experience',
                                           'description': 'Say UX impact is unlikely while '
                                                          'verification is still underway.',
                                           'difficulty': 'Intermediate'},
 'users cannot log in to production': {'type': 'phrase',
                                       'partOfSpeech': 'clause',
                                       'pronunciation': '/ˈjuːzəz ˈkænɒt lɒɡ ɪn tuː prəˈdʌkʃn/',
                                       'meaning': 'users cannot log in to production',
                                       'description': 'Report a production login outage or similar '
                                                      'functional failure.',
                                       'difficulty': 'Beginner'},
 'might have been affected during the downtime': {'type': 'phrase',
                                                  'partOfSpeech': 'clause',
                                                  'pronunciation': '/maɪt hæv biːn əˈfektɪd '
                                                                   'ˈdjʊərɪŋ ðə ˈdaʊntaɪm/',
                                                  'meaning': 'may have been affected during '
                                                             'downtime',
                                                  'description': 'State possible user impact when '
                                                                 'scope is not yet confirmed.',
                                                  'difficulty': 'Intermediate'},
 'at maximum, ... users were impacted': {'type': 'phrase',
                                         'partOfSpeech': 'clause',
                                         'pronunciation': '/æt ˈmæksɪməm ˈjuːzəz wɜː ˈɪmpæktɪd/',
                                         'meaning': 'at most, some users were impacted',
                                         'description': 'Share a worst-case estimate of how many '
                                                        'users were affected.',
                                         'difficulty': 'Intermediate'},
 'evaluate the number of impacted users': {'type': 'phrase',
                                           'partOfSpeech': 'verb phrase',
                                           'pronunciation': '/ɪˈvæljueɪt ðə ˈnʌmbər əv ˈɪmpæktɪd '
                                                            'ˈjuːzəz/',
                                           'meaning': 'to assess how many users were affected',
                                           'description': 'Call for measuring impact scope by '
                                                          'counting affected users.',
                                           'difficulty': 'Intermediate'},
 'have a significant impact on business KPIs': {'type': 'phrase',
                                                'partOfSpeech': 'verb phrase',
                                                'pronunciation': '/hæv ə sɪɡˈnɪfɪkənt ˈɪmpækt ɒn '
                                                                 'ˈbɪznəs keɪ piː aɪz/',
                                                'meaning': 'to significantly affect business KPIs',
                                                'description': 'Describe measurable business '
                                                               'impact such as sign-ups or '
                                                               'revenue.',
                                                'difficulty': 'Intermediate'},
 'clarify which features were unavailable': {'type': 'phrase',
                                             'partOfSpeech': 'verb phrase',
                                             'pronunciation': '/ˈklærɪfaɪ wɪtʃ ˈfiːtʃəz wɜː '
                                                              'ˌʌnəˈveɪləbl/',
                                             'meaning': 'to clarify unavailable features',
                                             'description': 'Identify which features were down to '
                                                            'define customer impact scope.',
                                             'difficulty': 'Intermediate'},
 'Identify the impact scope at the user or session level': {'type': 'phrase',
                                                            'partOfSpeech': 'verb phrase',
                                                            'pronunciation': '/aɪˈdentɪfaɪ ði '
                                                                             'ˈɪmpækt skəʊp æt ðə '
                                                                             'ˈjuːzə ɔː ˈseʃn '
                                                                             'ˈlevl/',
                                                            'meaning': 'to pinpoint impact per '
                                                                       'user or session',
                                                            'description': 'Ask for granular '
                                                                           'impact analysis at '
                                                                           'user or session level.',
                                                            'difficulty': 'Advanced'},
 'limit the impact scope to the target features': {'type': 'phrase',
                                                   'partOfSpeech': 'verb phrase',
                                                   'pronunciation': '/ˈlɪmɪt ði ˈɪmpækt skəʊp tuː '
                                                                    'ðə ˈtɑːɡɪt ˈfiːtʃəz/',
                                                   'meaning': 'to confine impact to target '
                                                              'features',
                                                   'description': 'Keep blast radius limited to '
                                                                  'specific features during '
                                                                  'mitigation.',
                                                   'difficulty': 'Intermediate'},
 'as long as production is healthy': {'type': 'phrase',
                                      'partOfSpeech': 'clause',
                                      'pronunciation': '/æz lɒŋ æz prəˈdʌkʃn ɪz ˈhelθi/',
                                      'meaning': 'while production remains healthy',
                                      'description': 'Propose deferring urgent work if production '
                                                     'is still stable.',
                                      'difficulty': 'Beginner'},
 'be safe on the product side': {'type': 'phrase',
                                 'partOfSpeech': 'verb phrase',
                                 'pronunciation': '/biː seɪf ɒn ðə ˈprɒdʌkt saɪd/',
                                 'meaning': 'to be safe on the product side',
                                 'description': 'Say backend looks fine while other layers still '
                                                'need investigation.',
                                 'difficulty': 'Intermediate'},
 'seem to be the same issue': {'type': 'phrase',
                               'partOfSpeech': 'verb phrase',
                               'pronunciation': '/siːm tuː biː ðə seɪm ˈɪʃuː/',
                               'meaning': 'to appear to be the same issue',
                               'description': 'Compare current symptoms with a prior incident or '
                                              'pattern.',
                               'difficulty': 'Beginner'},
 'look slightly different': {'type': 'phrase',
                             'partOfSpeech': 'verb phrase',
                             'pronunciation': '/lʊk ˈslaɪtli ˈdɪfrənt/',
                             'meaning': 'to look a bit different',
                             'description': 'Note differences from a previous similar incident or '
                                            'error log.',
                             'difficulty': 'Beginner'},
 "doesn't seem to be an app issue": {'type': 'phrase',
                                     'partOfSpeech': 'clause',
                                     'pronunciation': '/ˈdʌznt siːm tuː biː ən æp ˈɪʃuː/',
                                     'meaning': 'does not look like an app issue',
                                     'description': 'Rule out the application layer and look for '
                                                    'other causes.',
                                     'difficulty': 'Intermediate'},
 'the error originates from ...': {'type': 'phrase',
                                   'partOfSpeech': 'clause',
                                   'pronunciation': '/ði ˈerə əˈrɪdʒɪneɪts frɒm/',
                                   'meaning': 'the error comes from a specific layer',
                                   'description': 'Point to the component or layer where the error '
                                                  'starts.',
                                   'difficulty': 'Intermediate'},
 'come from canary': {'type': 'phrase',
                      'partOfSpeech': 'verb phrase',
                      'pronunciation': '/kʌm frɒm ˈkænəri/',
                      'meaning': 'to come from the canary environment',
                      'description': 'Clarify failing traffic is from canary, not production.',
                      'difficulty': 'Intermediate'},
 'cannot see errors from production': {'type': 'phrase',
                                       'partOfSpeech': 'clause',
                                       'pronunciation': '/ˈkænɒt siː ˈerəz frɒm prəˈdʌkʃn/',
                                       'meaning': 'cannot see production errors',
                                       'description': 'Report no matching server errors found in '
                                                      'production logs.',
                                       'difficulty': 'Intermediate'},
 'find the source': {'type': 'phrase',
                     'partOfSpeech': 'verb phrase',
                     'pronunciation': '/faɪnd ðə sɔːs/',
                     'meaning': 'to find the source',
                     'description': 'Locate where alert or error traffic originates before '
                                    'changing rules.',
                     'difficulty': 'Beginner'},
 'the URL path seems consistent': {'type': 'phrase',
                                   'partOfSpeech': 'clause',
                                   'pronunciation': '/ðə juː ɑːr el pɑːθ siːmz kənˈsɪstənt/',
                                   'meaning': 'the URL path looks consistent',
                                   'description': 'Highlight a common URL pattern across recent '
                                                  'incident events.',
                                   'difficulty': 'Intermediate'},
 'confirm whether ... is performing testing': {'type': 'phrase',
                                               'partOfSpeech': 'verb phrase',
                                               'pronunciation': '/kənˈfɜːm ˈweðər ɪz pəˈfɔːmɪŋ '
                                                                'ˈtestɪŋ/',
                                               'meaning': 'to confirm whether testing is running',
                                               'description': 'Check if load tests or another '
                                                              "team's work caused the alerts.",
                                               'difficulty': 'Intermediate'},
 'match the incident timeline': {'type': 'phrase',
                                 'partOfSpeech': 'verb phrase',
                                 'pronunciation': '/mætʃ ði ˈɪnsɪdənt ˈtaɪmlaɪn/',
                                 'meaning': 'to match the incident timeline',
                                 'description': 'Say log or event timestamps align with the '
                                                'incident window.',
                                 'difficulty': 'Intermediate'},
 'link the events together': {'type': 'phrase',
                              'partOfSpeech': 'verb phrase',
                              'pronunciation': '/lɪŋk ði ɪˈvents təˈɡeðə/',
                              'meaning': 'to connect related events',
                              'description': 'Relate separate signals such as traffic drops and '
                                             'log errors.',
                              'difficulty': 'Intermediate'},
 'confirm that the root cause is the same': {'type': 'phrase',
                                             'partOfSpeech': 'verb phrase',
                                             'pronunciation': '/kənˈfɜːm ðæt ðə ruːt kɔːz ɪz ðə '
                                                              'seɪm/',
                                             'meaning': 'to confirm a shared root cause',
                                             'description': 'Check whether multiple alerts share '
                                                            'one underlying cause.',
                                             'difficulty': 'Intermediate'},
 'have no spike and no obvious increase': {'type': 'phrase',
                                           'partOfSpeech': 'clause',
                                           'pronunciation': '/hæv nəʊ spaɪk ænd nəʊ ˈɒbviəs '
                                                            'ˈɪŋkriːs/',
                                           'meaning': 'no spike or clear increase seen',
                                           'description': 'Report no notable spike or error '
                                                          'increase after investigation.',
                                           'difficulty': 'Intermediate'},
 "can't seem to find any relevant logs": {'type': 'phrase',
                                          'partOfSpeech': 'clause',
                                          'pronunciation': '/kɑːnt siːm tuː faɪnd ˈeni ˈreləvənt '
                                                           'lɒɡz/',
                                          'meaning': 'cannot find relevant logs',
                                          'description': 'State that needed logs are missing or '
                                                         'not being emitted.',
                                          'difficulty': 'Intermediate'},
 'need more details to investigate further': {'type': 'phrase',
                                              'partOfSpeech': 'clause',
                                              'pronunciation': '/niːd mɔː ˈdiːteɪlz tuː '
                                                               'ɪnˈvestɪɡeɪt ˈfɜːðə/',
                                              'meaning': 'need more details to continue',
                                              'description': 'Ask for missing repro steps, logs, '
                                                             'or context to proceed.',
                                              'difficulty': 'Beginner'},
 'appear to be a consequence of ...': {'type': 'phrase',
                                       'partOfSpeech': 'verb phrase',
                                       'pronunciation': '/əˈpɪə tuː biː ə ˈkɒnsɪkwəns əv/',
                                       'meaning': 'to appear caused by something else',
                                       'description': 'Frame an error as a secondary effect of an '
                                                      'upstream failure.',
                                       'difficulty': 'Intermediate'},
 'seem like a network error': {'type': 'phrase',
                               'partOfSpeech': 'verb phrase',
                               'pronunciation': '/siːm laɪk ə ˈnetwɜːk ˈerə/',
                               'meaning': 'to seem like a network error',
                               'description': 'Hypothesize a network cause while seeking '
                                              'confirming logs.',
                               'difficulty': 'Beginner'},
 'I think it is very likely': {'type': 'phrase',
                               'partOfSpeech': 'clause',
                               'pronunciation': '/aɪ θɪŋk ɪt ɪz ˈveri ˈlaɪkli/',
                               'meaning': 'I think it is very likely',
                               'description': 'Express strong confidence without claiming '
                                              'certainty.',
                               'difficulty': 'Beginner'},
 'It seems like the call is failing': {'type': 'phrase',
                                       'partOfSpeech': 'clause',
                                       'pronunciation': '/ɪt siːmz laɪk ðə kɔːl ɪz ˈfeɪlɪŋ/',
                                       'meaning': 'the call appears to be failing',
                                       'description': 'Suspect an inter-service call is failing '
                                                      'before a response returns.',
                                       'difficulty': 'Intermediate'},
 "assuming that's the case": {'type': 'phrase',
                              'partOfSpeech': 'clause',
                              'pronunciation': '/əˈsjuːmɪŋ ðæts ðə keɪs/',
                              'meaning': 'assuming that is true',
                              'description': 'Reason through impact or explanation based on a '
                                             'working hypothesis.',
                              'difficulty': 'Intermediate'},
 'I suspect someone is trying to': {'type': 'phrase',
                                    'partOfSpeech': 'clause',
                                    'pronunciation': '/aɪ səˈspekt ˈsʌmwʌn ɪz ˈtraɪɪŋ tuː/',
                                    'meaning': 'I suspect someone is trying to',
                                    'description': 'Flag suspicious probing or possible '
                                                   'unauthorized access attempts.',
                                    'difficulty': 'Intermediate'},
 "I don't know yet the intensity or scale": {'type': 'phrase',
                                             'partOfSpeech': 'clause',
                                             'pronunciation': '/aɪ dəʊnt nəʊ jet ði ɪnˈtensəti ɔː '
                                                              'skeɪl/',
                                             'meaning': 'scale or intensity is not yet known',
                                             'description': 'Say the event is happening but '
                                                            'overall scale is still unclear.',
                                             'difficulty': 'Intermediate'},
 'look like random probing': {'type': 'phrase',
                              'partOfSpeech': 'verb phrase',
                              'pronunciation': '/lʊk laɪk ˈrændəm ˈprəʊbɪŋ/',
                              'meaning': 'to look like random probing',
                              'description': 'Assess suspicious requests as possible scanning or '
                                             'probing.',
                              'difficulty': 'Advanced'},
 'possibly due to load testing': {'type': 'phrase',
                                  'partOfSpeech': 'clause',
                                  'pronunciation': '/ˈpɒsəbli djuː tuː ləʊd ˈtestɪŋ/',
                                  'meaning': 'possibly caused by load testing',
                                  'description': 'Suggest load testing as a possible cause of '
                                                 'spikes or alerts.',
                                  'difficulty': 'Intermediate'},
 'if I understand the situation correctly': {'type': 'phrase',
                                             'partOfSpeech': 'clause',
                                             'pronunciation': '/ɪf aɪ ˌʌndəˈstænd ðə ˌsɪtʃuˈeɪʃn '
                                                              'kəˈrektli/',
                                             'meaning': 'if my understanding is correct',
                                             'description': 'State your read of the situation and '
                                                            'invite correction.',
                                             'difficulty': 'Beginner'},
 'errors could be caused by ...': {'type': 'phrase',
                                   'partOfSpeech': 'clause',
                                   'pronunciation': '/ˈerəz kʊd biː kɔːzd baɪ/',
                                   'meaning': 'errors may be caused by something',
                                   'description': 'Offer a candidate cause for observed errors.',
                                   'difficulty': 'Intermediate'},
 'someone likely retries': {'type': 'phrase',
                            'partOfSpeech': 'clause',
                            'pronunciation': '/ˈsʌmwʌn ˈlaɪkli riːˈtraɪz/',
                            'meaning': 'users likely retry after failure',
                            'description': 'Explain request spikes as possible user retry '
                                           'behavior.',
                            'difficulty': 'Intermediate'},
 'investigate why they failed and later succeeded': {'type': 'phrase',
                                                     'partOfSpeech': 'verb phrase',
                                                     'pronunciation': '/ɪnˈvestɪɡeɪt waɪ ðeɪ feɪld '
                                                                      'ænd ˈleɪtə səkˈsiːdɪd/',
                                                     'meaning': 'to investigate failure then '
                                                                'success',
                                                     'description': 'Look into sessions that '
                                                                    'failed first and later '
                                                                    'succeeded.',
                                                     'difficulty': 'Advanced'},
 'cannot be silenced the normal way': {'type': 'phrase',
                                       'partOfSpeech': 'clause',
                                       'pronunciation': '/ˈkænɒt biː ˈsaɪlənst ðə ˈnɔːml weɪ/',
                                       'meaning': 'cannot be silenced normally',
                                       'description': 'Report alerts that need a non-standard '
                                                      'silence or workaround.',
                                       'difficulty': 'Advanced'},
 'Turn them off': {'type': 'phrase',
                   'partOfSpeech': 'verb phrase',
                   'pronunciation': '/tɜːn ðem ɒf/',
                   'meaning': 'to turn them off',
                   'description': 'Propose temporarily disabling alerts while fixing or '
                                  'investigating.',
                   'difficulty': 'Beginner'},
 'suppress alerts': {'type': 'phrase',
                     'partOfSpeech': 'verb phrase',
                     'pronunciation': '/səˈpres əˈlɜːts/',
                     'meaning': 'to suppress alerts',
                     'description': 'Configure rules to reduce alerts for a known error pattern.',
                     'difficulty': 'Intermediate'},
 'create a silence': {'type': 'phrase',
                      'partOfSpeech': 'verb phrase',
                      'pronunciation': '/kriˈeɪt ə ˈsaɪləns/',
                      'meaning': 'to create an alert silence',
                      'description': 'Set a temporary silence for a known warning during an '
                                     'incident.',
                      'difficulty': 'Intermediate'},
 'adjust the rules': {'type': 'phrase',
                      'partOfSpeech': 'verb phrase',
                      'pronunciation': '/əˈdʒʌst ðə ruːlz/',
                      'meaning': 'to adjust alert rules',
                      'description': 'Tune alert rules to cut false positives or noisy '
                                     'notifications.',
                      'difficulty': 'Beginner'},
 'roll back the change': {'type': 'phrase',
                          'partOfSpeech': 'verb phrase',
                          'pronunciation': '/rəʊl bæk ðə tʃeɪndʒ/',
                          'meaning': 'to roll back the change',
                          'description': 'Discuss whether to revert a recent change during an '
                                         'incident.',
                          'difficulty': 'Beginner'},
 'manually clear the cache': {'type': 'phrase',
                              'partOfSpeech': 'verb phrase',
                              'pronunciation': '/ˈmænjuəli klɪə ðə kæʃ/',
                              'meaning': 'to manually clear the cache',
                              'description': 'Suggest manual cache clearing as a temporary '
                                             'recovery step.',
                              'difficulty': 'Intermediate'},
 'flush and re-scale the cache': {'type': 'phrase',
                                  'partOfSpeech': 'verb phrase',
                                  'pronunciation': '/flʌʃ ænd riː skeɪl ðə kæʃ/',
                                  'meaning': 'to flush and rescale the cache',
                                  'description': 'Propose flushing cache and rescaling to restore '
                                                 'capacity.',
                                  'difficulty': 'Advanced'},
 'upgrade the node type': {'type': 'phrase',
                           'partOfSpeech': 'verb phrase',
                           'pronunciation': '/ʌpˈɡreɪd ðə nəʊd taɪp/',
                           'meaning': 'to upgrade the node type',
                           'description': 'Report upgrading instance types to restore resource '
                                          'capacity.',
                           'difficulty': 'Intermediate'},
 're-enable login': {'type': 'phrase',
                     'partOfSpeech': 'verb phrase',
                     'pronunciation': '/riː ɪˈneɪbl ˈlɒɡɪn/',
                     'meaning': 'to re-enable login',
                     'description': 'Restore login via a temporary fix while preparing a permanent '
                                    'one.',
                     'difficulty': 'Beginner'},
 'delay the problem a bit': {'type': 'phrase',
                             'partOfSpeech': 'verb phrase',
                             'pronunciation': '/dɪˈleɪ ðə ˈprɒbləm ə bɪt/',
                             'meaning': 'to delay the problem briefly',
                             'description': 'Warn a fix may restore service but only postpone the '
                                            'root issue.',
                             'difficulty': 'Intermediate'},
 'resolve them with some notes': {'type': 'phrase',
                                  'partOfSpeech': 'verb phrase',
                                  'pronunciation': '/rɪˈzɒlv ðem wɪð sʌm nəʊts/',
                                  'meaning': 'to resolve alerts with notes',
                                  'description': 'Close expected alerts with notes when monitoring '
                                                 'can continue.',
                                  'difficulty': 'Intermediate'},
 'take this on': {'type': 'phrase',
                  'partOfSpeech': 'verb phrase',
                  'pronunciation': '/teɪk ðɪs ɒn/',
                  'meaning': 'to take this on',
                  'description': 'Volunteer to handle the incident when no one else is available.',
                  'difficulty': 'Beginner'},
 'working on it': {'type': 'phrase',
                   'partOfSpeech': 'clause',
                   'pronunciation': '/ˈwɜːkɪŋ ɒn ɪt/',
                   'meaning': 'currently working on it',
                   'description': 'Tell the team you are actively handling the incident.',
                   'difficulty': 'Beginner'},
 'involve the infrastructure team': {'type': 'phrase',
                                     'partOfSpeech': 'verb phrase',
                                     'pronunciation': '/ɪnˈvɒlv ði ˌɪnfrəˈstrʌktʃə tiːm/',
                                     'meaning': 'to involve the infrastructure team',
                                     'description': 'Bring in infra when the app layer cannot '
                                                    'resolve the issue.',
                                     'difficulty': 'Intermediate'},
 'escalate it to them': {'type': 'phrase',
                         'partOfSpeech': 'verb phrase',
                         'pronunciation': '/ˈeskəleɪt ɪt tuː ðem/',
                         'meaning': 'to escalate to them',
                         'description': 'Propose handing the incident to the owning or on-call '
                                        'team.',
                         'difficulty': 'Beginner'},
 'ping the members': {'type': 'phrase',
                      'partOfSpeech': 'verb phrase',
                      'pronunciation': '/pɪŋ ðə ˈmembəz/',
                      'meaning': 'to ping the members',
                      'description': 'Ask someone to notify on-call or specific members in chat.',
                      'difficulty': 'Beginner'},
 'join our call': {'type': 'phrase',
                   'partOfSpeech': 'verb phrase',
                   'pronunciation': '/dʒɔɪn ˈaʊə kɔːl/',
                   'meaning': 'to join our incident call',
                   'description': 'Invite others to join a live incident bridge for updates.',
                   'difficulty': 'Beginner'},
 'please help': {'type': 'phrase',
                 'partOfSpeech': 'clause',
                 'pronunciation': '/pliːz help/',
                 'meaning': 'please help',
                 'description': 'Ask for help when you lack access or cannot finish alone.',
                 'difficulty': 'Beginner'},
 'lack permissions': {'type': 'phrase',
                      'partOfSpeech': 'verb phrase',
                      'pronunciation': '/læk pəˈmɪʃnz/',
                      'meaning': 'to lack permissions',
                      'description': 'Explain a blocked change due to missing permissions.',
                      'difficulty': 'Beginner'},
 'post a summary shortly': {'type': 'phrase',
                            'partOfSpeech': 'verb phrase',
                            'pronunciation': '/pəʊst ə ˈsʌməri ˈʃɔːtli/',
                            'meaning': 'to post a summary soon',
                            'description': 'Promise a written incident update after initial '
                                           'investigation.',
                            'difficulty': 'Intermediate'},
 'wait and see': {'type': 'phrase',
                  'partOfSpeech': 'verb phrase',
                  'pronunciation': '/weɪt ænd siː/',
                  'meaning': 'to wait and see',
                  'description': 'Hold off on action and watch whether the issue recurs.',
                  'difficulty': 'Beginner'},
 'the suppression worked': {'type': 'phrase',
                            'partOfSpeech': 'clause',
                            'pronunciation': '/ðə səˈpreʃn wɜːkt/',
                            'meaning': 'the suppression worked',
                            'description': 'Report that alert suppression stopped notifications as '
                                           'expected.',
                            'difficulty': 'Intermediate'},
 'should be silenced by now': {'type': 'phrase',
                               'partOfSpeech': 'clause',
                               'pronunciation': '/ʃʊd biː ˈsaɪlənst baɪ naʊ/',
                               'meaning': 'should be silenced by now',
                               'description': 'Expect known alerts to be silenced after config '
                                              'propagation time.',
                               'difficulty': 'Intermediate'},
 'It looks like there are no more errors': {'type': 'phrase',
                                            'partOfSpeech': 'clause',
                                            'pronunciation': '/ɪt lʊks laɪk ðeər ɑː nəʊ mɔː ˈerəz/',
                                            'meaning': 'there seem to be no more errors',
                                            'description': 'Signal recovery while continuing to '
                                                           'monitor for recurrence.',
                                            'difficulty': 'Beginner'},
 "haven't seen any additional errors for ...": {'type': 'phrase',
                                                'partOfSpeech': 'clause',
                                                'pronunciation': '/ˈhævnt siːn ˈeni əˈdɪʃənl ˈerəz '
                                                                 'fɔː/',
                                                'meaning': 'no new errors for a period',
                                                'description': 'Give a clean-error window as '
                                                               'evidence toward recovery.',
                                                'difficulty': 'Intermediate'},
 'keep an eye on ...': {'type': 'phrase',
                        'partOfSpeech': 'verb phrase',
                        'pronunciation': '/kiːp ən aɪ ɒn/',
                        'meaning': 'to keep watching closely',
                        'description': 'Commit to continued monitoring of alerts or metrics.',
                        'difficulty': 'Beginner'},
 'keep a watch for future issues': {'type': 'phrase',
                                    'partOfSpeech': 'verb phrase',
                                    'pronunciation': '/kiːp ə wɒtʃ fɔː ˈfjuːtʃə ˈɪʃuːz/',
                                    'meaning': 'to watch for future issues',
                                    'description': 'Close current alerts while staying alert for '
                                                   'recurrence.',
                                    'difficulty': 'Intermediate'},
 'continue to monitor for some more time': {'type': 'phrase',
                                            'partOfSpeech': 'verb phrase',
                                            'pronunciation': '/kənˈtɪnjuː tuː ˈmɒnɪtə fɔː sʌm mɔː '
                                                             'taɪm/',
                                            'meaning': 'to keep monitoring longer',
                                            'description': 'Stay vigilant even when the system '
                                                           'looks stable again.',
                                            'difficulty': 'Intermediate'},
 'things look good now': {'type': 'phrase',
                          'partOfSpeech': 'clause',
                          'pronunciation': '/θɪŋz lʊk ɡʊd naʊ/',
                          'meaning': 'things look good now',
                          'description': 'Report that the situation has normalized after recovery.',
                          'difficulty': 'Beginner'},
 'the service has restarted': {'type': 'phrase',
                               'partOfSpeech': 'clause',
                               'pronunciation': '/ðə ˈsɜːvɪs hæz riːˈstɑːtɪd/',
                               'meaning': 'the service has restarted',
                               'description': 'Announce a service restart and that it accepts '
                                              'requests again.',
                               'difficulty': 'Beginner'},
 'all services recovered': {'type': 'phrase',
                            'partOfSpeech': 'clause',
                            'pronunciation': '/ɔːl ˈsɜːvɪsɪz rɪˈkʌvəd/',
                            'meaning': 'all services have recovered',
                            'description': 'Report full service recovery and the approximate time.',
                            'difficulty': 'Beginner'},
 'become available': {'type': 'phrase',
                      'partOfSpeech': 'verb phrase',
                      'pronunciation': '/bɪˈkʌm əˈveɪləbl/',
                      'meaning': 'to become available again',
                      'description': 'Report partial recovery as a component becomes available '
                                     'again.',
                      'difficulty': 'Beginner'},
 'error requests are dropping': {'type': 'phrase',
                                 'partOfSpeech': 'clause',
                                 'pronunciation': '/ˈerə rɪˈkwests ɑː ˈdrɒpɪŋ/',
                                 'meaning': 'error requests are decreasing',
                                 'description': 'Describe improving metrics as errors fall and '
                                                'successes rise.',
                                 'difficulty': 'Intermediate'},
 'usage dropped but is steadily increasing': {'type': 'phrase',
                                              'partOfSpeech': 'clause',
                                              'pronunciation': '/ˈjuːsɪdʒ drɒpt bət ɪz ˈstedɪli '
                                                               'ɪŋˈkriːsɪŋ/',
                                              'meaning': 'usage fell then rose steadily',
                                              'description': 'Note usage dipped then climbed again '
                                                             'after a release or fix.',
                                              'difficulty': 'Intermediate'},
 'full recovery': {'type': 'phrase',
                   'partOfSpeech': 'noun phrase',
                   'pronunciation': '/fʊl rɪˈkʌvəri/',
                   'meaning': 'complete recovery',
                   'description': 'Report total recovery and time from detection to full '
                                  'restoration.',
                   'difficulty': 'Beginner'},
 'mark it as resolved for now': {'type': 'phrase',
                                 'partOfSpeech': 'verb phrase',
                                 'pronunciation': '/mɑːk ɪt æz rɪˈzɒlvd fɔː naʊ/',
                                 'meaning': 'to mark it resolved for now',
                                 'description': 'Set incident status to resolved while still '
                                                'watching closely.',
                                 'difficulty': 'Intermediate'},
 'once the root cause is identified': {'type': 'phrase',
                                       'partOfSpeech': 'clause',
                                       'pronunciation': '/wʌns ðə ruːt kɔːz ɪz aɪˈdentɪfaɪd/',
                                       'meaning': 'after the root cause is found',
                                       'description': 'Promise follow-up actions such as '
                                                      'monitoring changes after RCA.',
                                       'difficulty': 'Intermediate'},
 'due to the maintenance': {'type': 'phrase',
                            'partOfSpeech': 'prepositional phrase',
                            'pronunciation': '/djuː tuː ðə ˈmeɪntənəns/',
                            'meaning': 'because of maintenance',
                            'description': 'Explain an issue as caused by planned or recent '
                                           'maintenance.',
                            'difficulty': 'Beginner'},
 'be caused by ...': {'type': 'phrase',
                      'partOfSpeech': 'verb phrase',
                      'pronunciation': '/biː kɔːzd baɪ/',
                      'meaning': 'to be caused by something',
                      'description': 'Hypothesize or analyze what likely caused the incident.',
                      'difficulty': 'Beginner'},
 'root cause analysis': {'type': 'phrase',
                         'partOfSpeech': 'noun phrase',
                         'pronunciation': '/ruːt kɔːz əˈnæləsɪs/',
                         'meaning': 'analysis of the root cause',
                         'description': 'Ask to capture findings in a post-incident root cause '
                                        'analysis.',
                         'difficulty': 'Intermediate'},
 'take a closer look at ...': {'type': 'phrase',
                               'partOfSpeech': 'verb phrase',
                               'pronunciation': '/teɪk ə ˈkləʊsə lʊk æt/',
                               'meaning': 'to examine more closely',
                               'description': 'Call for deeper review when routine checks are not '
                                              'enough.',
                               'difficulty': 'Beginner'},
 'next actions': {'type': 'phrase',
                  'partOfSpeech': 'noun phrase',
                  'pronunciation': '/nekst ˈækʃnz/',
                  'meaning': 'follow-up actions',
                  'description': 'List post-recovery tasks such as impact review and monitoring.',
                  'difficulty': 'Beginner'},
 'review in depth': {'type': 'phrase',
                     'partOfSpeech': 'verb phrase',
                     'pronunciation': '/rɪˈvjuː ɪn depθ/',
                     'meaning': 'to review in depth',
                     'description': 'Ask for deep review of assumptions or design, not surface '
                                    'checks.',
                     'difficulty': 'Intermediate'},
 'define the response procedure and decision criteria': {'type': 'phrase',
                                                         'partOfSpeech': 'verb phrase',
                                                         'pronunciation': '/dɪˈfaɪn ðə rɪˈspɒns '
                                                                          'prəˈsiːdʒə ænd dɪˈsɪʒn '
                                                                          'kraɪˈtɪəriə/',
                                                         'meaning': 'to define response steps and '
                                                                    'criteria',
                                                         'description': 'Document incident '
                                                                        'response steps and '
                                                                        'rollback or recovery '
                                                                        'criteria.',
                                                         'difficulty': 'Advanced'},
 'recover more quickly if a similar issue occurs again': {'type': 'phrase',
                                                          'partOfSpeech': 'clause',
                                                          'pronunciation': '/rɪˈkʌvə mɔː ˈkwɪkli '
                                                                           'ɪf ə ˈsɪmɪlə ˈɪʃuː '
                                                                           'əˈkɜːz əˈɡen/',
                                                          'meaning': 'to recover faster on '
                                                                     'recurrence',
                                                          'description': 'Say improvements should '
                                                                         'shorten recovery if a '
                                                                         'similar issue returns.',
                                                          'difficulty': 'Advanced'}}

USAGE_EXAMPLE_JA: dict[str, str] = {'notice the status had changed': 'インシデントのステータスがResolvedに変わったことに気づいた。',
 'An alert occurred in this thread as well': 'このスレッドでもアラートが発生した。',
 'The alert keeps getting triggered': '数分おきにアラートが繰り返し発生している。',
 'alerts suddenly started firing frequently': '正午過ぎからアラートが突然頻発し始めた。',
 'Is the alert still active?': 'アラートはまだ有効か、それとも自動解決したか？',
 'CPU usage briefly spiked again': 'CPU使用率が再び一時的に急上昇したが、現在は低下している。',
 'seeing lots of ... in the logs': 'ログにタイムアウトエラーが大量に出ている。',
 'usage is gradually increasing': 'メモリ使用量は徐々に増加しているが、ヒット率は安定している。',
 'successful requests have dropped to zero': '過去5分間で成功リクエストがゼロまで減少した。',
 'The error started again': '初期化エラーが18:00頃から再び発生し始めた。',
 'Be quickly auto-resolved': 'アラートは短時間で自動解決したため、一時的なスパイクの可能性がある。',
 'Might be worth checking what happened': 'スパイク発生時に何が起きたか確認する価値がありそうだ。',
 'check if there is any impact': '本番トラフィックへの影響があるか確認する。',
 'should not affect ... but let me verify': '本番への影響はないはずだが、確認する。',
 'should not impact the user experience': 'ユーザー体験への影響はない見込みだが、確認中である。',
 'users cannot log in to production': '現在、ユーザーは本番環境にログインできない。',
 'might have been affected during the downtime': '停止時間中に一部ユーザーが影響を受けた可能性がある。',
 'at maximum, ... users were impacted': '最大で500人のユーザーが影響を受けた可能性がある。',
 'evaluate the number of impacted users': '影響を受けたユーザー数を評価する必要がある。',
 'have a significant impact on business KPIs': 'インシデントはビジネスKPIに重大な影響を与えた可能性がある。',
 'clarify which features were unavailable': 'インシデント中に利用不能だった機能を明確にすべきだ。',
 'Identify the impact scope at the user or session level': 'ユーザーまたはセッション単位で影響範囲を特定できるか？',
 'limit the impact scope to the target features': '影響範囲を対象機能に限定する必要がある。',
 'as long as production is healthy': '本番が正常であれば、営業時間内に調査を継続できる。',
 'be safe on the product side': 'プロダクト側は問題なさそうだが、フロントエンドは調査が必要だ。',
 'seem to be the same issue': '昨日見た問題と同じ事象のようだ。',
 'look slightly different': 'このエラーは前回のものと少し異なって見える。',
 "doesn't seem to be an app issue": '下流ログから、アプリの問題ではなさそうだ。',
 'the error originates from ...': 'エラーはルーティング層から発生しているようだ。',
 'come from canary': '失敗リクエストは本番ではなくカナリア由来のようだ。',
 'cannot see errors from production': '本番環境から対応するサーバーエラーは確認できない。',
 'find the source': 'アラートルールを変更する前に発生元を特定する必要がある。',
 'the URL path seems consistent': '最近のイベント間でURLパスに一貫性があるようだ。',
 'confirm whether ... is performing testing': 'まず、他チームがテストを実行中か確認しよう。',
 'match the incident timeline': 'エラーのタイムスタンプはインシデントの時間帯と一致する。',
 'link the events together': 'トラフィック低下により2つの事象を関連付けられた。',
 'confirm that the root cause is the same': '最近のエラーすべてで根本原因が同じか確認すべきだ。',
 'have no spike and no obvious increase': '上流サービスにスパイクや明確なエラー増加はない。',
 "can't seem to find any relevant logs": 'このリクエストに該当するログが見つからない。',
 'need more details to investigate further': 'さらなる調査には詳細情報が必要だ。',
 'appear to be a consequence of ...': 'これは上流タイムアウトの結果として現れているようだ。',
 'seem like a network error': 'ネットワークエラーのように見えるが、クライアントログで確認が必要だ。',
 'I think it is very likely': 'クライアント側の問題である可能性が非常に高いと思う。',
 'It seems like the call is failing': 'レスポンス返却前に上流呼び出しが失敗しているようだ。',
 "assuming that's the case": 'それが事実だと仮定すると、重複リクエストがスパイクを説明できる。',
 'I suspect someone is trying to': '誰かが未サポートのエンドポイントを探索している疑いがある。',
 "I don't know yet the intensity or scale": 'トラフィックの規模や強度はまだわからない。',
 'look like random probing': 'リクエストはランダムな探索のようだが、発信元を確認中だ。',
 'possibly due to load testing': 'スパイクは負荷テストが原因の可能性がある。',
 'if I understand the situation correctly': '理解が正しければ、これはキャッシュ層に限定されている。',
 'errors could be caused by ...': 'エラーは古いクライアント側データが原因の可能性がある。',
 'someone likely retries': '最初のリクエスト失敗後、ユーザーが再試行している可能性が高い。',
 'investigate why they failed and later succeeded': '同じセッションが失敗後に成功した理由を調査すべきだ。',
 'cannot be silenced the normal way': 'これらのアラートは通常の方法では停止できない。',
 'Turn them off': '一時的にこれらのアラートを停止する追加ルールが必要かもしれない。',
 'suppress alerts': 'このルールは既知のエラーパターンのアラートを抑制する。',
 'create a silence': '既知の警告に対して明日までサイレンスを作成した。',
 'adjust the rules': 'アラートが再発したら、ルールを調整できる。',
 'roll back the change': '変更をロールバックするか判断する必要がある。',
 'manually clear the cache': 'ログインを一時復旧するため、キャッシュを手動消去すべきか？',
 'flush and re-scale the cache': 'キャッシュインスタンスのフラッシュと再スケールが必要かもしれない。',
 'upgrade the node type': '容量を回復するため、ノードタイプをアップグレード中だ。',
 're-enable login': '恒久対応の準備中、暫定クリーンアップでログインが再有効化される可能性がある。',
 'delay the problem a bit': 'サービスは回復するかもしれないが、問題を少し先送りするだけだ。',
 'resolve them with some notes': '想定内のエラーなら、メモを添えて解決済みにしよう。',
 'take this on': '誰も対応できなければ、私が引き受けられる。',
 'working on it': '対応中で、設定変更を準備している。',
 'involve the infrastructure team': 'インフラチームを巻き込む必要がある。',
 'escalate it to them': '所有チームへエスカレーションすべきか？',
 'ping the members': 'このサービスの当番メンバーに連絡してもらえるか？',
 'join our call': '更新共有や質問があれば、通話に参加してほしい。',
 'please help': '設定へのアクセスがないので、支援をお願いしたい。',
 'lack permissions': '変更を適用しようとしたが、必要な権限がない。',
 'post a summary shortly': '初期調査を完了した。まもなく概要を共有する。',
 'wait and see': '最後のアラートは10分前なので、しばらく様子を見る。',
 'the suppression worked': '抑止設定が機能したようだ。',
 'should be silenced by now': '既知のアラートは今頃停止されているはずだ。',
 'It looks like there are no more errors': '追加のエラーはなさそうだが、監視を継続する。',
 "haven't seen any additional errors for ...": '15分間、追加のエラーは確認されていない。',
 'keep an eye on ...': '夜間もアラートチャンネルを引き続き監視する。',
 'keep a watch for future issues': '現在のアラートを解決し、今後の問題にも注視する。',
 'continue to monitor for some more time': '安定しているが、もうしばらく監視を続ける。',
 'things look good now': '全サービスが復旧し、現状は問題なさそうだ。',
 'the service has restarted': 'サービスが再起動し、再びリクエストを受け付けている。',
 'all services recovered': '全サービスが14:20頃に復旧した。',
 'become available': 'キャッシュ層が再び利用可能になりつつある。',
 'error requests are dropping': 'エラーリクエストは減少し、成功リクエストは増加している。',
 'usage dropped but is steadily increasing': 'リリース後使用量は一度下がったが、再び徐々に増えている。',
 'full recovery': '検知から完全復旧まで約1時間かかった。',
 'mark it as resolved for now': '新規エラーがないため、一旦解決済みとする。',
 'once the root cause is identified': '根本原因が特定されたら、監視ルールを調整できる。',
 'due to the maintenance': 'メンテナンスにより、一部インスタンスが古い接続を保持した。',
 'be caused by ...': '再起動後のランタイム最適化が原因の可能性がある。',
 'root cause analysis': 'この調査結果を根本原因分析に含めてほしい。',
 'take a closer look at ...': '影響を受けたセッションをさらに詳しく調べる必要がある。',
 'next actions': '次の対応：影響の定量化、監視改善、タイムライン文書化。',
 'review in depth': '容量の前提条件を深くレビューすべきだ。',
 'define the response procedure and decision criteria': '次のインシデント前に対応手順と判断基準を定義すべきだ。',
 'recover more quickly if a similar issue occurs again': '同様の問題再発時、より迅速に復旧できるはずだ。'}

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
