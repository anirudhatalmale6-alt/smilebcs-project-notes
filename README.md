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

### Pending
- 5 replacement photos for service cards: Prints, Canvas, Photographer Services, Storybook Albums, Commercial Printing
- Remaining 11 service pages (copy needed from client for each)
- WordPress conversion (agreed direction - build in static HTML first, convert to WP theme once content finalised)
- Gallery: next/prev navigation in lightbox (will come with WP gallery plugin)

### Design Notes
- Fonts: Libre Baskerville (headings) + Inter (body)
- Colours: --teal #048A81, --rose #B5838D, --ink-deep #454851, --paper-bg #F1F2F6
- Service page template: hero banner (200px), two-column intro, feature cards with images, CTA, footer

---

## ContactLocal (contactlocal.co.uk)

### Cards Live
- **DC (Darren Cumberland)**: dc.contactlocal.co.uk - Call Studio (028 2588 2706), Call Mobile (077 6384 2761), Email (obfuscated via JS), Studio accordion
- **Kerry's Florist**: kerry.contactlocal.co.uk - reference card for accordion pattern

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

## Communication
- Primary: Freelancer.com messaging
- Reference: This GitHub page
- No email/phone available from developer side

---

*Last updated: 23 May 2026*
