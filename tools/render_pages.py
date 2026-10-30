#!/usr/bin/env python3
import json
from build_site import (
    BASE, BBB_URL, CCB_URL, CITIES, COMPANY_SITE, EMAIL, ONECALL, PHONE_DISP, PHONE_TEL,
    QUOTE, SERVICES, SHIELD, BRIDGE, WAVES, crumbs_schema, esc, footer, form, header, head, hero_svg, icon,
    page, plumber_schema, rel, write, ROOT,
)
from posts_data import POSTS


def service_body(slug, name, summary, kind, depth=1):
    related = [s for s in SERVICES if s[0] != slug][:4]
    links = " ".join(
        f'<a href="{s[0]}.html">{esc(s[1])}</a>' for s in related
    )
    pills = "\n".join(f'<a class="pill" href="../{c[0]}.html">{esc(c[1])}</a>' for c in CITIES[:8])
    return f"""<main id="main">
  <section class="page-hero"><div class="wrap">
    <p class="crumbs"><a href="../index.html">Home</a> / Services / {esc(name)}</p>
    <p class="eyebrow">Service</p>
    <h1>{esc(name)}</h1>
    <p>{esc(summary)} Plumbing 101, LLC lists this work through its BBB profile, and the company site names water heater installation directly. The company serves Lincoln County and Tillamook County and answers {PHONE_DISP} on weekdays.</p>
    <p class="page-actions"><a class="btn btn-gold" href="../contact.html" data-open-estimate="Service: {esc(name)}">Request an estimate</a> <a class="btn btn-outline" href="tel:{PHONE_TEL}">Call {PHONE_DISP}</a></p>
  </div></section>
  <section class="section"><div class="wrap prose">
    <div class="card-art" style="height:160px;border-radius:16px;margin-bottom:18px">{icon(kind)}</div>
    <h2>What this service covers</h2>
    <p>The Better Business Bureau profile for Plumbing 101, LLC describes a residential and commercial plumbing contractor that does new construction and remodeling. The listed work includes bathroom and kitchen remodels, new piping and re-piping, drain, toilet, and faucet services and repairs, water heater installations, and pipe inspection and evaluation. This page is about {esc(name.lower())} inside that published list.</p>
    <p>The company does not publish a flat price. Coastal houses differ: some are on crawlspaces, some have additions, and some sit empty for weeks. An estimate starts with a description of the building and the symptom. Call during posted hours, Monday through Friday, 8:30 a.m. to 3:30 p.m., or email {EMAIL}.</p>
    <h2>What helps a visit go smoothly</h2>
    <ul>
      <li>Say whether one fixture is affected or the whole house.</li>
      <li>Say whether water is leaking, draining slowly, or missing.</li>
      <li>Know if the house is in Lincoln County or Tillamook County, and which town.</li>
      <li>If a water heater or outlet got wet, leave it off.</li>
      <li>Clear a path to the fixture, the crawlspace hatch, or the heater.</li>
    </ul>
    <h2>Hours and license</h2>
    <p>Hours on this site match the company website and the BBB profile: Monday through Friday, 8:30 a.m. to 3:30 p.m. Closed Saturday and Sunday. <a href="{CCB_URL}">Oregon CCB #232697, Active</a>. First licensed October 19, 2020.</p>
    <p>Related services: {links}</p>
    <div class="pills">{pills}</div>
  </div></section>
</main>"""


