#!/bin/sh

SCRIPT_DIR=`dirname $0`

cd $SCRIPT_DIR

case "$1" in
    main)
        echo "Starting Re Index main..."
        /usr/local/coreseek/bin/indexer -c csft.conf main $2
        echo "Done."
        ;;
    delta)
        echo "Starting Re Index delta..."
        /usr/local/coreseek/bin/indexer -c csft.conf delta $2
        echo "Done."
        ;;
    all)
        echo -n "Starting Re Index all..."
        /usr/local/coreseek/bin/indexer -c csft.conf --all $2
        echo "Done."
        ;;
    *)
        echo "Usage: {main|delta|all} [--rotate]" >&2
        exit 1
        ;;
esac

exit 0
