#!/usr/bin/env python3
# =============================================================================
#
#   ██████╗ ██╗     ██╗  ██╗ ██████╗     ██████╗ ███████╗
#  ██╔═══██╗██║     ██║  ██║██╔═══██╗    ██╔══██╗██╔════╝
#  ██║   ██║██║     ███████║██║   ██║    ██║  ██║█████╗
#  ██║   ██║██║     ██╔══██║██║   ██║    ██║  ██║██╔══╝
#  ╚██████╔╝███████╗██║  ██║╚██████╔╝    ██████╔╝███████╗
#   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝     ╚═════╝ ╚══════╝
#   ██████╗ ███████╗██╗   ██╗███████╗
#  ██╔══██╗██╔════╝██║   ██║██╔════╝
#  ██║  ██║█████╗  ██║   ██║███████╗
#  ██║  ██║██╔══╝  ██║   ██║╚════██║
#  ██████╔╝███████╗╚██████╔╝███████║
#  ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝
#
#  OLHO DE DEUS — TERMUX EDITION v1.0
#  Criado por: BLAZING | Ethical Hacker & OSINT Specialist
#  Otimizado para Android via Termux
#  Uso exclusivo para fins éticos e legais
#
#  MÓDULOS:
#   🔍 A — OSINT:      IP, Domínio, Email, Username, Pessoa, Telefone, Keyword
#   🌑 B — DARKNET:    Links, Busca, Email Anônimo, Paste Monitor
#   🛡️  C — SEGURANÇA:  Hash, Senha, Malware, Threat Intel, Breach
#   📡 D — REDE:       Shodan, Certwatch, Metascraper, URL, Whois
#   🤖 E — AUTOMAÇÃO:  Shadow Recon, Autopilot, Dorks, Report
#   ❓ F — AJUDA:      Guia completo de todos os módulos
#
# =============================================================================

import sys, os, json, time, re, concurrent.futures
import subprocess, urllib.parse, hashlib
from datetime import datetime
from pathlib import Path

# Verificar dependências
MISSING = []
try:    import requests
except: MISSING.append('requests')
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.prompt import Prompt, Confirm
    from rich import box
    from rich.align import Align
    from rich.rule import Rule
except: MISSING.append('rich')
try:    import dns.resolver
except: MISSING.append('dnspython')
try:    import whois
except: MISSING.append('python-whois')

if MISSING:
    print(f"\n[ERRO] Instale: pip install {' '.join(MISSING)}")
    print("No Termux: pip install " + " ".join(MISSING))
    sys.exit(1)

console = Console()
GOLD='bold yellow'; RED='bold red'; GREEN='bold green'
BLUE='bold cyan'; WHITE='white'; DIM='dim white'

# Pasta de relatórios no Termux
REPORTS_DIR = Path.home() / "storage" / "downloads" / "olho-de-deus-reports"
try:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
except:
    REPORTS_DIR = Path.home() / "olho-de-deus-reports"
    REPORTS_DIR.mkdir(exist_ok=True)

SESSION_LOG = []

# =============================================================================
# BANNER — Compacto para tela de celular
# =============================================================================
def banner():
    os.system('clear')
    art = """\n  ██████╗ ██████╗ ███████╗██╗   ██╗███████╗
 ██╔═══██╗██╔══██╗██╔════╝██║   ██║██╔════╝
 ██║   ██║██║  ██║█████╗  ██║   ██║███████╗
 ██║   ██║██║  ██║██╔══╝  ██║   ██║╚════██║
 ╚██████╔╝██████╔╝███████╗╚██████╔╝███████║
  ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝"""
    console.print(Align.center(Text(art, style="yellow")))
    console.print(Align.center(Text("👁  OLHO DE DEUS — TERMUX EDITION v1.0", style="bold yellow")))
    console.print(Align.center(Text("━"*42, style="yellow dim")))
    console.print(Align.center(Text("by  B L A Z I N G", style="bold yellow")))
    console.print(Align.center(Text("Ethical Hacker & OSINT Specialist", style="dim yellow")))
    console.print(Align.center(Text("USO ÉTICO E LEGAL — DADOS PÚBLICOS", style="dim red")))
    console.print()
    console.print(Rule(style="yellow dim"))
    console.print()

# =============================================================================
# MENU PRINCIPAL
# =============================================================================
def menu():
    banner()
    t = Table(box=box.SIMPLE, show_header=False, padding=(0,1))
    t.add_column(style="yellow",    width=5)
    t.add_column(style="bold white",width=18)
    t.add_column(style="dim white")
    for code, name, desc in [
        ("A","🔍 OSINT",       "IP · Domínio · Email · Username · Pessoa"),
        ("B","🌑 DARKNET",     "Links · Busca · Email Anon · Pastes"),
        ("C","🛡️  SEGURANÇA",   "Hash · Senha · Malware · Threat · Breach"),
        ("D","📡 REDE",        "Shodan · Certs · URL · Whois · Meta"),
        ("E","🤖 AUTOMAÇÃO",   "Recon · Autopilot · Dorks · Report"),
        ("F","❓ AJUDA",       "Guia completo de todos os módulos"),
        ("0","❌ SAIR",        ""),
    ]: t.add_row(f"[{code}]", name, desc)
    console.print(Panel(t,
        title="[bold yellow]👁 OLHO DE DEUS[/]",
        border_style="yellow dim",
        subtitle="[dim yellow]TERMUX EDITION  •  by BLAZING[/]",
        padding=(0,1)))

# =============================================================================
# SUBMENUS
# =============================================================================
def submenu(title, items):
    banner()
    t = Table(box=box.SIMPLE, show_header=False, padding=(0,1))
    t.add_column(style="yellow",    width=5)
    t.add_column(style="bold white",width=22)
    t.add_column(style="dim white")
    for code, name, desc in items:
        t.add_row(f"[{code}]", name, desc)
    t.add_row("[0]", "↩ VOLTAR", "")
    console.print(Panel(t, title=f"[bold yellow]{title}[/]",
        border_style="yellow dim", padding=(0,1)))

# =============================================================================
# HELPERS
# =============================================================================
def section(t): console.print(); console.print(Rule(f"[bold yellow]{t}[/]", style="yellow dim"))
def ri(k, v, s=WHITE): console.print(f"  [dim yellow]{k:<24}[/][{s}]{v}[/]")
def ok(m):   console.print(f"  [bold green]✔[/]  {m}")
def warn(m): console.print(f"  [bold yellow]⚠[/]  {m}")
def err(m):  console.print(f"  [bold red]✖[/]  {m}")
def info(m): console.print(f"  [dim white]→[/]  {m}")
def tip(m):  console.print(f"  [bold cyan]💡[/]  [cyan]{m}[/]")
def lnk(n, u, w=20): console.print(f"  [yellow]↗[/] [cyan]{n:<{w}}[/] {u}")

def fetch(url, timeout=10):
    try:
        r = requests.get(url, timeout=timeout,
            headers={'User-Agent': 'Mozilla/5.0 (OSINT-Research; Ethical)'})
        if r.status_code == 200:
            return r.json()
    except: pass
    return None

def press_enter():
    console.print()
    Prompt.ask("[dim yellow]  ↩  ENTER para voltar[/]", default="")

