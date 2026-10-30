#!/usr/bin/env python3
"""Generate the Plumbing 101, LLC static site. Facts are limited to public sources."""
import html
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://luckygoats33.github.io/plumbing-101/"
PHONE_DISP = "(541) 614-1344"
PHONE_TEL = "+15416141344"
EMAIL = "office@plumbing101.net"
CCB_URL = "https://search.ccb.state.or.us/search/search_result.aspx?id=232697"
BBB_URL = "https://www.bbb.org/us/or/lincoln-city/profile/plumbing-renovation/plumbing-101-llc-1296-1000189882"
COMPANY_SITE = "https://www.plumbing101llc.com/"
ONECALL = "https://oregoncoast.onecalltoday.com/listings.html#plumbing-101"
QUOTE = "These folks do excellent work, they re-piped my whole beach home in record time at a fair price, five stars!!"

SERVICES = [
    ("residential-plumbing", "Residential plumbing", "Home plumbing repairs, fixtures, and replacements for houses and beach places.", "home"),
    ("commercial-plumbing", "Commercial plumbing", "Plumbing for small commercial spaces, including remodels and day-to-day repairs.", "shop"),
    ("new-construction-plumbing", "New construction plumbing", "New piping and plumbing for new construction, as listed on the BBB profile.", "build"),
    ("plumbing-remodeling", "Plumbing remodeling", "Plumbing renovations and remodeling for kitchens, baths, and re-pipes.", "remodel"),
    ("bathroom-plumbing", "Bathroom plumbing", "Bathroom installations, replacements, remodels, and fixture repairs.", "bath"),
    ("kitchen-plumbing", "Kitchen plumbing", "Kitchen plumbing installations, replacements, remodels, and sink work.", "kitchen"),
    ("repiping", "Re-piping and new piping", "New piping and whole-home re-piping, including older beach houses.", "pipe"),
    ("drain-services", "Drain and sink services", "Drain and sink services for homes and small businesses.", "drain"),
    ("toilet-repair", "Toilet repair", "Toilet services and repairs, from running tanks to worn seals.", "toilet"),
    ("faucet-repair", "Faucet repair", "Faucet services and repairs at sinks, tubs, and showers.", "faucet"),
    ("water-heaters", "Water heater installation", "Water heater installation, named on the company site and the BBB profile.", "heater"),
    ("pipe-inspection", "Pipe inspection", "Pipe inspection and evaluation before a repair, re-pipe, or remodel.", "inspect"),
]

