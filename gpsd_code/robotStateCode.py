from transitions import Machine

class RobotState(object):

    # Define states. 
    states = ['car_INIT', 'car_CALLED', 'car_ACCEPTED', 'car_ARRIVED', 'car_LOADED']

    def __init__(self):

        # Initialize the state machine
        self.machine = Machine(model=self, states=RobotState.states, initial='INIT')

        # self.machine.add_transition(source='curent_state', trigger='__enter__',      dest='new_state',    after='__exit__')

        # Transitions
        self.machine.add_transition(source='car_INIT',     trigger='call_robot',     dest='car_CALLED',   after='called_session')
        self.machine.add_transition(source='car_CALLED',   trigger='accepted_robot', dest='car_ACCEPTED', after='accepted_session')
        self.machine.add_transition(source='car_ACCEPTED', trigger='robot_arrived',  dest='car_ARRIVED',  after='arrived_session')
        self.machine.add_transition(source='car_ARRIVED',  trigger='robot_loaded',   dest='car_LOADED',   after='loaded_session')
        self.machine.add_transition(source='car_LOADED',   trigger='user_reset',     dest='car_COMPLETE', after='reset_session')

        # Cancellation routes
        self.machine.add_transition(source='car_CALLED',   trigger='cancel_robot',   dest='car_CANCEL',     after='canceled_session')
        self.machine.add_transition(source='car_ACCEPTED', trigger='cancel_accept',  dest='car_CANCEL',     after='canceled_accept_session')
        self.machine.add_transition(source='car_ARRIVED',  trigger='cancel_load',    dest='car_CANCEL',     after='canceled_load_session')

        # Reset route
        self.machine.add_transition(source='car_COMPLETE', trigger='reset_complete', dest='car_INIT',     after='reset_session')
        self.machine.add_transition(source='car_CANCEL',   trigger='reset_cancel',   dest='car_INIT',     after='reset_session')


    def called_session(self):           print("Now in state: " + self.state)
    def accepted_session(self):         print("Now in state: " + self.state)
    def arrived_session(self):          print("Now in state: " + self.state)
    def loaded_session(self):           print("Now in state: " + self.state)

    def canceled_session(self):         print("Now in state: " + self.state)
    def canceled_accept_session(self):  print("Now in state: " + self.state)
    def canceled_load_session(self):    print("Now in state: " + self.state)

    def reset_session(self):            print("Now in state: " + self.state)