def city_body(slug, name, county, setting, housing, notes):
    others = [c for c in CITIES if c[0] != slug and c[2] == county][:6]
    pills = "\n".join(f'<a class="pill" href="{c[0]}.html">{esc(c[1])}</a>' for c in others)
    services = "\n".join(
        f'<li><a href="services/{s[0]}.html">{esc(s[1])}</a></li>' for s in SERVICES
    )
    return f"""<main id="main">
  <section class="page-hero"><div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> / <a href="service-areas.html">Service areas</a> / {esc(name)}</p>
    <p class="eyebrow">{esc(county)} County</p>
    <h1>Plumbing in {esc(name)}, Oregon</h1>
    <p>Plumbing 101, LLC states that it serves Lincoln County and Tillamook County. {esc(name)} is in {esc(county)} County. The company is based in Lincoln City and posts weekday hours of 8:30 a.m. to 3:30 p.m.</p>
  </div></section>
  <section class="section"><div class="wrap prose">
    <h2>The town</h2>
    <p>{esc(setting)}</p>
    <h2>Houses and buildings</h2>
    <p>{esc(housing)}</p>
    <h2>What to mention when you call</h2>
    <p>{esc(notes)}</p>
    <p>Call <a href="tel:{PHONE_TEL}">{PHONE_DISP}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>. This site does not publish a street address, because public sources do not agree on one. The visit is arranged by phone or email.</p>
    <h2>Services listed for the company</h2>
    <ul>{services}</ul>
    <h2>Nearby in {esc(county)} County</h2>
    <div class="pills">{pills}</div>
  </div></section>
</main>"""


