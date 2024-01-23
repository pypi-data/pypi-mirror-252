#!/usr/bin/env bash

run_cdnbestip() {
        export SAVE_CLOUDFLARE_TOKEN=''
        export BARK_TOKEN=''
        export GCORE_DOMAIN='gcore.example.com'
        export CLOUDFLARE_DOMAIN='cloudflare.example.com'

        cdnbestip
}
