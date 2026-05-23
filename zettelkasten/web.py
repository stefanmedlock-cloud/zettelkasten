import asyncio
import json
import logging
import urllib.parse

logger = logging.getLogger("ZettelkastenWeb")

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zettelkasten 🗃️ Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0c0f1d;
            --glass-bg: rgba(18, 22, 45, 0.6);
            --glass-border: rgba(255, 255, 255, 0.08);
            --accent-primary: #5b21b6;
            --accent-secondary: #7c3aed;
            --accent-glow: rgba(124, 58, 237, 0.3);
            --text-color: #f3f4f6;
            --text-muted: #9ca3af;
            --neon-blue: #06b6d4;
            --neon-green: #10b981;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(91, 33, 182, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(6, 182, 212, 0.15) 0%, transparent 40%);
        }

        header {
            padding: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--glass-border);
            backdrop-filter: blur(12px);
            background: rgba(12, 15, 29, 0.5);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo {
            font-weight: 800;
            font-size: 1.5rem;
            background: linear-gradient(135deg, var(--text-color) 0%, var(--neon-blue) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .status-badge {
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid var(--neon-green);
            color: var(--neon-green);
            padding: 0.4rem 1rem;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
        }

        main {
            flex: 1;
            padding: 2rem;
            max-width: 1400px;
            width: 100%;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 2rem;
        }

        .panel {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 1.5rem;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        .panel-title {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1.2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 0.5rem;
            color: var(--neon-blue);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .stat-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        }

        .stat-val {
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--text-color);
            margin-bottom: 0.2rem;
        }

        .stat-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .terminal-container {
            font-family: 'JetBrains Mono', monospace;
            background: rgba(5, 7, 15, 0.95);
            border-radius: 12px;
            padding: 1rem;
            height: 200px;
            overflow-y: auto;
            font-size: 0.9rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 1rem;
            color: #38bdf8;
        }

        .terminal-line {
            margin-bottom: 0.4rem;
            white-space: pre-wrap;
        }

        .terminal-input-container {
            display: flex;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--glass-border);
            border-radius: 8px;
            overflow: hidden;
        }

        .terminal-input-container span {
            padding: 0.8rem 0 0.8rem 1rem;
            color: var(--neon-blue);
        }

        .terminal-input {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            color: var(--text-color);
            padding: 0.8rem;
            font-family: 'JetBrains Mono', monospace;
        }

        .key-list {
            list-style: none;
            max-height: 480px;
            overflow-y: auto;
        }

        .key-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.8rem 1rem;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            margin-bottom: 0.6rem;
        }

        .key-name {
            font-weight: 600;
        }

        .key-actions {
            display: flex;
            gap: 0.5rem;
        }

        .btn {
            background: transparent;
            border: 1px solid var(--glass-border);
            color: var(--text-color);
            padding: 0.3rem 0.8rem;
            border-radius: 6px;
            cursor: pointer;
        }

        .btn:hover {
            background: var(--accent-secondary);
            border-color: var(--accent-secondary);
        }

        .btn-danger:hover {
            background: #ef4444;
            border-color: #ef4444;
        }

        .refresh-btn {
            background: var(--accent-primary);
            border: none;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
        }

        footer {
            text-align: center;
            padding: 2rem;
            border-top: 1px solid var(--glass-border);
            font-size: 0.85rem;
            color: var(--text-muted);
        }
    </style>
</head>
<body>
    <header>
        <div class="logo">🗃️ Zettelkasten DB</div>
        <div class="status-badge">LIVE - Aktiv</div>
    </header>
    <main>
        <div class="panel">
            <div class="panel-title">Systemstatus <button class="refresh-btn" onclick="loadStats()">Aktualisieren</button></div>
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-val" id="stat-keys">0</div>
                    <div class="stat-label">Gespeicherte Keys</div>
                </div>
                <div class="stat-card">
                    <div class="stat-val" id="stat-engine">Memory</div>
                    <div class="stat-label">Storage Backend</div>
                </div>
                <div class="stat-card">
                    <div class="stat-val" id="stat-ram">1.2 MB</div>
                    <div class="stat-label">RAM-Nutzung</div>
                </div>
                <div class="stat-card">
                    <div class="stat-val" id="stat-uptime">0s</div>
                    <div class="stat-label">Uptime</div>
                </div>
            </div>
            
            <div class="panel-title">Kommando-Konsole</div>
            <div class="terminal-container" id="terminal">
                <div class="terminal-line">Zettelkasten CLI v0.3.5 initialisiert.</div>
            </div>
            <div class="terminal-input-container">
                <span>&gt;</span>
                <input type="text" class="terminal-input" id="term-in" placeholder="get key" onkeydown="handleTermKey(event)">
            </div>
        </div>
        
        <div class="panel">
            <div class="panel-title">Schlüssel (Keys)</div>
            <ul class="key-list" id="keys-ul"></ul>
        </div>
    </main>
    <footer>
        Zettelkasten DB &copy; 2024-2026.
    </footer>

    <script>
        async function loadStats() {
            try {
                const res = await fetch("/api/v1/stats");
                const data = await res.json();
                document.getElementById("stat-keys").innerText = data.keys_count;
                document.getElementById("stat-engine").innerText = data.backend;
                document.getElementById("stat-uptime").innerText = data.uptime;
                
                const keysRes = await fetch("/api/v1/keys");
                const keysData = await keysRes.json();
                const ul = document.getElementById("keys-ul");
                ul.innerHTML = "";
                keysData.keys.forEach(k => {
                    const li = document.createElement("li");
                    li.className = "key-item";
                    li.innerHTML = `
                        <span class="key-name">${k}</span>
                        <div class="key-actions">
                            <button class="btn" onclick="queryKey('${k}')">Ansehen</button>
                            <button class="btn btn-danger" onclick="deleteKey('${k}')">Löschen</button>
                        </div>
                    `;
                    ul.appendChild(li);
                });
            } catch(e) { console.error(e); }
        }

        async function queryKey(k) {
            try {
                const res = await fetch(`/api/v1/get?key=\${k}`);
                const data = await res.json();
                writeTerm(`get \${k}: \${JSON.stringify(data.val)}`);
            } catch(e) { writeTerm("Fehler: " + e); }
        }

        async function deleteKey(k) {
            try {
                await fetch(`/api/v1/delete?key=\${k}`, {method: "POST"});
                writeTerm(`delete \${k} erfolgreich.`);
                loadStats();
            } catch(e) { writeTerm("Fehler: " + e); }
        }

        function writeTerm(txt) {
            const term = document.getElementById("terminal");
            const div = document.createElement("div");
            div.className = "terminal-line";
            div.innerText = txt;
            term.appendChild(div);
        }

        async function handleTermKey(e) {
            if (e.key === "Enter") {
                const input = document.getElementById("term-in");
                const val = input.value.trim();
                input.value = "";
                const parts = val.split(" ");
                if (parts[0] === "get") await queryKey(parts[1]);
                else if (parts[0] === "delete") await deleteKey(parts[1]);
            }
        }
        window.onload = loadStats;
    </script>
