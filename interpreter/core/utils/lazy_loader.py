import queue
import threading


class LazyLoader:
    """
    Class to implement lazy loading mechanism for object initialization.

    This class serves as a decorator for heavy initialization functions.
    It starts a new thread to perform the initialization process of a heavy object
    when the decorated function is defined.

    The heavy object can be obtained by calling the get method of an instance
    of this class, which will block until the object is available.

    Attributes:
    -----------
    init_func : function
        The initialization function wrapped by this decorator.

    obj_queue : queue.Queue
        A Queue object to hold the created instance of the heavy object.

    init_thread : threading.Thread
        A separate thread to perform the initialization function.

    Methods:
    --------
    _init_object():
        Performs the initialization function and puts the result in the queue.

    get():
        Gets the initialized object. This method will block until the
        object is available in the queue.
    """

    def __init__(self, init_func: callable):
        """
        Constructs the LazyLoader with the specified initialization function.

        Parameters:
        -----------
        init_func : function
            The initialization function to wrap.
        """
        self.init_func = init_func
        self.obj_queue = queue.Queue()
        self.init_thread = threading.Thread(target=self._init_object)
        self.init_thread.start()
        self.initialized_obj = None

    def _init_object(self):
        """
        Performs the initialization function and puts the result in the queue.
        """
        obj = self.init_func()
        self.obj_queue.put(obj)

    def get(self):
        """
        Gets the initialized object. This method blocks until the object is available.

        Returns:
        --------
        The initialized object.
        """
        if not self.initialized_obj:
            self.initialized_obj = self.obj_queue.get(block=True)

        return self.initialized_obj
