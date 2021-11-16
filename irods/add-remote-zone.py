#!/usr/bin/python3

import json
import shutil
import datetime
import sys
import os
import warnings


zone = sys.argv[1]
if not zone:
    raise Error("missing zone")

negotiation_key = os.environ.get("NEGOTIATION_KEY")
zone_key = os.environ.get("ZONE_KEY")
provider = f"irods-provider-{zone}"

if not negotiation_key:
    warnings.warn("missing NEGOTIATION_KEY")

if not zone_key:
    warnings.warn("missing ZONE_KEY")

additional_zone = dict(
    catalog_provider_hosts = [provider],
    negotiation_key = negotiation_key,
    zone_key = zone_key,
    zone_name = zone,
    zone_port = 1247
)

file_name="/etc/irods/server_config.json"
file_backup_name=f"/etc/irods/server_config.json-{str(datetime.datetime.now())}"

shutil.copyfile(file_name, file_backup_name)

with open(file_name) as fh:
    file_content = fh.read()

server_config = json.loads(file_content)
server_config.get("federation").append(additional_zone)

with open(file_name, "w") as fh:
    fh.write(json.dumps(server_config, indent=4))