def log_session(module, target, summary):
    SESSION_LOG.append({
        'module': module, 'target': target,
        'summary': summary,
        'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    })

def risk_bar(score, label, style):
    filled = int(score / 100 * 36)
    bar = "█" * filled + "░" * (36 - filled)
    console.print(f"\n  [{style}]{bar}[/]")
    console.print(f"  [{style}]{label}[/]  [dim]({score}/100)[/]\n")

def spin(desc):
    return Progress(SpinnerColumn(style="yellow"),
                    TextColumn(f"[yellow]{desc}"),
                    transient=True)

# =============================================================================
# CATEGORIA A — OSINT
# =============================================================================

def scan_ip(ip_arg=None, silent=False):
    if not silent:
        banner(); section("📡  IP SCAN — 4 APIs PARALELAS"); console.print()
        tip("Use IPs públicos. 192.168.x / 10.x / 127.x não funcionam.")
        console.print()

    ip = ip_arg or Prompt.ask("  [yellow]Target IP[/]").strip()
    if not ip: err("IP não fornecido."); press_enter() if not silent else None; return None
    if re.match(r'^(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.|127\.|::1|0\.)', ip):
        err("IP privado/reservado."); press_enter() if not silent else None; return None

    results = {}

    def get_ipapi(i):
        d = fetch(f"http://ip-api.com/json/{i}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,proxy,hosting,query", timeout=10)
        results['a'] = d

    def get_ipwho(i):
        d = fetch(f"https://ipwho.is/{i}", timeout=10)
        results['b'] = d

    def get_ipinfo(i):
        d = fetch(f"https://ipinfo.io/{i}/json", timeout=10)
        results['c'] = d

    def get_ipapico(i):
        d = fetch(f"https://ipapi.co/{i}/json/", timeout=10)
        results['d'] = d

    with spin("Consultando 4 APIs...") as p:
        p.add_task("", total=None)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
            futs = [ex.submit(fn, ip) for fn in [get_ipapi, get_ipwho, get_ipinfo, get_ipapico]]
            concurrent.futures.wait(futs, timeout=15)

    d1=results.get('a',{}); d2=results.get('b',{})
    d3=results.get('c',{}); d4=results.get('d',{})

    ok1 = d1.get('status') == 'success'
    ok2 = d2.get('success') == True
    ok3 = bool(d3.get('ip'))
    ok4 = not d4.get('error')

    if not any([ok1, ok2, ok3, ok4]):
        err("Todas as APIs falharam.")
        tip("Tente com 8.8.8.8 para testar a conexão.")
        press_enter() if not silent else None; return None

    def best(*vals):
        for v in vals:
            if v and str(v) not in ('None','','—','null'): return str(v)
        return '—'

    country  = best(d1.get('country'),    d2.get('country'),       d4.get('country_name'),  d3.get('country'))
    cc       = best(d1.get('countryCode'),d2.get('country_code'),  d4.get('country_code'))
    region   = best(d1.get('regionName'), d2.get('region'),        d4.get('region'),         d3.get('region'))
    city     = best(d1.get('city'),       d2.get('city'),          d4.get('city'),           d3.get('city'))
    postal   = best(d1.get('zip'),        d2.get('postal'),        d4.get('postal'))
    lat      = best(d1.get('lat'),        d2.get('latitude'),      d4.get('latitude'))
    lon      = best(d1.get('lon'),        d2.get('longitude'),     d4.get('longitude'))
    tz       = best(d1.get('timezone'),   (d2.get('timezone') or {}).get('id'), d4.get('timezone'), d3.get('timezone'))
    isp      = best(d1.get('isp'),        (d2.get('connection') or {}).get('isp'), d4.get('isp'), d3.get('org'))
    org      = best(d1.get('org'),        (d2.get('connection') or {}).get('org'), d4.get('org'), d3.get('org'))
    asn      = best(d1.get('as'),         d4.get('asn'),           d3.get('org'))
    hostname = best(d3.get('hostname'),   d2.get('hostname'))
    mobile   = d1.get('mobile', False)
    is_proxy = d1.get('proxy',  False)
    hosting  = d1.get('hosting',False)
    is_eu    = d2.get('is_eu',  False)
    capital  = best(d2.get('capital'))
    currency = best(d4.get('currency_name'))
    calling  = best(d4.get('country_calling_code'))
    ipver    = "IPv6" if ":" in ip else "IPv4"

    org_l  = (str(org)+str(isp)+str(asn)).lower()
    h_hint = bool(re.search(r'hosting|cloud|vps|datacenter|amazon|google|microsoft|digitalocean|linode|vultr|ovh|hetzner|fastly|akamai', org_l))
    t_hint = bool(re.search(r'\btor\b|onion|exit.node', org_l))
    p_hint = is_proxy or bool(re.search(r'proxy|vpn|anonymize|hide|private|nordvpn|expressvpn', org_l))
    hfinal = hosting or h_hint

    if   t_hint:  rs,rl,rc = 96,"CRÍTICO — TOR EXIT",RED
    elif p_hint:  rs,rl,rc = 78,"ALTO — VPN/PROXY",RED
    elif hfinal:  rs,rl,rc = 52,"MÉDIO — DATACENTER",GOLD
    else:         rs,rl,rc = 10,"BAIXO — RESIDENCIAL",GREEN

    sources = []
    if ok1: sources.append('ip-api')
    if ok2: sources.append('ipwho')
    if ok3: sources.append('ipinfo')
    if ok4: sources.append('ipapi.co')

    if not silent:
        section("▸ IDENTIFICAÇÃO")
        ri("IP",         ip,                   GOLD)
        ri("Hostname",   hostname)
        ri("Versão",     ipver,                BLUE)
        ri("APIs OK",    " | ".join(sources),  GREEN)

        section("▸ RISCO")
        risk_bar(rs, rl, rc)
        if mobile:  warn("Rede MÓVEL/CELULAR")
        if hfinal:  warn("DATACENTER/HOSPEDAGEM")
        if p_hint:  warn("VPN ou PROXY")
        if t_hint:  err("NÓ TOR EXIT")
        if is_eu:   info("País UE — GDPR")

        section("▸ GEOLOCALIZAÇÃO")
        ri("País",        f"{country} ({cc})")
        ri("Capital",      capital)
        ri("Região",       region)
        ri("Cidade",       city)
        ri("CEP",          postal)
        ri("Coordenadas",  f"{lat}, {lon}", BLUE)
        ri("Fuso",         tz)
        ri("UE",           "SIM" if is_eu else "NÃO")

        section("▸ REDE")
        ri("ASN",    asn,  GOLD)
        ri("Org.",   org)
        ri("ISP",    isp)
        ri("Mobile", "SIM" if mobile else "NÃO")

        section("▸ PAÍS")
        ri("Moeda",   currency)
        ri("Tel.",    calling)

        if lat != '—' and lon != '—':
            section("▸ MAPA")
            console.print(f"\n  [cyan]OSM:[/] https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=13")
            console.print(f"  [cyan]GMaps:[/] https://maps.google.com/?q={lat},{lon}\n")

        section("▸ INVESTIGAÇÃO")
        for n,u in [
            ("Shodan",      f"https://www.shodan.io/host/{ip}"),
            ("VirusTotal",  f"https://www.virustotal.com/gui/ip-address/{ip}"),
            ("AbuseIPDB",   f"https://www.abuseipdb.com/check/{ip}"),
            ("BGP/ASN",     f"https://bgp.he.net/ip/{ip}"),
            ("CriminalIP",  f"https://www.criminalip.io/asset/report/{ip}"),
            ("GreyNoise",   f"https://www.greynoise.io/viz/ip/{ip}"),
            ("Censys",      f"https://censys.io/hosts/{ip}"),
            ("ThreatBook",  f"https://threatbook.io/ip/{ip}"),
        ]: lnk(n, u)

    log_session("IP SCAN", ip, f"País:{country}|Cidade:{city}|ISP:{isp}|Risco:{rl}")
    if not silent: press_enter()
    return {"ip":ip,"country":country,"cc":cc,"city":city,"lat":lat,"lon":lon,
            "isp":isp,"org":org,"asn":asn,"risk":rl}

def scan_domain(domain_arg=None, silent=False):
    if not silent:
        banner(); section("🌐  DOMÍNIO"); console.print()
        tip("Sem http:// — ex: example.com")
        console.print()

    domain = domain_arg or Prompt.ask("  [yellow]Domínio[/]").strip()
    domain = re.sub(r'^https?://','',domain).split('/')[0].lower().strip()
    if not domain: err("Domínio não fornecido."); press_enter() if not silent else None; return None

    dns_types = ['A','AAAA','MX','NS','TXT','CNAME','SOA']
    dns_res   = {}
    resolver  = dns.resolver.Resolver()
    resolver.timeout = resolver.lifetime = 5

    with spin("Consultando DNS...") as p:
        p.add_task("",total=None)
        for qt in dns_types:
            try:    dns_res[qt] = [str(r) for r in resolver.resolve(domain, qt)]
            except: dns_res[qt] = []

    whois_data = None
    try:
        with spin("Consultando WHOIS...") as p:
            p.add_task("",total=None)
            whois_data = whois.whois(domain)
    except: pass

    subdomains = []
    with spin("Buscando subdomínios...") as p:
        p.add_task("",total=None)
        try:
            crt = fetch(f"https://crt.sh/?q=%.{domain}&output=json", timeout=15)
            if crt:
                seen = set()
                for e in crt:
                    for n in e.get('name_value','').split('\n'):
                        n = n.strip().lstrip('*.')
                        if n and domain in n and n not in seen:
                            seen.add(n); subdomains.append(n)
                subdomains = sorted(set(subdomains))[:40]
        except: pass

    mx_str  = ' '.join(dns_res.get('MX',[])).lower()
    txt_all = ' '.join(dns_res.get('TXT',[])).lower()
    ns_str  = ' '.join(dns_res.get('NS',[])).lower()
    a_recs  = dns_res.get('A',[])
    is_g  = 'google' in mx_str; is_m = 'outlook' in mx_str or 'microsoft' in mx_str
    is_cf = 'cloudflare' in ns_str
    has_spf='v=spf1' in txt_all; has_dmarc='v=dmarc1' in txt_all; has_dkim='v=dkim1' in txt_all
    sec = (33 if has_spf else 0)+(34 if has_dmarc else 0)+(33 if has_dkim else 0)

    if not silent:
        section("▸ GERAL")
        ri("Domínio", domain, GOLD)
        ri("IPs (A)", ', '.join(a_recs) if a_recs else '—', BLUE)
        ri("CDN",     "Cloudflare" if is_cf else "—", GREEN if is_cf else WHITE)
        ri("Email",   "Google" if is_g else "Microsoft" if is_m else "Próprio" if dns_res.get('MX') else "Sem MX")

        section("▸ DNS")
        for qt in dns_types:
            recs = dns_res.get(qt,[])
            if recs:
                console.print(f"\n  [bold yellow]{qt}[/]")
                for r in recs[:4]: console.print(f"    [white]{r}[/]")

        section(f"▸ SUBDOMÍNIOS — {len(subdomains)}")
        if subdomains:
            for s in subdomains[:20]: console.print(f"  [cyan]{s}[/]")
            if len(subdomains)>20: info(f"+{len(subdomains)-20} mais")
        else: info("Nenhum encontrado.")

        section("▸ SEGURANÇA EMAIL")
        ri("SPF",   "✔" if has_spf   else "✖ Ausente", GREEN if has_spf   else RED)
        ri("DMARC", "✔" if has_dmarc else "✖ Ausente", GREEN if has_dmarc else RED)
        ri("DKIM",  "✔" if has_dkim  else "—",          GREEN if has_dkim  else WHITE)
        ri("Score", f"{sec}/100", GREEN if sec>=66 else (GOLD if sec>=33 else RED))

        if whois_data:
            section("▸ WHOIS")
            for k,v in [("Registrar",whois_data.registrar),("Criado",whois_data.creation_date),
                        ("Expira",whois_data.expiration_date),("País",whois_data.country)]:
                if v: ri(k, str(v)[:50])

        section("▸ INVESTIGAÇÃO")
        for n,u in [("Shodan",f"https://www.shodan.io/search?query={domain}"),
                    ("SSL/Certs",f"https://crt.sh/?q={domain}"),
                    ("Wayback",f"https://web.archive.org/web/*/{domain}"),
                    ("VirusTotal",f"https://www.virustotal.com/gui/domain/{domain}"),
                    ("URLScan",f"https://urlscan.io/search/#domain:{domain}")]: lnk(n,u)

    log_session("DOMÍNIO", domain, f"IPs:{','.join(a_recs)}|Subs:{len(subdomains)}|Sec:{sec}/100")
    if not silent: press_enter()
    return {"domain":domain,"a_recs":a_recs,"subdomains":subdomains,"sec_score":sec}

def scan_email(email_arg=None, silent=False):
    if not silent:
        banner(); section("✉  E-MAIL"); console.print()
        console.print()
    email = email_arg or Prompt.ask("  [yellow]Email[/]").strip()
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        err("E-mail inválido."); press_enter() if not silent else None; return None
    user, dom = email.split('@',1)
    resolver = dns.resolver.Resolver(); resolver.timeout=5
    mx,tx,aa = [],[],[]
    with spin("Consultando DNS...") as p:
        p.add_task("",total=None)
        for qt,lst in [('MX',mx),('TXT',tx),('A',aa)]:
            try: lst.extend([str(r) for r in resolver.resolve(dom,qt)])
            except: pass
    mx_s=(' '.join(mx)).lower(); tx_s=(' '.join(tx)).lower()
    is_g='google' in mx_s; is_m='outlook' in mx_s or 'microsoft' in mx_s
    has_mx=bool(mx); has_spf='v=spf1' in tx_s; has_dmarc='v=dmarc1' in tx_s
    prov="Google" if is_g else "Microsoft" if is_m else "Zoho" if 'zoho' in mx_s else "Próprio" if has_mx else "Sem MX"
    if not silent:
        section("▸ VALIDAÇÃO")
        ri("Email",email,GOLD); ri("Usuário",user,BLUE); ri("Domínio",dom)
        ri("IPs",', '.join(aa) if aa else '—',BLUE)
        ri("Aceita emails","✔ SIM" if has_mx else "✖ NÃO",GREEN if has_mx else RED)
        section("▸ INFRAESTRUTURA")
        ri("Provider",prov,GREEN if is_g else WHITE)
        ri("SPF","✔" if has_spf else "✖",GREEN if has_spf else RED)
        ri("DMARC","✔" if has_dmarc else "✖",GREEN if has_dmarc else RED)
        section("▸ INVESTIGAÇÃO")
        for n,u in [("HaveIBeenPwned",f"https://haveibeenpwned.com/account/{email}"),
                    ("Hunter.io",f"https://hunter.io/email-verifier/{email}"),
                    ("Intelligence X",f"https://intelx.io/?s={email}"),
                    ("Epieos",f"https://epieos.com/?q={email}&t=email"),
                    ("Google Dork",f'https://www.google.com/search?q="{email}"')]: lnk(n,u)
    log_session("EMAIL",email,f"Provider:{prov}|SPF:{has_spf}|DMARC:{has_dmarc}")
    if not silent: press_enter()
    return {"email":email,"provider":prov,"has_mx":has_mx}

def scan_username(user_arg=None, silent=False):
    if not silent:
        banner(); section("👤  USERNAME"); console.print()
        tip("Sem @ — ex: blazing")
        console.print()
    username = user_arg or Prompt.ask("  [yellow]Username[/]").strip()
    if not username: err("Username não fornecido."); press_enter() if not silent else None; return None

    api_plats = [
        ("GitHub",    f"https://api.github.com/users/{username}",             lambda d: bool(d.get('login')),          lambda d: f"Repos:{d.get('public_repos',0)}"),
        ("Reddit",    f"https://www.reddit.com/user/{username}/about.json",   lambda d: bool((d.get('data') or {}).get('name')), lambda d: f"Karma:{(d.get('data') or {}).get('total_karma',0)}"),
        ("Dev.to",    f"https://dev.to/api/users/by_username?url={username}", lambda d: bool(d.get('username')),       lambda d: f"Posts:{d.get('articles_count',0)}"),
        ("HN",        f"https://hacker-news.firebaseio.com/v0/user/{username}.json", lambda d: d is not None,          lambda d: f"Karma:{d.get('karma',0)}"),
        ("GitLab",    f"https://gitlab.com/api/v4/users?username={username}", lambda d: isinstance(d,list) and len(d)>0, lambda d: f"Nome:{d[0].get('name','—')}"),
        ("Keybase",   f"https://keybase.io/_/api/1.0/user/lookup.json?usernames={username}", lambda d: (d.get('status') or {}).get('code')==0 and len(d.get('them') or [])>0, lambda d: "OK"),
        ("NPM",       f"https://registry.npmjs.org/-/v1/search?text=maintainer:{username}&size=1", lambda d: (d.get('total') or 0)>0, lambda d: f"Pkgs:{d.get('total',0)}"),
    ]
    confirmed, not_found = [], []
    with Progress(SpinnerColumn(style="yellow"),TextColumn("[yellow]{task.description}"),
                  BarColumn(bar_width=24,style="yellow dim",complete_style="yellow"),transient=True) as prog:
        task = prog.add_task("...",total=len(api_plats))
        for name,api,check,details in api_plats:
            prog.update(task,description=f"  {name}...")
            d = fetch(api)
            try:    found = check(d) if d is not None else False
            except: found = False
            if found:
                try:    det = details(d)
                except: det = ""
                confirmed.append((name, f"https://{'github' if name=='GitHub' else 'reddit.com/user' if name=='Reddit' else name.lower()}.com/{username}", det))
            else: not_found.append(name)
            prog.advance(task)

    if not silent:
        section(f"▸ RESULTADO — @{username}")
        ri("Confirmados",  str(len(confirmed)),  GREEN)
        ri("Ausentes",     str(len(not_found)),  RED)

        if confirmed:
            section("▸ CONFIRMADOS")
            for name,url,det in confirmed:
                console.print(f"  [bold green]✔[/]  [bold]{name:<14}[/] [dim]{det}[/]")
                console.print(f"    [cyan]{url}[/]")

        section("▸ VERIFICAR MANUALMENTE")
        manual = [
            ("Twitter/X",  f"https://twitter.com/{username}"),
            ("Instagram",  f"https://instagram.com/{username}/"),
            ("TikTok",     f"https://tiktok.com/@{username}"),
            ("LinkedIn",   f"https://linkedin.com/in/{username}"),
            ("YouTube",    f"https://youtube.com/@{username}"),
            ("Twitch",     f"https://twitch.tv/{username}"),
            ("HackTheBox", f"https://app.hackthebox.com/users/{username}"),
            ("TryHackMe",  f"https://tryhackme.com/p/{username}"),
            ("Telegram",   f"https://t.me/{username}"),
            ("Steam",      f"https://steamcommunity.com/id/{username}"),
            ("Spotify",    f"https://open.spotify.com/user/{username}"),
            ("Snapchat",   f"https://snapchat.com/add/{username}"),
        ]
        for name,url in manual: lnk(name,url)

        section("▸ FERRAMENTAS")
        for n,u in [("WhatsMyName",f"https://whatsmyname.app/?q={username}"),
                    ("Intelligence X",f"https://intelx.io/?s={username}"),
                    ("Epieos",f"https://epieos.com/?q={username}")]: lnk(n,u)

    log_session("USERNAME",username,f"Confirmados:{len(confirmed)}")
    if not silent: press_enter()
    return {"username":username,"confirmed":confirmed}

def scan_person():
    banner(); section("🕵️  PESSOA"); console.print()
    name = Prompt.ask("  [yellow]Nome completo[/]").strip()
    if not name: err("Nome não fornecido."); press_enter(); return
    ctx  = Prompt.ask("  [yellow]Contexto (opcional)[/]", default="").strip()
    enc  = urllib.parse.quote(name)
    encc = urllib.parse.quote(f"{name} {ctx}" if ctx else name)

    section("▸ REDES SOCIAIS")
    for n,u in [("LinkedIn",f'https://www.google.com/search?q="{enc}"+site:linkedin.com'),
                ("Twitter",f'https://www.google.com/search?q="{enc}"+site:twitter.com'),
                ("Instagram",f'https://www.google.com/search?q="{enc}"+site:instagram.com'),
                ("Facebook",f'https://www.google.com/search?q="{enc}"+site:facebook.com'),
                ("GitHub",f'https://www.google.com/search?q="{enc}"+site:github.com')]: lnk(n,u)

    section("▸ DOCUMENTOS")
    for n,u in [("PDFs",f'https://www.google.com/search?q="{encc}"+filetype:pdf'),
                ("Google Docs",f'https://www.google.com/search?q="{encc}"+site:docs.google.com'),
                ("SlideShare",f'https://www.google.com/search?q="{encc}"+site:slideshare.net')]: lnk(n,u)

    section("▸ OSINT")
    for n,u in [("Intelligence X",f"https://intelx.io/?s={enc}"),
                ("Epieos",f"https://epieos.com/?q={enc}"),
                ("WebMii",f"https://webmii.com/people?n={enc}"),
                ("DuckDuckGo",f'https://duckduckgo.com/?q="{encc}"')]: lnk(n,u)

    section("▸ BRASIL")
    for n,u in [("Gov.br",f'https://www.google.com/search?q="{encc}"+site:gov.br'),
                ("JusBrasil",f'https://www.google.com/search?q="{encc}"+site:jusbrasil.com.br'),
                ("Lattes",f'https://buscatextual.cnpq.br/buscatextual/busca.do?textoBusca={enc}'),
                ("Escavador",f'https://www.google.com/search?q="{encc}"+site:escavador.com')]: lnk(n,u)

    section("▸ DORKS")
    for n,u in [("+ email",f'https://www.google.com/search?q="{encc}"+email'),
                ("+ telefone",f'https://www.google.com/search?q="{encc}"+telefone'),
                ("+ endereço",f'https://www.google.com/search?q="{encc}"+endereço')]: lnk(n,u)

    log_session("PESSOA",name,f"Ctx:{ctx}")
    press_enter()

def scan_phone():
    banner(); section("📞  TELEFONE"); console.print()
    phone = Prompt.ask("  [yellow]Número (com +55)[/]").strip()
    if not phone: err("Não fornecido."); press_enter(); return
    clean=re.sub(r'[^\d+]','',phone)
    is_br=clean.startswith('+55') or clean.startswith('55')
    cc='55' if is_br else '?'
    digits=re.sub(r'^\+?55','',clean) if is_br else clean
    is_mob=is_br and len(digits)>=10 and len(digits)>2 and digits[2]=='9'
    ddd=digits[:2] if is_br and len(digits)>=2 else '—'
    e164=clean if clean.startswith('+') else '+'+clean
    section("▸ ANÁLISE")
    ri("Número",phone,GOLD); ri("País","Brasil 🇧🇷" if is_br else "Verificar")
    ri("DDD",ddd); ri("Tipo","CELULAR" if is_mob else "FIXO",GREEN if is_mob else GOLD)
    ri("E.164",e164,BLUE)
    section("▸ INVESTIGAÇÃO")
    for n,u in [("TrueCaller",f"https://www.truecaller.com/search/br/{clean}"),
                ("Google",f'https://www.google.com/search?q="{phone}"'),
                ("Epieos",f"https://epieos.com/?q={phone}&t=phone"),
                ("WhatsApp",f"https://wa.me/{clean.lstrip('+')}")]: lnk(n,u)
    log_session("TELEFONE",phone,f"Tipo:{'celular' if is_mob else 'fixo'}|DDD:{ddd}")
    press_enter()

def keyword_hunter():
    banner(); section("🔎  KEYWORD HUNTER"); console.print()
    keyword = Prompt.ask("  [yellow]Palavra-chave[/]").strip()
    if not keyword: err("Não fornecida."); press_enter(); return
    enc=urllib.parse.quote(f'"{keyword}"'); enc2=urllib.parse.quote(keyword)
    section("▸ MOTORES DE BUSCA")
    for n,u in [("Google",f"https://www.google.com/search?q={enc}"),
                ("Bing",f"https://www.bing.com/search?q={enc}"),
                ("DuckDuckGo",f"https://duckduckgo.com/?q={enc}"),
                ("Yandex",f"https://yandex.com/search/?text={enc2}")]: lnk(n,u)
    section("▸ FONTES ESPECIALIZADAS")
    for n,u in [("GitHub Code",f"https://github.com/search?q={enc2}&type=code"),
                ("Grep.app",f"https://grep.app/search?q={enc2}"),
                ("Pastebin",f"https://pastebin.com/search?q={enc2}"),
                ("Reddit",f"https://www.reddit.com/search/?q={enc2}"),
                ("HackerNews",f"https://hn.algolia.com/?q={enc2}"),
                ("Intelligence X",f"https://intelx.io/?s={enc2}"),
                ("Ahmia",f"https://ahmia.fi/search/?q={enc2}")]: lnk(n,u)
    section("▸ DORKS AUTOMÁTICOS")
    for n,u in [(f"PDF",f'https://www.google.com/search?q="{enc}"+filetype:pdf'),
                (f"Gov.br",f'https://www.google.com/search?q="{enc}"+site:gov.br'),
                (f"Leak/Breach",f'https://www.google.com/search?q="{enc}"+leak+OR+breach')]: lnk(n,u,8)
    log_session("KEYWORD",keyword,"Busca multi-fonte")
    press_enter()

# =============================================================================
# CATEGORIA B — DARKNET
# =============================================================================

def dark_links():
    banner(); section("🌑  DARK LINKS — RECURSOS LÍCITOS"); console.print()
    warn("Links .onion requerem Tor Browser.")
    tip("Download Tor: https://www.torproject.org")
    console.print()
    section("▸ MOTORES (sem Tor)")
    for n,u,d in [("Ahmia","https://ahmia.fi","Busca dark web indexada"),
                  ("DarkSearch","https://darksearch.io","Motor indexado público"),
                  ("OnionSearch","https://onionsearchengine.com","Domínios .onion")]:
        console.print(f"\n  [bold cyan]{n}[/]  [dim]{d}[/]\n  [dim white]{u}[/]")
    section("▸ EMAIL ANÔNIMO")
    for n,u,d in [("ProtonMail","https://proton.me","E2E criptografado"),
                  ("Tutanota","https://tuta.com","Open source cifrado"),
                  ("Guerrilla Mail","https://guerrillamail.com","Temporário 60min")]:
        console.print(f"\n  [bold cyan]{n}[/]  [dim]{d}[/]\n  [dim white]{u}[/]")
    section("▸ FERRAMENTAS DE PRIVACIDADE")
    for n,u,d in [("Tor Project","https://www.torproject.org","Download Tor Browser"),
                  ("Tails OS","https://tails.boum.org","SO anônimo em pendrive"),
                  ("I2P","https://geti2p.net","Rede anônima alternativa"),
                  ("SecureDrop","https://securedrop.org","Plataforma whistleblowers")]:
        console.print(f"\n  [bold cyan]{n}[/]  [dim]{d}[/]\n  [dim white]{u}[/]")
    log_session("DARK LINKS","—","Links lícitos")
    press_enter()

def dark_search():
    banner(); section("🔍  DARK SEARCH"); console.print()
    keyword = Prompt.ask("  [yellow]Palavra-chave[/]").strip()
    if not keyword: err("Não fornecida."); press_enter(); return
    enc=urllib.parse.quote(keyword)
    section("▸ SEM TOR")
    for n,u in [("Ahmia",f"https://ahmia.fi/search/?q={enc}"),
                ("DarkSearch",f"https://darksearch.io/search?query={enc}"),
                ("OnionSearch",f"https://onionsearchengine.com/search.php?search={enc}")]: lnk(n,u)
    section("▸ VIA TOR BROWSER (copie a URL)")
    for n,u in [("Torch",f"http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5ayieeo2cfvwdnhjde.onion/4a1f6b371c/search.cgi?q={enc}"),
                ("Haystak",f"http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/?q={enc}")]:
        console.print(f"  [yellow]◆[/] [bold]{n}[/]\n    [dim white]{u[:60]}...[/]")
    section("▸ COMPLEMENTAR")
    for n,u in [("Intelligence X",f"https://intelx.io/?s={enc}"),
                ("Pastebin",f"https://pastebin.com/search?q={enc}")]: lnk(n,u)
    log_session("DARK SEARCH",keyword,"Busca dark")
    press_enter()

def anon_email():
    banner(); section("✉  EMAIL ANÔNIMO"); console.print()
    section("▸ GERAR VIA API — GUERRILLA MAIL")
    with spin("Gerando e-mail temporário...") as p:
        p.add_task("",total=None)
        try:
            r = fetch("https://api.guerrillamail.com/ajax.php?f=get_email_address", timeout=10)
            if r and r.get('email_addr'):
                email = r.get('email_addr')
                console.print(f"\n  [bold green]✔  E-mail gerado:[/]")
                console.print(f"\n  [bold yellow]  ›  {email}[/]\n")
                console.print(f"  [dim]Acesse: https://www.guerrillamail.com[/]")
                console.print(f"  [dim]Expira em ~60 minutos[/]\n")
            else: warn("API offline — use os links abaixo.")
        except: warn("API offline — use os links abaixo.")

    section("▸ SERVIÇOS ALTERNATIVOS")
    for n,u,d in [("Guerrilla Mail","https://www.guerrillamail.com","60min"),
                  ("Temp Mail","https://temp-mail.org","Descartável"),
                  ("10 Minute Mail","https://10minutemail.com","10min"),
                  ("Mailinator","https://www.mailinator.com","Público"),
                  ("YOPmail","https://yopmail.com","Permanente gratuito"),
                  ("ProtonMail","https://proton.me","Criptografado"),
                  ("Tutanota","https://tuta.com","Criptografado")]:
        lnk(n,u); info(d)
    press_enter()

def paste_monitor():
    banner(); section("📋  PASTE MONITOR"); console.print()
    target = Prompt.ask("  [yellow]E-mail, domínio ou palavra-chave[/]").strip()
    if not target: err("Não fornecido."); press_enter(); return
    enc=urllib.parse.quote(target)
    section("▸ SITES DE PASTE")
    for n,u in [("Pastebin",f"https://pastebin.com/search?q={enc}"),
                ("PastesDump",f"https://psbdmp.ws/search/{enc}"),
                ("Ghostbin","https://ghostbin.com"),
                ("ControlC",f"https://controlc.com/search?q={enc}")]: lnk(n,u)
    section("▸ CÓDIGO PÚBLICO")
    for n,u in [("GitHub Code",f"https://github.com/search?q={enc}&type=code"),
                ("Grep.app",f"https://grep.app/search?q={enc}"),
                ("GitLab",f"https://gitlab.com/search?search={enc}")]: lnk(n,u)
    section("▸ INTELIGÊNCIA")
    for n,u in [("Intelligence X",f"https://intelx.io/?s={enc}"),
                ("Google Dork",f'https://www.google.com/search?q=site:pastebin.com+"{enc}"')]: lnk(n,u)
    log_session("PASTE MONITOR",target,"Busca em pastes")
    press_enter()

# =============================================================================
# CATEGORIA C — SEGURANÇA
# =============================================================================

def hash_analyzer():
    banner(); section("🔑  HASH ANALYZER"); console.print()
    h = Prompt.ask("  [yellow]Hash[/]").strip()
    if not h: err("Não fornecido."); press_enter(); return
    clean=re.sub(r'[^a-fA-F0-9]','',h); length=len(clean)
    is_hex=bool(re.match(r'^[a-fA-F0-9]+$',h)); types=[]
    if h.startswith('$2'):   types.append(("bcrypt","Senhas web"))
    elif h.startswith('$6$'):types.append(("sha512crypt","Linux shadow"))
    elif h.startswith('$1$'):types.append(("md5crypt","Linux legado"))
    elif is_hex:
        if length==32:  types+=[("MD5","128-bit — comum CTFs"),("NTLM","Windows"),("LM","Windows legado")]
        if length==40:  types+=[("SHA-1","160-bit depreciado"),("MySQL4","MySQL")]
        if length==64:  types+=[("SHA-256","256-bit seguro"),("RIPEMD-256","256-bit")]
        if length==128: types+=[("SHA-512","512-bit"),("Whirlpool","512-bit")]
    if not types: types.append(("Desconhecido","—"))
    section("▸ IDENTIFICAÇÃO")
    ri("Hash",h[:60]+("..." if len(h)>60 else ""),GOLD)
    ri("Tamanho",f"{length}hex = {length*4}bits")
    ri("Formato","✔ Hex" if is_hex else "Não-hex",GREEN if is_hex else GOLD)
    console.print()
    for t,i in types: console.print(f"    [bold yellow]{t:<18}[/] [dim]{i}[/]")
    section("▸ CRACK/LOOKUP")
    for n,u in [("CrackStation","https://crackstation.net"),
                ("Hashes.com","https://hashes.com/en/decrypt/hash"),
                ("HashKiller","https://hashkiller.io"),
                ("CMD5","https://www.cmd5.org")]: lnk(n,u)
    if length==32: tip("MD5 de 32 chars — alta chance em bases públicas!")
    log_session("HASH",h[:32],f"Tipo:{','.join(t for t,_ in types)}")
    press_enter()

def password_analyzer():
    banner(); section("🔒  PASSWORD ANALYZER"); console.print()
    tip("A senha NÃO sai do seu dispositivo.")
    console.print()
    import getpass
    try:    pwd = getpass.getpass("  → Senha (oculta): ")
    except: pwd = Prompt.ask("  [yellow]Senha[/]", password=True)
    if not pwd: err("Não fornecida."); press_enter(); return

    import math
    length=len(pwd)
    has_upper=bool(re.search(r'[A-Z]',pwd)); has_lower=bool(re.search(r'[a-z]',pwd))
    has_digit=bool(re.search(r'\d',pwd)); has_special=bool(re.search(r'[^a-zA-Z0-9]',pwd))
    charset = (26 if has_lower else 0)+(26 if has_upper else 0)+(10 if has_digit else 0)+(32 if has_special else 0)
    entropy = length*math.log2(charset) if charset>0 else 0
    if   entropy>=80: strength,sc = "MUITO FORTE",GREEN
    elif entropy>=60: strength,sc = "FORTE",GREEN
    elif entropy>=40: strength,sc = "MÉDIO",GOLD
    elif entropy>=25: strength,sc = "FRACO",RED
    else:             strength,sc = "MUITO FRACO",RED

    combinations = charset**length if charset>0 else 1
    seconds = combinations/10_000_000_000
    if   seconds<60:       ts=f"{seconds:.1f}s"
    elif seconds<3600:     ts=f"{seconds/60:.1f}min"
    elif seconds<86400:    ts=f"{seconds/3600:.1f}h"
    elif seconds<31536000: ts=f"{seconds/86400:.1f}dias"
    else:                  ts=f"{seconds/31536000:.1f}anos"

    section("▸ ANÁLISE")
    ri("Comprimento",f"{length} chars",GREEN if length>=12 else RED)
    ri("Maiúsculas","✔" if has_upper else "✖",GREEN if has_upper else RED)
    ri("Minúsculas","✔" if has_lower else "✖",GREEN if has_lower else RED)
    ri("Números","✔" if has_digit else "✖",GREEN if has_digit else RED)
    ri("Especiais","✔" if has_special else "✖",GREEN if has_special else RED)
    ri("Entropia",f"{entropy:.1f} bits",sc)
    ri("Força",strength,sc)
    ri("Tempo crack",ts,sc)

    section("▸ VERIFICAR VAZAMENTOS — HIBP")
    try:
        sha1=hashlib.sha1(pwd.encode()).hexdigest().upper()
        prefix=sha1[:5]; suffix=sha1[5:]
        r=requests.get(f"https://api.pwnedpasswords.com/range/{prefix}",timeout=8,
            headers={'User-Agent':'OSINT-Tool'})
        if r.status_code==200:
            count=0
            for line in r.text.split('\n'):
                parts=line.strip().split(':')
                if len(parts)==2 and parts[0]==suffix: count=int(parts[1]); break
            if count>0: err(f"Senha em {count:,} vazamentos! MUDE JÁ.")
            else:       ok("Senha NÃO encontrada em vazamentos conhecidos.")
    except: warn("Não foi possível verificar HIBP.")

    log_session("PASSWORD","[OCULTO]",f"Força:{strength}|Entropia:{entropy:.1f}bits")
    press_enter()

def malware_checker():
    banner(); section("🦠  MALWARE CHECKER"); console.print()
    h = Prompt.ask("  [yellow]Hash MD5/SHA1/SHA256 do arquivo[/]").strip()
    if not h: err("Não fornecido."); press_enter(); return
    section("▸ MALWAREBAZAAR")
    with spin("Consultando MalwareBazaar...") as p:
        p.add_task("",total=None)
        try:
            r=requests.post("https://mb-api.abuse.ch/api/v1/",
                data={'query':'get_info','hash':h},timeout=10,
                headers={'User-Agent':'Mozilla/5.0'})
            if r.status_code==200:
                d=r.json()
                if d.get('query_status')=='ok' and d.get('data'):
                    item=d['data'][0]
                    err("MALWARE DETECTADO!")
                    ri("Nome",item.get('file_name','—'),RED)
                    ri("Tipo",item.get('file_type','—'),RED)
                    ri("Família",item.get('signature','—'),RED)
                    ri("1ª vez visto",item.get('first_seen','—'))
                else: ok("Hash NÃO encontrado no MalwareBazaar.")
        except: warn("MalwareBazaar não respondeu.")
    section("▸ FONTES ADICIONAIS")
    for n,u in [("VirusTotal",f"https://www.virustotal.com/gui/file/{h}"),
                ("MalwareBazaar",f"https://bazaar.abuse.ch/sample/{h}/"),
                ("Hybrid Analysis",f"https://www.hybrid-analysis.com/search?query={h}"),
                ("OTX AlienVault",f"https://otx.alienvault.com/indicator/file/{h}")]: lnk(n,u)
    log_session("MALWARE",h[:32],"Verificação hash")
    press_enter()

def threat_intel():
    banner(); section("🚨  THREAT INTEL"); console.print()
    target = Prompt.ask("  [yellow]IP ou domínio[/]").strip()
    if not target: err("Não fornecido."); press_enter(); return
    enc=urllib.parse.quote(target)
    section("▸ FONTES THREAT INTEL")
    for n,u in [("VirusTotal",f"https://www.virustotal.com/gui/ip-address/{target}"),
                ("AbuseIPDB",f"https://www.abuseipdb.com/check/{target}"),
                ("GreyNoise",f"https://www.greynoise.io/viz/ip/{target}"),
                ("Shodan",f"https://www.shodan.io/host/{target}"),
                ("ThreatFox",f"https://threatfox.abuse.ch/browse/?query={enc}"),
                ("OTX AlienVault",f"https://otx.alienvault.com/indicator/ip/{target}"),
                ("CriminalIP",f"https://www.criminalip.io/asset/report/{target}"),
                ("Pulsedive",f"https://pulsedive.com/indicator/?ioc={enc}")]: lnk(n,u)
    log_session("THREAT INTEL",target,"Análise de ameaça")
    press_enter()

def breach_checker():
    banner(); section("💧  BREACH CHECKER"); console.print()
    target = Prompt.ask("  [yellow]E-mail, domínio ou username[/]").strip()
    if not target: err("Não fornecido."); press_enter(); return
    enc=urllib.parse.quote(target)
    section("▸ VERIFICAÇÃO AUTOMÁTICA")
    if '@' in target:
        with spin("Consultando HaveIBeenPwned...") as p:
            p.add_task("",total=None)
            try:
                r=requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(target)}",
                    timeout=10,headers={'User-Agent':'OSINT-Tool','hibp-api-key':''})
                if r.status_code==200:
                    breaches=r.json(); err(f"Encontrado em {len(breaches)} vazamentos!")
                    for b in breaches[:5]: console.print(f"  [red]  ✖  {b.get('Name','—')} ({b.get('BreachDate','—')})[/]")
                elif r.status_code==404: ok("Não encontrado em vazamentos HIBP.")
                else: info("Verificação manual necessária.")
            except: warn("HIBP não respondeu.")
    section("▸ FONTES MANUAIS")
    for n,u,d in [("HaveIBeenPwned",f"https://haveibeenpwned.com/account/{enc}","✔ Gratuito"),
                  ("Intelligence X",f"https://intelx.io/?s={enc}","Dark web"),
                  ("Dehashed",f"https://dehashed.com/search?query={enc}","Credenciais"),
                  ("LeakCheck",f"https://leakcheck.io/?query={enc}","Rápido"),
                  ("Epieos",f"https://epieos.com/?q={enc}&t=email","OSINT"),
                  ("Pastebin",f'https://www.google.com/search?q=site:pastebin.com+"{enc}"',"Pastes")]:
        console.print(f"  [yellow]↗[/] [cyan]{n:<20}[/] [dim]{d}[/]  {u}")
    log_session("BREACH",target,"Verificação vazamentos")
    press_enter()

