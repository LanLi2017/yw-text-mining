#!/usr/bin/env bash
alias yw='java -jar ~/bin/yesworkflow-0.2.0-jar-with-dependencies.jar'

yw recon topic_modeling.py -c recon.comment='#' -c recon.factsfile=reconfacts.P