CITIES = [
    ("lincoln-city", "Lincoln City", "Lincoln", "Lincoln City stretches along Highway 101 through the older communities of Oceanlake, Delake, Nelscott, Taft, and Cutler City. The D River crosses the highway near the middle of town. Public listings place Plumbing 101, LLC in Lincoln City.", "Houses here range from older cottages on tight lots to newer places above the beach. Many sit close to salt air, and a lot of them are used as second homes that stay empty between visits.", "Empty weeks dry out drain traps. Hose bibs and exposed fittings take salt spray. Crawlspaces under raised beach houses collect damp air. A plumber visit often starts with finding the shutoff, which is not in the same place from one era of house to the next."),
    ("newport", "Newport", "Lincoln", "Newport is the Lincoln County seat, set on Yaquina Bay. The bayfront, Nye Beach, and the south side of the Yaquina Bay Bridge are different neighborhoods with different house ages.", "Bayfront buildings sit low and close together. Nye Beach has older homes on hills. South of the bridge, houses spread toward South Beach. Wind and rain reach all of them.", "A low commercial sink and a hillside cottage do not fail the same way. Say which part of Newport the building is in, and whether the problem is a single fixture or the whole supply, when you call."),
    ("depoe-bay", "Depoe Bay", "Lincoln", "Depoe Bay is a small harbor town on Highway 101 between Lincoln City and Newport. The highway crosses a short concrete bridge at the harbor, and many houses sit on steep, small lots.", "Lots are tight, parking is limited, and some plumbing runs are tucked under decks or in partial crawlspaces. Vacation use is common.", "If a hose bib or deck shower faces the ocean, salt air is part of the story. Mention stairs, limited parking, and whether the water is off at one fixture or the whole house."),
    ("toledo", "Toledo", "Lincoln", "Toledo sits inland on the Yaquina River, east of Newport. It is a mill town with colder nights than the beach strip and a housing stock that includes older mill-era homes.", "Inland houses see more freezing weather than oceanfront cottages. Pipes in garages, crawlspaces, and along exterior walls matter more here in a cold snap.", "Tell the plumber whether the house is on a hill, in the flats near the river, or in town, and whether any pipe run is in an unheated space."),
    ("waldport", "Waldport", "Lincoln", "Waldport sits at Alsea Bay on the south end of Lincoln County, where Highway 101 crosses the bay. The town includes bay-side houses and neighborhoods up the hill.", "Bay air is damp. Older houses and newer hillside homes share the same municipal questions: where is the shutoff, and is the leak on the house side of the meter?", "A main-line concern and a single dripping faucet are different calls. Describe which one you have, and whether the house is used year-round."),
    ("yachats", "Yachats", "Lincoln", "Yachats is a small rocky-shore town at the south edge of Lincoln County. Creeks come off the coast range, rain is heavy, and many homes sit above the rocks or in the village along Highway 101.", "Houses are often custom, with plumbing that follows additions made over time. Exterior pipe and hose bibs take wind-driven rain.", "If an addition has its own bathroom, say so. Separate water heaters and long pipe runs are common in houses that grew room by room."),
    ("siletz", "Siletz", "Lincoln", "Siletz is an inland community in the Siletz River valley, east of the beach towns. The valley is wet, and winter temperatures drop below what the immediate shoreline sees.", "Homes include older valley houses and places on wells or longer supply lines. Confirm the water source when you call so the visit starts with the right question.", "A loss of pressure can be a well, a filter, a valve, or a leak. Note whether neighbors have water and whether the issue started after a freeze or after heavy rain."),
    ("gleneden-beach", "Gleneden Beach", "Lincoln", "Gleneden Beach lies along Highway 101 between Lincoln City and Depoe Bay, near Salishan. Homes include beach-side places and houses set back in the trees.", "Many properties are part-time. Long vacancies, outdoor showers, and deck hose bibs show up often in coastal plumbing calls.", "Before a visit, check whether the main shutoff was closed for the off-season and whether traps were left dry. A sewer smell in an empty house is often a dry trap."),
    ("lincoln-beach", "Lincoln Beach", "Lincoln", "Lincoln Beach is a coastal community just south of Depoe Bay in Lincoln County. Houses sit near the ocean on a short stretch of Highway 101.", "Salt air and wind reach outdoor plumbing quickly. Small lots can hide the shutoff behind decks, skirting, or shrubs.", "Point out the shutoff if you know it, and say whether the house is occupied full time. That changes how traps, heaters, and hose bibs behave."),
    ("otis", "Otis", "Lincoln", "Otis is inland from Lincoln City along the Salmon River, where the coast highway meets the river valley. It is wet, and the river corridor has flooded in past storms.", "Houses may sit near the river or up side roads. After high water, a plumbing question is sometimes really a question about what got wet: the water heater, the insulation, or a crawlspace.", "If floodwater reached a water heater or appliance, leave it off and say that clearly when you call. Do not restart a heater that sat in water."),
    ("rose-lodge", "Rose Lodge", "Lincoln", "Rose Lodge is on the Salmon River near the Lincoln County and Tillamook County line, inland from the beach. It is a rural community with a mix of houses on open lots.", "Rural spacing means longer driveways and sometimes longer pipe runs from the meter or well to the house. Freeze risk is higher than on the immediate coast.", "Give a clear road description and say whether the supply is a meter or a well. Note any pipe that runs under a house, through a barn, or along an exterior wall."),
    ("seal-rock", "Seal Rock", "Lincoln", "Seal Rock is a basalt-shore community on Highway 101 between Newport and Waldport. Homes sit above the rocks and along the highway, with wind and salt as constants.", "Exposed hose bibs, deck lines, and exterior vents take spray. Houses on the ocean side and houses east of the highway weather differently.", "A pinhole on an exposed line and a clogged tub are different jobs. Say which fixtures are affected and whether water is pooling under the house."),
    ("south-beach", "South Beach", "Lincoln", "South Beach is the area south of the Yaquina Bay Bridge, including homes near South Beach State Park. It is still the Newport area, with open wind off the beach.", "Vacation rentals and full-time houses sit side by side. Turnover between guests is hard on toilets, drains, and supply lines that get forced.", "If you manage a rental, say so, and describe what the guest reported versus what you can see. A running toilet and a sewer backup need different urgency."),
    ("eddyville", "Eddyville", "Lincoln", "Eddyville is a small inland community on the Yaquina River, east of Toledo toward the valley. Nights run colder than in Newport.", "Houses are spread out. Unheated crawlspaces and well houses are worth mentioning if a pipe may have frozen or a leak is under the floor.", "Cell service can be uneven in the valley. Leave a phone number that works at the house, and describe gate codes or animals in the yard before the visit."),
    ("tidewater", "Tidewater", "Lincoln", "Tidewater is on the Alsea River, inland from Waldport. The river valley is narrow, wet, and shaded, with homes tucked along the water and the highway.", "River damp and hillside runoff are part of life here. A crawlspace can stay wet long after a storm even when the plumbing itself is sound.", "Separate a plumbing leak from hillside water if you can: is the water only under a pipe, or is the whole crawlspace wet after rain? That detail saves a wrong diagnosis."),
    ("tillamook", "Tillamook", "Tillamook", "Tillamook is the county seat, set in a broad dairy valley that takes heavy rain. The town is inland from the beaches, with river flood history in the surrounding valley.", "Housing runs from older in-town homes to ranch houses on the valley floor. High groundwater after storms can wet crawlspaces and confuse a leak hunt.", "Say whether the water showed up only after rainfall, and whether it is at a fixture or under the house. A water heater in a garage is common. Mention if that space got wet."),
    ("pacific-city", "Pacific City", "Tillamook", "Pacific City faces the ocean at Cape Kiwanda, with the Nestucca River and sand spit nearby. Beach houses and dune-area homes take wind and salt.", "Many homes are vacation houses. Outdoor showers, hose bibs, and water heaters left on between visits are routine topics.", "If the house was closed up, say whether the water was shut off and the heater was left on. A sulfur or sewer smell after a vacancy is often a dry trap, which a bucket of water can confirm at a floor drain or shower."),
    ("neskowin", "Neskowin", "Tillamook", "Neskowin is a small village at the south end of the Tillamook County coast, known for Proposal Rock and a creek that meets the beach. Homes sit in the trees and near the shore.", "The village is quiet and residential. Houses can be seasonal. Creek-side damp and ocean air both reach the plumbing that sits outside the heated rooms.", "Mention whether the house is on a slope and whether any bathroom was added later. Added baths sometimes have long, poorly sloped drains."),
    ("garibaldi", "Garibaldi", "Tillamook", "Garibaldi is a port town on Tillamook Bay, north of the city of Tillamook. Buildings cluster near the bay and the highway, with wind off the water.", "Older commercial buildings and houses sit close to the bay. Salt air and older pipe often show up together.", "If the property is a shop, a rental, or a house, say which. Commercial sinks and house baths are both within the services listed for Plumbing 101, LLC, and the access is different."),
    ("rockaway-beach", "Rockaway Beach", "Tillamook", "Rockaway Beach is a long, sandy beach town on Highway 101. Houses and cottages line the ocean side and the east side of the highway.", "Salt, sand, and vacation turnover are the local pattern. Outdoor showers clog with sand. Supply lines in crawlspaces corrode where air stays damp.", "A sand-clogged shower drain and a corroded supply line need different parts and time. Say what you see: slow drain, drip, stain, or no water."),
    ("manzanita", "Manzanita", "Tillamook", "Manzanita sits at the edge of Nehalem Bay, with oceanfront houses and cottages in town under the trees. It is a village with a high share of second homes.", "Vacant weeks are normal. Dry traps, closed valves, and water heaters that sat idle are common first checks when someone arrives to a problem.", "If you are opening a house for the season, walk the fixtures before guests arrive. A slow fill valve or a drip under a sink is easier to fix on an empty calendar."),
    ("nehalem", "Nehalem", "Tillamook", "Nehalem is a river town just inland from Manzanita, on the Nehalem River. The valley is wet, and the town is small.", "Houses sit near the river and on the hills around it. Flood-prone ground and ordinary household plumbing are separate issues that can show up in the same week.", "If river water entered a crawlspace or garage, leave electrical equipment and the water heater alone and describe the water line when you call."),
    ("wheeler", "Wheeler", "Tillamook", "Wheeler is a small town on Nehalem Bay, between Nehalem and Rockaway Beach. Buildings face the bay along a short main stretch of Highway 101.", "Bay damp and older wood buildings go together. Plumbing is often in tight crawlspaces or in added rooms.", "Mention low clearance under the house if you know it. A person needs room to reach a leak, and some bay houses sit close to the ground."),
    ("bay-city", "Bay City", "Tillamook", "Bay City is on Tillamook Bay between Tillamook and Garibaldi. The town is small, with houses and a few commercial buildings along the water and the highway.", "Wind off the bay and rain off the hills keep everything damp. Exterior penetrations and older galvanized lines are worth naming if you already know the pipe material.", "You do not need to diagnose the metal. A photo of an exposed pipe, sent by email to office@plumbing101.net, can help the conversation before a visit."),
    ("oceanside", "Oceanside", "Tillamook", "Oceanside is a bluff village west of Tillamook, above the beach and south of Cape Meares. The road is steep, and houses stack on the hill.", "Bluff homes take direct salt wind. Decks, outdoor showers, and long exterior runs are exposed. Parking and stairs matter for a service visit.", "Describe access: street parking, stairs, and which level the water heater is on. A heater in a lower garage is a different carry than one in an upstairs closet."),
    ("netarts", "Netarts", "Tillamook", "Netarts sits on Netarts Bay, west of Tillamook, with the ocean beach just over the dune line. The bay is known for oysters, and the air stays damp.", "Houses range from bay-side cottages to homes in the trees. Vacation use is common. Boat rinsing and outdoor showers add sand and grit to drains.", "A grit-filled trap is a small job compared with a water heater that failed while the house was empty. Say which one you are seeing."),
    ("beaver", "Beaver", "Tillamook", "Beaver is an inland community on the Nestucca River, east of the beaches. It is rural, wet, and cooler than Pacific City.", "Houses sit on larger lots. Pipe runs from a meter or well can be long, and outbuildings sometimes share water.", "If a barn, shop, or guest cabin is on the same supply, say so. A leak in an outbuilding can drop pressure in the house."),
    ("hebo", "Hebo", "Tillamook", "Hebo is inland at the foot of Mount Hebo, higher and colder than the beach towns. Frost reaches pipes that would stay safe at sea level.", "Unheated crawlspaces, well houses, and exterior walls are the first places a cold snap shows up. Insulation and heat tape are homeowner topics. A split pipe is a plumbing call.", "If you suspect a freeze, open a faucet slowly after the thaw starts and watch for leaks. Shut the main if water appears where it should not, then call."),
    ("cloverdale", "Cloverdale", "Tillamook", "Cloverdale is in the Nestucca valley, inland from Pacific City. It is a small rural community on the way from the valley to the cape.", "The mix is farmhouses, newer homes, and rentals used by people heading to the beach. Supply lines can cross yards.", "A wet spot in a yard between the meter and the house can be the service line. Note whether the meter is spinning when every faucet is off. That is useful information, and it is safe to observe."),
    ("cape-meares", "Cape Meares", "Tillamook", "Cape Meares is a bluff community west of Tillamook, near the cape and the state park. Houses face wind off the Pacific and sit above steep ground.", "Salt spray and steep access define the plumbing that lives outdoors: hose bibs, vents, and any line under a deck. Indoor plumbing is ordinary, but the trip to reach it is not.", "Give directions from the bay road, mention steep driveways, and say whether the problem is inside or on an exposed exterior line."),
]


