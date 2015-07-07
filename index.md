---
title: "Legile Internetului"
---
<ul>
  {% for page in site.pages %}
    <li>
      <a href="{{ site.base_url }}{{ page.url }}">{{ page.title }}</a>
    </li>
  {% endfor %}
</ul>
