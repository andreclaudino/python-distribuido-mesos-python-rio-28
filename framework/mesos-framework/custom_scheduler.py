import logging
import uuid

from pymesos.interface import Scheduler

logging.basicConfig(level=logging.INFO)


class CustomScheduler(Scheduler):

    def __init__(self, executor):
        self.executor = executor

    def registered(self, driver, frameworkId, masterInfo):
        logging.info(f"Registered with framework id {frameworkId} on master host {masterInfo.hostname}")

    def resourceOffers(self, driver, offers):
        filters = {'refuse_seconds': 5}

        for offer in offers:
            logging.info(f"Recieved resource offers: {offer.id.value}")

            task = new_task(self.executor, offer)
            driver.launchTasks(offer.id, [task], filters)

    def getResource(self, res, name):
        for r in res:
            if r.name == name:
                return r.scalar.value

    def statusUpdate(self, driver, update):
        logging.debug('Status update TID %s %s',
                      update.task_id.value,
                      update.state)


def new_task(executor, offer, mem, cpu):
    task = dict()
    task.task_id = dict()
    task.task_id.value = str(uuid.uuid4())
    task.agent_id = dict()
    task.agent_id.value = offer.agent_id.value
    task.name = f'task {task.task_id.value}'
    task.executor = executor
    task.data = f'Hello from task {task_id}!'

    task.resources = [
        dict(name='cpus', type='SCALAR', scalar={'value': cpu}),
        dict(name='mem', type='SCALAR', scalar={'value': mem}),
    ]

    return task

