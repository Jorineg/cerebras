#!/bin/bash

# Delete directories
rm -rf /home/cerebras/llm/test/out
rm -rf /home/cerebras/llm/test/simfab_traces

# Delete files
rm -f /home/cerebras/llm/test/sim_stats.json
rm -f /home/cerebras/llm/test/sim.log
rm -f /home/cerebras/llm/test/simconfig.json
rm -f /home/cerebras/llm/test/wio_flow.json
rm -f /home/cerebras/llm/test/sim_filtered.log