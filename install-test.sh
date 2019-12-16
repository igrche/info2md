#!/usr/bin/env bash

export LD_LIBRARY_PATH=/local/ichebykin/ichebykin.l/work/sorrento/i-chebykin.coverage/build/llvm/lib:$LD_LIBRARY_PATH
export PATH=/local/ichebykin/ichebykin.l/work/sorrento/i-chebykin.coverage/install/bin/:$PATH
/local/ichebykin/ichebykin.l/work/sorrento/i-chebykin.coverage/build/llvm/bin/llvm-lit \
    -a \
    -j 1 \
    --path /local/ichebykin/ichebykin.l/work/sorrento/i-chebykin.coverage/install/bin/ \
    /local/ichebykin/ichebykin.l/work/sorrento/i-chebykin.coverage/sorrento/p4c/extensions/capri/test/