def esc(text):
    return html.escape(text, quote=True)


def rel(depth, path):
    return ("../" * depth) + path


def icon(kind):
    common = {
        "home": '<path d="M16 28L32 14l16 14v18H36V34h-8v12H16V28z" fill="#F0A552"/>',
        "shop": '<path d="M14 28h36v16H14z" fill="#F5F8FA"/><path d="M12 28l4-10h32l4 10" fill="#F0A552"/>',
        "build": '<path d="M18 44V24l14-8 14 8v20" fill="none" stroke="#F0A552" stroke-width="3"/><path d="M28 44V32h8v12" fill="#F5F8FA"/>',
        "remodel": '<path d="M16 40h32v6H16zM20 22h8v18h-8zM34 28h10v12H34z" fill="#F0A552"/>',
        "bath": '<path d="M16 30h32v8H16z" fill="#F5F8FA"/><path d="M20 30V20a6 6 0 0 1 12 0" fill="none" stroke="#F0A552" stroke-width="3"/>',
        "kitchen": '<path d="M18 18h28v22H18z" fill="#F5F8FA"/><path d="M24 18v-4h6M34 40v6M28 40v6" stroke="#F0A552" stroke-width="3"/>',
        "pipe": '<path d="M14 26h16v8H14zM30 22h8v20h-8zM38 34h12v8H38z" fill="#F0A552"/>',
        "drain": '<circle cx="32" cy="30" r="10" fill="none" stroke="#F5F8FA" stroke-width="3"/><path d="M32 40v10" stroke="#F0A552" stroke-width="4"/>',
        "toilet": '<path d="M24 16h16v8H24zM20 26h24c0 12-4 18-12 18S20 38 20 26z" fill="#F5F8FA"/>',
        "faucet": '<path d="M20 22h24v6H20zM30 28h4v16h-4zM22 44h20" stroke="#F0A552" stroke-width="3" fill="none"/>',
        "heater": '<rect x="22" y="14" width="20" height="32" rx="8" fill="#F5F8FA"/><path d="M28 22h8M28 28h8M28 34h8" stroke="#E8913A" stroke-width="2"/>',
        "inspect": '<circle cx="28" cy="28" r="10" fill="none" stroke="#F0A552" stroke-width="3"/><path d="M36 36l10 10" stroke="#F5F8FA" stroke-width="4"/>',
    }
    inner = common.get(kind, common["pipe"])
    return f'<svg viewBox="0 0 64 64" aria-hidden="true">{inner}</svg>'