def homepage():
    cards = "\n".join(
        f'''<article class="card reveal stagger-{(i % 4) + 1}"><div class="card-art">{icon(kind)}</div><div class="card-body"><h3>{esc(name)}</h3><p>{esc(blurb)}</p><a class="more" href="services/{slug}.html">Learn more <span aria-hidden="true">&rarr;</span></a></div></article>'''
        for i, (slug, name, blurb, kind) in enumerate(SERVICES)
    )
    pills = "\n".join(f'<a class="pill" href="{slug}.html">{esc(name)}</a>' for slug, name, *_ in CITIES)
    body = f"""<main id="main">
  <section class="hero">
    <div class="hero-sky">
      {BRIDGE}
      <div class="road-sign">
        <div class="sign-top">
          {SHIELD}
          <p class="sign-route">Highway 101</p>
        </div>
        <h1>Plumbing along the Oregon Coast</h1>
        <p class="town-line">Lincoln City, Depoe Bay, Newport, Waldport, Yachats, Tillamook, Pacific City, Neskowin.</p>
        <p class="hero-lead">Plumbing 101, LLC serves Lincoln County and Tillamook County from Lincoln City. Weekdays, 8:30 a.m. to 3:30 p.m.</p>
        <div class="hero-actions">
          <a class="btn btn-gold" href="tel:{PHONE_TEL}">Call {PHONE_DISP}</a>
          <a class="btn btn-outline-dark" href="contact.html" data-open-estimate="Hero">Request an estimate</a>
        </div>
      </div>
      {WAVES}
    </div>
  </section>
  <section class="trust-strip" aria-label="Business facts">
    <div class="wrap trust-row">
      <div class="trust-item"><a href="{CCB_URL}"><strong>Oregon CCB #232697, Active</strong></a></div>
      <div class="trust-item"><strong>BBB</strong> Accredited, A+</div>
      <div class="trust-item"><strong>Since 2020</strong> both counties</div>
      <div class="trust-item"><strong>Weekdays</strong> 8:30 a.m. to 3:30 p.m.</div>
      <div class="trust-item"><strong>Lincoln City</strong> Oregon</div>
    </div>
  </section>
  <section class="section">
    <div class="orb" aria-hidden="true"></div>
    <div class="wrap">
      <p class="eyebrow">Services</p>
      <h2>From Depoe Bay to Pacific City</h2>
      <p class="lede">These services come from the company website and its BBB profile. The company serves Lincoln County and Tillamook County. Call {PHONE_DISP}.</p>
      <div class="cards">{cards}</div>
    </div>
  </section>
  <section class="section why">
    <div class="wrap">
      <p class="eyebrow">Why call</p>
      <h2>Facts you can check</h2>
      <p class="lede">The useful details are public: a license number, a BBB profile, posted hours, and a phone that goes to the company.</p>
      <div class="reasons">
        <article class="reason reveal"><h3>Active CCB license</h3><p><a href="{CCB_URL}">Oregon CCB #232697, Active</a>. First licensed October 19, 2020.</p></article>
        <article class="reason reveal"><h3>BBB Accredited, A+</h3><p>The BBB profile shows accreditation since October 31, 2025 and an A+ rating. File opened November 3, 2025.</p></article>
        <article class="reason reveal"><h3>Two coastal counties</h3><p>The company website says it serves Lincoln County and Tillamook County. One Call Today lists the same territory.</p></article>
        <article class="reason reveal"><h3>Posted weekday hours</h3><p>Monday through Friday, 8:30 a.m. to 3:30 p.m. Saturday and Sunday are closed on the company site and the BBB profile.</p></article>
      </div>
    </div>
  </section>
  <section class="section reviews">
    <div class="wrap">
      <p class="eyebrow">From their website</p>
      <h2>A note they published</h2>
      <p class="lede">This is the testimonial printed on plumbing101llc.com. This site does not republish other reviews.</p>
      <div class="review-grid">
        <article class="review"><p>&ldquo;{esc(QUOTE)}&rdquo;</p><cite>Andrew Perry</cite><p class="source">Published on plumbing101llc.com</p></article>
      </div>
      <p><a href="reviews.html">Read the review page</a></p>
    </div>
  </section>
  <section class="section">
    <div class="wrap split">
      <div>
        <p class="eyebrow">About</p>
        <h2>Based in Lincoln City since 2020</h2>
        <p class="lede">Plumbing 101, LLC is an Oregon limited liability company. The BBB profile lists Faith A. Worthington as owner/manager and Michael E. Worthington as owner/member. The company tagline is &ldquo;Always at Your Service.&rdquo;</p>
        <div class="stats">
          <div class="stat"><strong>232697</strong><span>CCB license</span></div>
          <div class="stat"><strong>2020</strong><span>Serving the counties</span></div>
          <div class="stat"><strong>A+</strong><span>BBB rating</span></div>
        </div>
        <p><a class="btn btn-outline-dark" href="about.html">About the company</a></p>
      </div>
      <div class="panel">
        <h3>Talk to a person</h3>
        <p><a class="phone-link" href="tel:{PHONE_TEL}">{PHONE_DISP}</a></p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p>Monday to Friday, 8:30 a.m. to 3:30 p.m. Closed Saturday and Sunday.</p>
      </div>
    </div>
  </section>
  <section class="section" style="background:#fff">
    <div class="wrap">
      <p class="eyebrow">Highway 101</p>
      <h2>Lincoln County and Tillamook County</h2>
      <p class="lede">Town pages cover communities in the two counties the company says it serves, including Lincoln City, Newport, Waldport, Yachats, Tillamook, and Neskowin. Each page is a town in that area, not a separate shop.</p>
      <div class="pills">{pills}</div>
    </div>
  </section>
  <section class="cta-band">
    <h2>Call from Lincoln City to Tillamook</h2>
    <p>Phone the Lincoln City office, or send a note to the company email.</p>
    <p><a class="phone-link" href="tel:{PHONE_TEL}">{PHONE_DISP}</a></p>
    <p><a class="btn btn-white glow" href="contact.html" data-open-estimate="Home CTA">Request a free estimate</a> <a class="btn btn-outline" href="mailto:{EMAIL}">Email the office</a></p>
  </section>
</main>"""
    schema = plumber_schema()
    doc = head("Plumbing 101, LLC | Lincoln City plumber", "Plumbing 101, LLC serves Lincoln and Tillamook counties from Lincoln City. CCB #232697. Call (541) 614-1344, weekdays 8:30 a.m. to 3:30 p.m.", "index.html", 0, schema)
    return doc + header(0) + body + footer(0) + "</body></html>\n"


