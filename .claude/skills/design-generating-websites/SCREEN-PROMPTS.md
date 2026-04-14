# Screen Prompt Templates

Templates for generating each screen type. Replace `{placeholders}` with actual lead data.

## General Rules

- Every prompt must be specific and data-driven — never generic
- Include real business data: name, address, phone, reviews
- Describe visual hierarchy explicitly: what is large, what is small
- Specify spacing and layout intent
- Always mention "professional, clean, modern" to avoid AI-generic aesthetic
- Reference the business type for contextual design decisions

---

## 0. Single Page (Landing) — All-in-One

Use this when the user chose "Single Page" in Step 1b. Generate ONE screen with all sections.

```
Design a professional single-page landing website for "{business_name}", a {business_type} located in {address}.

NAVIGATION BAR (sticky top):
- Logo/business name on the left
- Anchor links: Inicio, Servicios, Opiniones, Contacto
- CTA button: "Contactanos"

HERO SECTION:
- Large bold headline: "{business_name}"
- Tagline: "{tagline_from_reviews}"
- CTA button: "Agendar Consulta" or appropriate for {business_type}
- {if_has_rating}Rating: {rating} stars from {rating_count} reviews{end_if}
- Minimum 112px padding below

SERVICES SECTION (id="servicios"):
- Section title: "Nuestros Servicios" or appropriate for {business_type}
- 3-4 key services in asymmetric grid (first service larger)
- Icons, not images. Brief descriptions.
- 112px spacing from hero

TESTIMONIAL SECTION (id="opiniones"):
- Section title: "Lo que dicen nuestros clientes"
- Featured review: "{best_review_text}" — {review_author}, {review_rating} stars
- 2-3 additional reviews as smaller cards
- Overall rating display

CONTACT SECTION (id="contacto"):
- Section title: "Contacto"
- Two columns: info + form
- Left: phone {phone}, address {full_address}, hours summary
- Right: simple form (name, email, message, send button)
- Google Maps link: {maps_url}

FOOTER:
- Business name, address, phone
- Navigation links echoing the top bar
- No social media unless provided

Style: professional, single-color backgrounds per section, 112px minimum between sections, no gradients, no floating elements.
```

---

## 1. Landing / Home Page

```
Design a professional landing page for "{business_name}", a {business_type} located in {address}.

HERO SECTION:
- Large bold headline: "{business_name}" taking up significant visual space
- Tagline derived from their reputation: "{tagline_from_reviews}"
- A prominent call-to-action button: "Contactanos" or "Agendar Consulta"
- {if_has_rating}Display rating: {rating} stars from {rating_count} reviews as social proof{end_if}
- Clean, spacious layout with minimum 112px section padding

SERVICES PREVIEW:
- 3 key services based on their business type: {services_list}
- Use icons, not images. Minimal description per service
- Asymmetric grid, not uniform cards

TESTIMONIAL:
- One featured review: "{best_review_text}" — {review_author}
- Star rating displayed visually

CONTACT BAR:
- Phone: {phone}
- Address: {short_address}
- Hours summary: {hours_summary}

FOOTER:
- Business name, address, phone
- Simple navigation links
- No social media icons unless provided

Style: professional, clean, ample whitespace. Single-color backgrounds only. No gradients, no floating elements, no decorative blurs.
```

## 2. About Page

```
Design an About page for "{business_name}", a {business_type} in {address}.

HERO:
- Section title "Sobre Nosotros" with large typography
- {if_editorial}Brief description: "{editorial_summary}"{end_if}
- {if_no_editorial}Generate a professional description for a {business_type} emphasizing trust, experience, and local presence in {neighborhood}{end_if}

VALUES SECTION:
- 3 core values derived from review themes: {value_1}, {value_2}, {value_3}
- Each with an icon and 1-2 sentence description
- Staggered layout, not a uniform row

EXPERIENCE:
- Highlight years of presence (if inferable)
- {rating_count} clients served, {rating} average rating

{if_has_photos}
GALLERY:
- Display business photos in an asymmetric masonry-style grid
- Photos should be large and prominent
{end_if}

Style: warm, trustworthy. Generous whitespace. Typography-driven hierarchy.
```

## 3. Services Page

```
Design a Services page for "{business_name}", a {business_type}.

HEADER:
- "Nuestros Servicios" as section title
- Brief intro: what this business specializes in based on type

SERVICES GRID:
- {services_count} services appropriate for a {business_type}
- Each service: icon + name + 2-line description
- Use a 2-column layout with generous spacing (64px between items)
- Alternate card sizes: first service gets a larger hero card

CTA SECTION:
- "Consulta sin cargo" or appropriate CTA
- Phone number: {phone}
- Clean button design: white text on dark background or inverse

Style: organized, scannable. Clear visual hierarchy between service tiers. No decorative elements.
```

## 4. Reviews / Testimonials Page

```
Design a Testimonials page for "{business_name}" showcasing real client reviews.

HEADER:
- "Lo que dicen nuestros clientes" as title
- Overall rating display: {rating} stars from {rating_count} reviews

FEATURED REVIEW:
- Largest card at top
- "{featured_review_text}"
- Author: {featured_review_author}
- {featured_review_rating} stars
- Generous padding, quote-style typography

ADDITIONAL REVIEWS:
{for_each_review}
- "{review_text}"
- {review_author} — {review_rating} stars — {review_time}
{end_for}
- Display as stacked cards with alternating subtle background tones
- Star ratings shown visually in gold/amber

CTA:
- "Dejanos tu opinion" or "Contactanos"
- Phone: {phone}

Style: social proof focused. Large quote marks or review styling. Trust-building layout.
```

