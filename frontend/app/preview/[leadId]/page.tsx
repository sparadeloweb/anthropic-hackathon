import { MOCK_LEADS } from "@/lib/mock-data"

interface Props {
  params: Promise<{ leadId: string }>
}

export default async function PreviewPage({ params }: Props) {
  const { leadId } = await params
  const lead = MOCK_LEADS.find((l) => l.id === leadId)

  if (!lead) {
    return (
      <html>
        <body style={{ fontFamily: "sans-serif", padding: "40px", color: "#999" }}>
          <p>Lead not found: {leadId}</p>
        </body>
      </html>
    )
  }

  // In production this serves the Stitch-generated HTML file from storage/previews/[leadId]/index.html
  // For the demo, we render a representative landing page inline
  return (
    <html lang="es">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{lead.name}</title>
        {/* next/font does not apply here — this is a standalone client-site HTML document
            rendered inside an iframe (Stitch output). It is not part of the Next.js app shell. */}
        {/* eslint-disable-next-line @next/next/no-page-custom-font */}
        <link
          href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Inter:wght@400;500;600&display=swap"
          rel="stylesheet"
        />
        <style>{DEMO_STYLES}</style>
      </head>
      <body>
        <div dangerouslySetInnerHTML={{ __html: DEMO_SITE_HTML }} />
      </body>
    </html>
  )
}

// ─── Demo site HTML (represents Stitch output for La Parrilla de Juan) ────────

const DEMO_STYLES = `
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Inter', sans-serif; color: #292524; }
  .hero { background: #1A1108; color: white; padding: 80px 40px; text-align: center; min-height: 480px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; overflow: hidden; }
  .hero-bg { position: absolute; inset: 0; background: url('https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=1200') center/cover; opacity: 0.4; }
  .hero-content { position: relative; z-index: 1; }
  .hero h1 { font-family: 'Playfair Display', serif; font-size: 52px; font-weight: 700; line-height: 1.1; margin-bottom: 16px; }
  .hero p { font-size: 18px; color: #FEF3C7; margin-bottom: 32px; }
  .btn-primary { background: #C2410C; color: white; padding: 14px 32px; border-radius: 8px; font-weight: 600; font-size: 15px; border: none; cursor: pointer; text-decoration: none; display: inline-block; }
  .btn-secondary { border: 2px solid rgba(255,255,255,0.3); color: white; padding: 12px 28px; border-radius: 8px; font-weight: 500; font-size: 15px; margin-left: 12px; text-decoration: none; display: inline-block; }
  .section { padding: 64px 40px; }
  .section-light { background: #FFFAF5; }
  .section-dark { background: #1A1108; color: white; }
  .section-cream { background: #FEF3C7; }
  .container { max-width: 960px; margin: 0 auto; }
  .section-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.12em; color: #C2410C; font-weight: 600; margin-bottom: 8px; }
  .section-title { font-family: 'Playfair Display', serif; font-size: 36px; margin-bottom: 16px; }
  .menu-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 32px; }
  .menu-card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
  .menu-img { height: 160px; background: #F5E6D3; display: flex; align-items: center; justify-content: center; color: #92400E; font-size: 12px; font-weight: 500; }
  .menu-card-body { padding: 16px; }
  .menu-card-body h3 { font-family: 'Playfair Display', serif; font-size: 18px; margin-bottom: 4px; }
  .menu-card-body p { font-size: 13px; color: #78716C; }
  .price { font-weight: 700; color: #C2410C; margin-top: 8px; font-size: 15px; }
  .reviews-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 32px; }
  .review-card { background: rgba(255,255,255,0.08); border-radius: 10px; padding: 20px; }
  .stars { color: #F59E0B; font-size: 14px; margin-bottom: 8px; }
  .review-text { font-size: 14px; color: rgba(255,255,255,0.8); font-style: italic; }
  .review-author { font-size: 12px; color: rgba(255,255,255,0.5); margin-top: 10px; }
  .contact-section { background: #C2410C; color: white; text-align: center; padding: 64px 40px; }
  .contact-section h2 { font-family: 'Playfair Display', serif; font-size: 40px; margin-bottom: 12px; }
  .contact-section p { font-size: 16px; opacity: 0.85; margin-bottom: 32px; }
  .btn-white { background: white; color: #C2410C; padding: 14px 36px; border-radius: 8px; font-weight: 700; font-size: 15px; border: none; cursor: pointer; text-decoration: none; display: inline-block; margin: 0 6px; }
  .btn-outline-white { border: 2px solid white; color: white; padding: 12px 28px; border-radius: 8px; font-weight: 600; font-size: 15px; text-decoration: none; display: inline-block; margin: 0 6px; }
  .rating-badge { display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.12); padding: 8px 16px; border-radius: 100px; font-size: 13px; margin-bottom: 24px; }
  footer { background: #0D0A08; color: rgba(255,255,255,0.4); text-align: center; padding: 24px; font-size: 12px; }
  @media (max-width: 640px) {
    .hero h1 { font-size: 32px; }
    .menu-grid { grid-template-columns: 1fr; }
    .reviews-grid { grid-template-columns: 1fr; }
    .section { padding: 40px 24px; }
    .btn-secondary { display: none; }
  }
`