def core_pages():
    pages = {}
    pages["index.html"] = homepage()
    about = f"""<main id="main"><section class="page-hero"><div class="wrap">
      <p class="crumbs"><a href="index.html">Home</a> / About</p>
      <p class="eyebrow">About</p>
      <h1>Plumbing 101, LLC</h1>
      <p>A Lincoln City plumbing company serving Lincoln County and Tillamook County since 2020.</p>
    </div></section>
    <section class="section"><div class="wrap prose">
      <h2>What the company says</h2>
      <p>On plumbing101llc.com, Plumbing 101, LLC says it has served Lincoln County and Tillamook County since 2020. The site describes a priority on quality, efficiency, and professionalism, and it uses the line &ldquo;Always at Your Service.&rdquo; The about page on that site names water heater installation as a service. Weekday hours are listed as 8:30 a.m. to 3:30 p.m., with Saturday and Sunday closed.</p>
      <h2>People named on the BBB profile</h2>
      <p>The Better Business Bureau profile lists Faith A. Worthington as owner/manager and Michael E. Worthington as owner/member. It lists the business as a limited liability company, incorporated August 21, 2020, with a business start date of October 19, 2020. BBB accredited the business on October 31, 2025 and shows an A+ rating. The local bureau is BBB Great West and Pacific. The file was opened November 3, 2025.</p>
      <p>The same profile describes residential and commercial new construction and remodeling, including bathroom and kitchen work, new piping and re-piping, drain, toilet, and faucet service and repair, water heater installation, and pipe inspection and evaluation.</p>
      <h2>License</h2>
      <p><a href="{CCB_URL}">Oregon CCB #232697, Active</a>. First licensed October 19, 2020.</p>
      <h2>How to reach the company</h2>
      <p>Phone <a href="tel:{PHONE_TEL}">{PHONE_DISP}</a>. Email <a href="mailto:{EMAIL}">{EMAIL}</a>. The email address is printed on the company website. A street address is not printed here, because public listings disagree on the street direction and older registry mirrors list more than one past address.</p>
      <p>Existing website: <a href="{COMPANY_SITE}">plumbing101llc.com</a>. Directory listing: <a href="{ONECALL}">One Call Today</a>. BBB profile: <a href="{BBB_URL}">Plumbing 101 LLC</a>.</p>
    </div></section></main>"""
    pages["about.html"] = page(
        "About Plumbing 101, LLC",
        "Plumbing 101, LLC of Lincoln City. Owners listed on BBB, CCB license 232697, serving Lincoln and Tillamook counties since 2020.",
        "about.html", 0, about, crumbs_schema([("Home", "index.html"), ("About", "about.html")]),
    )
    contact = f"""<main id="main"><section class="page-hero"><div class="wrap">
      <p class="crumbs"><a href="index.html">Home</a> / Contact</p>
      <p class="eyebrow">Contact</p>
      <h1>Call or email</h1>
      <p>Estimates start with a phone call or an email. The form on this page opens your email app and addresses the message to the company.</p>
    </div></section>
    <section class="section"><div class="wrap split">
      <div class="prose">
        <h2>Phone and email</h2>
        <p><a class="phone-link" href="tel:{PHONE_TEL}">{PHONE_DISP}</a></p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <h2>Hours</h2>
        <p>Monday through Friday, 8:30 a.m. to 3:30 p.m. Saturday and Sunday, closed. These hours match plumbing101llc.com and the BBB profile. Some map listings show a 4:00 p.m. close. If you are unsure, call.</p>
        <h2>Where</h2>
        <p>Lincoln City, Oregon. The company states that it serves Lincoln County and Tillamook County. This site does not print a street address, because public listings do not agree on one. Call or email to arrange the visit.</p>
        <div class="panel diagram" aria-hidden="false">
          <svg viewBox="0 0 360 180" role="img" aria-label="Simple map of the north and central Oregon Coast labeling Lincoln County and Tillamook County">
            <rect width="360" height="180" fill="#E7F2F5"/>
            <path d="M70 10c20 20 10 40 18 60 10 24-8 30 4 52 8 16 6 28 16 48h40c-6-24 8-36 2-58-8-28 10-40-4-70-6-16-18-28-40-32z" fill="#0B7285"/>
            <text x="150" y="70" fill="#063E48" font-size="14" font-family="Outfit,sans-serif">Tillamook County</text>
            <text x="150" y="120" fill="#063E48" font-size="14" font-family="Outfit,sans-serif">Lincoln County</text>
            <text x="150" y="150" fill="#9A5A1A" font-size="13" font-family="Outfit,sans-serif">Based in Lincoln City</text>
          </svg>
          <p>Service area sketch, not a driving map and not a pin at a shop.</p>
        </div>
      </div>
      <div class="panel">
        <h2>Email an estimate request</h2>
        {form("Contact page")}
      </div>
    </div></section></main>"""
    pages["contact.html"] = page(
        "Contact Plumbing 101, LLC",
        "Call Plumbing 101, LLC at (541) 614-1344 or email office@plumbing101.net. Weekdays 8:30 a.m. to 3:30 p.m. Lincoln City, Oregon.",
        "contact.html", 0, contact, crumbs_schema([("Home", "index.html"), ("Contact", "contact.html")]),
    )
    reviews = f"""<main id="main"><section class="page-hero"><div class="wrap">
      <p class="crumbs"><a href="index.html">Home</a> / Reviews</p>
      <p class="eyebrow">Reviews</p>
      <h1>What is published here</h1>
      <p>One testimonial appears on the company website. It is quoted below. Other review counts on third-party pages do not match each other, so they are not repeated here.</p>
    </div></section>
    <section class="section reviews"><div class="wrap">
      <article class="review"><p>&ldquo;{esc(QUOTE)}&rdquo;</p><cite>Andrew Perry</cite><p class="source">Published on <a href="{COMPANY_SITE}">plumbing101llc.com</a>. The note describes a beach-home re-pipe.</p></article>
      <div class="prose" style="margin-top:22px">
        <h2>Where else to look</h2>
        <p>The company invites clients to share experiences on its own site. The BBB profile is public at <a href="{BBB_URL}">bbb.org</a>. The Oregon CCB record is public at <a href="{CCB_URL}">license 232697</a>. This site does not invent star totals.</p>
        <p><a class="btn btn-gold" href="contact.html" data-open-estimate="Reviews">Request an estimate</a></p>
      </div>
    </div></section></main>"""
    pages["reviews.html"] = page(
        "Reviews | Plumbing 101, LLC",
        "The testimonial Plumbing 101, LLC publishes on its website, plus links to the BBB profile and the Oregon CCB record.",
        "reviews.html", 0, reviews, crumbs_schema([("Home", "index.html"), ("Reviews", "reviews.html")]),
    )
    gallery = """<main id="main"><section class="page-hero"><div class="wrap">
      <p class="crumbs"><a href="index.html">Home</a> / Diagrams</p>
      <p class="eyebrow">Diagrams</p>
      <h1>Pictures of parts, not of jobs</h1>
      <p>These drawings explain common parts. They are not photographs of Plumbing 101 work.</p>
    </div></section>
    <section class="section"><div class="wrap city-grid">
      <figure class="diagram"><svg viewBox="0 0 320 200" role="img" aria-label="Diagram of a main water shutoff valve on a pipe"><rect width="320" height="200" fill="#F5F8FA"/><path d="M20 100h120" stroke="#0B7285" stroke-width="12"/><rect x="140" y="78" width="36" height="44" rx="4" fill="#E8913A"/><path d="M176 100h120" stroke="#0B7285" stroke-width="12"/><text x="20" y="40" fill="#063E48" font-size="16" font-family="Outfit,sans-serif">Main shutoff</text><text x="20" y="170" fill="#3E515B" font-size="13" font-family="Outfit,sans-serif">Often near the meter or where the line enters.</text></svg><figcaption>Diagram: a shutoff in a supply line. Find yours before a leak spreads.</figcaption></figure>
      <figure class="diagram"><svg viewBox="0 0 320 200" role="img" aria-label="Diagram of a P-trap under a sink"><rect width="320" height="200" fill="#F5F8FA"/><path d="M150 20 v50 c0 30-40 30-40 60 c0 24 40 24 40 24 h70" fill="none" stroke="#0B7285" stroke-width="10"/><text x="20" y="40" fill="#063E48" font-size="16" font-family="Outfit,sans-serif">P-trap</text><text x="20" y="180" fill="#3E515B" font-size="13" font-family="Outfit,sans-serif">The bend holds water so sewer gas stays in the pipe.</text></svg><figcaption>Diagram: a trap under a sink. A dry trap in an empty house smells like a sewer.</figcaption></figure>
      <figure class="diagram"><svg viewBox="0 0 320 200" role="img" aria-label="Diagram of a tank water heater with a relief valve and a pan"><rect width="320" height="200" fill="#F5F8FA"/><rect x="120" y="36" width="80" height="120" rx="16" fill="#fff" stroke="#0B7285" stroke-width="4"/><path d="M200 60 h40 v16 h-40" fill="#E8913A"/><rect x="100" y="156" width="120" height="16" rx="3" fill="#9A5A1A"/><text x="20" y="28" fill="#063E48" font-size="16" font-family="Outfit,sans-serif">Water heater</text><text x="20" y="190" fill="#3E515B" font-size="13" font-family="Outfit,sans-serif">Tank, relief valve, and a pan. Diagram only.</text></svg><figcaption>Diagram: tank, temperature and pressure relief valve, and a catch pan.</figcaption></figure>
      <figure class="diagram"><svg viewBox="0 0 320 200" role="img" aria-label="Diagram of an outdoor hose bib with a vacuum breaker cap"><rect width="320" height="200" fill="#F5F8FA"/><path d="M40 90 h140" stroke="#0B7285" stroke-width="12"/><circle cx="200" cy="90" r="18" fill="#E8913A"/><path d="M200 108 v40" stroke="#063E48" stroke-width="8"/><text x="20" y="40" fill="#063E48" font-size="16" font-family="Outfit,sans-serif">Hose bib</text><text x="20" y="170" fill="#3E515B" font-size="13" font-family="Outfit,sans-serif">Salt air on the Oregon Coast is hard on outdoor valves.</text></svg><figcaption>Diagram: an outdoor hose bib. On the coast, these fittings age in salt air.</figcaption></figure>
    </div></section></main>"""
    pages["gallery.html"] = page(
        "Plumbing diagrams | Plumbing 101, LLC",
        "Simple plumbing diagrams for shutoffs, traps, water heaters, and hose bibs. These are drawings, not photos of Plumbing 101 jobs.",
        "gallery.html", 0, gallery, crumbs_schema([("Home", "index.html"), ("Diagrams", "gallery.html")]),
    )
    faqs = [
        ("What area do you serve?", "The company website says Lincoln County and Tillamook County. Public listings place the business in Lincoln City. Town pages on this site are communities inside those two counties."),
        ("How do I reach you?", f"Call {PHONE_DISP} or email {EMAIL}. The email address is printed on plumbing101llc.com. The contact form opens an email to that address."),
        ("What are the hours?", "Monday through Friday, 8:30 a.m. to 3:30 p.m. Saturday and Sunday are closed. That schedule is on the company website and the BBB profile. Some other listings show 4:00 p.m. Call if you need the day confirmed."),
        ("Are you licensed?", "Oregon CCB #232697, Active. First licensed October 19, 2020. The official record is linked in the footer."),
        ("Who is listed as the owner?", "The BBB profile lists Faith A. Worthington as owner/manager and Michael E. Worthington as owner/member."),
        ("What work is listed?", "The BBB profile lists residential and commercial plumbing, new construction, remodeling, bathroom and kitchen plumbing, new piping and re-piping, drain, toilet, and faucet service and repair, water heater installation, and pipe inspection and evaluation. The company site also names water heater installation."),
        ("Do you publish prices?", "No prices are published on the company website or on this site. Ask for an estimate and describe the house and the problem."),
        ("Where is the shop?", "Lincoln City is the published city. This site does not print a street address, because public listings do not agree on one. Call or email to arrange a visit."),
        ("Do you list an after-hours number?", "The published phone number and the weekday hours are what this site repeats. A separate after-hours line was not found on the company website or the BBB hours table."),
        ("Can I read reviews here?", "One testimonial from Andrew Perry is quoted from the company website. Star totals that differ from site to site are left off this site."),
        ("What should I do before someone arrives?", "Make a path to the fixture or the water heater. If you can do it safely, find the main shutoff. Note which fixtures are affected. If a heater sat in water, leave it off."),
        ("How do I check the license myself?", "Use the Oregon CCB search for license 232697. The BBB profile is public as well. Both links are in the footer."),
    ]
    faq_html = "\n".join(
        f'<div class="faq-item"><button type="button" aria-expanded="false">{esc(q)}</button><div class="answer"><p>{esc(a)}</p></div></div>'
        for q, a in faqs
    )
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }
    faq_body = f"""<main id="main"><section class="page-hero"><div class="wrap">
      <p class="crumbs"><a href="index.html">Home</a> / FAQ</p>
      <p class="eyebrow">FAQ</p>
      <h1>Questions with public answers</h1>
      <p>Hours, license, service area, and contact details that match the company site, the BBB profile, or the CCB record.</p>
    </div></section>
    <section class="section"><div class="wrap">{faq_html}</div></section></main>"""
    pages["faq.html"] = page(
        "FAQ | Plumbing 101, LLC",
        "Hours, service area, license number, and contact details for Plumbing 101, LLC in Lincoln City, Oregon.",
        "faq.html", 0, faq_body, json.dumps(faq_schema),
    )
    area_cards = "\n".join(
        f'<a class="mini" href="{slug}.html"><h3>{esc(name)}</h3><p>{esc(county)} County</p></a>'
        for slug, name, county, *_ in CITIES
    )
    areas = f"""<main id="main"><section class="page-hero"><div class="wrap">
      <p class="crumbs"><a href="index.html">Home</a> / Service areas</p>
      <p class="eyebrow">Service area</p>
      <h1>Lincoln County and Tillamook County</h1>
      <p>Plumbing 101, LLC says it serves both counties. The towns below sit inside that published area. The company is based in Lincoln City.</p>
    </div></section>
    <section class="section"><div class="wrap city-grid">{area_cards}</div></section></main>"""
    pages["service-areas.html"] = page(
        "Service areas | Plumbing 101, LLC",
        "Plumbing 101, LLC serves Lincoln County and Tillamook County from Lincoln City, Oregon.",
        "service-areas.html", 0, areas, crumbs_schema([("Home", "index.html"), ("Service areas", "service-areas.html")]),
    )
    missing = """<main id="main"><section class="page-hero"><div class="wrap">
      <p class="eyebrow">404</p>
      <h1>That page is not on this site</h1>
      <p>The link may be old. The phone number still works on weekdays.</p>
      <p><a class="btn btn-gold" href="index.html">Back to the home page</a> <a class="btn btn-outline" href="tel:+15416141344">(541) 614-1344</a></p>
    </div></section></main>"""
    pages["404.html"] = page(
        "Page not found | Plumbing 101, LLC",
        "This page is not on the Plumbing 101, LLC site.",
        "404.html", 0, missing, crumbs_schema([("Home", "index.html")]), robots="noindex,follow",
    )
    return pages