def services_links(depth):
    return "\n".join(
        f'<a href="{rel(depth, "services/" + slug + ".html")}">{esc(name)}</a>'
        for slug, name, _, _ in SERVICES
    )


def header(depth):
    p = lambda path: rel(depth, path)
    drops = services_links(depth)
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{p('index.html')}" aria-label="Plumbing 101, LLC home">
      <img src="{p('images/brand-logo.jpg')}" width="56" height="48" alt="">
      <span><span class="brand-name">Plumbing 101</span><span class="brand-tag">Always at Your Service</span></span>
    </a>
    <nav class="desktop-nav" aria-label="Primary">
      <a href="{p('index.html')}">Home</a>
      <div class="drop">
        <button class="menu-btn" aria-expanded="false" aria-haspopup="true">Services</button>
        <div class="drop-panel">{drops}</div>
      </div>
      <a href="{p('service-areas.html')}">Areas</a>
      <a href="{p('about.html')}">About</a>
      <a href="{p('faq.html')}">FAQ</a>
      <a href="{p('blog/index.html')}">Guides</a>
      <a href="{p('contact.html')}">Contact</a>
      <a class="btn btn-gold" href="{p('contact.html')}" data-open-estimate="Nav">Free estimate</a>
    </nav>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-drawer" aria-label="Open menu">
      <svg width="22" height="16" viewBox="0 0 22 16" aria-hidden="true"><path d="M0 1h22M0 8h22M0 15h22" stroke="currentColor" stroke-width="2"/></svg>
    </button>
  </div>