const DEMO_SITE_HTML = `
<section class="hero">
  <div class="hero-bg"></div>
  <div class="hero-content">
    <div class="rating-badge">⭐ 4.8 · 412 reseñas en Google</div>
    <h1>La mejor parrilla<br/>de Palermo</h1>
    <p>15 años de tradición, fuego y sabor argentino en el corazón del barrio</p>
    <a href="#reservar" class="btn-primary">Reservar mesa</a>
    <a href="#menu" class="btn-secondary">Ver carta</a>
  </div>
</section>

<section class="section section-light" id="menu">
  <div class="container">
    <div class="section-label">La carta</div>
    <h2 class="section-title">Nuestros cortes estrella</h2>
    <p style="color:#78716C; max-width:540px">Trabajamos con proveedores seleccionados de carne Aberdeen Angus. Cada corte preparado al punto exacto.</p>
    <div class="menu-grid">
      <div class="menu-card">
        <div class="menu-img">FOTO: Entraña a las brasas</div>
        <div class="menu-card-body">
          <h3>Entraña a las brasas</h3>
          <p>Corte tierno, jugoso, cocinado a fuego lento durante 25 minutos</p>
          <div class="price">$4,200</div>
        </div>
      </div>
      <div class="menu-card">
        <div class="menu-img">FOTO: Tira de asado</div>
        <div class="menu-card-body">
          <h3>Tira de asado</h3>
          <p>Cocción lenta 3 horas. La favorita de los domingos en familia</p>
          <div class="price">$3,800</div>
        </div>
      </div>
      <div class="menu-card">
        <div class="menu-img">FOTO: Empanadas caseras</div>
        <div class="menu-card-body">
          <h3>Empanadas caseras</h3>
          <p>Receta de la abuela Juan. Masa artesanal, relleno jugoso. Docena por pedido.</p>
          <div class="price">$2,400 / docena</div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-dark">
  <div class="container">
    <div class="section-label" style="color:#D97706">Qué dicen nuestros clientes</div>
    <h2 class="section-title" style="color:white">4.8 ★ en Google — 412 reseñas</h2>
    <div class="reviews-grid">
      <div class="review-card">
        <div class="stars">★★★★★</div>
        <div class="review-text">"La mejor entraña de Buenos Aires. Vine con mi familia el domingo y todos quedamos encantados. El servicio excelente."</div>
        <div class="review-author">— María González · hace 2 semanas</div>
      </div>
      <div class="review-card">
        <div class="stars">★★★★★</div>
        <div class="review-text">"15 años viniendo y nunca me decepciona. La tira de asado es perfecta. Que sigan así."</div>
        <div class="review-author">— Roberto Acosta · hace 1 mes</div>
      </div>
      <div class="review-card">
        <div class="stars">★★★★★</div>
        <div class="review-text">"Pedimos las empanadas para llevar y eran increíbles. El lugar tiene mucha onda, ya reservamos para el próximo finde."</div>
        <div class="review-author">— Paula Ríos · hace 3 semanas</div>
      </div>
    </div>
  </div>
</section>

<section class="contact-section" id="reservar">
  <h2>¿Reservás para esta semana?</h2>
  <p>Mesas disponibles de lunes a domingo, 12:00 a 15:30 y 20:00 a 23:30</p>
  <div>
    <a href="https://wa.me/5491100000000" class="btn-white">💬 WhatsApp</a>
    <a href="tel:+5491100000000" class="btn-outline-white">📞 Llamar</a>
  </div>
</section>

<footer>
  La Parrilla de Juan · Palermo, Buenos Aires · laparrillajuan.com.ar · Generado por Folio AI
</footer>
`