# =============================================================================
# CATEGORIA D — REDE
# =============================================================================

def shodan_explorer():
    banner(); section("🔭  SHODAN EXPLORER"); console.print()
    query = Prompt.ask("  [yellow]Busca[/]").strip()
    if not query: err("Não fornecida."); press_enter(); return
    enc=urllib.parse.quote(query)
    section("▸ BUSCA")
    for n,u in [("Shodan Search",f"https://www.shodan.io/search?query={enc}"),
                ("Censys",f"https://search.censys.io/hosts?q={enc}"),
                ("Shodan Exploits",f"https://exploits.shodan.io/?q={enc}")]: lnk(n,u)
    section("▸ QUERIES PRONTAS")
    for name,q in [("Câmeras Brasil",   'country:BR product:"webcam"'),
                   ("MongoDB exposto",   'product:"MongoDB" -authentication'),
                   ("Elasticsearch",     'product:"Elastic" port:9200'),
                   ("FTP anônimo",       'port:21 Anonymous'),
                   ("Painéis admin",     'http.title:"admin panel"')]:
        console.print(f"  [yellow]◆[/] [bold white]{name:<22}[/] [dim]{q}[/]")
    log_session("SHODAN",query,"Busca Shodan")
    press_enter()

def certwatch():
    banner(); section("🔒  CERTWATCH"); console.print()
    domain = Prompt.ask("  [yellow]Domínio[/]").strip().lower()
    domain = re.sub(r'^https?://','',domain).split('/')[0]
    if not domain: err("Não fornecido."); press_enter(); return
    subdomains=[]
    with spin("Consultando crt.sh...") as p:
        p.add_task("",total=None)
        try:
            data=fetch(f"https://crt.sh/?q=%.{domain}&output=json",timeout=15)
            if data:
                seen=set()
                for e in data:
                    for n in e.get('name_value','').split('\n'):
                        n=n.strip().lstrip('*.')
                        if n and domain in n and n not in seen: seen.add(n); subdomains.append(n)
                subdomains=sorted(set(subdomains))
        except: pass
    section(f"▸ SUBDOMÍNIOS — {len(subdomains)}")
    if subdomains:
        for s in subdomains[:30]: console.print(f"  [cyan]{s}[/]")
        if len(subdomains)>30: info(f"+{len(subdomains)-30} mais")
    else: info("Nenhum encontrado.")
    section("▸ ANÁLISE SSL")
    for n,u in [("SSLLabs",f"https://www.ssllabs.com/ssltest/analyze.html?d={domain}"),
                ("SecurityHeaders",f"https://securityheaders.com/?q={domain}"),
                ("crt.sh",f"https://crt.sh/?q=%.{domain}")]: lnk(n,u)
    log_session("CERTWATCH",domain,f"Subs:{len(subdomains)}")
    press_enter()