</header>
<div class="nav-overlay"></div>
<nav class="nav-drawer" id="nav-drawer" aria-label="Mobile">
  <a href="{p('index.html')}">Home</a>
  <a href="{p('service-areas.html')}">Service areas</a>
  <a href="{p('about.html')}">About</a>
  <a href="{p('reviews.html')}">Reviews</a>
  <a href="{p('gallery.html')}">Diagrams</a>
  <a href="{p('faq.html')}">FAQ</a>
  <a href="{p('blog/index.html')}">Guides</a>
  <a href="{p('contact.html')}">Contact</a>
  <p class="eyebrow" style="margin-top:16px">Services</p>
  {drops}
  <button class="linkish" data-open-estimate="Mobile menu">Request an estimate</button>
  <a href="tel:{PHONE_TEL}">Call {PHONE_DISP}</a>
</nav>"""


def footer(depth):
    p = lambda path: rel(depth, path)
    svc = "\n".join(f'<li><a href="{p("services/" + slug + ".html")}">{esc(name)}</a></li>' for slug, name, _, _ in SERVICES)
    pills = "\n".join(
        f'<a class="pill" href="{p(slug + ".html")}">{esc(name)}</a>' for slug, name, *_ in CITIES
    )
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <a class="brand" href="{p('index.html')}"><img src="{p('images/brand-logo.jpg')}" width="56" height="48" alt=""><span><span class="brand-name">Plumbing 101</span><span class="brand-tag">Always at Your Service</span></span></a>
      <p>Plumbing 101, LLC serves Lincoln County and Tillamook County from Lincoln City. Weekdays 8:30 a.m. to 3:30 p.m.</p>
      <p><a href="tel:{PHONE_TEL}">{PHONE_DISP}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div>
      <h2>Company</h2>
      <ul>
        <li><a href="{p('about.html')}">About</a></li>
        <li><a href="{p('reviews.html')}">Reviews</a></li>
        <li><a href="{p('gallery.html')}">Diagrams</a></li>
        <li><a href="{p('faq.html')}">FAQ</a></li>
        <li><a href="{p('contact.html')}">Contact</a></li>
        <li><a href="{p('blog/index.html')}">Guides</a></li>
        <li><a href="{p('service-areas.html')}">Service areas</a></li>
      </ul>
    </div>
    <div>
      <h2>Services</h2>
      <ul>{svc}</ul>
    </div>
    <div>
      <h2>Records</h2>
      <ul>
        <li><a href="{CCB_URL}">Oregon CCB #232697</a></li>
        <li><a href="{BBB_URL}">BBB profile</a></li>
        <li><a href="{COMPANY_SITE}">plumbing101llc.com</a></li>
        <li><a href="{ONECALL}">One Call Today listing</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap">
    <h2>Towns in the two counties</h2>
    <div class="pills">{pills}</div>
    <div class="legal">
      <span>Copyright 2026 Plumbing 101, LLC. Oregon CCB #232697.</span>
      <span>Lincoln City, Oregon. Hours Monday to Friday, 8:30 a.m. to 3:30 p.m.</span>
    </div>
  </div>
</footer>
<div class="sticky-cta" aria-label="Call Plumbing 101">
  <a class="call" href="tel:{PHONE_TEL}">Call {PHONE_DISP}</a>
  <button class="book" type="button" data-open-estimate="Sticky bar">Estimate</button>
</div>
<a class="btn btn-gold float-estimate" href="{p('contact.html')}" data-open-estimate="Floating button">Free estimate</a>
<div class="modal" id="estimate-modal" hidden role="dialog" aria-modal="true" aria-labelledby="estimate-title">
  <div class="modal-card">
    <button class="modal-close" type="button" data-close-modal aria-label="Close estimate form">&times;</button>
    <h2 id="estimate-title">Request an estimate</h2>
    <p>This form opens an email to {EMAIL}. You can also call <a href="tel:{PHONE_TEL}">{PHONE_DISP}</a>.</p>
    {form("Modal")}
  </div>
</div>
<script src="{p('site.js')}" defer></script>"""


