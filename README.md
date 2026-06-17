# Brendan / SmileBCS - Project Notes

Shared workspace for notes, task lists, and reference material across all active projects.
Combines all Freelancer threads and work history.

---

## Kira - AI Voice Receptionist (smilecreative.agency/kira/)

**For**: Smile Creative / Brendan
**Live demo**: http://smilecreative.agency/kira/

### What It Does
- AI-powered virtual receptionist answering inbound business calls
- Northern Irish receptionist persona
- Captures caller info and routes messages to staff
- 24/7 availability including evenings, weekends, holidays
- Trained on each client's business services, team details, and FAQs
- Screens out telemarketers and irrelevant sales calls

### Technical Build
- Voice agent prompt written and refined for Kira persona
- SIP/VoIP integration investigated with Soho66 and Retell AI
- US phone number set up through Retell for inbound calls
- Backend API endpoint (kira-api.php) creating Retell web calls server-side
- Custom call widget built with Retell Web SDK (zero Retell branding)
- Kira's face avatar integrated into widget
- Transparent Smile Creative logo added
- Kira_03 hero image as landing page background
- Sales-oriented landing page with features, how-it-works, and CTA sections

### Twilio Elastic SIP Trunking (Completed 28 May 2026)
- UK phone number acquired via Twilio: +44 333 344 3344
- Elastic SIP Trunk created (TKb4309ade7ec0af8221d44a8e7a5b64b9, Ireland IE1 region)
- Origination URI: sip:sip.retellai.com (routes inbound calls to Retell)
- Termination URI: kira-smilecreative.pstn.twilio.com (allows Retell outbound via Twilio)
- IP ACL configured with Retell IP range (18.98.16.120/30)
- Number registered in Retell as SIP trunk number, assigned to Kira agent
- Calls to +443333443344 now answered by Kira via Retell
- Key fix: phone number region had to match trunk region (both Ireland IE1) - US1 mismatch caused calls to hit default Twilio webhook instead of trunk

### Pending - Kira
- Soho66 forwarding: main number (+442890993525) needs call forwarding rule to +443333443344 so customers calling the normal line get Kira
- Time awareness: Kira's prompt references business hours but agent has no time check - needs custom tool calling timeapi.io/api/time/current/zone?timeZone=Europe/London to determine UK time before greeting
- Call transfer: enable Kira to transfer calls to Brendan/DC live via Soho66 when caller requests a real person
- Natural call endings: end_call tool fires abruptly - prompt needs refinement for warmer wind-down

---

## Accountant Quiz AI (accountantbelfast.co.uk)

**For**: Brendan
**Source**: https://github.com/anirudhatalmale6-alt/accountant-quiz-ai

### Completed
- Custom WordPress plugin (Accountant Quiz AI) replacing n8n workflow entirely
- Plugin installed and activated on accountantbelfast.co.uk
- 11 quiz questions mapped with correct scoring (Q1-Q9 scored 1-4, Q10-Q11 unscored)
- Contact fields captured from QSM form (first name, surname, phone, email)
- AI analysis generates 4-paragraph report format (same as original n8n setup)
- Results display inline on quiz page after submission with animated score bar
- ResponsiveVoice text-to-speech integration
- All submissions logged to database (viewable in Settings > Quiz AI in WP admin)

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
- "Our Services" label set to white, "How it Works" section removed
- Studio Standard section moved below service cards, all section margins halved
- Whole cards clickable, "More" buttons centred, testimonials removed
- Nav links updated: Gallery and Prints pages linked from homepage nav + footer

### May 27-28 Updates (19-task edit list from DC & Bev)
- Homepage: hero title restyled, teal tagline added, Studio Standard rewritten with prints content, "View Gallery" button added, phone numbers separated, footer updated with full address
- Gallery: filter buttons removed, "Our Work" label removed, spacing reduced, "Visit the Studio" + map section added after CTA
- Prints: "Our Print Studio" section removed (moved to homepage), feature cards restyled to coloured blocks matching homepage, "Find Us" + map section added
- All pages: Services dropdown menu added to header nav (12 service categories), consistent link styling across pages (.location-detail-inner class), hamburger menu desktop display bug fixed on gallery page
- Service Content Questionnaire: 25-page Word document (GIF-Service-Content-Questions.docx) with 5 questions per service for all 12 categories, delivered to DC & Bev to generate 500-800 words per service page

### Pending
- Content from DC & Bev: answers to service questionnaire + one strong image per service
- Remaining 11 service pages (copy needed from client for each)
- WordPress conversion (agreed direction - build in static HTML first, convert to WP theme once content finalised)
- Gallery: real images from DC & Bev to replace stock, next/prev navigation (will come with WP gallery plugin)

### Future - Online Shop
- DC has expressed interest in adding an online shop to Get It Framed
- Reference site: lauraflynn.co.uk (Wix-based art/print shop - prints, canvas, framed work, merchandise)
- Will be built on WordPress/WooCommerce to keep everything on one platform
- On hold until current site content and service pages are finalised

