import asyncio
from loguru import logger

import sys, os

sys.path.append(os.path.abspath(os.curdir))
from ablelabs.neon.utils.network.messenger import MessengerClient, run_server_func
from ablelabs.neon.utils.network.tcp_client import TcpClient
from ablelabs.neon.controllers.notable.api.robot_router import RobotRouter
from ablelabs.neon.controllers.notable.api.set_api import SetAPI
from ablelabs.neon.controllers.notable.api.motion_api import MotionAPI
from ablelabs.neon.controllers.notable.api.axis_api import AxisAPI
from ablelabs.neon.common.notable.constants import PIPETTE_NUMBERS
from ablelabs.neon.common.notable.enums import LocationType, Axis, LocationReference
from ablelabs.neon.common.notable.structs import Speed, FlowRate, location


class RobotAPI(MessengerClient):
    def __init__(self) -> None:
        tcp_client = TcpClient(name="tcp_client", log_func=logger.trace)
        super().__init__(tcp_client)
        self._set_api = SetAPI(tcp_client=tcp_client)
        self._motion_api = MotionAPI(tcp_client=tcp_client)
        self._axis_api = AxisAPI(tcp_client=tcp_client)

    @property
    def set(self):
        return self._set_api

    @property
    def motion(self):
        return self._motion_api

    @property
    def axis(self):
        return self._axis_api

    async def connect(self, ip, port):
        await self._tcp_client.connect(ip=ip, port=port)

    @run_server_func(RobotRouter.robot_wait_boot)
    async def wait_boot(self):
        pass

    @run_server_func(RobotRouter.robot_stop)
    async def stop(self):
        pass

    @run_server_func(RobotRouter.robot_clear_error)
    async def clear_error(self):
        pass

    @run_server_func(RobotRouter.robot_pause)
    async def pause(self):
        pass

    @run_server_func(RobotRouter.robot_resume)
    async def resume(self):
        pass

    @run_server_func(RobotRouter.robot_is_connected)
    async def is_connected(self):
        pass


async def main():
    import subprocess

    subprocess.Popen(
        [
            r"/Users/sypark/Code/ABLE-Elba/.venv/bin/python",
            r"/Users/sypark/Code/ABLE-Elba/robot/src/controllers/notable/robot_router.py",
        ],
        cwd=r"/Users/sypark/Code/ABLE-Elba",
    )
    await asyncio.sleep(1)

    logger.remove()
    # logger.add(sys.stdout, level="TRACE")
    # logger.add(sys.stdout, level="DEBUG")
    logger.add(sys.stdout, level="INFO")
    # logger.add("logs/trace.log", level="TRACE")
    # logger.add("logs/debug.log", level="DEBUG")
    logger.add("logs/info.log", level="INFO")

    ip = "localhost"
    port = 1234

    robot_api = RobotAPI()
    try:
        await robot_api.connect(ip=ip, port=port)
    except Exception as e:
        pass

    # set
    await robot_api.set.pipettes(
        {
            1: "8ch1000ul",
            2: "1ch200ul",
        }
    )
    await robot_api.set.tips(
        {
            1: "tip_1000",
            2: "tip_200",
        }
    )
    await robot_api.set.labwares(
        {
            1: "spl_trayplate_60ml_#30001",
            2: "spl_96_well_0.2ml_#30096",
            11: "ablelabs_tiprack_#AL-CT-1000",
            11: "ablelabs_tiprack_#AL-CT-200",
            12: "trash_#v2.5",
        }
    )

    # robot
    await robot_api.stop()
    await robot_api.clear_error()  # stop 이후, motion 전에.
    await robot_api.pause()
    await robot_api.resume()
    logger.info(f"is_connected = {await robot_api.is_connected()}")

    # motion
    await robot_api.motion.initialize()
    await robot_api.motion.move_to(
        pipette_number=1,
        location=location(
            location_number=1,
            well="a1",
        ),
    )

    await robot_api.motion.pick_up_tip(
        pipette_number=1,
        location=location(
            location_number=10,
            well="a1",
        ),
    )
    # await robot_api.motion.drop_tip(
    #     pipette_number=1,
    #     location=location(
    #         location_number=10,
    #         well="a1",
    #     ),
    # )
    await robot_api.motion.drop_tip(
        pipette_number=1,
        location=location(
            location_number=12,
        ),
    )

    await robot_api.motion.aspirate(
        pipette_number=1,
        volume=200,
        location=location(
            location_number=1,
            well="a1",
            reference=LocationReference.BOTTOM,
        ),
        flow_rate=FlowRate.from_ul(100),
    )
    await robot_api.motion.rise_tip(
        pipette_number=1,
        height_offset=5,
        z_speed=Speed.from_mm(2),
    )
    await robot_api.motion.dispense(
        pipette_number=1,
        volume=200,
        location=location(
            location_number=2,
            well="a1",
            reference=LocationReference.BOTTOM,
        ),
        flow_rate=FlowRate.from_ul(100),
    )
    await robot_api.motion.mix(
        pipette_number=1,
        volume=100,
        iteration=2,
        # location=location(
        #     location_number=2,
        #     well="a1",
        #     reference=LocationReference.BOTTOM,
        # ),
        flow_rate=FlowRate.from_ul(70),
        delay=0.1,
    )
    await robot_api.motion.blow_out(
        pipette_number=1,
        flow_rate=FlowRate.from_ul(200),
    )
    await robot_api.motion.move_to_ready()

    # axis
    position = await robot_api.axis.get_position(axis=Axis.X)  # mm
    await robot_api.axis.set_speed(axis=Axis.X, value=10)  # mm/sec
    await robot_api.axis.set_accel(axis=Axis.X, value=10)  # mm/sec2
    await robot_api.axis.set_decel(axis=Axis.X, value=10)  # mm/sec2
    await robot_api.axis.disable(axis=Axis.X)
    await robot_api.axis.enable(axis=Axis.X)
    await robot_api.axis.stop(axis=Axis.X)
    await robot_api.axis.home(axis=Axis.X)
    await robot_api.axis.wait_home_done(axis=Axis.X)
    await robot_api.axis.jog(axis=Axis.X, value=10)  # mm/sec
    await robot_api.axis.jog(axis=Axis.X, value=0)  # mm/sec
    await robot_api.axis.step(axis=Axis.X, value=10)  # mm
    await robot_api.axis.wait_move_done(axis=Axis.X)
    await robot_api.axis.move(axis=Axis.X, value=10)  # mm
    await robot_api.axis.wait_move_done(axis=Axis.X)


if __name__ == "__main__":
    asyncio.run(main())
