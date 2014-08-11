"""
http://stackoverflow.com/questions/8637254/intercept-operator-lookup-on-metaclass
"""

operators = ["add", "mul"]


class OperatorHackiness(object):
  """
  Use this base class if you want your object
  to intercept __add__, __iadd__, __radd__, __mul__ etc.
  using __getattr__.
  __getattr__ will called at most _once_ during the
  lifetime of the object, as the result is cached!
  """

  def __init__(self):
    # create a instance-local base class which we can
    # manipulate to our needs
    self.__class__ = self.meta = type('tmp', (self.__class__,), {})


# add operator methods dynamically, because we are damn lazy.
# This loop is however only called once in the whole program
# (when the module is loaded)
def create_operator(name):
  def dynamic_operator(self, *args):
    # call getattr to allow interception
    # by user
    func = self.__getattr__(name)
    # save the result in the temporary
    # base class to avoid calling getattr twice
    setattr(self.meta, name, func)
    # use provided function to calculate result
    return func(self, *args)
  return dynamic_operator


for op in operators:
    for name in ["__%s__" % op, "__r%s__" % op, "__i%s__" % op]:
        setattr(OperatorHackiness, name, create_operator(name))
