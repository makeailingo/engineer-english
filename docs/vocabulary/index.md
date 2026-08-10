---
layout: default
title: Vocabulary
---

# Vocabulary

{% assign entries = site.pages
  | where_exp: "item", "item.layout == 'vocabulary'"
  | sort: "id" %}

| ID | Term | Difficulty | Scene | 意味 | Usage Example | Usage Example (Ja) |
| --- | --- | --- | --- | --- | --- | --- |
{% for item in entries %}| {{ item.id }} | [{{ item.term }}]({{ item.url | relative_url }}) | {{ item.difficulty }} | {{ item.scene }} | {{ item.meaningJa }} | {{ item.usageExample }} | {{ item.usageExampleJa }} |
{% endfor %}