def url_analyzer():
    banner(); section("🔗  URL ANALYZER"); console.print()
    url = Prompt.ask("  [yellow]URL[/]").strip()
    if not url: err("Não fornecida."); press_enter(); return
    if not url.startswith('http'): url='https://'+url
    from urllib.parse import urlparse
    parsed=urlparse(url); hostname=parsed.hostname or '—'
    params=parsed.query or ''
    section("▸ ANATOMIA")
    ri("URL",url[:50]+(("...") if len(url)>50 else ""),GOLD)
    ri("Domínio",hostname); ri("Parâmetros",params if params else "Nenhum",GOLD if params else WHITE)
    ri("Protocolo","HTTPS ✔" if url.startswith('https') else "HTTP ✖",GREEN if url.startswith('https') else RED)
    section("▸ HEADERS AO VIVO")
    try:
        r=requests.get(url,timeout=10,headers={'User-Agent':'Mozilla/5.0'},allow_redirects=True)
        ri("Status",str(r.status_code),GREEN if r.status_code==200 else RED)
        ri("Server",r.headers.get('Server','—'),GOLD)
        ri("X-Powered-By",r.headers.get('X-Powered-By','—'),GOLD)
        ri("HSTS","✔" if r.headers.get('Strict-Transport-Security') else "✖",
           GREEN if r.headers.get('Strict-Transport-Security') else RED)
        if r.history: info(f"Redirecionamentos: {len(r.history)}")
    except: warn("Não foi possível conectar.")
    section("▸ REPUTAÇÃO")
    for n,u in [("VirusTotal",f"https://www.virustotal.com/gui/url/{url}"),
                ("URLScan",f"https://urlscan.io/search/#page.url:{url}"),
                ("Google Safety",f"https://transparencyreport.google.com/safe-browsing/search?url={url}"),
                ("PhishTank",f"https://www.phishtank.com/phish_search.php?valid=y&search={hostname}"),
                ("Wayback",f"https://web.archive.org/web/*/{url}")]: lnk(n,u)
    log_session("URL",url,f"Domínio:{hostname}")
    press_enter()

