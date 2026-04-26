#!/usr/bin/env python3
"""
CheckTheWorld — генератор страниц стран
Использование: python3 generate_country.py <slug>
Пример: python3 generate_country.py georgia

Скрипт берёт thailand.html как шаблон и заменяет страно-специфичные данные.
Все данные стран хранятся в словаре COUNTRIES ниже.
"""

import re, sys, json, os

# ─────────────────────────────────────────────────────────────
# ДАННЫЕ СТРАН
# ─────────────────────────────────────────────────────────────
COUNTRIES = {
  'georgia': {
    'slug': 'georgia',
    'name_ru': 'Грузия',
    'name_en': 'Georgia',
    'title_styled': 'Гру<em>зия</em>',        # HTML с курсивом
    'flag': '🇬🇪',
    'region': 'Южный Кавказ',
    'gmt': 'GMT+4',
    'currency': 'Лари · GEL',
    'population': '3.7 млн чел.',
    'visa_badge': 'Без визы · 365 дней',
    'visa_badge_color': 'green',               # green | amber | red
    'stat_budget': '~1 800 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~35K ₽',
    'stat_rent_sub': '1 комн.',
    'stat_climate': '+22°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '80',
    'stat_internet_sub': 'Мбит · 4G',
    'qc_flight': 'от 15 000 ₽',
    'qc_hostel': '600–1 200 ₽',
    'qc_hotel': '2 000–4 500 ₽',
    'qc_rent': '20–45К ₽',
    'qc_food': '150–400 ₽',
    'qc_taxi': '60–300 ₽',
    'aviasales_dest': 'TBS',
    'yesim_sub': 'georgia',
    'currency_rate': 'курс: 1 ₽ ≈ 0.04 GEL · апр 2026',
    'local_currency_symbol': '₾',
    'local_currency_name': 'GEL',
    'breadcrumb_region': 'Южный Кавказ',
    'overline': 'Южный Кавказ · Досье',
    'country_num': '#1',
    'prev_country': None,
    'next_country': {'slug': 'turkey', 'flag': '🇹🇷', 'name': 'Турция'},
    'currency_pairs': {
      'rub': {'rate': 24, 'symbol': '₾'},
      'usd': {'rate': 0.37, 'symbol': '$'},
      'eur': {'rate': 0.34, 'symbol': '€'},
    },
    # Pexels запросы для городов
    'city_queries': {
      'tbilisi':  'Tbilisi Georgia old town',
      'batumi':   'Batumi Georgia sea boulevard',
      'kutaisi':  'Kutaisi Georgia monastery',
      'kazbegi':  'Kazbegi Georgia mountains Gergeti',
    },
    'hero_query': 'Tbilisi Georgia aerial cityscape',
  },

  'serbia': {
    'slug': 'serbia',
    'name_ru': 'Сербия',
    'name_en': 'Serbia',
    'title_styled': 'Сер<em>бия</em>',
    'flag': '🇷🇸',
    'region': 'Балканы',
    'gmt': 'GMT+1',
    'currency': 'Динар · RSD',
    'population': '6.9 млн чел.',
    'visa_badge': 'Без визы · 30 дней',
    'visa_badge_color': 'amber',
    'stat_budget': '~2 000 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~30K ₽',
    'stat_rent_sub': '1 комн.',
    'stat_climate': '+13°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '100',
    'stat_internet_sub': 'Мбит · 4G/5G',
    'qc_flight': 'от 18 000 ₽',
    'qc_hostel': '700–1 400 ₽',
    'qc_hotel': '2 200–4 800 ₽',
    'qc_rent': '22–50К ₽',
    'qc_food': '160–450 ₽',
    'qc_taxi': '80–350 ₽',
    'aviasales_dest': 'BEG',
    'yesim_sub': 'serbia',
    'currency_rate': 'курс: 1 ₽ ≈ 1.2 RSD · апр 2026',
    'local_currency_symbol': 'дин',
    'local_currency_name': 'RSD',
    'breadcrumb_region': 'Балканы',
    'overline': 'Балканы · Досье',
    'country_num': '#2',
    'prev_country': {'slug': 'georgia', 'flag': '🇬🇪', 'name': 'Грузия'},
    'next_country': {'slug': 'turkey', 'flag': '🇹🇷', 'name': 'Турция'},
    'hero_query': 'Belgrade Serbia city skyline night',
  },

  'turkey': {
    'slug': 'turkey',
    'name_ru': 'Турция',
    'name_en': 'Turkey',
    'title_styled': 'Тур<em>ция</em>',
    'flag': '🇹🇷',
    'region': 'Ближний Восток / Европа',
    'gmt': 'GMT+3',
    'currency': 'Лира · TRY',
    'population': '85 млн чел.',
    'visa_badge': 'Без визы · 60 дней',
    'visa_badge_color': 'green',
    'stat_budget': '~2 400 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~38K ₽',
    'stat_rent_sub': '1 комн.',
    'stat_climate': '+18°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '70',
    'stat_internet_sub': 'Мбит · 4G',
    'qc_flight': 'от 12 000 ₽',
    'qc_hostel': '500–1 200 ₽',
    'qc_hotel': '1 800–4 500 ₽',
    'qc_rent': '25–55К ₽',
    'qc_food': '120–380 ₽',
    'qc_taxi': '70–320 ₽',
    'aviasales_dest': 'IST',
    'yesim_sub': 'turkey',
    'currency_rate': 'курс: 1 ₽ ≈ 2.8 TRY · апр 2026',
    'local_currency_symbol': '₺',
    'local_currency_name': 'TRY',
    'breadcrumb_region': 'Ближний Восток',
    'overline': 'Ближний Восток · Досье',
    'country_num': '#3',
    'prev_country': {'slug': 'serbia', 'flag': '🇷🇸', 'name': 'Сербия'},
    'next_country': {'slug': 'armenia', 'flag': '🇦🇲', 'name': 'Армения'},
    'hero_query': 'Istanbul Turkey Bosphorus sunset',
  },

  'armenia': {
    'slug': 'armenia',
    'name_ru': 'Армения',
    'name_en': 'Armenia',
    'title_styled': 'Арме<em>ния</em>',
    'flag': '🇦🇲',
    'region': 'Южный Кавказ',
    'gmt': 'GMT+4',
    'currency': 'Драм · AMD',
    'population': '3 млн чел.',
    'visa_badge': 'Без визы · 180 дней',
    'visa_badge_color': 'green',
    'stat_budget': '~1 600 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~25K ₽',
    'stat_rent_sub': '1 комн.',
    'stat_climate': '+13°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '100',
    'stat_internet_sub': 'Мбит · 4G',
    'qc_flight': 'от 14 000 ₽',
    'qc_hostel': '500–1 000 ₽',
    'qc_hotel': '1 800–4 000 ₽',
    'qc_rent': '18–40К ₽',
    'qc_food': '120–350 ₽',
    'qc_taxi': '50–200 ₽',
    'aviasales_dest': 'EVN',
    'yesim_sub': 'armenia',
    'currency_rate': 'курс: 1 ₽ ≈ 43 AMD · апр 2026',
    'local_currency_symbol': '֏',
    'local_currency_name': 'AMD',
    'breadcrumb_region': 'Южный Кавказ',
    'overline': 'Южный Кавказ · Досье',
    'country_num': '#4',
    'prev_country': {'slug': 'turkey', 'flag': '🇹🇷', 'name': 'Турция'},
    'next_country': {'slug': 'vietnam', 'flag': '🇻🇳', 'name': 'Вьетнам'},
    'hero_query': 'Yerevan Armenia Ararat mountain',
  },

  'vietnam': {
    'slug': 'vietnam',
    'name_ru': 'Вьетнам',
    'name_en': 'Vietnam',
    'title_styled': 'Вьет<em>нам</em>',
    'flag': '🇻🇳',
    'region': 'Юго-Восточная Азия',
    'gmt': 'GMT+7',
    'currency': 'Донг · VND',
    'population': '98 млн чел.',
    'visa_badge': 'Без визы · 45 дней',
    'visa_badge_color': 'green',
    'stat_budget': '~1 900 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~28K ₽',
    'stat_rent_sub': '1 комн.',
    'stat_climate': '+28°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '60',
    'stat_internet_sub': 'Мбит · 4G',
    'qc_flight': 'от 28 000 ₽',
    'qc_hostel': '400–900 ₽',
    'qc_hotel': '1 500–4 000 ₽',
    'qc_rent': '15–35К ₽',
    'qc_food': '90–300 ₽',
    'qc_taxi': '50–200 ₽',
    'aviasales_dest': 'HAN',
    'yesim_sub': 'vietnam',
    'currency_rate': 'курс: 1 ₽ ≈ 230 VND · апр 2026',
    'local_currency_symbol': '₫',
    'local_currency_name': 'VND',
    'breadcrumb_region': 'Юго-Восточная Азия',
    'overline': 'Юго-Восточная Азия · Досье',
    'country_num': '#5',
    'prev_country': {'slug': 'armenia', 'flag': '🇦🇲', 'name': 'Армения'},
    'next_country': {'slug': 'china', 'flag': '🇨🇳', 'name': 'Китай'},
    'hero_query': 'Hanoi Vietnam old quarter street',
  },

  'georgia': dict(  # уже определена выше, перезаписываем
    slug='georgia',
    name_ru='Грузия',
    name_en='Georgia',
    title_styled='Гру<em>зия</em>',
    flag='🇬🇪',
    region='Южный Кавказ',
    gmt='GMT+4',
    currency='Лари · GEL',
    population='3.7 млн чел.',
    visa_badge='Без визы · 365 дней',
    visa_badge_color='green',
    stat_budget='~1 800 ₽',
    stat_budget_sub='комфорт',
    stat_rent='~35K ₽',
    stat_rent_sub='1 комн.',
    stat_climate='+22°',
    stat_climate_sub='средний год',
    stat_internet='80',
    stat_internet_sub='Мбит · 4G',
    qc_flight='от 15 000 ₽',
    qc_hostel='600–1 200 ₽',
    qc_hotel='2 000–4 500 ₽',
    qc_rent='20–45К ₽',
    qc_food='150–400 ₽',
    qc_taxi='60–300 ₽',
    aviasales_dest='TBS',
    yesim_sub='georgia',
    currency_rate='курс: 1 ₽ ≈ 0.04 GEL · апр 2026',
    local_currency_symbol='₾',
    local_currency_name='GEL',
    breadcrumb_region='Южный Кавказ',
    overline='Южный Кавказ · Досье',
    country_num='#1',
    prev_country=None,
    next_country={'slug': 'turkey', 'flag': '🇹🇷', 'name': 'Турция'},
    hero_query='Tbilisi Georgia aerial cityscape',
  ),
}

