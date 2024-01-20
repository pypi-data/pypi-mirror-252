# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.1.1
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _tesseract_motion_planners_python
else:
    import _tesseract_motion_planners_python

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "this":
            set(self, name, value)
        elif name == "thisown":
            self.this.own(value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


import weakref

SHARED_PTR_DISOWN = _tesseract_motion_planners_python.SHARED_PTR_DISOWN
class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _tesseract_motion_planners_python.delete_SwigPyIterator

    def value(self):
        return _tesseract_motion_planners_python.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _tesseract_motion_planners_python.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _tesseract_motion_planners_python.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _tesseract_motion_planners_python.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _tesseract_motion_planners_python.SwigPyIterator_equal(self, x)

    def copy(self):
        return _tesseract_motion_planners_python.SwigPyIterator_copy(self)

    def next(self):
        return _tesseract_motion_planners_python.SwigPyIterator_next(self)

    def __next__(self):
        return _tesseract_motion_planners_python.SwigPyIterator___next__(self)

    def previous(self):
        return _tesseract_motion_planners_python.SwigPyIterator_previous(self)

    def advance(self, n):
        return _tesseract_motion_planners_python.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _tesseract_motion_planners_python.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _tesseract_motion_planners_python.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _tesseract_motion_planners_python.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _tesseract_motion_planners_python.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _tesseract_motion_planners_python.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _tesseract_motion_planners_python.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _tesseract_motion_planners_python:
_tesseract_motion_planners_python.SwigPyIterator_swigregister(SwigPyIterator)
import tesseract_robotics.tesseract_environment.tesseract_environment_python
import tesseract_robotics.tesseract_kinematics.tesseract_kinematics_python
import tesseract_robotics.tesseract_common.tesseract_common_python
import tesseract_robotics.tesseract_scene_graph.tesseract_scene_graph_python
import tesseract_robotics.tesseract_geometry.tesseract_geometry_python
import tesseract_robotics.tesseract_srdf.tesseract_srdf_python
import tesseract_robotics.tesseract_state_solver.tesseract_state_solver_python
import tesseract_robotics.tesseract_collision.tesseract_collision_python
import tesseract_robotics.tesseract_command_language.tesseract_command_language_python
@_swig_add_metaclass(_SwigNonDynamicMeta)
class PlannerProfileRemappingUPtr(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __setattr__ = _swig_setattr_nondynamic_instance_variable(object.__setattr__)
    __repr__ = _swig_repr

    def __init__(self, *args):
        _tesseract_motion_planners_python.PlannerProfileRemappingUPtr_swiginit(self, _tesseract_motion_planners_python.new_PlannerProfileRemappingUPtr(*args))

    def __deref__(self):
        return _tesseract_motion_planners_python.PlannerProfileRemappingUPtr___deref__(self)

    def release(self):
        return _tesseract_motion_planners_python.PlannerProfileRemappingUPtr_release(self)

    def reset(self, *args):
        return _tesseract_motion_planners_python.PlannerProfileRemappingUPtr_reset(self, *args)

    def swap(self, __u):
        return _tesseract_motion_planners_python.PlannerProfileRemappingUPtr_swap(self, __u)

    def get(self):
        return _tesseract_motion_planners_python.PlannerProfileRemappingUPtr_get(self)

    def __nonzero__(self):
        return _tesseract_motion_planners_python.PlannerProfileRemappingUPtr___nonzero__(self)
    __bool__ = __nonzero__


    __swig_destroy__ = _tesseract_motion_planners_python.delete_PlannerProfileRemappingUPtr

# Register PlannerProfileRemappingUPtr in _tesseract_motion_planners_python:
_tesseract_motion_planners_python.PlannerProfileRemappingUPtr_swigregister(PlannerProfileRemappingUPtr)
@_swig_add_metaclass(_SwigNonDynamicMeta)
class PlannerRequest(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __setattr__ = _swig_setattr_nondynamic_instance_variable(object.__setattr__)
    __repr__ = _swig_repr
    name = property(_tesseract_motion_planners_python.PlannerRequest_name_get, _tesseract_motion_planners_python.PlannerRequest_name_set, doc=r""" The name of the process manager to use""")
    env = property(_tesseract_motion_planners_python.PlannerRequest_env_get, _tesseract_motion_planners_python.PlannerRequest_env_set, doc=r""" The environment""")
    env_state = property(_tesseract_motion_planners_python.PlannerRequest_env_state_get, _tesseract_motion_planners_python.PlannerRequest_env_state_set, doc=r""" The start state to use for planning""")
    profiles = property(_tesseract_motion_planners_python.PlannerRequest_profiles_get, _tesseract_motion_planners_python.PlannerRequest_profiles_set, doc=r""" The profile dictionary""")
    instructions = property(_tesseract_motion_planners_python.PlannerRequest_instructions_get, _tesseract_motion_planners_python.PlannerRequest_instructions_set, doc=r"""
    The program instruction
    This must contain a minimum of two move instruction the first move instruction is the start state
    """)
    plan_profile_remapping = property(_tesseract_motion_planners_python.PlannerRequest_plan_profile_remapping_get, _tesseract_motion_planners_python.PlannerRequest_plan_profile_remapping_set, doc=r"""
    This allows the remapping of the Plan Profile identified in the command language to a specific profile for a
    given motion planner.
    """)
    composite_profile_remapping = property(_tesseract_motion_planners_python.PlannerRequest_composite_profile_remapping_get, _tesseract_motion_planners_python.PlannerRequest_composite_profile_remapping_set, doc=r"""
    This allows the remapping of the Composite Profile identified in the command language to a specific profile
    for a given motion planner.
    """)
    verbose = property(_tesseract_motion_planners_python.PlannerRequest_verbose_get, _tesseract_motion_planners_python.PlannerRequest_verbose_set, doc=r""" Indicate if output should be verbose""")
    format_result_as_input = property(_tesseract_motion_planners_python.PlannerRequest_format_result_as_input_get, _tesseract_motion_planners_python.PlannerRequest_format_result_as_input_set, doc=r"""
    Format the result as input for motion planning

       - If true it uses the input waypoint but updates the seed component
       - If false, it replace the input waypoint with a state waypoint
    """)
    data = property(_tesseract_motion_planners_python.PlannerRequest_data_get, _tesseract_motion_planners_python.PlannerRequest_data_set, doc=r"""
    data Planner specific data. For planners included in Tesseract_planning this is the planner problem that
    will be used if it is not null
    """)

    def __init__(self):
        _tesseract_motion_planners_python.PlannerRequest_swiginit(self, _tesseract_motion_planners_python.new_PlannerRequest())
    __swig_destroy__ = _tesseract_motion_planners_python.delete_PlannerRequest

# Register PlannerRequest in _tesseract_motion_planners_python:
_tesseract_motion_planners_python.PlannerRequest_swigregister(PlannerRequest)
@_swig_add_metaclass(_SwigNonDynamicMeta)
class PlannerResponse(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __setattr__ = _swig_setattr_nondynamic_instance_variable(object.__setattr__)
    __repr__ = _swig_repr
    results = property(_tesseract_motion_planners_python.PlannerResponse_results_get, _tesseract_motion_planners_python.PlannerResponse_results_set)
    successful = property(_tesseract_motion_planners_python.PlannerResponse_successful_get, _tesseract_motion_planners_python.PlannerResponse_successful_set, doc=r""" Indicate if planning was successful""")
    message = property(_tesseract_motion_planners_python.PlannerResponse_message_get, _tesseract_motion_planners_python.PlannerResponse_message_set, doc=r""" The status message""")
    succeeded_instructions = property(_tesseract_motion_planners_python.PlannerResponse_succeeded_instructions_get, _tesseract_motion_planners_python.PlannerResponse_succeeded_instructions_set, doc=r""" Waypoints for which the planner succeeded""")
    failed_instructions = property(_tesseract_motion_planners_python.PlannerResponse_failed_instructions_get, _tesseract_motion_planners_python.PlannerResponse_failed_instructions_set, doc=r""" Waypoints for which the planner failed""")
    data = property(_tesseract_motion_planners_python.PlannerResponse_data_get, _tesseract_motion_planners_python.PlannerResponse_data_set, doc=r""" Planner specific data. Planners in Tesseract_planning use this to store the planner problem that was solved""")

    def __nonzero__(self):
        return _tesseract_motion_planners_python.PlannerResponse___nonzero__(self)
    __bool__ = __nonzero__



    def __init__(self):
        _tesseract_motion_planners_python.PlannerResponse_swiginit(self, _tesseract_motion_planners_python.new_PlannerResponse())
    __swig_destroy__ = _tesseract_motion_planners_python.delete_PlannerResponse

# Register PlannerResponse in _tesseract_motion_planners_python:
_tesseract_motion_planners_python.PlannerResponse_swigregister(PlannerResponse)
@_swig_add_metaclass(_SwigNonDynamicMeta)
class MotionPlanner(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __setattr__ = _swig_setattr_nondynamic_instance_variable(object.__setattr__)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _tesseract_motion_planners_python.delete_MotionPlanner

    def getName(self):
        r"""
        Get the name of this planner
        This is also used as the namespace for the profiles in the profile dictionary
        """
        return _tesseract_motion_planners_python.MotionPlanner_getName(self)

    def solve(self, request):
        r"""
        Solve the planner request problem
        :type request: :py:class:`PlannerRequest`
        :param request: The planning request
        :rtype: :py:class:`PlannerResponse`
        :return: A planner reponse
        """
        return _tesseract_motion_planners_python.MotionPlanner_solve(self, request)

    def terminate(self):
        r"""
        If solve() is running, terminate the computation. Return false if termination not possible. No-op if
        solve() is not running (returns true).
        """
        return _tesseract_motion_planners_python.MotionPlanner_terminate(self)

    def clear(self):
        r""" Clear the data structures used by the planner"""
        return _tesseract_motion_planners_python.MotionPlanner_clear(self)

    def clone(self):
        r""" Clone the motion planner"""
        return _tesseract_motion_planners_python.MotionPlanner_clone(self)

    @staticmethod
    def checkRequest(request):
        r""" Check planning request"""
        return _tesseract_motion_planners_python.MotionPlanner_checkRequest(request)

    @staticmethod
    def assignSolution(mi, joint_names, joint_values, format_result_as_input):
        r""" Assign a solution to the move instruction"""
        return _tesseract_motion_planners_python.MotionPlanner_assignSolution(mi, joint_names, joint_values, format_result_as_input)

# Register MotionPlanner in _tesseract_motion_planners_python:
_tesseract_motion_planners_python.MotionPlanner_swigregister(MotionPlanner)

def toToolpath(*args):
    r"""
    *Overload 1:*

    Extract toolpath from a instruction
    :type instruction: :py:class:`InstructionPoly`
    :param instruction: The instruction to extract toolpath
    :type env: :py:class:`Environment`
    :param env: The environment object used for getting kinematics and tcp information
    :rtype: tesseract_common::Toolpath
    :return: A toolpath in world coordinate system

    |

    *Overload 2:*

    Extract toolpath from a composite instruction
    :param instruction: The instruction to extract toolpath
    :type env: :py:class:`Environment`
    :param env: The environment object used for getting kinematics and tcp information
    :rtype: tesseract_common::Toolpath
    :return: A toolpath in world coordinate system

    |

    *Overload 3:*

    Extract toolpath from a move instruction
    :param instruction: The instruction to extract toolpath
    :type env: :py:class:`Environment`
    :param env: The environment object used for getting kinematics and tcp information
    :rtype: tesseract_common::Toolpath
    :return: A toolpath in world coordinate system
    """
    return _tesseract_motion_planners_python.toToolpath(*args)

def assignCurrentStateAsSeed(composite_instructions, env):
    r"""
    This will assign the current state as the seed for all cartesian waypoint
    :type composite_instructions: :py:class:`CompositeInstruction`
    :param composite_instructions: The input program
    :type env: :py:class:`Environment`
    :param env: The environment information
    """
    return _tesseract_motion_planners_python.assignCurrentStateAsSeed(composite_instructions, env)

def formatProgram(composite_instructions, env):
    r"""
    This formats the joint and state waypoints to align with the kinematics object
    :type composite_instructions: :py:class:`CompositeInstruction`
    :param composite_instructions: The input program to format
    :type env: :py:class:`Environment`
    :param env: The environment information
    :rtype: boolean
    :return: True if the program required formatting.
    """
    return _tesseract_motion_planners_python.formatProgram(composite_instructions, env)

def contactCheckProgram(*args):
    r"""
    *Overload 1:*

    Should perform a continuous collision check over the trajectory.
    :type contacts: std::vector< tesseract_collision::ContactResultMap,std::allocator< tesseract_collision::ContactResultMap > >
    :param contacts: A vector of vector of ContactMap where each index corresponds to a timestep
    :type manager: :py:class:`ContinuousContactManager`
    :param manager: A continuous contact manager
    :type state_solver: :py:class:`StateSolver`
    :param state_solver: The environment state solver
    :type program: :py:class:`CompositeInstruction`
    :param program: The program to check for contacts
    :type config: :py:class:`CollisionCheckConfig`
    :param config: CollisionCheckConfig used to specify collision check settings
    :rtype: boolean
    :return: True if collision was found, otherwise false.

    |

    *Overload 2:*

    Should perform a discrete collision check over the trajectory
    :type contacts: std::vector< tesseract_collision::ContactResultMap,std::allocator< tesseract_collision::ContactResultMap > >
    :param contacts: A vector of vector of ContactMap where each index corresponds to a timestep
    :type manager: :py:class:`DiscreteContactManager`
    :param manager: A continuous contact manager
    :type state_solver: :py:class:`StateSolver`
    :param state_solver: The environment state solver
    :type program: :py:class:`CompositeInstruction`
    :param program: The program to check for contacts
    :type config: :py:class:`CollisionCheckConfig`
    :param config: CollisionCheckConfig used to specify collision check settings
    :rtype: boolean
    :return: True if collision was found, otherwise false.
    """
    return _tesseract_motion_planners_python.contactCheckProgram(*args)
RobotConfig_NUT = _tesseract_motion_planners_python.RobotConfig_NUT
RobotConfig_FUT = _tesseract_motion_planners_python.RobotConfig_FUT
RobotConfig_NDT = _tesseract_motion_planners_python.RobotConfig_NDT
RobotConfig_FDT = _tesseract_motion_planners_python.RobotConfig_FDT
RobotConfig_NDB = _tesseract_motion_planners_python.RobotConfig_NDB
RobotConfig_FDB = _tesseract_motion_planners_python.RobotConfig_FDB
RobotConfig_NUB = _tesseract_motion_planners_python.RobotConfig_NUB
RobotConfig_FUB = _tesseract_motion_planners_python.RobotConfig_FUB

def getRobotConfig(*args):
    r"""
    Get the configuration of a six axis industrial robot
    :type joint_group: :py:class:`JointGroup`
    :param joint_group: The kinematics JointGroup.
    :type base_link: string
    :param base_link: The base link to use.
    :type tcp_frame: string
    :param tcp_frame: The tip link to use.
    :type joint_values: Eigen::Ref< Eigen::Matrix< double,Eigen::Dynamic,1 > const >
    :param joint_values: The joint group joint values and assumes the last six are for the robot.
    :type sign_correction: Eigen::Ref< Eigen::Vector2i const >, optional
    :param sign_correction: Correct the sign for Joint 3 and Joint 5 based on the robot manufacturer.
    :rtype: int
    :return: Robot Config
    """
    return _tesseract_motion_planners_python.getRobotConfig(*args)

def getJointTurns(joint_values):
    r"""
    Get number of turns for joints that allow rotation beyond +- 180 degrees
    :param joint: values The joint values of the robot
    :rtype: Eigen::VectorXi
    :return: The number of turns (as integers), in a vector
    """
    return _tesseract_motion_planners_python.getJointTurns(joint_values)

cvar = _tesseract_motion_planners_python.cvar
RobotConfigString = cvar.RobotConfigString