</body>
</html>
"""

class ZettelkastenWebServer:
    def __init__(self, db, host="0.0.0.0", port=8000):
        self.db = db
        self.host = host
        self.port = port
        self.start_time = asyncio.get_event_loop().time()

    async def start(self):
        server = await asyncio.start_server(self.handle_connection, self.host, self.port)
        logger.info(f"Webserver gestartet unter http://{self.host}:{self.port}/dashboard")
        async with server:
            await server.serve_forever()

    async def handle_connection(self, reader, writer):
        try:
            req_line = await reader.readline()
            if not req_line:
                return
            parts = req_line.decode("utf-8").strip().split(" ")
            if len(parts) < 2:
                return
            method, path = parts[0], parts[1]
            
            headers = {}
            while True:
                line = await reader.readline()
                if line == b"\r\n" or line == b"\n" or not line:
                    break
                h_parts = line.decode("utf-8").strip().split(":", 1)
                if len(h_parts) == 2:
                    headers[h_parts[0].strip().lower()] = h_parts[1].strip()

            content_len = int(headers.get("content-length", 0))
            body = b""
            if content_len > 0:
                body = await reader.readexactly(content_len)

            parsed_url = urllib.parse.urlparse(path)
            query = urllib.parse.parse_qs(parsed_url.query)
            clean_path = parsed_url.path

            if clean_path == "/dashboard":
                await self.send_html(writer, DASHBOARD_HTML)
            elif clean_path == "/api/v1/stats":
                uptime = int(asyncio.get_event_loop().time() - self.start_time)
                stats = {
                    "keys_count": len(self.db.keys()),
                    "backend": self.db.backend.__class__.__name__,
                    "uptime": f"{uptime}s"
                }
                await self.send_json(writer, stats)
            elif clean_path == "/api/v1/keys":
                await self.send_json(writer, {"keys": self.db.keys()})
            elif clean_path == "/api/v1/get":
                k = query.get("key", [None])[0]
                await self.send_json(writer, {"key": k, "val": self.db.get(k) if k else None})
            elif clean_path == "/api/v1/set":
                try:
                    payload = json.loads(body.decode("utf-8"))
                    k = payload.get("key")
                    v = payload.get("val")
                    if k:
                        self.db.set(k, v)
                        await self.send_json(writer, {"status": "ok"})
                    else:
                        await self.send_json(writer, {"status": "error"}, 400)
                except Exception as e:
                    await self.send_json(writer, {"status": "error", "msg": str(e)}, 400)
            elif clean_path == "/api/v1/delete":
                k = query.get("key", [None])[0]
                deleted = self.db.delete(k) if k else False
                await self.send_json(writer, {"status": "ok" if deleted else "not_found"})
            else:
                await self.send_html(writer, "<h1>404 Nicht Gefunden</h1>", 404)
        except Exception as e:
            logger.error(f"Fehler: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def send_html(self, writer, html, status=200):
        resp = f"HTTP/1.1 {status} OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(html.encode('utf-8'))}\r\nConnection: close\r\n\r\n{html}"
        writer.write(resp.encode("utf-8"))
        await writer.drain()

    async def send_json(self, writer, data, status=200):
        body = json.dumps(data)
        resp = f"HTTP/1.1 {status} OK\r\nContent-Type: application/json\r\nContent-Length: {len(body.encode('utf-8'))}\r\nConnection: close\r\n\r\n{body}"
        writer.write(resp.encode("utf-8"))
        await writer.drain()
