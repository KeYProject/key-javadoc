#!/usr/bin/env python3

from pprint import pprint
import json, os, sys
import requests

API_URL = "https://api.github.com/repos/keyproject/key/"
HEADERS = {"Content-Type": "application/json",
           "Accept": "application/vnd.github+json",
           "Authorization": "Bearer " + os.environ['GITHUB_TOKEN'],
           "X-GitHub-Api-Version":"2026-03-10"}

resp = requests.get(API_URL+"releases", headers=HEADERS)

if resp.status_code != 200:
    print(resp.json())
    sys.exit(1)


releases = resp.json()

for release in releases:
    rname = release["tag_name"]
    url = release["assets_url"]
    
    assets = requests.get(url, headers=HEADERS).json()
    release["assets"] = assets

    for asset in assets:
        aname = asset['name']
        
        target = f"downloads/{rname}-{aname}"
        folder = f"docs/{rname}"

        if os.path.exists(target) or os.path.exists(folder): continue
        
        if 'doc' in aname:
            dlurl = f"https://github.com/KeYProject/key/releases/download/{rname}/{aname}"
            print(f"wget {dlurl} -O downloads/{target}")

            if target.endswith(".zip") or target.endswith(".jar"):
                print(f"unzip {target} -o {folder}")
            else:
                print(f"tar xz {target} -o {folder}")
        else:
            print(f"# Not javadoc {aname}")
            

with open("releases.json",'w') as fh:
    json.dump(releases, fh)