def form(source):
    sid = re.sub(r"[^a-z0-9]+", "-", source.lower()).strip("-")
    options = "\n".join(f'<option>{esc(name)}</option>' for _, name, _, _ in SERVICES)
    return f"""<form data-mailto action="mailto:{EMAIL}" method="post" enctype="text/plain">
      <div class="hp" aria-hidden="true"><label>Company<input name="_honey" tabindex="-1" autocomplete="off"></label></div>
      <input type="hidden" name="_source" value="{esc(source)}">
      <div class="form-grid">
        <div><label for="name-{sid}">Name</label><input id="name-{sid}" name="name" autocomplete="name" required></div>
        <div><label for="phone-{sid}">Phone</label><input id="phone-{sid}" name="phone" type="tel" autocomplete="tel" required></div>
        <div><label for="email-{sid}">Email</label><input id="email-{sid}" name="email" type="email" autocomplete="email" required></div>
        <div><label for="city-{sid}">City</label><input id="city-{sid}" name="city" autocomplete="address-level2"></div>
        <div class="full"><label for="service-{sid}">Service</label><select id="service-{sid}" name="service"><option value="">Select a service</option>{options}</select></div>
        <div class="full"><label for="message-{sid}">What is going on?</label><textarea id="message-{sid}" name="message" required></textarea></div>
        <div class="full"><button class="btn btn-gold" type="submit">Email this request</button></div>
      </div>
      <p class="form-note" hidden>If your email app did not open, write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </form>"""