def metascraper():
    banner(); section("📄  METASCRAPER"); console.print()
    console.print("  [1]  URL / Página web\n  [2]  Arquivo local\n")
    choice = Prompt.ask("  [yellow]Escolha[/]",choices=["1","2"],default="1")
    if choice=="1":
        url = Prompt.ask("  [yellow]URL[/]").strip()
        if not url: err("Não fornecida."); press_enter(); return
        if not url.startswith('http'): url='https://'+url
        with spin("Analisando...") as p:
            p.add_task("",total=None)
            try: r=requests.get(url,timeout=12,headers={'User-Agent':'Mozilla/5.0'}); html=r.text
            except Exception as ex: err(f"Erro: {ex}"); press_enter(); return
        section("▸ HEADERS")
        ri("Status",str(r.status_code),GREEN if r.status_code==200 else RED)
        ri("Server",r.headers.get('Server','—'),GOLD)
        ri("X-Powered-By",r.headers.get('X-Powered-By','—'),GOLD)
        ri("HSTS","✔" if r.headers.get('Strict-Transport-Security') else "✖",GREEN if r.headers.get('Strict-Transport-Security') else RED)
        ri("CSP","✔" if r.headers.get('Content-Security-Policy') else "✖",GREEN if r.headers.get('Content-Security-Policy') else RED)
        section("▸ TECNOLOGIAS")
        TECH={'WordPress':r'wp-content','React':r'react\.js|__NEXT_DATA__','Vue.js':r'vue\.js',
              'jQuery':r'jquery\.js','Bootstrap':r'bootstrap\.css','GA':r'gtag\(',
              'Cloudflare':r'cloudflare','Next.js':r'__NEXT_DATA__','Laravel':r'laravel_session'}
        found=[t for t,p in TECH.items() if re.search(p,html,re.I)]
        for t in found: ok(t)
        if not found: info("Nenhuma identificada.")
        log_session("METASCRAPER",url,f"Server:{r.headers.get('Server','—')}|Techs:{','.join(found)}")
    else:
        fpath=Prompt.ask("  [yellow]Caminho[/]").strip()
        if not os.path.exists(fpath): err("Não encontrado."); press_enter(); return
        stat=os.stat(fpath)
        section("▸ METADADOS")
        ri("Arquivo",fpath,GOLD); ri("Tamanho",f"{stat.st_size/1024:.2f}KB")
        ri("Modificado",datetime.fromtimestamp(stat.st_mtime).strftime('%d/%m/%Y %H:%M'))
        section("▸ HASH")
        with open(fpath,'rb') as f: content=f.read()
        ri("MD5",  hashlib.md5(content).hexdigest(),  BLUE)
        ri("SHA256",hashlib.sha256(content).hexdigest(),BLUE)
        log_session("METASCRAPER",fpath,f"Tamanho:{stat.st_size}B")
    press_enter()

