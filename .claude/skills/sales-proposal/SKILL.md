---
name: sales-proposal
model: sonnet
description: Generates a professional business proposal for a lead by combining the Stitch design, estimated roadmap, and business data. Produces a ready-to-send message to the client. Use when the user wants to create a proposal, sales pitch, or commercial presentation for a lead.
---

# Commercial proposal generator

This skill generates a professional business proposal message by combining three data sources for the lead:

1. **Stitch design** (`stitch_designs/<lead>/`) — what was designed, how many screens, visual style
2. **Roadmap** (`roadmaps/<lead>/`) — timelines, team, phases, estimated hours
3. **Business data** (`leads/`) — business type, reviews, address, rating, hours

## When to use

- "Create a proposal for this lead"
- "Generate a sales message for Fernando Bliman"
- "Put together a pitch with what we have"
- "I want to send the client a proposal"

## Workflow

1. **List available leads** — find folders in `<repo_root>/stitch_designs/` that also have a folder in `<repo_root>/roadmaps/` (i.e., leads that have both a design AND a roadmap). Show the list to the user.

2. **User picks a lead** — or specifies one directly if already mentioned.

3. **Ask for language** — ask the user what language they want the proposal in. Auto-detect the default language from the lead's location:
   - Search in `leads/` for the `leads_data.json` file containing the lead (by `displayName`)
   - Use the `postalAddress.regionCode` or `formattedAddress` field to infer the country
   - If the country is Spanish-speaking → **Spanish** by default
   - If the country is Brazil → **Portuguese** by default
   - If it can't be determined or is another country → **English** by default
   - Show the suggested language and ask: "Does [language] work for you, or would you prefer another?"

4. **Gather context** — read the three files for the lead:

   a. **Stitch** — `stitch_designs/<lead-slug>/stitch_project.json`:
      - `leadName` — business name
      - `projectType` — project type (single_page, multi_page, app)
      - `screens[]` — designed screens (names and count)
      - `designSystem` — colors, typography, style

   b. **Roadmap** — `roadmaps/<lead-slug>/*.md` (if there are several, use the main project one, not features):
      - Start and end dates
      - Duration in working days
      - Total hours
      - Phases and their durations
      - Assigned team

   c. **Lead data** — search in `leads/*/leads_data.json` for the entry with a matching `displayName`:
      - `primaryTypeDisplayName` — business type
      - `rating` + `userRatingCount` — reputation
      - `reviews[]` — what clients say (to understand the business)
      - `regularOpeningHours` — schedule
      - `formattedAddress` — location
      - `internationalPhoneNumber` — contact
      - `websiteUri` — whether they currently have a website or not

5. **Generate the proposal** — write a professional message in the chosen language. The tone should be:
   - **Professional but approachable** — consultive, not cold corporate
   - **Value-oriented** — sell results for the business, not technology
   - **Specific** — mention real data about the business, not generic
   - **Concise** — readable in 2-3 minutes

   ### Proposal structure

   **Subject / Header**
   - Catchy subject line specific to the business

   **Opening (2-3 lines)**
   - Brief introduction of who we are (digital development studio)
   - Specific reference to the lead's business (type, location, reputation)

   **Current situation (2-3 lines)**
   - Observation about their current digital presence (has website / no website)
   - Opportunity they're missing

   **Our proposal (main body)**
   - What we designed: description of the site/app with screens (no technical jargon)
   - How it looks: mention the visual style (colors, tone, feel)
   - What's included: list the sections/pages in the client's language

   **Execution plan (roadmap summary)**
   - Total duration (in weeks, not working days)
   - Main phases with simple timelines
   - Dedicated team (number of people, not internal names)
   - DO NOT include detailed hours or technical breakdown

   **Closing**
   - Invitation to a meeting/call
   - Our contact details
   - Tone of availability and enthusiasm

   ### What NOT to include in the proposal
   - Prices (discussed in the meeting)
   - Internal team member names
   - Technical jargon (frameworks, seniority, sprints, deployment)
   - Hours broken down by task
   - Architecture or stack details

6. **Save the proposal** — write the file to:
   ```
   <repo_root>/proposals/<lead-slug>/proposal.txt
   ```
   Use the **same folder name** as in `stitch_designs/` and `roadmaps/`.

   Adjust the filename based on language:
   - Spanish → `propuesta.txt`
   - English → `proposal.txt`
   - Portuguese → `proposta.txt`

7. **Show the proposal** to the user — paste the full content so they can review and request adjustments before sending.
