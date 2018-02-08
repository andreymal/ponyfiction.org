#!/usr/bin/env bash
. env/bin/activate
exec searchd -c sphinxconf.sh --nodetach
