# CheckTheWorld — Резюме проекта

## Концепция
Агрегатор для путешественников и эмигрантов из России/СНГ. Визы, цены на жильё, авиабилеты, города по 180+ странам. Аналоги: Nomad List, Teleport.org, Expatistan — но на русском с live-данными. Целевая аудитория: туристы, цифровые кочевники, эмигранты из РФ.

---

## Технический стек
- **Фронтенд:** Чистый HTML/CSS/JS, без фреймворков
- **Хостинг:** Cloudflare Pages (бесплатно), домен **checktheworld.ru** — куплен на рег.ру, подключён через Cloudflare (DNS управляется в Cloudflare, домен проксируется через Cloudflare CDN).
- **Auth & DB:** Firebase (Spark plan) — Authentication (Email/Password + Google), Firestore. Проект: `checktheworld-a631d`
- **Email:** EmailJS — Public key: `EWJ_3i5lkBRcBkjMg`, Service: `service_yj0l9dd`, шаблоны: `template_3sirk17` (пользователю), `template_sa9p4su` (владельцу)
- **Партнёрки:** Travelpayouts Drive скрипт `<script nowprocket src='https://tp-em.com/NTE1NTI2.js?t=515526'>` — вставлен в `<head>` всех страниц. Аккаунт: nikromashin07@gmail.com
- **Шрифты:** Playfair Display + Manrope (Google Fonts)

---

## Firebase конфиг
```js
const firebaseConfig = {
  apiKey: "AIzaSyC_erJyfCASKgjMaMXTF4ovqfwfC4-5GmU",
  authDomain: "checktheworld-a631d.firebaseapp.com",
  projectId: "checktheworld-a631d",
  storageBucket: "checktheworld-a631d.firebasestorage.app",
  messagingSenderId: "1006756841439",
  appId: "1:1006756841439:web:ab81d8f3f469ea3d07666a"
};
```
Firebase SDK подключается через CDN: `https://cdn.jsdelivr.net/npm/firebase@9.23.0/`

### Структура Firestore (коллекция `users`)
```
users/{uid}:
  name: string
  email: string
  createdAt: timestamp
  favorites: string[]   // ключи стран: ['thailand', 'georgia', ...]
  visited: string[]     // посещённые страны
  visas: array          // [{country, entry, allowed}]
  currency: string      // 'rub' | 'usd' | 'eur'
  status: string        // 'planning' | 'moving' | 'living' | 'traveling' | 'returned'
```

---

