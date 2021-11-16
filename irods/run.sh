#!/bin/sh

# run.sh is the single entrypoint.

SETUP_IRODS_TIMEOUT=55
SETUP_IRODS_KILL_AFTER=60

case $1 in
    run-client )
        echo "[run.sh] run-client"

        if [ ! -f /home/irods/.irods/irods_environment.json ]; then
            su - irods --command "/usr/bin/iinit < /home/irods/iinit.input"
            touch /var/lib/irods/MIRODS_CLIENT_CONFIGURED
        fi

        echo "[run.sh] done."
        sleep 13d
    ;;

    run-server )
        echo "[run.sh] run-server"

        if [ ! -f /var/lib/irods/MIRODS_SERVER_CONFIGURED ]; then
            echo "[run.sh] run setup_irods.py ..."

            # note: setup_irods.py *should* start the irods service
            timeout \
                --foreground \
                --kill-after ${SETUP_IRODS_KILL_AFTER} \
                --signal KILL \
                ${SETUP_IRODS_TIMEOUT} \
                /usr/bin/python /var/lib/irods/scripts/setup_irods.py < /home/irods/setup_irods.input

            RET=$?

            if [ ${RET} = 124 ]; then
                echo "[run.sh] setup_irods.py timed out after ${SETUP_IRODS_TIMEOUT}"
            elif [ ${RET} = 0 ]; then
                echo "[run.sh] setup_irods.py ok"
                touch /var/lib/irods/MIRODS_SERVER_CONFIGURED
            else
                echo "[run.sh] setup_irods.py reported an error"
            fi
        fi

        # setup_irods.py blocks (often, but not always) for a
        # very long time without starting the service
        # but wait-for-irods-server (check_irods) already sees a running server
        # reproduce: run `./test.sh` and when test01 fails check with `bin/status`
        # if mike and buzz are up; they will be eventually, test01 will then also work

        STATUS=`su - irods --command "/var/lib/irods/irodsctl status" | grep "No iRODS servers running."`

        if [ ! "${STATUS}" ]; then
            echo "[run.sh] kill irods service as we want to start it clean and run it in the foreground ..."
            su - irods --command "/var/lib/irods/irodsctl stop"
        fi

        echo "[run.sh] starting iRODS Server as process..."
        # TODO: iRODS v4.3 will bring a recommended option to run:
        # su - irods --command "/var/lib/irods/irodsctl start --stdout"
        su - irods --command  "cd /usr/sbin; ./irodsServer -u"
    ;;

    * )
        echo "[run.sh] ERROR: invalid command: $1"
        echo "[run.sh] $0 (run-server|run-client)"
        exit 1
esac
