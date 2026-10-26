"""
Generador de datasets para Workshop Salesforce Data Cloud — Logística.
Volúmenes corporativos: 600 cuentas · 50,000 guías · ~7,170 incidencias.
Fechas en formato YYYY-MM-DD (compatible con DMO Shipment.Date tipo Date).
"""
import csv, random, string, os
from datetime import date, timedelta

random.seed(7)
OUT = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT, exist_ok=True)

def rdate(start, end):
    s = date.fromisoformat(start)
    e = date.fromisoformat(end)
    return (s + timedelta(days=random.randint(0, (e - s).days))).isoformat()

def rdatetime(start, end):
    """ISO 8601 DateTime with Z suffix — required for DMO Incident Detected DateTime."""
    d = date.fromisoformat(start) + timedelta(
        days=random.randint(0, (date.fromisoformat(end) - date.fromisoformat(start)).days)
    )
    return f"{d.isoformat()}T{random.randint(6,22):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}Z"

# ─── RFC generator ────────────────────────────────────────────────────────────
CONSONANTS = "BCDFGHJKLMNPQRSTVWXYZ"
VOWELS     = "AEIOU"

def gen_rfc():
    letters = (random.choice(CONSONANTS) + random.choice(VOWELS) +
               random.choice(CONSONANTS) + random.choice(VOWELS))
    yr  = random.randint(60, 99)
    mo  = random.randint(1, 12)
    dy  = random.randint(1, 28)
    hom = (random.choice(string.ascii_uppercase) +
           random.choice(string.ascii_uppercase) +
           random.choice(string.digits))
    return f"{letters}{yr:02d}{mo:02d}{dy:02d}{hom}"

# ─── Company name pieces ───────────────────────────────────────────────────────
PREFIXES = [
    "Distribuidora","Logística","Grupo","Comercializadora","Transportes",
    "Industrias","Corporativo","Manufactura","Servicios","Retail",
    "Farmacéutica","Alimentos","Constructora","Tecnología","Automotriz",
    "Química","Textiles","Agropecuaria","Plásticos","Bebidas",
    "Electrónica","Consolidadora","Internacional","Nacional","Empacadora",
]
MIDS = [
    "del Norte","del Sur","del Este","del Bajío","del Golfo","del Pacífico",
    "del Centro","de México","Norteña","Fronteriza","Industrial","Comercial",
    "Metropolitana","Regional","Integral","Moderna","Avanzada","Global",
    "Express","Eficiente","Especializada","Premier","Plus","Ágil",
]
SURNAMES = [
    "García","López","Martínez","Rodríguez","González","Hernández",
    "Pérez","Sánchez","Ramírez","Torres","Flores","Cruz","Medina","Vargas",
    "Jiménez","Morales","Reyes","Ruiz","Gutiérrez","Ávila","Castillo",
]
SUFFIXES = ["SA de CV","SC","SA","S de RL de CV","SAPI de CV"]

CITIES = [
    "CDMX","Guadalajara","Monterrey","Puebla","Tijuana","León",
    "Hermosillo","Culiacán","Tampico","Mérida","Saltillo","Querétaro",
    "Torreón","Ciudad Juárez","Cancún","Oaxaca","Chihuahua","Veracruz",
    "Aguascalientes","Morelia","Toluca","Xalapa","Durango","Mexicali",
]

EMAIL_PREFIXES = ["contacto","admin","operaciones","ventas","logistica",
                  "compras","facturacion","gerencia","info","servicios"]

def gen_name():
    style = random.randint(0, 2)
    if style == 0:
        return f"{random.choice(PREFIXES)} {random.choice(MIDS)}"
    elif style == 1:
        return f"{random.choice(PREFIXES)} {random.choice(SURNAMES)} y {random.choice(SURNAMES)}"
    else:
        return f"{random.choice(PREFIXES)} {random.choice(MIDS)} {random.choice(SURNAMES)}"

def slug(name):
    return name.lower().replace(" ","").replace(".","").replace(",","")[:14]

def phone():
    return f"55{random.randint(10000000,99999999)}"

# ─── 1. CUENTAS B2B (600 registros, AccountId 1000-1599) ─────────────────────
print("Generando cuentas...")

# 10 pares de duplicados intencionales para Identity Resolution
DUP_PAIRS = [
    ("DBA950215AB1","Distribuidora Bajio SA de CV","contacto@bajio.com"),
    ("DBA950215AB1","Distribuidora Bajío",          "ventas@bajio.com"),

    ("BAJA850312KL5","Grupo Bajío SA de CV",         "contacto@grupobajio.mx"),
    ("BAJA850312KL5","GRUPO BAJIO S.A.",              "ventas@grupobajio.mx"),

    ("MXIN760401AB2","Transportes del Norte SA de CV","admin@tdnorte.mx"),
    ("MXIN760401AB2","Trans. del Norte SC",           "ops@tdnorte.mx"),

    ("COMS901115GH7","Comercializadora del Sur SA de CV","compras@comsur.mx"),
    ("COMS901115GH7","Com. del Sur SA",               "gerencia@comsur.mx"),

    ("LGEX830228FD4","Logística Express SA de CV",   "info@logexpress.mx"),
    ("LGEX830228FD4","Log. Expres SA de CV",          "contacto@logexpress.mx"),

    ("PQXR910703JK8","Paquetería Rápida SC",          "ops@paqrapida.mx"),
    ("PQXR910703JK8","Paqueteria Rapida SA",           "ventas@paqrapida.mx"),

    ("AMXL740512PL3","Almacenes México SA de CV",    "almacenes@amxl.mx"),
    ("AMXL740512PL3","Almacenes MX SC",               "admin@amxl.mx"),

    ("FDEX880629RV7","Fletes del Este SC",             "contacto@flesteste.mx"),
    ("FDEX880629RV7","Fletes Este SA de CV",           "ventas@flesteste.mx"),

    ("SERV950310MK2","Servicios Integrales SA de CV", "info@servint.mx"),
    ("SERV950310MK2","Servicios Integrales SC",        "contacto@servint.mx"),

    ("NRTX860415HL9","Norteña Textiles SA de CV",     "ventas@nortex.mx"),
    ("NRTX860415HL9","Nortena Textiles SA",            "admin@nortex.mx"),
]

