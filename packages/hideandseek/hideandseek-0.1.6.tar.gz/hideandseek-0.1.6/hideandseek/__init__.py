__version__ = "0.1.6"
from . import eval as E
# from . import trainer
from .trainer import Trainer
from . import validation as V
from . import utils as U
from . import dataset as D

# TODO: Change V.EarlyStopping funcionality into node. patience & primary scorer etc should be managed by node, not validation.
# TODO: Change naming: cross validation -> validation
# TODO: Change naming: eval -> evaluation (eval is a python function)