def whois_history():
    banner(); section("🌐  WHOIS HISTORY"); console.print()
    domain=Prompt.ask("  [yellow]Domínio[/]").strip()
    domain=re.sub(r'^https?://','',domain).split('/')[0].lower()
    if not domain: err("Não fornecido."); press_enter(); return
    with spin("Consultando WHOIS...") as p:
        p.add_task("",total=None)
        try:
            wd=whois.whois(domain)
            section("▸ WHOIS ATUAL")
            for k,v in [("Domínio",domain),("Registrar",wd.registrar),("Criado",wd.creation_date),
                        ("Expira",wd.expiration_date),("País",wd.country)]:
                if v: ri(k,str(v)[:50])
        except Exception as ex: err(f"WHOIS falhou: {ex}")
    section("▸ HISTÓRICO")
    for n,u in [("ViewDNS",f"https://viewdns.info/iphistory/?domain={domain}"),
                ("SecurityTrails",f"https://securitytrails.com/domain/{domain}/history/a"),
                ("DomainTools",f"https://whois.domaintools.com/{domain}"),
                ("DNSHistory",f"https://dnshistory.org/dns-records/{domain}")]: lnk(n,u)
    log_session("WHOIS",domain,"Histórico WHOIS")
    press_enter()

# =============================================================================
# CATEGORIA E — AUTOMAÇÃO
# =============================================================================

def shadow_recon():
    banner(); section("🦅  SHADOW RECON"); console.print()
    warn("100% passivo — apenas dados públicos.")
    console.print()
    target_type=Prompt.ask("  [yellow]Tipo[/]",choices=["ip","dominio","email","username"],default="dominio")
    target=Prompt.ask("  [yellow]Alvo[/]").strip()
    if not target: err("Não fornecido."); press_enter(); return
    console.print()
    console.print(Panel(f"[bold yellow]SHADOW RECON[/]\n[dim]{target} | {target_type}[/]",border_style="yellow dim"))
    console.print()
    report={"target":target,"type":target_type,"ts":datetime.now().strftime('%d/%m/%Y %H:%M:%S'),"data":{}}

    if target_type=="ip":
        info("→ IP SCAN"); d=scan_ip(target,silent=True)
        if d: report["data"]["ip"]=d
    elif target_type=="dominio":
        info("→ DOMÍNIO"); d=scan_domain(target,silent=True)
        if d:
            report["data"]["domain"]=d
            for ip_a in (d.get("a_recs") or [])[:1]:
                info(f"→ IP SCAN — {ip_a}"); id_=scan_ip(ip_a,silent=True)
                if id_: report["data"][f"ip_{ip_a}"]=id_
    elif target_type=="email":
        info("→ EMAIL"); d=scan_email(target,silent=True)
        if d: report["data"]["email"]=d
        if '@' in target:
            dom=target.split('@')[1]; info(f"→ DOMÍNIO — {dom}"); dd=scan_domain(dom,silent=True)
            if dd: report["data"]["domain"]=dd
    elif target_type=="username":
        info("→ USERNAME"); d=scan_username(target,silent=True)
        if d: report["data"]["username"]=d

    section("▸ SUMÁRIO")
    ri("Alvo",target,GOLD); ri("Módulos",str(len(report["data"])),GREEN)
    console.print()
    for mod,data in report["data"].items():
        console.print(f"  [bold yellow]▸ {mod.upper()}[/]")
        if isinstance(data,dict):
            for k,v in list(data.items())[:3]:
                if v and str(v) not in ('None','[]','{}','—'):
                    console.print(f"    [dim]{k:<18}[/] [white]{str(v)[:40]}[/]")
        console.print()

    fname=REPORTS_DIR/f"recon_{target.replace('.','_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(fname,'w',encoding='utf-8') as f: json.dump(report,f,ensure_ascii=False,indent=2,default=str)
        ok(f"JSON: {fname}")
    except Exception as ex: warn(f"Não foi possível salvar: {ex}")
    log_session("SHADOW RECON",target,f"Módulos:{len(report['data'])}")
    press_enter()

