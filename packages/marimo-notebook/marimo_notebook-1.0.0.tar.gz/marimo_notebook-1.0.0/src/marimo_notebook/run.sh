###
# #%L
# Marimo Notebook
# %%
# Copyright (C) 2021 Booz Allen
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
while true
    do
        cp /tmp/admin_console.py /app/;
        cd /venv/bootstrap-env;
        . $(poetry env info --path)/bin/activate;
        cd /app;
        marimo edit --host 0.0.0.0 --port 9090 --no-token; 

        # Opens up the port
        fuser -k 9090/tcp;
    done