# ─────────────────────────────────────────────────────────────
# ФУНКЦИЯ ГЕНЕРАЦИИ
# ─────────────────────────────────────────────────────────────
def generate(slug, template_path='/mnt/user-data/outputs/thailand.html', out_dir='/mnt/user-data/outputs'):
    c = COUNTRIES.get(slug)
    if not c:
        print(f"❌ Страна '{slug}' не найдена в словаре COUNTRIES")
        return

    with open(template_path) as f:
        html = f.read()

    print(f"Генерирую {c['name_ru']} ({slug})...")

    # ── 1. Заголовок и мета ──────────────────────────────────
    html = html.replace(
        '<title>Тайланд — визы, цены, жильё | CheckTheWorld</title>',
        f'<title>{c["name_ru"]} — визы, цены, жильё | CheckTheWorld</title>'
    )
    html = html.replace(
        'content="Всё о Тайланде — визовый режим, стоимость жизни, цены на жильё, авиабилеты.',
        f'content="Всё о {c["name_ru"]} — визовый режим, стоимость жизни, цены на жильё, авиабилеты.'
    )

    # ── 2. Breadcrumb и overline ─────────────────────────────
    html = html.replace(
        '<span>Юго-Восточная Азия</span>\n    <span class="breadcrumb-sep">/</span>\n    <span>Тайланд</span>',
        f'<span>{c["breadcrumb_region"]}</span>\n    <span class="breadcrumb-sep">/</span>\n    <span>{c["name_ru"]}</span>'
    )
    html = html.replace(
        '<div class="hero-overline">Юго-Восточная Азия · Досье</div>',
        f'<div class="hero-overline">{c["overline"]}</div>'
    )

    # ── 3. Заголовок страны ──────────────────────────────────
    html = html.replace(
        '<h1 class="country-title">Тай<em>ланд</em></h1>',
        f'<h1 class="country-title">{c["title_styled"]}</h1>'
    )

    # ── 4. Мета-чипы ─────────────────────────────────────────
    html = re.sub(
        r'<span class="hero-chip"><span class="dot"></span>Тайское Королевство</span>',
        f'<span class="hero-chip"><span class="dot"></span>{c["name_ru"]}</span>', html
    )
    html = re.sub(r'GMT\+7', c['gmt'], html, count=3)
    html = re.sub(
        r'<span class="hero-chip"><span class="dot"></span>Бат · THB</span>',
        f'<span class="hero-chip"><span class="dot"></span>{c["currency"]}</span>', html
    )
    html = re.sub(
        r'<span class="hero-chip"><span class="dot"></span>70 млн чел\.</span>',
        f'<span class="hero-chip"><span class="dot"></span>{c["population"]}</span>', html
    )

    # ── 5. Визовый бейдж ─────────────────────────────────────
    html = html.replace(
        '<div class="visa-badge"><div class="visa-badge-dot"></div>Без визы · 60 дней</div>',
        f'<div class="visa-badge"><div class="visa-badge-dot"></div>{c["visa_badge"]}</div>'
    )

    # ── 6. Статы hero ────────────────────────────────────────
    html = html.replace('<div class="stat-val">~3 200 ₽</div>\n          <div class="stat-sub">комфорт</div>',
                        f'<div class="stat-val">{c["stat_budget"]}</div>\n          <div class="stat-sub">{c["stat_budget_sub"]}</div>')
    html = html.replace('<div class="stat-val">~41K ₽</div>\n          <div class="stat-sub">1 комн.</div>',
                        f'<div class="stat-val">{c["stat_rent"]}</div>\n          <div class="stat-sub">{c["stat_rent_sub"]}</div>')
    html = html.replace('<div class="stat-val">+32°</div>\n          <div class="stat-sub">средний год</div>',
                        f'<div class="stat-val">{c["stat_climate"]}</div>\n          <div class="stat-sub">{c["stat_climate_sub"]}</div>')
    html = html.replace('<div class="stat-val">50</div>\n          <div class="stat-sub">Мбит · 4G/5G</div>',
                        f'<div class="stat-val">{c["stat_internet"]}</div>\n          <div class="stat-sub">{c["stat_internet_sub"]}</div>')

    # ── 7. Quick card ─────────────────────────────────────────
    qc_replacements = [
        ('от 34 500 ₽', c['qc_flight']),
        ('730–1 400 ₽', c['qc_hostel']),
        ('2 700–5 500 ₽', c['qc_hotel']),
        ('27–55К ₽', c['qc_rent']),
        ('180–450 ₽', c['qc_food']),
        ('90–450 ₽', c['qc_taxi']),
    ]
    for old, new in qc_replacements:
        html = html.replace(old, new, 1)

    # ── 8. Aviasales destination ─────────────────────────────
    html = html.replace('destination=BKK', f'destination={c["aviasales_dest"]}')

    # ── 9. Yesim sub_id ──────────────────────────────────────
    html = html.replace('sub_id=thailand', f'sub_id={c["yesim_sub"]}')

    # ── 10. Курс валюты ──────────────────────────────────────
    html = html.replace(
        'курс: 1 ฿ = 2.43 ₽ · апр 2026',
        c['currency_rate']
    )

    # ── 11. Кнопки переключателя валют ───────────────────────
    html = html.replace(
        'onclick="setCurrency(\'local\',this)">฿ THB',
        f'onclick="setCurrency(\'local\',this)">{c["local_currency_symbol"]} {c["local_currency_name"]}'
    )

    # ── 12. Pexels запрос для hero ───────────────────────────
    hero_query = c.get('hero_query', f'{c["name_en"]} city landscape')
    # Меняем первый data-query (hero bg img)
    import re as _re
    html = _re.sub(
        r'(hero-bg img[^>]*data-query=")[^"]+"',
        f'\\g<1>{hero_query}"',
        html, count=1
    )

    # ── 13. WORKER — обновляем city queries ──────────────────
    # Меняем запросы в CITY_QUERIES JS объекте
    old_queries = re.search(r'const CITY_QUERIES = \{.*?\};', html, re.DOTALL)
    if old_queries and 'city_queries' in c:
        new_q = 'const CITY_QUERIES = {\n' + ',\n'.join(
            f"  {k}: '{v}'" for k,v in c['city_queries'].items()
        ) + '\n};'
        html = html.replace(old_queries.group(0), new_q)

    # ── 14. Навигация между странами ────────────────────────
    prev = c.get('prev_country')
    nxt = c.get('next_country')

    if prev:
        prev_html = f'''<a class="cnav-card" href="{prev['slug']}.html">
      <span class="cnav-flag">{prev['flag']}</span>
      <div><div class="cnav-label">Предыдущая</div><div class="cnav-name">{prev['name']}</div></div>
      <span class="cnav-arrow">←</span>
    </a>'''
    else:
        prev_html = '<div></div>'

    if nxt:
        nxt_html = f'''<a class="cnav-card" href="{nxt['slug']}.html">
      <span class="cnav-flag">{nxt['flag']}</span>
      <div><div class="cnav-label">Следующая страна</div><div class="cnav-name">{nxt['name']}</div></div>
      <span class="cnav-arrow">→</span>
    </a>'''
    else:
        nxt_html = '<div></div>'

    old_nav = re.search(r'<div class="country-nav reveal">.*?</div>\s*\n\s*</div><!-- /main-wrap -->', html, re.DOTALL)
    if old_nav:
        new_nav = f'<div class="country-nav reveal">\n    {prev_html}\n    {nxt_html}\n  </div>'
        html = html[:old_nav.start()] + new_nav + '\n\n</div><!-- /main-wrap -->' + html[old_nav.end():]

    # ── 15. VISAS и CITIES — очищаем (нужно заполнить вручную) ─
    # Оставляем как заглушку — данные специфичны для каждой страны
    placeholder_comment = f"""
  // ⚠️ VISAS и CITIES для {c['name_ru']} — заполнить вручную!
  // Скопировать структуру из thailand.html и адаптировать
  """
    html = re.sub(
        r'(// ── DATA ──\n)(const VISAS.*?)(const CITIES.*?)(// ── CURRENCY)',
        r'\1' + placeholder_comment + r'\4',
        html, flags=re.DOTALL
    )

    # ── Сохраняем ────────────────────────────────────────────
    out_path = os.path.join(out_dir, f'{slug}.html')
    with open(out_path, 'w') as f:
        f.write(html)
    print(f"✅ Сохранён: {out_path} ({len(html)} bytes)")
    print(f"⚠️  Нужно вручную заполнить: VISAS, CITIES, секции контента (визовый режим, цены, бюджет, советы и т.д.)")
    return out_path