seen_rfcs = set(rfc for rfc, _, _ in DUP_PAIRS)
acc_rows  = []

# Inject duplicate pairs first (20 rows → AccountId 1000-1019)
for i, (rfc, name, email) in enumerate(DUP_PAIRS):
    acc_rows.append([1000 + i, rfc, name, email, phone(), random.choice(CITIES)])

# Fill remaining 580 unique accounts (AccountId 1020-1599)
while len(acc_rows) < 600:
    rfc = gen_rfc()
    if rfc in seen_rfcs:
        continue
    seen_rfcs.add(rfc)
    name  = gen_name() + " " + random.choice(SUFFIXES)
    ep    = EMAIL_PREFIXES[len(acc_rows) % len(EMAIL_PREFIXES)]
    email = f"{ep}@{slug(name)}.mx"
    acc_rows.append([1000 + len(acc_rows), rfc, name, email, phone(), random.choice(CITIES)])

with open(f"{OUT}/cuentas_b2b_logistica.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["AccountId","RFC","RazonSocial","Email","Telefono","Ciudad"])
    w.writerows(acc_rows)
print(f"  cuentas_b2b_logistica.csv: {len(acc_rows)} filas")

account_ids = [r[0] for r in acc_rows]

# ─── 2. GUÍAS / SHIPMENTS (50,000 registros) ─────────────────────────────────
print("Generando guías...")

STATUSES = (["Entregado"] * 65 + ["En_Transito"] * 25 + ["Retrasado"] * 10)
DEST_CITIES = [
    "CDMX","Guadalajara","Monterrey","Puebla","Tijuana","León",
    "Hermosillo","Culiacán","Tampico","Mérida","Saltillo","Querétaro",
    "Torreón","Ciudad Juárez","Cancún","Oaxaca","Chihuahua","Veracruz",
    "Aguascalientes","Morelia","Toluca","Xalapa","Durango","Mexicali",
    "Irapuato","Celaya","Nuevo Laredo","Matamoros","Reynosa","Ensenada",
]

guia_rows = []
for n in range(50000):
    guia_rows.append([
        f"TRK23{1000 + n:06d}",
        random.choice(account_ids),
        rdate("2023-01-01", "2024-10-31"),
        random.choice(STATUSES),
        random.choice(DEST_CITIES),
    ])

with open(f"{OUT}/guias_shipments_logistica.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["NumGuia","AccountId_Remitente","FechaEnvio","Status","Ciudad_Destino"])
    w.writerows(guia_rows)

guias_size = os.path.getsize(f"{OUT}/guias_shipments_logistica.csv")
print(f"  guias_shipments_logistica.csv: {len(guia_rows):,} filas · {guias_size/1024/1024:.2f} MB")

# ─── 3. INCIDENCIAS (7,170 registros) ────────────────────────────────────────
print("Generando incidencias...")

TIPOS      = ["Demora_Ruta","Retencion_Aduana","Direccion_Incorrecta",
              "Paquete_Danado","Cancelacion_Cliente"]
SEVERIDADES = ["Alta","Media","Baja"]
SEV_WEIGHTS = [30, 45, 25]

# Sample 7,170 guías at random (without replacement) for incidents
inc_guias = random.sample([r[0] for r in guia_rows], 7170)

inc_rows = []
for i, guia in enumerate(inc_guias):
    inc_rows.append([
        f"INC-2023-{i:05d}",
        guia,
        rdatetime("2023-01-15", "2024-11-15"),
        random.choices(SEVERIDADES, weights=SEV_WEIGHTS)[0],
        random.choice(TIPOS),
    ])

with open(f"{OUT}/incidencias_entrega.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["IncidentID","NumGuia","FechaApertura","Severidad","TipoIncidencia"])
    w.writerows(inc_rows)
print(f"  incidencias_entrega.csv: {len(inc_rows):,} filas")

# ─── Summary ──────────────────────────────────────────────────────────────────
print("\n=== RESUMEN FINAL ===")
for fn in ["cuentas_b2b_logistica.csv","guias_shipments_logistica.csv","incidencias_entrega.csv"]:
    path = f"{OUT}/{fn}"
    with open(path, newline="", encoding="utf-8") as f:
        rows = sum(1 for _ in f) - 1  # exclude header
    sz = os.path.getsize(path)
    print(f"  {fn}: {rows:,} filas · {sz/1024:.1f} KB")
print("DONE")
