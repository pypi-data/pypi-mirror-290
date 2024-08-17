import enum
import numpy as np

class SupportPhase(enum.Enum):
    SINGLE: int
    DOUBLE: int
    
class FootType(enum.Enum):
    RIGHT: int
    LEFT: int

class Footsteps:
    timestamps: np.ndarray
    num_predicted_footsteps: int
    num_controlled_footsteps: int
    theta: np.ndarray
    x: np.ndarray
    y: np.ndarray
    footstep_indices: list[int]
    support_phases: list[SupportPhase]
    
    
class BodyPart:
    pos: np.ndarray
    vel: np.ndarray
    acc: np.ndarray
    orientation: np.ndarray
    theta: float # TODO temporary
    
class State:
    left_foot: BodyPart
    right_foot: BodyPart
    com: BodyPart
    zmp_pos: np.ndarray
    zmp_vel: np.ndarray
    
class WalkState:
    current_support_foot: BodyPart
    last_support_foot: BodyPart
    support_foot_type: FootType
    walk_phase: SupportPhase
    time_of_last_step: float
    
class Robot:
    def __init__(self) -> None: ...
    def get_state(self) -> State: ...
    def get_history(self) -> list[State]: ...
    def get_walk_state(self) -> WalkState: ...
    def get_walk_history(self) -> list[WalkState]: ...
    
class Reference:
    def __init__(self) -> None: ...
    def get_trajectory(self) -> np.ndarray: ...
    def get_velocity(self) -> np.ndarray: ...
    
class MpcData:
    Xdz: np.ndarray
    Ydz: np.ndarray
    Xf: np.ndarray
    Yf: np.ndarray
    
class SimulationData:
    tk: float
    k: int

class Program:
    def __init__(self) -> None: ...
    def update(self) -> None: ...
    def run(self) -> None: ...
    def get_footsteps(self) -> Footsteps: ...
    def get_reference(self) -> Reference: ...
    def get_robot(self) -> Robot: ...
    def get_mpc_data(self) -> MpcData: ...
    def get_sim_data(self) -> SimulationData: ...