# ─────────────────────────────────────────────────────────────
# ДОПОЛНИТЕЛЬНЫЕ СТРАНЫ
# ─────────────────────────────────────────────────────────────
COUNTRIES.update({
  'kazakhstan': {
    'slug': 'kazakhstan',
    'name_ru': 'Казахстан',
    'name_en': 'Kazakhstan',
    'title_styled': 'Казах<em>стан</em>',
    'flag': '🇰🇿',
    'region': 'Центральная Азия',
    'gmt': 'GMT+5',
    'currency': 'Тенге · KZT',
    'population': '19 млн чел.',
    'visa_badge': 'Внутренний паспорт',
    'visa_badge_color': 'green',
    'stat_budget': '~2 200 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~30K ₽',
    'stat_rent_sub': '1 комн.',
    'stat_climate': '+10°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '80',
    'stat_internet_sub': 'Мбит · 4G',
    'qc_flight': 'от 12 000 ₽',
    'qc_hostel': '600–1 200 ₽',
    'qc_hotel': '2 000–5 000 ₽',
    'qc_rent': '22–50К ₽',
    'qc_food': '130–350 ₽',
    'qc_taxi': '60–250 ₽',
    'aviasales_dest': 'ALA',
    'yesim_sub': 'kazakhstan',
    'currency_rate': 'курс: 1 ₽ ≈ 4.8 KZT · апр 2026',
    'local_currency_symbol': '₸',
    'local_currency_name': 'KZT',
    'breadcrumb_region': 'Центральная Азия',
    'overline': 'Центральная Азия · Досье',
    'country_num': '#6',
    'prev_country': {'slug': 'vietnam', 'flag': '🇻🇳', 'name': 'Вьетнам'},
    'next_country': {'slug': 'belarus', 'flag': '🇧🇾', 'name': 'Беларусь'},
    'hero_query': 'Almaty Kazakhstan mountains city',
  },
  'belarus': {
    'slug': 'belarus',
    'name_ru': 'Беларусь',
    'name_en': 'Belarus',
    'title_styled': 'Бела<em>русь</em>',
    'flag': '🇧🇾',
    'region': 'Восточная Европа',
    'gmt': 'GMT+3',
    'currency': 'Рубль · BYN',
    'population': '9.4 млн чел.',
    'visa_badge': 'Внутренний паспорт',
    'visa_badge_color': 'green',
    'stat_budget': '~2 500 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~35K ₽',
    'stat_rent_sub': '1 комн.',
    'stat_climate': '+7°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '100',
    'stat_internet_sub': 'Мбит · 4G/5G',
    'qc_flight': 'от 8 000 ₽',
    'qc_hostel': '600–1 200 ₽',
    'qc_hotel': '2 200–5 000 ₽',
    'qc_rent': '25–55К ₽',
    'qc_food': '150–400 ₽',
    'qc_taxi': '70–300 ₽',
    'aviasales_dest': 'MSQ',
    'yesim_sub': 'belarus',
    'currency_rate': 'курс: 1 ₽ ≈ 0.033 BYN · апр 2026',
    'local_currency_symbol': 'Br',
    'local_currency_name': 'BYN',
    'breadcrumb_region': 'Восточная Европа',
    'overline': 'Восточная Европа · Досье',
    'country_num': '#7',
    'prev_country': {'slug': 'kazakhstan', 'flag': '🇰🇿', 'name': 'Казахстан'},
    'next_country': {'slug': 'indonesia', 'flag': '🇮🇩', 'name': 'Индонезия'},
    'hero_query': 'Minsk Belarus city center avenue',
  },
  'indonesia': {
    'slug': 'indonesia',
    'name_ru': 'Индонезия',
    'name_en': 'Indonesia',
    'title_styled': 'Индоне<em>зия</em>',
    'flag': '🇮🇩',
    'region': 'Юго-Восточная Азия',
    'gmt': 'GMT+8',
    'currency': 'Рупия · IDR',
    'population': '277 млн чел.',
    'visa_badge': 'Без визы · 30 дней',
    'visa_badge_color': 'amber',
    'stat_budget': '~2 200 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~32K ₽',
    'stat_rent_sub': '1 комн. Бали',
    'stat_climate': '+28°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '40',
    'stat_internet_sub': 'Мбит · 4G',
    'qc_flight': 'от 32 000 ₽',
    'qc_hostel': '500–1 000 ₽',
    'qc_hotel': '1 800–5 000 ₽',
    'qc_rent': '20–60К ₽',
    'qc_food': '100–400 ₽',
    'qc_taxi': '60–250 ₽',
    'aviasales_dest': 'DPS',
    'yesim_sub': 'indonesia',
    'currency_rate': 'курс: 1 ₽ ≈ 145 IDR · апр 2026',
    'local_currency_symbol': 'Rp',
    'local_currency_name': 'IDR',
    'breadcrumb_region': 'Юго-Восточная Азия',
    'overline': 'Юго-Восточная Азия · Досье',
    'country_num': '#8',
    'prev_country': {'slug': 'belarus', 'flag': '🇧🇾', 'name': 'Беларусь'},
    'next_country': {'slug': 'malaysia', 'flag': '🇲🇾', 'name': 'Малайзия'},
    'hero_query': 'Bali Indonesia rice terraces temple',
  },
  'malaysia': {
    'slug': 'malaysia',
    'name_ru': 'Малайзия',
    'name_en': 'Malaysia',
    'title_styled': 'Малай<em>зия</em>',
    'flag': '🇲🇾',
    'region': 'Юго-Восточная Азия',
    'gmt': 'GMT+8',
    'currency': 'Ринггит · MYR',
    'population': '33 млн чел.',
    'visa_badge': 'Без визы · 90 дней',
    'visa_badge_color': 'green',
    'stat_budget': '~2 500 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~35K ₽',
    'stat_rent_sub': '1 комн. KL',
    'stat_climate': '+27°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '100',
    'stat_internet_sub': 'Мбит · 4G/5G',
    'qc_flight': 'от 30 000 ₽',
    'qc_hostel': '500–1 100 ₽',
    'qc_hotel': '2 000–5 500 ₽',
    'qc_rent': '22–50К ₽',
    'qc_food': '120–400 ₽',
    'qc_taxi': '60–300 ₽',
    'aviasales_dest': 'KUL',
    'yesim_sub': 'malaysia',
    'currency_rate': 'курс: 1 ₽ ≈ 0.043 MYR · апр 2026',
    'local_currency_symbol': 'RM',
    'local_currency_name': 'MYR',
    'breadcrumb_region': 'Юго-Восточная Азия',
    'overline': 'Юго-Восточная Азия · Досье',
    'country_num': '#9',
    'prev_country': {'slug': 'indonesia', 'flag': '🇮🇩', 'name': 'Индонезия'},
    'next_country': {'slug': 'uae', 'flag': '🇦🇪', 'name': 'ОАЭ'},
    'hero_query': 'Kuala Lumpur Malaysia Petronas towers night',
  },
  'uae': {
    'slug': 'uae',
    'name_ru': 'ОАЭ',
    'name_en': 'UAE',
    'title_styled': 'О<em>АЭ</em>',
    'flag': '🇦🇪',
    'region': 'Ближний Восток',
    'gmt': 'GMT+4',
    'currency': 'Дирхам · AED',
    'population': '10 млн чел.',
    'visa_badge': 'Без визы · 90 дней',
    'visa_badge_color': 'green',
    'stat_budget': '~6 000 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~90K ₽',
    'stat_rent_sub': '1 комн. Дубай',
    'stat_climate': '+28°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '200',
    'stat_internet_sub': 'Мбит · 5G',
    'qc_flight': 'от 16 000 ₽',
    'qc_hostel': '1 500–3 000 ₽',
    'qc_hotel': '5 000–15 000 ₽',
    'qc_rent': '70–150К ₽',
    'qc_food': '300–900 ₽',
    'qc_taxi': '150–600 ₽',
    'aviasales_dest': 'DXB',
    'yesim_sub': 'uae',
    'currency_rate': 'курс: 1 ₽ ≈ 0.040 AED · апр 2026',
    'local_currency_symbol': 'AED',
    'local_currency_name': 'AED',
    'breadcrumb_region': 'Ближний Восток',
    'overline': 'Ближний Восток · Досье',
    'country_num': '#10',
    'prev_country': {'slug': 'malaysia', 'flag': '🇲🇾', 'name': 'Малайзия'},
    'next_country': {'slug': 'montenegro', 'flag': '🇲🇪', 'name': 'Черногория'},
    'hero_query': 'Dubai UAE skyline Burj Khalifa night',
  },
  'montenegro': {
    'slug': 'montenegro',
    'name_ru': 'Черногория',
    'name_en': 'Montenegro',
    'title_styled': 'Черно<em>гория</em>',
    'flag': '🇲🇪',
    'region': 'Балканы',
    'gmt': 'GMT+1',
    'currency': 'Евро · EUR',
    'population': '0.6 млн чел.',
    'visa_badge': 'Без визы · 90 дней',
    'visa_badge_color': 'green',
    'stat_budget': '~3 000 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~40K ₽',
    'stat_rent_sub': '1 комн.',
    'stat_climate': '+15°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '80',
    'stat_internet_sub': 'Мбит · 4G',
    'qc_flight': 'от 20 000 ₽',
    'qc_hostel': '900–1 800 ₽',
    'qc_hotel': '2 500–6 000 ₽',
    'qc_rent': '30–65К ₽',
    'qc_food': '200–500 ₽',
    'qc_taxi': '100–400 ₽',
    'aviasales_dest': 'TGD',
    'yesim_sub': 'montenegro',
    'currency_rate': 'курс: 1 ₽ ≈ 0.010 EUR · апр 2026',
    'local_currency_symbol': '€',
    'local_currency_name': 'EUR',
    'breadcrumb_region': 'Балканы',
    'overline': 'Балканы · Досье',
    'country_num': '#11',
    'prev_country': {'slug': 'uae', 'flag': '🇦🇪', 'name': 'ОАЭ'},
    'next_country': {'slug': 'cyprus', 'flag': '🇨🇾', 'name': 'Кипр'},
    'hero_query': 'Montenegro Kotor bay mountains sea',
  },
  'cyprus': {
    'slug': 'cyprus',
    'name_ru': 'Кипр',
    'name_en': 'Cyprus',
    'title_styled': 'Ки<em>пр</em>',
    'flag': '🇨🇾',
    'region': 'Восточное Средиземноморье',
    'gmt': 'GMT+2',
    'currency': 'Евро · EUR',
    'population': '1.2 млн чел.',
    'visa_badge': 'Шенген · 90 дней',
    'visa_badge_color': 'amber',
    'stat_budget': '~4 000 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~55K ₽',
    'stat_rent_sub': '1 комн.',
    'stat_climate': '+21°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '100',
    'stat_internet_sub': 'Мбит · 4G',
    'qc_flight': 'от 18 000 ₽',
    'qc_hostel': '1 200–2 500 ₽',
    'qc_hotel': '3 500–8 000 ₽',
    'qc_rent': '40–80К ₽',
    'qc_food': '250–600 ₽',
    'qc_taxi': '120–450 ₽',
    'aviasales_dest': 'LCA',
    'yesim_sub': 'cyprus',
    'currency_rate': 'курс: 1 ₽ ≈ 0.010 EUR · апр 2026',
    'local_currency_symbol': '€',
    'local_currency_name': 'EUR',
    'breadcrumb_region': 'Средиземноморье',
    'overline': 'Средиземноморье · Досье',
    'country_num': '#12',
    'prev_country': {'slug': 'montenegro', 'flag': '🇲🇪', 'name': 'Черногория'},
    'next_country': {'slug': 'portugal', 'flag': '🇵🇹', 'name': 'Португалия'},
    'hero_query': 'Cyprus Limassol sea coast sunset',
  },
  'portugal': {
    'slug': 'portugal',
    'name_ru': 'Португалия',
    'name_en': 'Portugal',
    'title_styled': 'Порту<em>галия</em>',
    'flag': '🇵🇹',
    'region': 'Западная Европа',
    'gmt': 'GMT+0',
    'currency': 'Евро · EUR',
    'population': '10 млн чел.',
    'visa_badge': 'D7 виза · от 1 года',
    'visa_badge_color': 'amber',
    'stat_budget': '~4 500 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~65K ₽',
    'stat_rent_sub': '1 комн. Лиссабон',
    'stat_climate': '+17°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '150',
    'stat_internet_sub': 'Мбит · 4G/5G',
    'qc_flight': 'от 25 000 ₽',
    'qc_hostel': '1 200–2 500 ₽',
    'qc_hotel': '4 000–10 000 ₽',
    'qc_rent': '50–100К ₽',
    'qc_food': '250–700 ₽',
    'qc_taxi': '150–600 ₽',
    'aviasales_dest': 'LIS',
    'yesim_sub': 'portugal',
    'currency_rate': 'курс: 1 ₽ ≈ 0.010 EUR · апр 2026',
    'local_currency_symbol': '€',
    'local_currency_name': 'EUR',
    'breadcrumb_region': 'Западная Европа',
    'overline': 'Западная Европа · Досье',
    'country_num': '#13',
    'prev_country': {'slug': 'cyprus', 'flag': '🇨🇾', 'name': 'Кипр'},
    'next_country': {'slug': 'germany', 'flag': '🇩🇪', 'name': 'Германия'},
    'hero_query': 'Lisbon Portugal Alfama tram sunset',
  },
  'germany': {
    'slug': 'germany',
    'name_ru': 'Германия',
    'name_en': 'Germany',
    'title_styled': 'Герма<em>ния</em>',
    'flag': '🇩🇪',
    'region': 'Западная Европа',
    'gmt': 'GMT+1',
    'currency': 'Евро · EUR',
    'population': '84 млн чел.',
    'visa_badge': 'Opportunity Card · 1 год',
    'visa_badge_color': 'amber',
    'stat_budget': '~5 500 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~90K ₽',
    'stat_rent_sub': '1 комн. Берлин',
    'stat_climate': '+10°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '200',
    'stat_internet_sub': 'Мбит · 4G/5G',
    'qc_flight': 'от 18 000 ₽',
    'qc_hostel': '1 500–3 000 ₽',
    'qc_hotel': '5 000–12 000 ₽',
    'qc_rent': '70–120К ₽',
    'qc_food': '300–800 ₽',
    'qc_taxi': '200–700 ₽',
    'aviasales_dest': 'BER',
    'yesim_sub': 'germany',
    'currency_rate': 'курс: 1 ₽ ≈ 0.010 EUR · апр 2026',
    'local_currency_symbol': '€',
    'local_currency_name': 'EUR',
    'breadcrumb_region': 'Западная Европа',
    'overline': 'Западная Европа · Досье',
    'country_num': '#14',
    'prev_country': {'slug': 'portugal', 'flag': '🇵🇹', 'name': 'Португалия'},
    'next_country': {'slug': 'argentina', 'flag': '🇦🇷', 'name': 'Аргентина'},
    'hero_query': 'Berlin Germany Brandenburg Gate sunset',
  },
  'argentina': {
    'slug': 'argentina',
    'name_ru': 'Аргентина',
    'name_en': 'Argentina',
    'title_styled': 'Арген<em>тина</em>',
    'flag': '🇦🇷',
    'region': 'Латинская Америка',
    'gmt': 'GMT-3',
    'currency': 'Песо · ARS',
    'population': '46 млн чел.',
    'visa_badge': 'Без визы · 90 дней',
    'visa_badge_color': 'green',
    'stat_budget': '~2 000 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~25K ₽',
    'stat_rent_sub': '1 комн. Буэнос-Айрес',
    'stat_climate': '+18°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '60',
    'stat_internet_sub': 'Мбит · 4G',
    'qc_flight': 'от 55 000 ₽',
    'qc_hostel': '600–1 400 ₽',
    'qc_hotel': '2 000–6 000 ₽',
    'qc_rent': '18–45К ₽',
    'qc_food': '100–400 ₽',
    'qc_taxi': '60–250 ₽',
    'aviasales_dest': 'BUE',
    'yesim_sub': 'argentina',
    'currency_rate': 'курс: 1 ₽ ≈ 11 ARS · апр 2026',
    'local_currency_symbol': '$',
    'local_currency_name': 'ARS',
    'breadcrumb_region': 'Латинская Америка',
    'overline': 'Латинская Америка · Досье',
    'country_num': '#15',
    'prev_country': {'slug': 'germany', 'flag': '🇩🇪', 'name': 'Германия'},
    'next_country': {'slug': 'mexico', 'flag': '🇲🇽', 'name': 'Мексика'},
    'hero_query': 'Buenos Aires Argentina city colorful',
  },
  'mexico': {
    'slug': 'mexico',
    'name_ru': 'Мексика',
    'name_en': 'Mexico',
    'title_styled': 'Мек<em>сика</em>',
    'flag': '🇲🇽',
    'region': 'Латинская Америка',
    'gmt': 'GMT-6',
    'currency': 'Песо · MXN',
    'population': '130 млн чел.',
    'visa_badge': 'Без визы · 180 дней',
    'visa_badge_color': 'green',
    'stat_budget': '~2 800 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~38K ₽',
    'stat_rent_sub': '1 комн. Мехико',
    'stat_climate': '+20°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '80',
    'stat_internet_sub': 'Мбит · 4G',
    'qc_flight': 'от 60 000 ₽',
    'qc_hostel': '700–1 500 ₽',
    'qc_hotel': '2 500–7 000 ₽',
    'qc_rent': '25–60К ₽',
    'qc_food': '150–500 ₽',
    'qc_taxi': '80–350 ₽',
    'aviasales_dest': 'MEX',
    'yesim_sub': 'mexico',
    'currency_rate': 'курс: 1 ₽ ≈ 0.18 MXN · апр 2026',
    'local_currency_symbol': '$',
    'local_currency_name': 'MXN',
    'breadcrumb_region': 'Латинская Америка',
    'overline': 'Латинская Америка · Досье',
    'country_num': '#16',
    'prev_country': {'slug': 'argentina', 'flag': '🇦🇷', 'name': 'Аргентина'},
    'next_country': {'slug': 'egypt', 'flag': '🇪🇬', 'name': 'Египет'},
    'hero_query': 'Mexico City Zocalo colorful streets',
  },
  'egypt': {
    'slug': 'egypt',
    'name_ru': 'Египет',
    'name_en': 'Egypt',
    'title_styled': 'Еги<em>пет</em>',
    'flag': '🇪🇬',
    'region': 'Северная Африка',
    'gmt': 'GMT+2',
    'currency': 'Фунт · EGP',
    'population': '105 млн чел.',
    'visa_badge': 'e-Visa · 30 дней',
    'visa_badge_color': 'amber',
    'stat_budget': '~1 500 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~18K ₽',
    'stat_rent_sub': '1 комн. Каир',
    'stat_climate': '+26°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '40',
    'stat_internet_sub': 'Мбит · 4G',
    'qc_flight': 'от 14 000 ₽',
    'qc_hostel': '400–900 ₽',
    'qc_hotel': '1 500–4 500 ₽',
    'qc_rent': '12–30К ₽',
    'qc_food': '80–300 ₽',
    'qc_taxi': '40–200 ₽',
    'aviasales_dest': 'CAI',
    'yesim_sub': 'egypt',
    'currency_rate': 'курс: 1 ₽ ≈ 0.47 EGP · апр 2026',
    'local_currency_symbol': '£',
    'local_currency_name': 'EGP',
    'breadcrumb_region': 'Северная Африка',
    'overline': 'Северная Африка · Досье',
    'country_num': '#17',
    'prev_country': {'slug': 'mexico', 'flag': '🇲🇽', 'name': 'Мексика'},
    'next_country': {'slug': 'morocco', 'flag': '🇲🇦', 'name': 'Марокко'},
    'hero_query': 'Egypt Cairo pyramids Giza sunset',
  },
  'morocco': {
    'slug': 'morocco',
    'name_ru': 'Марокко',
    'name_en': 'Morocco',
    'title_styled': 'Марок<em>ко</em>',
    'flag': '🇲🇦',
    'region': 'Северная Африка',
    'gmt': 'GMT+1',
    'currency': 'Дирхам · MAD',
    'population': '37 млн чел.',
    'visa_badge': 'Без визы · 90 дней',
    'visa_badge_color': 'green',
    'stat_budget': '~2 000 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~22K ₽',
    'stat_rent_sub': '1 комн.',
    'stat_climate': '+18°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '50',
    'stat_internet_sub': 'Мбит · 4G',
    'qc_flight': 'от 22 000 ₽',
    'qc_hostel': '500–1 200 ₽',
    'qc_hotel': '2 000–5 500 ₽',
    'qc_rent': '15–38К ₽',
    'qc_food': '100–380 ₽',
    'qc_taxi': '50–250 ₽',
    'aviasales_dest': 'CMN',
    'yesim_sub': 'morocco',
    'currency_rate': 'курс: 1 ₽ ≈ 0.10 MAD · апр 2026',
    'local_currency_symbol': 'د.م.',
    'local_currency_name': 'MAD',
    'breadcrumb_region': 'Северная Африка',
    'overline': 'Северная Африка · Досье',
    'country_num': '#18',
    'prev_country': {'slug': 'egypt', 'flag': '🇪🇬', 'name': 'Египет'},
    'next_country': {'slug': 'china', 'flag': '🇨🇳', 'name': 'Китай'},
    'hero_query': 'Marrakech Morocco medina colorful streets',
  },
  'china': {
    'slug': 'china',
    'name_ru': 'Китай',
    'name_en': 'China',
    'title_styled': 'Ки<em>тай</em>',
    'flag': '🇨🇳',
    'region': 'Восточная Азия',
    'gmt': 'GMT+8',
    'currency': 'Юань · CNY',
    'population': '1.4 млрд чел.',
    'visa_badge': 'Без визы · 30 дней',
    'visa_badge_color': 'amber',
    'stat_budget': '~3 500 ₽',
    'stat_budget_sub': 'комфорт',
    'stat_rent': '~45K ₽',
    'stat_rent_sub': '1 комн. Шанхай',
    'stat_climate': '+15°',
    'stat_climate_sub': 'средний год',
    'stat_internet': '100',
    'stat_internet_sub': 'Мбит · 4G/5G',
    'qc_flight': 'от 20 000 ₽',
    'qc_hostel': '600–1 400 ₽',
    'qc_hotel': '2 500–7 000 ₽',
    'qc_rent': '30–70К ₽',
    'qc_food': '150–500 ₽',
    'qc_taxi': '80–350 ₽',
    'aviasales_dest': 'PEK',
    'yesim_sub': 'china',
    'currency_rate': 'курс: 1 ₽ ≈ 0.080 CNY · апр 2026',
    'local_currency_symbol': '¥',
    'local_currency_name': 'CNY',
    'breadcrumb_region': 'Восточная Азия',
    'overline': 'Восточная Азия · Досье',
    'country_num': '#19',
    'prev_country': {'slug': 'morocco', 'flag': '🇲🇦', 'name': 'Марокко'},
    'next_country': {'slug': 'thailand', 'flag': '🇹🇭', 'name': 'Тайланд'},
    'hero_query': 'Shanghai China skyline Bund night',
  },
})
print("All countries loaded:", list(COUNTRIES.keys()))


# ─────────────────────────────────────────────────────────────
# ЗАПУСК
# ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Использование: python3 generate_country.py <slug>")
        print("Доступные страны:", list(COUNTRIES.keys()))
        sys.exit(1)

    slug = sys.argv[1]
    generate(slug)