### Design Notes
- Fonts: Libre Baskerville (headings) + Inter (body)
- Colours: --teal #048A81, --rose #B5838D, --ink-deep #454851, --paper-bg #F1F2F6
- Service page template: hero banner (200px), two-column intro, feature cards with images, CTA, footer

---

## He Hath Done - CD-to-Testimony Pipeline

**For**: Brendan
**Source**: https://github.com/anirudhatalmale6-alt/smilebcs-project-notes/blob/master/cd_to_testimony.py
**Website**: hehathdone.org

### What It Does
- Batch processes ripped CD testimonies (84 CDs, one per speaker)
- Merges multi-track CD folders into single MP3 per speaker
- Transcribes audio using local Whisper model (medium, CPU)
- Generates cinematic title, hook (250 chars), and tags via GPT-4o
- Outputs: merged audio, transcripts, metadata files with title/hook/tags
- Skips already-processed files (resume-safe)

### Setup
- Runs on Brendan's Windows PC (HP-HighSpec)
- Python 3.14, FFmpeg 16.1.0 (essentials build)
- Input: G:\HeHathDone\RippedCDs (84 speaker subfolders)
- Output: G:\HeHathDone\FirstPassAI
- OpenAI API key configured locally (not in repo)

### Related - TranscriptionService Web App
- GitHub: github.com/BenniFX/TranscriptionService
- FastAPI + React + MongoDB web app for ongoing YouTube/audio transcription
- Has user auth, YouTube extraction (yt-dlp), cloud Whisper API, export to PDF/DOCX/TXT
- Missing: title/hook/tags AI generation (to be merged from CD pipeline later)
- Plan: CD script for backlog, then enhance web app with AI metadata for ongoing use

### Status (28 May 2026)
- Script running, merge phase complete, transcription in progress
- All dependencies installed (openai-whisper, pydub, openai, audioop-lts)

### Report an Issue Form (June 2026)
- Standalone PHP form at hehathdone.org/report-issue.php
- Issue type dropdown, page/testimony field, details textarea, optional name/email
- Honeypot spam protection, PHP mail() to brendan@keygrowth.co.uk
- Styled to match HHD dark/gold theme (no WordPress dependency)
- Footer link added in theme footer.php

---

## Paul McKay Building & Plastering (paulmckaybuildingandplastering.co.uk)

**For**: Client via Brendan (CastleHost DNS)

### Google Search Console & SEO Fix (June 2026)
- Fixed domain verification: TXT record had full domain name in Name field instead of "@"
- Discovered sitewide "Discourage search engines from indexing this site" was checked in WordPress Settings > Reading
- This was blocking ALL pages from Google indexing (noindex meta tag on every page)
- Unchecked the setting, submitted sitemap and individual pages for indexing
- Wrote client-facing explanation of the issue and resolution

---

## ContactLocal (contactlocal.co.uk)

### Cards Live
- **DC (Darren Cumberland)**: dc.contactlocal.co.uk - Call Studio (028 2588 2706), Call Mobile (077 6384 2761), Email (obfuscated via JS), Studio accordion, QR code toggle
- **Kerry's Florist**: kerry.contactlocal.co.uk - reference card for accordion pattern
- **Pendyprints (Sarah Pendleton-Sharp)**: contactlocal.co.uk/pendyprints/ - Floral artist, Portglenone. Hero painting with name/tagline overlay, services section, WhatsApp (07888 733389), Email, Facebook, Instagram buttons, Save Contact vCard, QR code toggle. Purple/plum theme (Playfair Display + Inter). Added June 2026

### Platform
- Template 01 uploaded to /templates/01/, embedded as live iframe in hero
- ContactLocal-Card-Spec-v1.docx delivered (10-section SOP)
- Brendan's avatar embedded in About section

### Future Plans
- Sign-up form, GA4 analytics, redirect QR codes, automation/scaling
- Pricing model: one-off 35 GBP vs recurring monthly

---

## BNI Payment Gateway (payment.bninorthernireland.co.uk)

**For**: Andrew / BNI Northern Ireland

### Malware Cleanup (Completed)
- 3 spam posts, 4 rogue accounts, Russian spam category removed
- Backdoor plugin (init-help) removed
- WP File Manager plugin deleted (was the attack vector)
- wp-file-manager-pro uploads cleaned
- Security salts regenerated
- .htaccess hardened (XML-RPC blocked, PHP in uploads blocked, directory browsing off)
- Wordfence installed and configured
- SMTP configured (WP Mail SMTP via cloud.hostnx.uk)
- DMARC record added for bninorthernireland.co.uk
- Forminator form email notifications set up (admin to Andrew + Brendan, receipt to submitter)

### Reputation Recovery (Ongoing)
- pcrisk: Trust Score 35/100, 3 of 92 threat engines still flagging
- Category label: "Phishing And Other Frauds" (legacy from compromise)
- Action needed: Identify the 3 specific flagging engines and submit false positive disputes
- Client couldn't find dispute submission forms - needs help locating them

---

## Eternitywhere.com Migration

**For**: Andrew Dobbin

