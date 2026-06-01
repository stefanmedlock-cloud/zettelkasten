# Zettelkasten 🗃️

![Tests](https://github.com/stefanmedlock-cloud/zettelkasten/actions/workflows/test.yml/badge.svg) ![License](https://img.shields.io/github/license/stefanmedlock-cloud/zettelkasten)

Eine extrem leichtgewichtige, schnelle und serverlose Key-Value-Datenbank für Python mit TTL-Caching, asynchroner Unterstützung, Komprimierung, plattformspezifischem File-Locking, Replikation und einem Web-Dashboard.

[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://pypi.org/project/zettelkasten/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`Zettelkasten` ist als minimaler, aber robuster Datenspeicher konzipiert.

---

## Features
- **Einfache API**: Minimalistisches Interface (`set`, `get`, `delete`, `keys`).
- **Master-Replica Replikation**: Automatische Synchronisation über TCP-Sockets.
- **Web-Dashboard**: Ein integriertes, glassmorphisches HTML5-Dashboard mit REST-Schnittstelle.
- **Plattformübergreifendes File-Locking**: Sichert die Persistenzdatei prozesssicher ab.
- **Framework-Support**: Contrib-Module für Django Cache, Flask Sessions und FastAPI.
- **Kubernetes & Serverless Ready**: StatefulSets und AWS Lambda-Handler vorhanden.
