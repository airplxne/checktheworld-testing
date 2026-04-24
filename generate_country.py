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
# ЗАПУСК
# ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Использование: python3 generate_country.py <slug>")
        print("Доступные страны:", list(COUNTRIES.keys()))
        sys.exit(1)

    slug = sys.argv[1]
    generate(slug)