## 5. Contact Page

```
Design a Contact page for "{business_name}" located at {address}.

HEADER:
- "Contacto" as title
- Brief message: "Estamos para ayudarte"

CONTACT INFO GRID:
- Phone: {phone} (with click-to-call styling)
- Address: {full_address}
- {if_has_website}Website: {website}{end_if}
- Google Maps link: {maps_url}

HOURS SECTION:
- Display full weekly schedule:
{for_each_hour_line}
  - {hour_line}
{end_for}
- Clean table or list layout
- Highlight current day if applicable

MAP PLACEHOLDER:
- Large area reserved for map embed
- Show a placeholder with the address text and a "Ver en Google Maps" link

CONTACT FORM:
- Simple form: Name, Email/Phone, Message
- Single CTA button: "Enviar Mensaje"
- Minimal fields, no unnecessary complexity

Style: functional, clean. Information-first. Easy to scan and act on.
```

---

## App Screens (Mobile)

Use these when the user chose "App" in Step 1b.

### App 1. Splash / Onboarding

```
Design a mobile app splash screen for "{business_name}", a {business_type}.

- Centered logo area with business name in large bold text
- Tagline: "{tagline_from_reviews}"
- {if_has_rating}Small badge: "{rating} ★ · {rating_count} reviews"{end_if}
- Full-screen layout, single background color
- Bottom: primary button "Comenzar" and secondary text "Ya tengo cuenta"
- No navigation bar on this screen
- Clean, premium feel. No gradients, no decorative elements.
```

### App 2. Home Feed

```
Design a mobile app home screen for "{business_name}", a {business_type} in {address}.

TOP BAR:
- Business name as title, left-aligned
- Notification bell icon on the right

HERO CARD:
- Featured image or business photo placeholder
- "{business_name}" overlay text
- Quick action: "Llamar" or "Reservar"

QUICK ACTIONS ROW:
- 3-4 icon buttons: Servicios, Opiniones, Ubicacion, Contacto
- Horizontal scrollable if needed

HIGHLIGHTS:
- Rating card: {rating} stars from {rating_count} reviews
- Next open/close: based on {hours_summary}
- Featured service or promo

BOTTOM TAB BAR (sticky):
- Icons: Inicio (active), Servicios, Opiniones, Perfil
- Standard mobile tab bar pattern

Style: card-based layout, mobile-native spacing (16px padding), rounded corners, no desktop patterns.
```

### App 3. Services / Menu

```
Design a mobile app services screen for "{business_name}", a {business_type}.

TOP BAR:
- Back arrow + "Servicios" title

SERVICES LIST:
- Scrollable vertical list of service cards
- Each card: icon + service name + 1-line description + optional price
- Services appropriate for a {business_type}: {services_list}
- Cards with subtle border, rounded corners
- 12px gap between cards

CTA:
- Floating bottom button: "Consultar por un servicio"
- Phone: {phone}

BOTTOM TAB BAR: same as home

Style: clean list, easy to scan, tap-friendly (min 44px touch targets).
```

### App 4. Reviews

```
Design a mobile app reviews screen for "{business_name}".

TOP BAR:
- Back arrow + "Opiniones" title

RATING SUMMARY:
- Large display: {rating} with star visualization
- "{rating_count} opiniones"
- Rating distribution bar (5 stars, 4 stars, etc.) if data available

REVIEW CARDS (scrollable):
{for_each_review}
- Card with: author name, star rating, time, review text
- "{review_text}" — {review_author}
{end_for}
- Cards stacked vertically with 8px gap

BOTTOM TAB BAR: same as home

Style: social proof focused, readable review cards, gold/amber stars.
```

### App 5. Profile / Contact

```
Design a mobile app profile/contact screen for "{business_name}", a {business_type} at {address}.

TOP BAR:
- "Perfil" title

BUSINESS CARD:
- Business name large
- Type badge: {business_type}
- Rating: {rating} ★

ACTION BUTTONS:
- Row of 3: Llamar ({phone}), Ubicacion (maps link), Web ({website} or disabled)
- Icon + label per button

INFO SECTIONS:
- Direccion: {full_address} with map link
- Telefono: {phone}
- Horarios: {hours_list}

{if_has_photos}
GALLERY:
- Horizontal scrollable photo row
{end_if}

BOTTOM TAB BAR: same as home (Perfil active)

Style: information-dense but organized, easy tap actions, mobile-native.
```

---

## Multi Page: Navigation Bar Template

When generating multi-page websites, every screen must include this consistent nav. Add to the top of each multi-page prompt:

```
NAVIGATION BAR (consistent across all pages):
- Logo/business name on the left
- Links: Inicio, Nosotros, Servicios, Opiniones, Contacto
- Current page link is visually active (underline or bold)
- CTA button on the right: "Contactanos"
- Sticky on scroll

FOOTER (consistent across all pages):
- Business name, address, phone
- Same navigation links
- "© {current_year} {business_name}"
```

---

## Prompt Construction Tips

When building prompts from lead data:

1. **Always use real data** — never placeholder text like "Lorem ipsum"
2. **Quote actual reviews** — they add authenticity
3. **Be specific about layout** — "2-column grid with 48px gap" not "show services"
4. **Specify what NOT to include** — "no gradients, no floating decorations"
5. **Include business context** — "{business_type} in {neighborhood}" helps the model understand the tone
6. **Mention spacing explicitly** — "112px between sections, 64px between groups"
7. **For apps** — always mention "mobile-native", "44px min touch targets", "bottom tab bar"
8. **For single page** — always mention "anchor navigation", "sticky nav", section IDs
