import json
from modulefinder import LOAD_CONST

## Information handling
def info_treatment(node_info, node, logger):
    '''
    This function is in charge of all the operations over the received JSON data from the glances API.

    From https://github.com/nicolargo/glances/blob/fieldsdescription/docs/api.rst
    
    CPU INFO        
    total: Sum of all CPU percentages (except idle) (unit is percent)
    system: percent time spent in kernel space. System CPU time is the time spent running code in the Operating System kernel (unit is percent)
    user: CPU percent time spent in user space. User CPU time is the time spent on the processor running your program's code (or code in libraries) (unit is percent)
    iowait: (Linux): percent time spent by the CPU waiting for I/O operations to complete (unit is percent)
    idle: percent of CPU used by any program. Every program or task that runs on a computer system occupies a certain amount of processing time on the CPU. If the CPU has completed all tasks it is idle (unit is percent)
    irq: (Linux and BSD): percent time spent servicing/handling hardware/software interrupts. Time servicing interrupts (hardware + software) (unit is percent)
    nice: (Unix): percent time occupied by user level processes with a positive nice value. The time the CPU has spent running users' processes that have been niced (unit is percent)
    steal: (Linux): percentage of time a virtual CPU waits for a real CPU while the hypervisor is servicing another virtual processor (unit is percent)
    ctx_switches: number of context switches (voluntary + involuntary) per second. A context switch is a procedure that a computer's CPU (central processing unit) follows to change from one task (or process) to another while ensuring that the tasks do not conflict (unit is percent)
    interrupts: number of interrupts per second (unit is percent)
    soft_interrupts: number of software interrupts per second. Always set to 0 on Windows and SunOS (unit is percent)
    cpucore: Total number of CPU core (unit is number)
    time_since_update: Number of seconds since last update (unit is seconds)
    
    MEM INFO
    total: Total physical memory available (unit is bytes)
    available: The actual amount of available memory that can be given instantly to processes that request more memory in bytes; this is calculated by summing different memory values depending on the platform (e.g. free + buffers + cached on Linux) and it is supposed to be used to monitor actual memory usage in a cross platform fashion (unit is bytes)
    percent: The percentage usage calculated as (total - available) / total * 100 (unit is percent)
    used: Memory used, calculated differently depending on the platform and designed for informational purposes only (unit is bytes)
    free: Memory not being used at all (zeroed) that is readily available; note that this doesn't reflect the actual memory available (use 'available' instead) (unit is bytes)
    active: (UNIX): memory currently in use or very recently used, and so it is in RAM (unit is bytes)
    inactive: (UNIX): memory that is marked as not used (unit is bytes)
    buffers: (Linux, BSD): cache for things like file system metadata (unit is bytes)
    cached: (Linux, BSD): cache for various things (unit is bytes)
    wired: (BSD, macOS): memory that is marked to always stay in RAM. It is never moved to disk (unit is bytes)
    shared: (BSD): memory that may be simultaneously accessed by multiple processes (unit is bytes)   

    LOAD INFO 
    min1: Average sum of the number of processes waiting in the run-queue plus the number currently executing over 1 minute (unit is number)
    min5: Average sum of the number of processes waiting in the run-queue plus the number currently executing over 5 minutes (unit is number)
    min15: Average sum of the number of processes waiting in the run-queue plus the number currently executing over 15 minutes (unit is number)
    cpucore: Total number of CPU core (unit is number)  
    '''

    # Parse the JSON info into Python objects
    parsed_node_info = []

    for node_parameter in node_info:    
        parsed_node_info.append(json.loads(node_parameter))

    #[0] is CPU, [1] is MEM, [2] is ALERTS, [3] is LOAD, [4] is PROCESSES
    CPU = parsed_node_info[0]
    MEM = parsed_node_info[1]
    ALERTS = parsed_node_info[2]
    LOAD = parsed_node_info[3]
    PROCESSES = parsed_node_info[4]

    logger.info(f'{node} information:\n'+
                f'Total CPU usage: {CPU["total"]}\n'+
                f'Load avg 1 min: {LOAD["min1"]}\n'+
                f'Total memory: {MEM["total"] * 1E-9 } Gb\n'+
                f'Available memory: {MEM["available"] * 1E-9 } Gb\n'+
                f'Total memory usage: {MEM["percent"]}\n'+
                f'Alerts: {ALERTS}\n')