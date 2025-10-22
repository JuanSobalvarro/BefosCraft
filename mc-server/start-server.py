#!/usr/bin/env python3
import os
import subprocess
import urllib.parse
import requests

SERVER_DIR = "/server"
FABRIC_JAR = os.path.join(SERVER_DIR, "fabric-server-launch.jar")
EULA_FILE = os.path.join(SERVER_DIR, "eula.txt")
SERVER_URL = "https://meta.fabricmc.net/v2/versions/loader/1.21.10/0.17.3/1.1.0/server/jar"
MODS_FILE = os.path.join(SERVER_DIR, "mods.txt")
MODS_DIR = os.path.join(SERVER_DIR, "mods")

JVM_OPTS = os.environ.get("JVM_OPTS", "-Xmx3G -Xms1G")

os.makedirs(SERVER_DIR, exist_ok=True)
os.makedirs(MODS_DIR, exist_ok=True)

def download_file(url, dest_path):
    """Download a file from url to dest_path."""
    print(f"Downloading {url} -> {dest_path}")
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded {dest_path}")

# 1️⃣ Download Fabric server if missing
if not os.path.isfile(FABRIC_JAR):
    download_file(SERVER_URL, FABRIC_JAR)

# 2️⃣ Download mods if mods.txt exists
if os.path.isfile(MODS_FILE):
    print("Checking mods in mods.txt...")
    with open(MODS_FILE, "r") as f:
        for line in f:
            url = line.strip()
            if not url:
                continue
            mod_filename = os.path.basename(urllib.parse.unquote(url))
            mod_path = os.path.join(MODS_DIR, mod_filename)
            if not os.path.isfile(mod_path):
                download_file(url, mod_path)
            else:
                print(f"{mod_filename} already exists.")

# 3️⃣ Accept EULA if missing
if not os.path.isfile(EULA_FILE):
    print("Creating eula.txt...")
    with open(EULA_FILE, "w") as f:
        f.write("eula=true\n")

# 4️⃣ Start server
print("Starting Minecraft Fabric server...")
subprocess.run(f"java {JVM_OPTS} -jar {FABRIC_JAR} nogui", shell=True, check=True)
