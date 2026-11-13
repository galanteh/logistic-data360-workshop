import jwt, requests, random, time, datetime

# ================================================================
# CONFIGURACIÓN — Valores de tu org
# ================================================================
SF_LOGIN_URL  = "https://login.salesforce.com"
TSE           = "gm3wczlgg0zd0nbxg5st8nztgy.c360a.salesforce.com"
CONSUMER_KEY  = "3MVG9HtWXcDGV.nEAoiBp45ijCwLiM4dLvSgyRgbZk_YJYtd3yA80_A7Egc934rq8WrRA.K3oD53bcp5zylkN"
PRIVATE_KEY   = "private_key.pem"
SF_USERNAME   = "epic.94ca15684680@orgfarm.salesforce.com"

ENDPOINT = f"https://{TSE}/api/v1/ingest/sources/LOG_CEDIS_SCANS/scaneventos"

CIUDADES  = ["Monterrey", "CDMX", "Guadalajara", "Tijuana", "Puebla", "Merida"]
HUBS      = ["HUB-MTY-01", "HUB-CDMX-02", "HUB-GDL-03", "HUB-TIJ-04", "HUB-PUE-05", "HUB-MID-06"]
OPERARIOS = ["EMP-4421", "EMP-3308", "EMP-5571", "EMP-2291", "EMP-6612"]
EVENTOS   = ["SCAN_HUB_LLEGADA", "SCAN_HUB_SALIDA", "SCAN_EN_RUTA", "SCAN_ENTREGADO", "SCAN_RETENIDO"]
RFCS      = ["DBA950215AB1", "TRK881201XX0", "PKG760315YZ9", "MED450922KL1", "AUT330510MN3"]
ESTADOS   = ["En_Transito", "Entregado", "Retenido", "En_Clasificacion", "Retorno"]

# ── Paso 1: Obtener Core Token via JWT ──────────────────────────
def get_core_token():
    with open(PRIVATE_KEY, "r") as f:
        private_key = f.read()
    claim = {
        "iss": CONSUMER_KEY,
        "sub": SF_USERNAME,
        "aud": SF_LOGIN_URL,
        "exp": int(time.time()) + 180
    }
    encoded_jwt = jwt.encode(claim, private_key, algorithm="RS256")
    resp = requests.post(f"{SF_LOGIN_URL}/services/oauth2/token", data={
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": encoded_jwt
    })
    resp.raise_for_status()
    data = resp.json()
    return data["access_token"], data["instance_url"]

# ── Paso 2: Intercambiar por Token CDP ──────────────────────────
def get_cdp_token(core_token, instance_url):
    url = f"{instance_url}/services/a360/token"
    params = {
        "grant_type": "urn:salesforce:grant-type:external:cdp",
        "subject_token": core_token,
        "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
        "client_id": CONSUMER_KEY
    }
    resp = requests.post(url, data=params)
    
    if resp.status_code != 200:
        print(f"\nError en Token Exchange: {resp.text}")
        resp.raise_for_status()
        
    return resp.json()["access_token"]

def gen_escaneo():
    idx = random.randint(0, len(HUBS) - 1)
    ts  = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return {
        "NumGuia":       f"TRK{random.randint(2024000000, 2024999999)}",
        "EventType":     random.choice(EVENTOS),
        "HubID":         HUBS[idx],
        "HubCiudad":     CIUDADES[idx] if idx < len(CIUDADES) else random.choice(CIUDADES),
        "Timestamp":     ts,
        "Operador":      random.choice(OPERARIOS),
        "Status_Nuevo":  random.choice(ESTADOS),
        "RFC_Remitente": random.choice(RFCS),
        "Temperatura_C": round(random.uniform(2.0, 38.0), 1),
        "Anomalia":      random.random() < 0.05
    }

# ── Paso 3: Enviar Datos ────────────────────────────────────────
def enviar(evento, cdp_token):
    resp = requests.post(
        ENDPOINT,
        headers={"Authorization": f"Bearer {cdp_token}", "Content-Type": "application/json", "Accept": "application/json"},
        json={"data": [evento]},
        timeout=10
    )
    if resp.status_code == 400:
        print(f"\nError 400 en Ingestion API. Body: {resp.text}")
    return resp

print("Iniciando streaming CEDIS -> Salesforce Data Cloud...")
core_token, instance_url = get_core_token()
print(f"✓ [Paso 1] Core Token (JWT) obtenido. Dominio: {instance_url}")
cdp_token = get_cdp_token(core_token, instance_url)
print("✓ [Paso 2] Intercambio CDP completado en /a360/token.\n")

n = 0
while True:
    try:
        evento = gen_escaneo()
        resp   = enviar(evento, cdp_token)

        # Si el token expira, renovar todo el ciclo
        if resp.status_code == 401:
            core_token, instance_url = get_core_token()
            cdp_token = get_cdp_token(core_token, instance_url)
            resp  = enviar(evento, cdp_token)

        n += 1
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] #{n:04d}  {evento['NumGuia']}  {evento['EventType']:<22}  HTTP {resp.status_code}")
        time.sleep(3)

    except KeyboardInterrupt:
        print(f"\nStreaming detenido. Total enviados: {n}")
        break
    except Exception as e:
        print(f"  Error: {e}")
        time.sleep(5)


