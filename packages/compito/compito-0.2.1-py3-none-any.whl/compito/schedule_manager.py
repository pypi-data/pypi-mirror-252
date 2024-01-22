import datetime
import multiprocessing
import sys
from typing import List

from compito.command import Command
from compito.utils import get_commands


class ScheduleManager:

    def __init__(self):
        self.commands = get_commands()
        self.utcnow = datetime.datetime.now(datetime.UTC).replace(second=0, microsecond=0)

    def get_start_candidates(self) -> List[Command]:
        return [command() for command in self.commands.values() if command.scheduler and command.scheduler.is_due(self.utcnow)]

    def start_scheduled_commands(self):
        candidates = self.get_start_candidates()
        sys.stdout.write(f'[{self.utcnow}] Starting {len(candidates)} scheduled commands:\n')
        sys.stdout.write(
            '\n'.join([f"{command.command_name}({command.scheduler.cron_pattern})\n" for command in candidates])
        )
        processes = []

        for command in candidates:
            process = multiprocessing.Process(target=command.execute, kwargs=command.default_args)
            process.start()
            processes.append(process)
        for process in processes:
            process.join()