def blog_index():
    cats = ["All"] + sorted({p["category"] for p in POSTS})
    buttons = "\n".join(
        f'<button class="pill" type="button" data-filter="{esc(c if c != "All" else "all")}" aria-pressed="{"true" if c=="All" else "false"}">{esc(c)}</button>'
        for c in cats
    )
    cards = "\n".join(
        f'<a class="mini" data-category="{esc(p["category"])}" href="{esc(p["slug"])}.html"><h3>{esc(p["title"])}</h3><p>{esc(p["category"])}</p></a>'
        for p in POSTS
    )
    body = f"""<main id="main"><section class="page-hero"><div class="wrap">
      <p class="crumbs"><a href="../index.html">Home</a> / Guides</p>
      <p class="eyebrow">Guides</p>
      <h1>Plain-language plumbing notes</h1>
      <p>Homeowner guides for coast houses. They explain what to look at and when to call. They are not quotes and they are not a claim that every job is offered outside the published service list.</p>
      <div class="pills" style="margin-top:16px">{buttons}</div>
    </div></section>
    <section class="section"><div class="wrap post-grid">{cards}</div></section></main>"""
    return page(
        "Plumbing guides | Plumbing 101, LLC",
        "Plumbing guides for Lincoln County and Tillamook County homes, from Plumbing 101, LLC in Lincoln City.",
        "blog/index.html", 1, body, crumbs_schema([("Home", "index.html"), ("Guides", "blog/index.html")]),
    )