def osint_autopilot():
    banner(); section("🤖  OSINT AUTOPILOT"); console.print()
    tip("Detecta o tipo do alvo e roda todos os módulos automaticamente.")
    console.print()
    target=Prompt.ask("  [yellow]Alvo (IP, domínio, e-mail ou username)[/]").strip()
    if not target: err("Não fornecido."); press_enter(); return

    if re.match(r'^\d+\.\d+\.\d+\.\d+$',target):   detected="ip"
    elif re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$',target): detected="email"
    elif re.match(r'^[a-zA-Z0-9][a-zA-Z0-9\-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$',target): detected="dominio"
    else: detected="username"

    console.print(f"\n  [dim yellow]Tipo detectado:[/] [bold yellow]{detected.upper()}[/]\n")
    if detected=="ip":
        scan_ip(target,silent=True)
    elif detected=="email":
        scan_email(target,silent=True)
        scan_domain(target.split('@')[1],silent=True)
    elif detected=="dominio":
        d=scan_domain(target,silent=True)
        if d and d.get('a_recs'): scan_ip(d['a_recs'][0],silent=True)
    elif detected=="username":
        scan_username(target,silent=True)

    section("▸ CONCLUÍDO")
    ok(f"Análise de {target} finalizada.")
    tip("Use E4 (OSINT Report) para gerar o relatório.")
    log_session("AUTOPILOT",target,f"Tipo:{detected}")
    press_enter()

def dork_builder():
    banner(); section("🔍  DORK BUILDER"); console.print()
    TMPL={
        '1':("Google Docs",'site:docs.google.com "confidential"'),
        '2':("Login Pages",'inurl:login OR inurl:signin intitle:login'),
        '3':("PDFs Expostos",'filetype:pdf "confidential" OR "restricted"'),
        '4':("Câmeras IP",'inurl:view/index.shtml OR inurl:ViewerFrame'),
        '5':("Config Files",'filetype:env DB_PASSWORD OR SECRET_KEY'),
        '6':("SQL Dumps",'filetype:sql "INSERT INTO" OR "CREATE TABLE"'),
        '7':("Senhas Expostas",'intext:password filetype:txt OR filetype:log'),
        '8':("Admin Panels",'inurl:admin OR inurl:wp-admin intitle:"admin"'),
    }
    console.print("  [bold yellow]TEMPLATES:[/]\n")
    for k,(n,_) in TMPL.items(): console.print(f"  [{k}]  {n}")
    console.print("\n  [00]  Manual\n")
    choice=Prompt.ask("  [yellow]Escolha[/]",default="00")
    if choice in TMPL:
        name,query=TMPL[choice]
        site=Prompt.ask("  [yellow]site: (opcional)[/]",default="")
        if site: query=f"site:{site} {query}"
    else:
        fields={k:Prompt.ask(f"  [yellow]{k}:[/]",default="") for k in ['site','inurl','intitle','intext','filetype']}
        free=Prompt.ask("  [yellow]Termo livre:[/]",default="")
        parts=[f"{k}:{v}" for k,v in fields.items() if v]+([free] if free else [])
        query=' '.join(parts)
    qe=urllib.parse.quote(query)
    section("▸ QUERY")
    console.print(f"\n  [bold green]{query}[/]\n")
    section("▸ BUSCAR")
    for n,u in [("Google",f"https://www.google.com/search?q={qe}"),
                ("Bing",f"https://www.bing.com/search?q={qe}"),
                ("DuckDuckGo",f"https://duckduckgo.com/?q={qe}")]: lnk(n,u)
    log_session("DORK",query[:50],"Builder")
    press_enter()

