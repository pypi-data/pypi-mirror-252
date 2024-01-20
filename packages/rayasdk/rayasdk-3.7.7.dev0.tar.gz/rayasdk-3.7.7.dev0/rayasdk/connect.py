# Copyright 2020 Unlimited Robotics
import subprocess
import json

import rayasdk.constants as constants
from rayasdk.sshKeyGen import SshKeyGen
from rayasdk.logger import log_verbose, log_info


class URConnect:

    COMMAND = 'connect'

    def __init__(self):
        pass


    def init_parser(self, subparser):
        self.parser = subparser.add_parser(
            type(self).COMMAND, help="execute current Raya project.")
        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--robot-id',
                           help='robot identificator (from scan list)',
                           type=str)
        group.add_argument('--robot-ip',
                           help='robot ip (from scan list)',
                           type=str)
        group.add_argument('--simulator',
                           help='connect the project to the simulator',
                           action="store_true")

    def run(self, args, unknownargs):
        self.args = args
        self.unknownargs = unknownargs

        robot_id = self.args.robot_id
        robot_ip = self.args.robot_ip
        try:
            exec_settings = dict()
            exec_settings[constants.JSON_EXECINFO_SIM] = False
            exec_settings[constants.JSON_EXECINFO_ROBCONN] = dict()
            robot_connection = exec_settings[constants.JSON_EXECINFO_ROBCONN]
            robot_connection[constants.JSON_EXECINFO_ROBID] = ''
            robot_connection[constants.JSON_EXECINFO_ROBIP] = ''

            if self.args.simulator:
                exec_settings[constants.JSON_EXECINFO_SIM] = True
                # Send ssh key to simulation
                SshKeyGen(user=constants.SSH_USER,
                          host='localhost',
                          port=constants.SSH_PORT)
                log_info(f'You have successfully connected to the simulator')
            else:
                with open(file=constants.LAST_SCANNING_PATH,
                          mode='r',
                          encoding='utf-8') as f:
                    scanned_robots = json.load(f)
                # Check if robot is in last scan
                for robot in scanned_robots:
                    scanned_robot = scanned_robots[robot]
                    is_robot_id = robot_id and robot_id in scanned_robot[
                        "ROBOT_ID"]
                    is_robot_ip = robot_ip and robot_ip in scanned_robot[
                        "ROBOT_IP"]
                    if is_robot_id or is_robot_ip:
                        if constants.JSON_EXECINFO_ROBCONN not in exec_settings:
                            robot_connection = {}

                        if robot_connection[
                                constants.JSON_EXECINFO_ROBID] != '':
                            raise NameError(
                                (f'\'{robot_id}\' was detected with '
                                 'multiple IP addresses, connect using the'
                                 ' \'--robot-ip\' argument instead.'))

                        robot_connection[constants.JSON_EXECINFO_ROBID] = \
                            scanned_robot[constants.JSON_SCAN_ID]
                        robot_connection[constants.JSON_EXECINFO_ROBIP] = \
                            scanned_robot[constants.JSON_SCAN_IP]
                        robot_connection[constants.JSON_EXECINFO_ROBSERIAL] = \
                            scanned_robot[constants.JSON_SCAN_SERIAL]

                # If the robot was not found on the scan raise exception
                if robot_connection[constants.JSON_EXECINFO_ROBID] == '':
                    if robot_id:
                        raise NameError(
                            (f'Robot ID "{robot_id}" not found in scan info, '
                             'verify it or scan again.'))
                    elif robot_ip:
                        raise NameError(
                            (f'Robot IP "{robot_ip}" not found in scan info, '
                             'verify it or scan again.'))
                    else:
                        raise KeyError('')

                # Send ssh key to robot
                SshKeyGen(user=constants.SSH_USER,
                          host=robot_connection[constants.JSON_EXECINFO_ROBIP],
                          port=constants.SSH_PORT)
                log_info(f'You have successfully connected to '
                         f'{robot_connection[constants.JSON_EXECINFO_ROBID]}')

            # Save connection globally
            with open(
                file=constants.CONNECTION_SETTINGS_PATH,
                mode='w',
                encoding='utf-8'
            ) as f:
                settings = dict()
                settings[constants.JSON_EXECINFO_SIM] = exec_settings[
                    constants.JSON_EXECINFO_SIM]
                settings[constants.JSON_EXECINFO_ROBCONN] = exec_settings[
                    constants.JSON_EXECINFO_ROBCONN]
                json.dump(settings, f, ensure_ascii=False, indent=4)

        except FileNotFoundError:
            raise Exception((
                f'Last scan was empty or wasn\'t executed, '
                'execute \'rayasdk scan\' and check '
                'if the robot is appears in the scan.'
            ))
        except subprocess.SubprocessError:
            raise Exception("SSH Key not send, Check if raya_os is running")
        except NameError as error:
            raise Exception(str(error))
        except KeyError as error:
            log_info(error)
            raise Exception((f'Scanning info malformed, '
                             'please scan again by running "rayasdk scan".'))

        log_verbose('\nCorrect!')
        return True
