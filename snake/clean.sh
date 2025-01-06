#!/bin/bash

# Delete directories
rm -rf /home/cerebras/llm/snake/out
rm -rf /home/cerebras/llm/snake/simfab_traces

# Delete files
rm -f /home/cerebras/llm/snake/sim_stats.json
rm -f /home/cerebras/llm/snake/sim.log
rm -f /home/cerebras/llm/snake/simconfig.json
rm -f /home/cerebras/llm/snake/wio_flow.json
rm -f /home/cerebras/llm/snake/sim_filtered.log