def blog_page(post):
    service = next(s for s in SERVICES if s[0] == post["service"])
    sections = "\n".join(f"<h2>{esc(h)}</h2>\n" + "\n".join(f"<p>{esc(para)}</p>" for para in paras) for h, paras in post["sections"])
    bullets = "\n".join(f"<li>{esc(b)}</li>" for b in post["checks"])
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post["title"],
        "description": post["description"],
        "datePublished": "2026-10-30",
        "dateModified": "2026-10-30",
        "author": {"@type": "Organization", "name": "Plumbing 101, LLC"},
        "publisher": {"@type": "Organization", "name": "Plumbing 101, LLC", "url": BASE},
        "mainEntityOfPage": BASE + "blog/" + post["slug"] + ".html",
    })
    body = f"""<main id="main"><section class="page-hero"><div class="wrap">
      <p class="crumbs"><a href="../index.html">Home</a> / <a href="index.html">Guides</a> / {esc(post["category"])}</p>
      <p class="eyebrow">{esc(post["category"])}</p>
      <h1>{esc(post["title"])}</h1>
      <p>{esc(post["description"])}</p>
    </div></section>
    <section class="section"><div class="wrap prose">
      {sections}
      <h2>Safe checks</h2>
      <ul>{bullets}</ul>
      <h2>Call Plumbing 101, LLC</h2>
      <p>For {esc(service[1].lower())}, call <a href="tel:{PHONE_TEL}">{PHONE_DISP}</a> Monday through Friday, 8:30 a.m. to 3:30 p.m., or email <a href="mailto:{EMAIL}">{EMAIL}</a>. The company serves Lincoln County and Tillamook County and holds Oregon CCB license 232697.</p>
      <p><a href="../services/{service[0]}.html">{esc(service[1])}</a> · <a href="../contact.html">Contact</a> · <a href="index.html">All guides</a></p>
    </div></section></main>"""
    return page(post["title"] + " | Plumbing 101, LLC", post["description"], "blog/" + post["slug"] + ".html", 1, body, schema)