## Деплой на Cloudflare Pages
1. Зайти на [pages.cloudflare.com](https://pages.cloudflare.com)
2. Создать новый проект → Connect to Git или Direct Upload
3. Добавить кастомный домен `checktheworld.ru`
4. SSL/HTTPS включается автоматически

### Конфигурационные файлы
- **`_redirects`** — HTTP→HTTPS редиректы
- **`_headers`** — заголовки безопасности
Оба файла лежат в корне проекта рядом с index.html.

---

## Цветовая палитра и дизайн
```css
--bg: #faf8f2;          /* молочный фон */
--white: #ffffff;
--black: #1a1a18;
--g500: #484842;        /* основной текст */
--g300: #848480;        /* вторичный текст */
--g100: #e6e2d8;        /* границы */
--green: #1c7a54;       /* акцент */
--green-mid: #30b278;
--green-light: #d8f2e6;
--amber: #e08c2a;       /* янтарный акцент */
--amber-light: #fef3e2;
```
- Навигация: sticky, янтарная нижняя линия 2px
- Блоб-фон: 2 размытых пятна (зелёный + янтарный), анимация
- Анимации появления: IntersectionObserver, opacity 0→1

---

## Файлы проекта

### Лендинг
- **checktheworld_v9.html** — главный лендинг с формой раннего доступа

### Авторизация и личный кабинет
- **login.html** — страница входа/регистрации:
  - Вход по Email/Password и через Google
  - Подтверждение пароля при регистрации
  - Индикатор сложности пароля (слабый/средний/надёжный)
  - Блокировка кириллицы с предупреждением
  - Восстановление пароля через Firebase (`sendPasswordResetEmail`)
  - Русские тексты всех ошибок Firebase
- **dashboard.html** — личный кабинет (layout: сайдбар слева + контент справа, `position:fixed`):
  - **Обзор** — 4 статы (избранное, посещено, визы, маршруты), мини-блоки избранного/виз/карты/калькулятора/достижений
  - **Избранное** — карточки стран с бюджетом и визовым режимом, удаление
  - **Визовый трекер** — добавление стран с датой въезда и сроком, прогресс-бар, цветовые статусы
  - **Калькулятор бюджета** — страна, дни (слайдер), кол-во людей, жильё, питание
  - **Профиль** — статус переезда (5 вариантов), настройки имени и валюты, выход
  - Динамическая подпись виз: "нет активных" / "всё в порядке ✓" / "скоро истекают" / "⚠ истекает через неделю"

### Каталог
- **index.html** — каталог стран с поиском и фильтрами (безвиз / бюджет / климат)

### Страницы стран (9 штук)
- **thailand.html** — эталонный шаблон
- **serbia.html**, **turkey.html**, **armenia.html**, **vietnam.html**, **china.html**, **georgia.html**, **belarus.html**, **kazakhstan.html**

### Вспомогательные файлы
- **auth-snippet.html** — сниппет Firebase Auth для навигации всех страниц
- **_redirects**, **_headers** — конфигурация Cloudflare Pages
- **sitemap.xml** ✅

### Скрипты
- **/home/claude/inject_auth.py** — вставляет auth-snippet во все HTML файлы автоматически
- **/home/claude/build_final.py** — генерирует страницы стран из шаблона Тайланда

---

## Структура страницы страны (шаблон thailand.html)

1. **Hero** — флаг, название, регион/валюта/TZ, бейдж визы, 4 стата, липкая quick-карточка справа
2. **Визовый режим** — 4 кликабельные карточки → попап
3. **Стоимость жизни** — 9 карточек + переключатель валют
4. **Авиабилеты** — виджет Aviasales (Travelpayouts)
5. **Жильё** — кнопка → Booking.com
6. **Города и курорты** — горизонтальный слайдер, попапы
7. **Полезные советы** — 5-6 пунктов
8. **SIM-карта и страховка** — Yesim + Cherehapa
9. **Навигация** между странами

---

## Данные по странам

| Страна | Визовый режим | Бюджет/день | Местная валюта | Курс |
|--------|--------------|-------------|----------------|------|
| Тайланд | 60 дней | ~3 200 ₽ | Баты (฿) | ×33 |
| Сербия | 30 дней | ~2 000 ₽ | Динары (дин.) | ×1.2 |
| Турция | 60 дней | ~2 400 ₽ | Лиры (TRY) | ×2.8 |
| Армения | 180 дней | ~1 600 ₽ | Драмы (AMD) | ×43 |
| Вьетнам | 45 дней | ~1 900 ₽ | Донги (K VND) | ×2.3 |
| Китай | 30 дней | ~3 500 ₽ | Юани (¥) | ×12.5 |
| Грузия | 365 дней | ~1 800 ₽ | Лари (GEL) | ×24 |
| Беларусь | Внутренний паспорт | ~2 500 ₽ | Рубли (BYN) | ×30 |
| Казахстан | Внутренний паспорт | ~2 200 ₽ | Тенге (₸) | ×220 |

---

## Travelpayouts партнёрки
Подключены: Aviasales, Суточно.ру, Яндекс Путешествия, Островок, Cherehapa, Yesim, Airalo.

Партнёрские ссылки:
- Yesim eSIM: `https://yesim.app`
- Cherehapa страховка: `https://cherehapa.ru`
- Booking.com: `https://www.booking.com/country/[код].ru.html`

---

## Что реализовано ✅
- Лендинг v9 с анимациями, лентой стран, попапами, EmailJS, Travelpayouts
- index.html с поиском и фильтрами
- 9 страниц стран с полным функционалом (визы, города, валюты, Aviasales)
- Домен checktheworld.ru подключён через Cloudflare Pages ✅
- sitemap.xml создан ✅
- Кнопка "Войти" / имя пользователя во всех страницах навигации ✅
- **Личный кабинет (Firebase)** ✅:
  - login.html — вход/регистрация с полной валидацией
  - dashboard.html — профиль, статус переезда, избранное, визовый трекер, калькулятор бюджета

---

## Pending задачи

### Кнопка «В избранное» на страницах стран
Добавить кнопку на каждую страницу страны — сохраняет в `users/{uid}/favorites` в Firestore. Незалогиненным — редирект на login.html.

### Фото городов
Фото в слайдере городов ссылаются на Unsplash — не загружаются без реферера. Скачать вручную в папку `img/` и обновить src в HTML.

### Детальные визовые попапы для 8 стран
VISAS JS упрощён. Нужно интегрировать FULL_VISAS в build_final.py.

### Авиабилеты для стран (кроме Тайланда)
Обновить destination в виджете Aviasales:
- Сербия: BEG · Турция: IST · Армения: EVN · Вьетнам: HAN
- Китай: PEK · Грузия: TBS · Беларусь: MSQ · Казахстан: ALA

### SEO
- Open Graph мета-теги для каждой страницы
- Schema.org FAQPage разметку
- Зарегистрировать в Google Search Console

### Ещё не сделанные страницы стран
Португалия, ОАЭ, Индонезия, Черногория, Германия, Кипр

---

## Продвижение (план)
1. **Telegram** — посты в чатах эмигрантов при запуске
2. **VC.ru** — статья «Как я делал альтернативу Nomad List»
3. **Product Hunt** — запуск в 00:01 SF time
4. **SEO** — под запросы «виза в Грузию для россиян», «переезд в Сербию» и т.д.
5. **Монетизация** — Travelpayouts уже подключён, добавить Booking.com Affiliate и Wise реферальную

---

## Как пересобрать страницы стран
```bash
python3 /home/claude/build_final.py
```
Скрипт берёт шаблон из `/mnt/user-data/uploads/thailand__9__ПОКА__КРАЙНЯЯ.html` и генерирует 8 файлов.

**Важно:** после пересборки нужно заново применить патч VISAS/CITIES и вставить auth-snippet через inject_auth.py.
