#!/usr/bin/python3

import json
import shutil
import datetime
import sys

target = sys.argv[1]
if not target:
    raise Error("missing target")

file_name="/home/irods/.irods/irods_environment.json"
file_backup_name=f"{file_name}-{str(datetime.datetime.now())}"

shutil.copyfile(file_name, file_backup_name)

with open(file_name) as fh:
    file_content = fh.read()

config = json.loads(file_content)

if target == "server":
    config.update({
        "irods_client_server_negotiation": "request_server_negotiation",
        "irods_client_server_policy": "CS_NEG_REQUIRE",
        "irods_ssl_certificate_chain_file": "/etc/certs/chain.pem",
        "irods_ssl_certificate_key_file": "/etc/certs/mirods.key",
        "irods_ssl_ca_certificate_file": "/etc/certs/mirods.crt",
        "irods_ssl_ca_certificate_path": "/etc/certs/",
        "irods_ssl_dh_params_file": "/etc/certs/dhparams.pem",
        "irods_ssl_verify_server": "cert",
        "irods_encryption_algorithm": "AES-256-CBC",
        "irods_encryption_key_size": 32,
        "irods_encryption_num_hash_rounds": 16,
        "irods_encryption_salt_size": 8,
    })
elif target == "client":
    config.update({
        "irods_client_server_negotiation": "request_server_negotiation",
        "irods_client_server_policy": "CS_NEG_REQUIRE",
        "irods_ssl_ca_certificate_file": "/etc/certs/mirods.crt",
        "irods_ssl_verify_server": "cert",
        "irods_encryption_algorithm": "AES-256-CBC",
        "irods_encryption_key_size": 32,
        "irods_encryption_num_hash_rounds": 16,
        "irods_encryption_salt_size": 8,

    })

with open(file_name, "w") as fh:
    fh.write(json.dumps(config, indent=4))