def main():
    written = []
    for path, html_doc in core_pages().items():
        written.append(write(path, html_doc))
    for slug, name, summary, kind in SERVICES:
        schema = json.dumps({
            "@context": "https://schema.org",
            "@type": "Service",
            "name": name,
            "provider": {"@type": "Plumber", "name": "Plumbing 101, LLC", "telephone": "+1-541-614-1344"},
            "areaServed": ["Lincoln County, Oregon", "Tillamook County, Oregon"],
            "url": BASE + "services/" + slug + ".html",
        })
        doc = page(
            f"{name} | Plumbing 101, LLC",
            summary + " Plumbing 101, LLC, Lincoln City. Call (541) 614-1344.",
            f"services/{slug}.html",
            1,
            service_body(slug, name, summary, kind),
            schema,
        )
        written.append(write(f"services/{slug}.html", doc))
    for city in CITIES:
        slug, name, county = city[0], city[1], city[2]
        doc = page(
            f"Plumber in {name}, OR | Plumbing 101, LLC",
            f"Plumbing 101, LLC serves {name} in {county} County, Oregon. Call (541) 614-1344. Weekdays 8:30 a.m. to 3:30 p.m.",
            f"{slug}.html",
            0,
            city_body(*city),
            crumbs_schema([("Home", "index.html"), ("Service areas", "service-areas.html"), (name, slug + ".html")]),
        )
        written.append(write(f"{slug}.html", doc))
    written.append(write("blog/index.html", blog_index()))
    for post in POSTS:
        written.append(write(f"blog/{post['slug']}.html", blog_page(post)))
    urls = []
    for path in written:
        if path.endswith("404.html"):
            continue
        urls.append(BASE + path)
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        sitemap.append(f"<url><loc>{url}</loc><lastmod>2026-10-30</lastmod></url>")
    sitemap.append("</urlset>\n")
    write("sitemap.xml", "\n".join(sitemap))
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: https://luckygoats33.github.io/plumbing-101/sitemap.xml\n")
    print(f"wrote {len(written)} html pages")


if __name__ == "__main__":
    main()
