import enum
import numpy as np
from naompc import \
    Program as ProgramCpp, MpcData as MpcDataCpp, SimulationData as SimulationDataCpp, \
        Reference as ReferenceCpp, Footsteps as FootstepsCpp, FootType as FootTypeCpp, SupportPhase as SupportPhaseCpp, \
            Robot as RobotCpp, State as StateCpp, BodyPart as BodyPartCpp, WalkState as WalkStateCpp

class Footsteps(FootstepsCpp):
    def __init__(self) -> None:
        FootstepsCpp.__init__(self)
        
class FootType(enum.Enum):
    RIGHT = FootTypeCpp.RIGHT
    LEFT = FootTypeCpp.LEFT
    
class SupportPhase(enum.Enum):
    SINGLE = SupportPhaseCpp.SINGLE
    DOUBLE = SupportPhaseCpp.DOUBLE
        
class BodyPart(BodyPartCpp):
    def __init__(self) -> None:
        BodyPartCpp.__init__(self)
    
    def __str__(self) -> str:
        return super().__str__()
    
class State(StateCpp):
    def __init__(self) -> None:
        StateCpp.__init__(self)
    
    def __str__(self) -> str:
        return super().__str__()

class WalkState(WalkStateCpp):
    def __init__(self) -> None:
        WalkStateCpp.__init__(self)
    
    def __str__(self) -> str:
        return super().__str__()
    
class Robot(RobotCpp):
    def __init__(self) -> None:
        RobotCpp.__init__(self)
        
    def get_state(self) -> State:
        return super().get_state()
    
    def get_history(self) -> list[State]:
        return super().get_history()
    
    def get_walk_state(self) -> WalkState:
        return super().get_walk_state()
    
    def get_walk_history(self) -> list[WalkState]:
        return super().get_walk_history()
    
class Reference(ReferenceCpp):
    def __init__(self) -> None:
        ReferenceCpp.__init__(self)
    
    def get_trajectory(self) -> np.ndarray:
        return super().get_trajectory()
    
    def get_velocity(self) -> np.ndarray:
        return super().get_velocity()
    
class MpcData(MpcDataCpp):
    def __init__(self) -> None:
        MpcDataCpp.__init__(self)
        
class SimulationData(SimulationDataCpp):
    def __init__(self) -> None:
        SimulationDataCpp.__init__(self)

class Program(ProgramCpp):
    def __init__(self) -> None:
        ProgramCpp.__init__(self)
        
    def update(self) -> None:
        super().update()
        
    def run(self) -> None:
        super().run()
        
    def get_footsteps(self) -> Footsteps:
        return super().get_footsteps()
    
    def get_reference(self) -> Reference:
        return super().get_reference()
    
    def get_robot(self) -> Robot:
        return super().get_robot()
    
    def get_mpc_data(self) -> MpcData:
        return super().get_mpc_data()
    
    def get_sim_data(self) -> SimulationData:
        return super().get_sim_data()
