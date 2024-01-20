import asyncio
import base64
import os
from pathlib import Path
import requests
from .assets import Asset
from .flow import RobotFlow
from .logs import Log
from .queues import Queue
from .server import OrchestratorAPI


class Bot(object):
    """
    This class is used to interact with the iBott Orchestrator API.
    Arguments:
        RobotId: The ID of the robot.
        ExecutionId: The ID of the execution.
    Attributes:
        connection: The connection to the Orchestrator API.
        robot_id: The ID of the robot.
        execution_id: The ID of the execution.
        log: log class instance.
        queue: queue class instance.
    Methods:
        create_queue(queue_name): Create a queue.
        find_queue_by_id(queue_id): Find a queue by its ID.
        find_queues_by_name(queue_name): Find all queues by its name.
        get_asset_by_name(asset_name): Get an asset by its name.
        get_asset_by_id(asset_id): Get an asset by its ID.
        save_file_from_orchestrator(file_path, file_name): Save a file from the Orchestrator API.
        finish_execution(): Finish the execution in the Orchestrator API.

    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        disabled = kwargs.get('disabled', True)
        self.connection = None
        if not disabled:
            self.connection = OrchestratorAPI(**self.kwargs)
            self.robot_id = kwargs.get('RobotId', None)
            self.execution_id = kwargs.get('ExecutionId', None)
            self.parameters = kwargs.get('params', None)
            if not self.robot_id:
                self.robot_id = str(input("Write RobotId: "))
            self.queue = None
        self.log = Log(self.connection)
        self.exception = None
        self.flow = RobotFlow.connect_nodes()
        self.node = RobotFlow.nodes[0]
        self.run()

    def run(self):
        while self.node:
            try:
                if self.node.args is None:
                    args = self.node.method(self)
                    self.node.retry_times = 0
                else:
                    args = self.node.method(self, self.node.args)
                    self.node.retry_times = 0
                if args is None:
                    self.node = self.node.get_next()
                else:
                    self.node = self.node.get_next(args)
                if self.node:
                    self.node.args = args
            except Exception as e:
                if self.node.exception:
                    self.node.exception.process_exception()
                else:
                    raise Exception(e)


    def create_queue(self, queue_name: str):
        """
        This method is used to create a queue.
        Arguments:
            queue_name: The name of the queue.
        Returns:
            queue object.
        """
        queue = Queue(connection=self.connection, robot_id=self.robot_id, queue_name=queue_name)
        return queue

    def find_queue_y_id(self, queue_id: str):
        """b
        This method is used to find a queue by its ID.
        Arguments:
            queue_id: The ID of the queue.
        Returns:
            Queue object: The Queue where items are stored in

        """
        queue = Queue(connection=self.connection, robot_id=self.robot_id, queue_id=queue_id)
        return queue

    def find_queues_by_name(self, queue_name: str):
        """
        This method is used to find queues by their name.
        Arguments:
             queue_name:  The name of the queue.
        Returns:
            list: A list of Queue objects.
        """
        queue_list = []
        end_point = f'{self.connection.http_protocol}{self.connection.url}/api/queues/QueueName={queue_name}/'
        try:
            queues = requests.get(end_point, headers=self.connection.headers)
        except:
            raise Exception("Orchestrator is not connected")
        for queue_data in queues.json():
            queue = Queue(connection=self.connection, queue_id=queue_data['QueueId'])
            queue_list.append(queue)
        return queue_list

    def get_asset_by_name(self, asset_name: str):
        """
        This method is used to find an asset by its name.
        Arguments:
            asset_name: The name of the asset.
        Returns:
            Asset object: The Asset object.
        """
        return Asset(connection=self.connection, asset_name=asset_name)

    def get_asset_by_id(self, asset_id: str):
        """
        This method is used to find an asset by its ID.
        Arguments:
            asset_id: The ID of the asset.
        Returns:
            Asset object: The Asset object.
        """
        return Asset(connection=self.connection, asset_id=asset_id)

    @staticmethod
    def save_file_from_console(string, folder=None):
        """
        This method is used to save a file sent to the robot execution from the orchestrator console.
        Arguments:
            string: The string  in base64 format to save.
            folder: The folder where to save the file.
        Returns:
            file_path: The path of the saved file.
        """
        if folder is None:
            folder = Path(os.path.dirname(os.path.realpath(__file__))).parent
        base = string.split(",")[-1]
        filename = string.split(",")[0]
        file = base64.b64decode(base)
        f = open(os.path.join(folder, filename), "wb")
        f.write(file)
        f.close()
        return os.path.join(folder, filename)