def head(title, desc, canonical_path, depth, schema, robots="index,follow"):
    p = lambda path: rel(depth, path)
    url = BASE + canonical_path
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#D42329">
<link rel="icon" href="{p('images/brand-logo.jpg')}" type="image/jpeg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800&amp;family=Literata:wght@500;600;700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p('styles.css')}">
<script type="application/ld+json">{schema}</script>
</head>
<body>"""


def plumber_schema():
    return """{
  "@context": "https://schema.org",
  "@type": "Plumber",
  "name": "Plumbing 101, LLC",
  "slogan": "Always at Your Service",
  "url": "https://luckygoats33.github.io/plumbing-101/",
  "telephone": "+1-541-614-1344",
  "email": "office@plumbing101.net",
  "image": "https://luckygoats33.github.io/plumbing-101/images/brand-logo.jpg",
  "address": {"@type": "PostalAddress", "addressLocality": "Lincoln City", "addressRegion": "OR", "addressCountry": "US"},
  "areaServed": [
    {"@type": "AdministrativeArea", "name": "Lincoln County, Oregon"},
    {"@type": "AdministrativeArea", "name": "Tillamook County, Oregon"}
  ],
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "08:30",
    "closes": "15:30"
  }],
  "sameAs": [
    "https://www.plumbing101llc.com/",
    "https://www.bbb.org/us/or/lincoln-city/profile/plumbing-renovation/plumbing-101-llc-1296-1000189882",
    "https://oregoncoast.onecalltoday.com/listings.html#plumbing-101"
  ],
  "identifier": "Oregon CCB 232697"
}"""


def crumbs_schema(items):
    elements = []
    for i, (name, path) in enumerate(items, 1):
        elements.append(f'{{"@type":"ListItem","position":{i},"name":{js(name)},"item":"{BASE + path}"}}')
    return '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[' + ",".join(elements) + "]}"


def js(text):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def page(title, desc, path, depth, body, schema_extra="", robots="index,follow"):
    schema = schema_extra or crumbs_schema([("Home", "index.html"), (title, path)])
    doc = head(title, desc, path, depth, schema, robots)
    doc += header(depth) + body + footer(depth) + "</body></html>\n"
    return doc


def write(path, content):
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    return path


def hero_svg():
    return """<svg class="hero-scene" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <path d="M0 520 C 180 470 280 430 460 470 C 680 520 760 390 980 420 C 1180 446 1280 360 1440 390 L1440 900 L0 900 Z" fill="#085465"/>
  <path d="M1040 430 l70 90 90-40 40 70-200 20z" fill="#063E48"/>
  <circle cx="1180" cy="180" r="46" fill="#F0A552" opacity=".85"/>
</svg>
<svg class="wave" viewBox="0 0 1440 90" preserveAspectRatio="none" role="img" aria-label="Ocean wave">
  <path fill="#085465" fill-opacity=".45" d="M0 40c80 20 160-20 240 0s160 20 240 0 160-20 240 0 160 20 240 0 160-20 240 0 160 20 240 0v50H0z"/>
  <path fill="#0B7285" fill-opacity=".7" d="M0 55c90 18 150-18 240 0s150 18 240 0 150-18 240 0 150 18 240 0 150-18 240 0 150 18 240 0v35H0z"/>
  <path fill="#F5F8FA" d="M0 70c100 14 140-14 240 0s140 14 240 0 140-14 240 0 140 14 240 0 140-14 240 0 140 14 240 0v20H0z"/>
</svg>"""
