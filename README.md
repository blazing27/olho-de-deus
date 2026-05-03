# 👁️ OLHO DE DEUS — OSINT Tool

Ferramenta OSINT para Termux (Android), focada em análise de IP, domínio, email, usuários e muito mais.

---
## 📦 Instalação (Termux)

```bash
pkg update && pkg upgrade -y
pkg install python git -y

git clone https://github.com/blazing27/olho-de-deus.git
cd olho-de-deus

pip install -r requirements.txt
python3 olho_de_deus_termux.py

---
 ## comando global

echo 'alias olho="python3 $(pwd)/olho_de_deus_termux.py"' >> ~/.bashrc
source ~/.bashrc