def osint_report():
    banner(); section("📊  OSINT REPORT"); console.print()
    if not SESSION_LOG:
        warn("Nenhuma pesquisa nesta sessão."); tip("Execute módulos primeiro.")
        press_enter(); return
    ts=datetime.now().strftime('%Y%m%d_%H%M%S')
    dt=datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    # TXT
    txt_path=REPORTS_DIR/f"relatorio_{ts}.txt"
    try:
        with open(txt_path,'w',encoding='utf-8') as f:
            f.write("="*60+"\n")
            f.write("  OLHO DE DEUS — TERMUX EDITION v1.0\n")
            f.write("  Criado por: BLAZING | Ethical Hacker & OSINT Specialist\n")
            f.write(f"  Data: {dt}\n"+"="*60+"\n\n")
            for i,e in enumerate(SESSION_LOG,1):
                f.write(f"  [{i:02d}] {e['module']} — {e['target']}\n")
                f.write(f"       {e['summary']}\n")
                f.write(f"       {e['timestamp']}\n\n")
        ok(f"TXT → {txt_path}")
    except Exception as ex: warn(f"Não foi possível salvar TXT: {ex}")

    # HTML
    rows="".join(f"<tr><td>{i:02d}</td><td><span class='b'>{e['module']}</span></td><td class='tg'>{e['target']}</td><td>{e['summary']}</td><td class='ts'>{e['timestamp']}</td></tr>" for i,e in enumerate(SESSION_LOG,1))
    html_path=REPORTS_DIR/f"relatorio_{ts}.html"
    try:
        with open(html_path,'w',encoding='utf-8') as f:
            f.write(f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OLHO DE DEUS — Relatório</title>
<style>body{{background:#02010a;color:#e8d9a0;font-family:monospace;padding:1rem;font-size:14px}}
h1{{color:#f0c040;text-align:center;letter-spacing:.15em}}
.author{{text-align:center;color:#f0c040;margin:.5rem 0}}
.sub{{text-align:center;color:#5a4a28;font-size:.8rem;margin-bottom:1.5rem}}
table{{width:100%;border-collapse:collapse}}
th{{background:#0c0a18;color:#f0c040;padding:.5rem;text-align:left;font-size:.75rem;border-bottom:1px solid rgba(240,192,64,.3)}}
td{{padding:.45rem .5rem;border-bottom:1px solid rgba(240,192,64,.06);font-size:.78rem;vertical-align:top}}
.b{{background:rgba(240,192,64,.08);border:1px solid rgba(240,192,64,.3);color:#f0c040;padding:.1rem .4rem;font-size:.65rem}}
.tg{{color:#00aaff}}.ts{{color:#5a4a28;font-size:.65rem}}
.footer{{text-align:center;margin-top:1.5rem;color:#5a4a28;font-size:.65rem;border-top:1px solid rgba(240,192,64,.1);padding-top:.8rem}}
.footer b{{color:#f0c040}}</style></head><body>
<h1>👁 OLHO DE DEUS</h1>
<div class="author">B L A Z I N G — Ethical Hacker & OSINT Specialist</div>
<div class="sub">{dt} · {len(SESSION_LOG)} módulos · TERMUX EDITION v1.0</div>
<table><tr><th>#</th><th>MÓDULO</th><th>ALVO</th><th>SUMÁRIO</th><th>TIMESTAMP</th></tr>{rows}</table>
<div class="footer"><b>OLHO DE DEUS v1.0 TERMUX</b> · Criado por <b>BLAZING</b><br>Uso exclusivo para fins éticos e legais</div>
</body></html>""")
        ok(f"HTML → {html_path}")
        info("Abra o HTML no Chrome do Android para visualização completa.")
    except Exception as ex: warn(f"Não foi possível salvar HTML: {ex}")

    console.print()
    ri("Módulos executados",str(len(SESSION_LOG)),GREEN)
    ri("Pasta de relatórios",str(REPORTS_DIR),BLUE)
    press_enter()

# =============================================================================
# AJUDA COMPLETA
# =============================================================================
def show_help():
    banner()
    section("❓  AJUDA — OLHO DE DEUS TERMUX v1.0")
    console.print(Panel(
        "[bold yellow]O que é o OLHO DE DEUS?[/]\n\n"
        "Ferramenta de [bold]OSINT[/] com 30 módulos em 5 categorias.\n"
        "100% público e legal. NÃO invade sistemas.\n\n"
        "[bold yellow]Categorias:[/]\n"
        "  🔍 A — OSINT:     IP, Domínio, Email, Username, Pessoa, Tel, Keyword\n"
        "  🌑 B — DARKNET:   Links, Busca, Email Anon, Paste Monitor\n"
        "  🛡️  C — SEGURANÇA: Hash, Senha, Malware, Threat, Breach\n"
        "  📡 D — REDE:      Shodan, Certs, URL, Whois, Metascraper\n"
        "  🤖 E — AUTOMAÇÃO: Recon, Autopilot, Dorks, Report\n\n"
        "[dim]Criado por [bold yellow]BLAZING[/] — Ethical Hacker & OSINT Specialist[/]",
        border_style="yellow dim", padding=(1,1)
    ))
    console.print()
    Prompt.ask("  [yellow]ENTER para guia detalhado[/]",default="")

    help_data = [
        ("🔍 CATEGORIA A — OSINT", [
            ("A — IP SCAN",        "4 APIs paralelas. Retorna país, cidade, ISP, ASN, coordenadas, mapa, risco (VPN/Tor/DC).","Ex: 8.8.8.8 ou 1.1.1.1","IPs privados 192.168.x não funcionam"),
            ("A — DOMÍNIO",        "DNS completo, WHOIS, subdomínios via crt.sh, análise SPF/DMARC/DKIM.","Ex: google.com","WHOIS privado não revela dono"),
            ("A — E-MAIL",         "Valida formato, MX, detecta provider (Google/MS/Zoho), SPF, DMARC.","Ex: user@gmail.com","Não confirma se caixa existe"),
            ("A — USERNAME",       "7 plataformas via API + 12 links manuais + ferramentas externas.","Ex: blazing","Perfis privados não confirmam"),
            ("A — PESSOA",         "Dorks para redes sociais, PDFs, JusBrasil, Lattes, Escavador.","Ex: João Silva","Só dados indexados publicamente"),
            ("A — TELEFONE",       "País, DDD, tipo celular/fixo, E.164, TrueCaller, WhatsApp.","Ex: +55 11 99999-9999","Não revela titular"),
            ("A — KEYWORD HUNTER", "Busca em Google, Bing, GitHub, Grep.app, Pastebin, Reddit, IntelX, Ahmia.","Qualquer palavra","Depende de indexação pública"),
        ]),
        ("🌑 CATEGORIA B — DARKNET", [
            ("B — DARK LINKS",   "Links lícitos organizados: motores de busca, email anônimo, privacidade.","—","Links .onion precisam do Tor Browser"),
            ("B — DARK SEARCH",  "Gera links para Ahmia (sem Tor) e Torch/Haystak (com Tor).","Palavra-chave","Conteúdo ilegal não é responsabilidade sua"),
            ("B — EMAIL ANON",   "Gera email via API Guerrilla Mail + lista de 7 serviços alternativos.","—","Expira em 60 minutos"),
            ("B — PASTE MONITOR","Busca em Pastebin, GitHub, Grep.app e repositórios públicos.","Email, domínio, username","Nem todos os pastes são indexados"),
        ]),
        ("🛡️ CATEGORIA C — SEGURANÇA", [
            ("C — HASH",     "Identifica tipo pelo comprimento: MD5(32), SHA-1(40), SHA-256(64), bcrypt($2).","5d41402abc4b2a76...","bcrypt difícil de quebrar"),
            ("C — SENHA",    "Força, entropia, tempo de crack, verifica HIBP (k-anonymity — senha não sai do device).","Qualquer senha","Senha nunca enviada ao servidor"),
            ("C — MALWARE",  "Verifica hash na API pública do MalwareBazaar (abuse.ch).","Hash MD5/SHA256 do arquivo","Arquivos novos podem não estar na base"),
            ("C — THREAT",   "8 fontes: VirusTotal, AbuseIPDB, GreyNoise, Shodan, OTX, CriminalIP...","IP ou domínio","Algumas fontes requerem cadastro"),
            ("C — BREACH",   "Verifica HIBP automaticamente + links para 6 outras fontes.","Email, domínio, username","HIBP v3 precisa de API key para completo"),
        ]),
        ("📡 CATEGORIA D — REDE", [
            ("D — SHODAN",     "Interface Shodan + queries prontas para câmeras, MongoDB, FTP anônimo.","apache brasil","Shodan gratuito tem resultados limitados"),
            ("D — CERTWATCH",  "Subdomínios via Certificate Transparency (crt.sh).","empresa.com.br","Só captura domínios com SSL"),
            ("D — URL",        "Anatomia, headers ao vivo, headers segurança, reputação em 5 fontes.","https://example.com","Sites que bloqueiam bots não respondem"),
            ("D — METASCRAPER","Headers HTTP, tecnologias detectadas (10), hash de arquivo local.","URL ou caminho","Não funciona em sites protegidos"),
            ("D — WHOIS",      "WHOIS atual + links histórico: ViewDNS, SecurityTrails, DomainTools.","example.com","Histórico completo pode ser pago"),
        ]),
        ("🤖 CATEGORIA E — AUTOMAÇÃO", [
            ("E — SHADOW RECON", "Detecta tipo e roda módulos em sequência. Para domínio: DNS+IP+subdomínios.","IP, domínio, email, username","100% passivo"),
            ("E — AUTOPILOT",    "Auto-detecta tipo e executa todos os módulos relevantes automaticamente.","Qualquer alvo","Salvo na sessão para relatório"),
            ("E — DORK BUILDER", "8 templates + construtor manual com site:, inurl:, filetype:, intitle:.","Templates ou manual","Google limita queries agressivas"),
            ("E — OSINT REPORT", "Gera TXT e HTML com todos os módulos da sessão. Salvo em Downloads.","—","Só sessão atual — sem memória"),
        ]),
    ]

    for cat_name, modules in help_data:
        banner()
        section(f"❓  {cat_name}")
        for mod_name, desc, example, limitation in modules:
            console.print(f"\n  [bold yellow]▸ {mod_name}[/]")
            console.print(f"  [white]{desc}[/]")
            console.print(f"  [dim cyan]Ex: {example}[/]")
            console.print(f"  [dim red]⚠ {limitation}[/]")
        console.print()
        resp=Prompt.ask("  [dim yellow]ENTER = próximo  |  's' = sair[/]",default="")
        if resp.lower()=='s': break

    banner()
    section("❓  METODOLOGIA & ATALHOS")
    console.print(Panel(
        "[bold yellow]METODOLOGIA OSINT[/]\n\n"
        "[bold]1.[/] Defina o alvo: IP, domínio, email, username ou nome\n"
        "[bold]2.[/] Use E2 (Autopilot) para visão geral rápida\n"
        "[bold]3.[/] Aprofunde com módulos específicos\n"
        "[bold]4.[/] Gere relatório com E4 ao final\n\n"
        "[bold yellow]GLOSSÁRIO[/]\n\n"
        "[cyan]OSINT[/]     Inteligência de fontes abertas\n"
        "[cyan]ASN[/]       Identificador de rede de um ISP\n"
        "[cyan]MX[/]        Servidor de e-mail de um domínio\n"
        "[cyan]SPF/DMARC[/] Proteção contra spoofing de email\n"
        "[cyan]Hash[/]      Resultado de função matemática\n"
        "[cyan]Dork[/]      Query avançada para buscadores\n"
        "[cyan]crt.sh[/]    Banco público de certificados SSL\n\n"
        "[bold yellow]ATALHOS[/]\n\n"
        "  [yellow]CTRL+C[/]  Interrompe o módulo atual\n"
        "  [yellow]0[/]       Volta / sai\n"
        f"  Relatórios: [cyan]{REPORTS_DIR}[/]",
        border_style="yellow dim", padding=(1,1)
    ))
    press_enter()

# =============================================================================
# MAIN LOOP
# =============================================================================
ACTIONS = {
    'A': {
        '1': scan_ip,        '2': scan_domain,    '3': scan_email,
        '4': scan_username,  '5': scan_person,    '6': scan_phone,
        '7': keyword_hunter,
    },
    'B': {
        '1': dark_links,     '2': dark_search,    '3': anon_email,
        '4': paste_monitor,
    },
    'C': {
        '1': hash_analyzer,  '2': password_analyzer, '3': malware_checker,
        '4': threat_intel,   '5': breach_checker,
    },
    'D': {
        '1': shodan_explorer,'2': certwatch,      '3': url_analyzer,
        '4': metascraper,    '5': whois_history,
    },
    'E': {
        '1': shadow_recon,   '2': osint_autopilot,'3': dork_builder,
        '4': osint_report,
    },
}

SUBMENUS = {
    'A': ("🔍  OSINT", [
        ("1","📡 IP SCAN",       "4 APIs + geo + risco"),
        ("2","🌐 DOMÍNIO",        "DNS + WHOIS + Subs"),
        ("3","✉  E-MAIL",         "Validação + MX + SPF"),
        ("4","👤 USERNAME",        "API + 12 plataformas"),
        ("5","🕵️  PESSOA",         "Dorks + Brasil"),
        ("6","📞 TELEFONE",        "País + tipo + links"),
        ("7","🔎 KEYWORD HUNTER", "10+ fontes simultâneas"),
    ]),
    'B': ("🌑  DARKNET", [
        ("1","🌑 DARK LINKS",    "Links lícitos organizados"),
        ("2","🔍 DARK SEARCH",   "Busca em motores dark"),
        ("3","✉  EMAIL ANÔNIMO", "Guerrilla Mail API"),
        ("4","📋 PASTE MONITOR", "Pastebin + GitHub + código"),
    ]),
    'C': ("🛡️  SEGURANÇA", [
        ("1","🔑 HASH",          "Identificação + crack links"),
        ("2","🔒 SENHA",         "Força + HIBP k-anonymity"),
        ("3","🦠 MALWARE",       "MalwareBazaar + fontes"),
        ("4","🚨 THREAT INTEL",  "8 fontes de ameaça"),
        ("5","💧 BREACH",        "HIBP automático + 6 fontes"),
    ]),
    'D': ("📡  REDE", [
        ("1","🔭 SHODAN",        "Queries + dispositivos expostos"),
        ("2","🔒 CERTWATCH",     "Subdomínios SSL + crt.sh"),
        ("3","🔗 URL",           "Headers ao vivo + reputação"),
        ("4","📄 METASCRAPER",   "Tecnologias + headers + hash"),
        ("5","🌐 WHOIS HISTORY", "WHOIS atual + histórico"),
    ]),
    'E': ("🤖  AUTOMAÇÃO", [
        ("1","🦅 SHADOW RECON",  "Reconhecimento automatizado"),
        ("2","🤖 AUTOPILOT",     "Detecta tipo e roda tudo"),
        ("3","🔍 DORK BUILDER",  "8 templates + manual"),
        ("4","📊 OSINT REPORT",  "Relatório HTML + TXT"),
    ]),
}

def run_category(cat):
    while True:
        title, items = SUBMENUS[cat]
        submenu(title, items)
        console.print(f"\n  [dim yellow]─── {datetime.now().strftime('%H:%M:%S')} ─── BLAZING ───[/]\n")
        choice = Prompt.ask("  [bold yellow]Módulo[/]", default="0")
        if choice == '0': break
        fn = ACTIONS.get(cat, {}).get(choice)
        if fn:
            try:    fn()
            except KeyboardInterrupt:
                console.print("\n  [dim red]Interrompido.[/]"); time.sleep(0.5)
        else:
            err("Inválido."); time.sleep(0.7)

def main():
    while True:
        menu()
        console.print(f"\n  [dim yellow]─── {datetime.now().strftime('%H:%M:%S')} ─── BLAZING ─── TERMUX v1.0 ───[/]\n")
        choice = Prompt.ask("  [bold yellow]Categoria[/]", default="0").upper()

        if choice == '0':
            banner()
            if SESSION_LOG:
                if Confirm.ask("  [yellow]Gerar relatório antes de sair?[/]", default=True):
                    osint_report()
            console.print(Align.center(Text(
                "\n  OLHO DE DEUS — TERMUX EDITION v1.0\n  by  B L A Z I N G\n",
                style="bold yellow")))
            sys.exit(0)

        if   choice == 'F': show_help()
        elif choice in ACTIONS: run_category(choice)
        else: err(f"'{choice}' inválido. Use A B C D E F ou 0."); time.sleep(0.8)

if __name__ == "__main__":
    try:    main()
    except KeyboardInterrupt:
        console.print("\n\n  [bold yellow]OLHO DE DEUS TERMUX — by BLAZING[/]\n"); sys.exit(0)