### Completed
- Full site migration from StackCP (20i/Omega SYS, shutting down) to DirectAdmin (KeyGrowth server)
- WordPress files, database, themes, plugins all migrated
- PHP 5.6 configured for old WordPress install
- Email account created (andrew@eternitywhere.com) with 10GB quota
- Email forwarders set up (andrew, gail, stephen)
- SSL certificate issued via Let's Encrypt
- DNS records updated at StackCP to point to new server

### AWStats Export (Pending)
- Goal: Export monthly AWStats reports from StackCP (Jan 2020 to present, ~77 months)
- Issue: StackCP URLs don't carry month parameter (session-based)
- Next step: Browser console script to automate save-to-PDF from within AWStats page

---

## Logan's Removals (logansremovals.co.uk)

**For**: Logan's Removals (via Brendan)

### Completed - Volume Calculator & Quote System
- Full item list integrated across 7 rooms: Living Room (55), Dining Room (10), Kitchen (16), Bedrooms (25), Office/Study (17), Garage & Garden (42), Cartons & Misc (5)
- Vehicle suggestions based on cubic volume: Small Van, Transit Van, Luton Van, 7.5t Truck, 14t Truck, Two vehicles
- AJAX email submission to logansremovals@hotmail.co.uk with formatted HTML (item breakdown, contact details, move details, volumes)
- WP admin panel: Logan's Quotes page showing all submissions in table with "View Details"
- Validation: UK postcode, required fields, email format, minimum 1 item
- 10 additional services: full/partial packing, unpacking, dismantling, short/long-term storage, insurance upgrade, specialist items, office moves, cross-channel
- Code in two WP Code Snippets: Snippet 7 (front-end shortcode), Snippet 8 (AJAX handler, email, admin page)

---

## TheBusinessMindset.co.uk

**For**: Brendan

### Completed
- 19 plugin updates + 2 theme updates
- Mailchimp domain authentication (duplicate DMARC removed)

---

## Hope2Families.com

**For**: Client on Brendan's server

- Verified site exists on DirectAdmin server with full WordPress install
- cPanel backup restore attempted from Certa hosting

---

## LeadsToGrowth.co.uk

**For**: Brendan

### Completed
- Removed .maintenance file (cPanel WordPress Toolkit leftover) to bring site live
- Deleted v2 folder (149MB duplicate WordPress install)
- Cleaned up cPanel maintenance template files
- Deleted orphaned database (leadstogrowth_w589)

---

## MySiteHost Server Audit (91.238.160.248)

**For**: Brendan

### Completed
- Full audit of 47 cPanel accounts
- Identified 21 to keep, 26 to delete
- Identified 3 accounts still pointing to server with live sites
- Identified email delivery interception issues (keygrowth.co.uk and smileprinting.co.uk)

---

## Dougans Furniture (dougansfurniture.com)

- Site down (HTTP 500), 123-reg hosting, domain expires June 28 2026
- Brendan contacted Jenna - they have someone on it
- Not pushing further. Seed planted.

---

## Hosting & Access

| Service | Details |
|---------|---------|
| Get It Framed preview | FTP: framing@newdevsite.co.uk |
| ContactLocal main | FTP: anirudhat@contactlocal.co.uk |
| DC subdomain | FTP: DC@contactlocal.co.uk (docroot: /public_html/) |
| DirectAdmin hosting | AWStats enabled, account "kgrowth" |
| MySiteHost server | 91.238.160.248 (47 cPanel accounts audited) |
| StackCP | Eternitywhere stats access (pre-migration) |

---

## The Frame Gallery - Demo Framing Shop

**URL**: https://leadsites.co.uk/gallery/shop/
**Platform**: WordPress + WooCommerce + Astra (child theme: frame-gallery-child)
**Server**: 185.109.170.140 (CastleHost DirectAdmin, LiteSpeed)

### Design
- Teal (#048A81) / Rose (#B5838D) colour palette
- Libre Baskerville (headings) + Inter (body) fonts
- "Cousin of Get It Framed NI" style per Brendan's request
- White header, teal social icons, dark footer
- Card-style product grid with hover effects

### Products (6 demo products, 5 categories)
- Coastal Sunrise - Framed Print (variable: 4 sizes x 4 frames = 16 variations)
- Forest Canopy - Canvas Wrap (variable: 5 sizes)
- Mountain Peak - Premium Framed (variable: 3 sizes x 3 frames x 3 glass = 16 variations)
- Abstract Flow - Mounted Print (variable: 4 sizes)
- Custom Frame Package (simple: £149)
- Photo Slate Gift (variable: 3 sizes)

### Categories
- Framed Prints (120), Canvas Prints (121), Custom Framing (122), Mounting & Display (123), Photo Gifts (124)

### Technical
- Child theme CSS hosted on GitHub, deployed via install-theme.php
- WC API keys: ck_EBSdG... / cs_iVGEX...
- Currency: GBP
- Elementor header overridden via CSS (title, background, social icons)

### Status
- COMPLETE: Theme, products, images, variations, categories, CSS styling
- Note: install-theme.php and setup-wc-keys.php still on server (should be removed)

---

## Communication
- Primary: Freelancer.com messaging
- Reference: This GitHub page
- No email/phone available from developer side

---

*Last updated: 17 June 2026*
