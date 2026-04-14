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

## Prompt Construction Tips

When building prompts from lead data:

1. **Always use real data** — never placeholder text like "Lorem ipsum"
2. **Quote actual reviews** — they add authenticity
3. **Be specific about layout** — "2-column grid with 48px gap" not "show services"
4. **Specify what NOT to include** — "no gradients, no floating decorations"
5. **Include business context** — "{business_type} in {neighborhood}" helps the model understand the tone
6. **Mention spacing explicitly** — "112px between sections, 64px between groups"
