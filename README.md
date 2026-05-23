# Brendan / SmileBCS - Project Notes

Shared workspace for notes, task lists, and reference material across all active projects.
Combines both Freelancer threads (ContactLocal/Get It Framed + WordPress Malware Audit & Cleanup).

---

## Get It Framed NI (newdevsite.co.uk/framing/)

**Client**: Darren Cumberland (also runs MusicDC Group, photography, sound & light)
**Live preview**: https://newdevsite.co.uk/framing/

### Completed
- Homepage built with all May 12th updates applied (12 service cards, new hero copy, header changes)
- Prints service page live at /framing/prints.html (magazine-style layout, approved by client)
- Gallery page live at /framing/gallery.html (grid layout, filter buttons, lightbox)
- CTA section moved to full-width teal band above Find Us/map section
- Card titles: sentence case, centred, descriptions centred
- "Our Services" label set to white
- "How it Works" section removed
- Studio Standard section moved below service cards
- All section margins halved
- Whole cards clickable, "More" buttons centred
- Testimonials section removed
- Nav links updated: Gallery and Prints pages linked from homepage nav + footer

### Pending
- 5 replacement photos for service cards: Prints, Canvas, Photographer Services, Storybook Albums, Commercial Printing
- Remaining 11 service pages (copy needed from client for each)
- WordPress conversion (agreed direction - build in static HTML first, convert to WP theme once content finalised)
- Gallery: next/prev navigation in lightbox (will come with WP gallery plugin)
- May 12th update review - client said "not all edits implemented", needs follow-up check

### Design Notes
- Fonts: Libre Baskerville (headings) + Inter (body)
- Colours: --teal #048A81, --rose #B5838D, --ink-deep #454851, --paper-bg #F1F2F6
- Service page template: hero banner (200px), two-column intro, feature cards with images, CTA, footer
- Base64 logo embedded in HTML (large file ~44KB)

---

## ContactLocal (contactlocal.co.uk)

### Cards Live
- **DC (Darren Cumberland)**: dc.contactlocal.co.uk - Call Studio (028 2588 2706), Call Mobile (077 6384 2761), Email (obfuscated via JS), Studio address (accordion with "Get directions")
- **Kerry's Florist**: kerry.contactlocal.co.uk - reference card for accordion pattern

### Platform
- Template 01 uploaded to /templates/01/, embedded as live iframe in hero section on main page
- ContactLocal-Card-Spec-v1.docx delivered (10-section SOP for future builds)
- Brendan's avatar embedded in About section (Smile_Creative_Office.jfif)

### Future Plans
- Sign-up form (self-service at the 35 GBP price point)
- Analytics: GA4 on each card, redirect QR codes for scan tracking, AWStats enabled in DirectAdmin
- Automation/scaling: template engine + database to generate cards automatically
- Pricing model evolution: one-off 35 GBP vs recurring monthly (e.g. 5 GBP/month)

---

## BNI Payment Portal (payment.bninorthernireland.co.uk)

- **Background**: WordPress site previously compromised (malware), cleanup done
- **Reputation**: pcrisk scan shows Trust Score 35/100, 3 of 92 threat engines flagging
- **Category label**: "Phishing And Other Frauds" (legacy from compromise period)
- **Action needed**: Identify the 3 specific flagging engines and submit false positive disputes to each
- **Timeline**: Reputation databases take 2-6 weeks to update after dispute submission
- **Client couldn't find**: Dispute submission forms on the 3 flagging engines - needs help locating them

---

## Dougans Furniture (dougansfurniture.com)

- **Status**: Site down (HTTP 500 error), hosted on 123-reg shared hosting
- **Domain**: Registered since 2012, expires June 28 2026
- **Outreach**: Brendan contacted Jenna alongside a print job - she responded saying they have someone tasked to sort it
- **Decision**: Not pushing further. Seed planted, door open for future

---

## AWStats Export (Eternitywhere from StackCP)

- **Goal**: Export monthly AWStats reports from StackCP before migration (Jan 2020 to present, ~77 months)
- **Issue**: StackCP AWStats URLs don't carry month parameter - month selection is session/cookie based, so generated URLs all load the same page
- **AWStats helper page**: Delivered (awstats-export.html) but URLs won't work per-month
- **Next step**: Browser console script to automate save-to-PDF from within the AWStats page
- **DirectAdmin AWStats**: Now enabled for account "kgrowth" (confirmed by hosting support)

---

## Hosting & Access

| Service | Details |
|---------|---------|
| Get It Framed preview | FTP: framing@newdevsite.co.uk |
| ContactLocal main | FTP: anirudhat@contactlocal.co.uk |
| DC subdomain | FTP: DC@contactlocal.co.uk (docroot: /public_html/) |
| DirectAdmin hosting | AWStats enabled, account "kgrowth" |
| StackCP | Eternitywhere stats access (pre-migration) |

---

## Communication
- Primary: Freelancer.com messaging
- Reference: This GitHub page (https://github.com/anirudhatalmale6-alt/smilebcs-project-notes)
- No email/phone available from developer side

---

*Last updated: 23 May 2026*
