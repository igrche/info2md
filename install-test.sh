#!/usr/bin/env bash

SECONDS=0
LOG_FILE=$0.log

# Save stdout, stderr
exec 3>&1 4>&2
# Redirect output ( > ) into a named pipe ( >() ) running "tee"
exec >  >(tee -i ${LOG_FILE}) 2>&1

function finish {
    EXIT_CODE=$?
    SCRIPT_RUN_TIME=$SECONDS
    TZ=UTC0
    printf '%(%H:%M:%S)T\n' "${SCRIPT_RUN_TIME}"
    # Restore output
    exec 1>&3 2>&4
    exit $EXIT_CODE
}
trap finish EXIT

export LD_LIBRARY_PATH=/local/ichebykin/ichebykin.l/work/sorrento/i-chebykin.coverage/build/llvm/lib:$LD_LIBRARY_PATH
export PATH=/local/ichebykin/ichebykin.l/work/sorrento/i-chebykin.coverage/install/bin/:$PATH
/local/ichebykin/ichebykin.l/work/sorrento/i-chebykin.coverage/build/llvm/bin/llvm-lit \
    -a \
    -j 1 \
    --path /local/ichebykin/ichebykin.l/work/sorrento/i-chebykin.coverage/install/bin/ \
    /local/ichebykin/ichebykin.l/work/sorrento/i-chebykin.coverage/sorrento/p4c/extensions/capri/test/
