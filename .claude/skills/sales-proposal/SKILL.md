---
name: sales-proposal
model: sonnet
description: Genera una propuesta comercial profesional para un lead, combinando el diseño de Stitch, el roadmap estimado y los datos del negocio. Produce un mensaje listo para enviar al cliente. Úsala cuando el usuario quiera armar una propuesta, mensaje de venta, pitch comercial o presentación para un lead.
---

# Generador de propuestas comerciales

Esta skill genera un mensaje de propuesta comercial profesional, combinando tres fuentes de datos del lead:

1. **Diseño de Stitch** (`stitch_designs/<lead>/`) — qué se diseñó, cuántas pantallas, estilo visual
2. **Roadmap** (`roadmaps/<lead>/`) — tiempos, equipo, fases, horas estimadas
3. **Datos del negocio** (`leads/`) — tipo de negocio, reseñas, dirección, rating, horarios

## Cuándo usarla

- "Armame una propuesta para este lead"
- "Generá un mensaje de venta para Fernando Bliman"
- "Haceme un pitch comercial con lo que ya tenemos"
- "Quiero mandarle una propuesta al cliente"

## Workflow

1. **Listar leads disponibles** — buscar carpetas en `<repo_root>/stitch_designs/` que también tengan carpeta en `<repo_root>/roadmaps/` (es decir, leads que ya tienen diseño Y roadmap). Mostrar la lista al usuario.

2. **El usuario elige un lead** — o lo indica directamente si ya lo mencionó.

3. **Preguntar idioma** — preguntar al usuario en qué idioma quiere la propuesta. Detectar el idioma por defecto según la ubicación del lead:
   - Buscar en `leads/` el archivo `leads_data.json` que contenga el lead (por `displayName`)
   - Usar el campo `postalAddress.regionCode` o `formattedAddress` para inferir el país
   - Si el país es hispanohablante → **español** por defecto
   - Si el país es Brasil → **portugués** por defecto
   - Si no se puede determinar o es otro país → **inglés** por defecto
   - Mostrar el idioma sugerido y preguntar: "¿Te parece bien en [idioma] o preferís otro?"

4. **Recolectar contexto** — leer los tres archivos del lead:

   a. **Stitch** — `stitch_designs/<lead-slug>/stitch_project.json`:
      - `leadName` — nombre del negocio
      - `projectType` — tipo de proyecto (single_page, multi_page, app)
      - `screens[]` — pantallas diseñadas (nombres y cantidad)
      - `designSystem` — colores, tipografía, estilo

   b. **Roadmap** — `roadmaps/<lead-slug>/*.md` (si hay varios, usar el del proyecto principal, no features):
      - Fecha de inicio y fin
      - Duración en días laborales
      - Horas totales
      - Fases y sus duraciones
      - Equipo asignado

   c. **Lead data** — buscar en `leads/*/leads_data.json` la entrada con el `displayName` que matchee:
      - `primaryTypeDisplayName` — tipo de negocio
      - `rating` + `userRatingCount` — reputación
      - `reviews[]` — qué dicen los clientes (para entender el negocio)
      - `regularOpeningHours` — horarios
      - `formattedAddress` — ubicación
      - `internationalPhoneNumber` — contacto
      - `websiteUri` — si tiene o no web actual

5. **Generar la propuesta** — redactar un mensaje profesional en el idioma elegido. El tono debe ser:
   - **Profesional pero cercano** — no corporativo frío, sino consultivo
   - **Orientado al valor** — no vender tecnología, vender resultados para el negocio
   - **Específico** — mencionar datos reales del negocio, no genéricos
   - **Conciso** — que se pueda leer en 2-3 minutos

   ### Estructura de la propuesta

   **Asunto / Encabezado**
   - Línea de asunto atractiva y específica al negocio

   **Apertura (2-3 líneas)**
   - Presentación breve de quiénes somos (estudio de desarrollo digital)
   - Referencia específica al negocio del lead (tipo, ubicación, reputación)

   **Situación actual (2-3 líneas)**
   - Observación sobre su presencia digital actual (tiene web / no tiene web)
   - Oportunidad que están dejando pasar

   **Nuestra propuesta (cuerpo principal)**
   - Qué diseñamos: descripción del sitio/app con las pantallas (sin jerga técnica)
   - Cómo se ve: mencionar el estilo visual (colores, tono, sensación)
   - Qué incluye: listar las secciones/páginas en lenguaje del cliente

   **Plan de ejecución (resumen del roadmap)**
   - Duración total (en semanas, no días laborales)
   - Fases principales con tiempos simples
   - Equipo dedicado (cantidad de personas, no nombres internos)
   - NO incluir horas detalladas ni breakdown técnico

   **Cierre**
   - Invitación a una reunión/llamada
   - Datos de contacto nuestros
   - Tono de disponibilidad y entusiasmo

   ### Qué NO incluir en la propuesta
   - Precios (se discuten en la reunión)
   - Nombres del equipo interno
   - Jerga técnica (frameworks, seniority, sprints, deployment)
   - Horas desglosadas por tarea
   - Detalles de arquitectura o stack

6. **Guardar la propuesta** — escribir el archivo en:
   ```
   <repo_root>/proposals/<lead-slug>/propuesta.txt
   ```
   Usar el **mismo nombre de carpeta** que en `stitch_designs/` y `roadmaps/`.

   Si el idioma no es español, ajustar el nombre del archivo:
   - Español → `propuesta.txt`
   - Inglés → `proposal.txt`
   - Portugués → `proposta.txt`

7. **Mostrar la propuesta** al usuario — pegar el contenido completo para que pueda revisarlo y pedir ajustes antes de enviarlo.
