class Task:
    """
    Implement each task's attributes
    Attributes:
    -------
        id: int
            Task id (a reference number)   
        description: str
            Task short description   
        duration: int
            Task duration in minutes  
        expected_start: int
            Expected starting time        
        dependencies: lst
            List of task ids that need to preceed this task  
        fixed : bool
            Either the task is fixed or flexible in its expected starting time 
        completed : bool
            Current status of the task with relation to completeness
        value : int
            The utility value of the task

    """
    #Initializes an instance of Task
    
    def __init__(self, id, description, duration, expected_start, dependencies=[], fixed=False, completed=False):
        self.id = id
        self.description = description
        self.duration = duration
        self.expected_start = expected_start
        self.dependencies = dependencies
        self.fixed = fixed
        self.completed = completed
        if self.fixed == True:
            self.value = 1
        # utility value: if 1, tasks has the highest utility when done in its expected time.
        if self.dependencies == [] and self.fixed == False:
            self.value = 0.9
        # utility values has a minimum value of 0.1
        elif self.dependencies != [] and self.fixed == False:
            self.value = (1 - len(dependencies)*0.1)
            if self.value < 0.1:
                self.value = 0.1


    def __lt__(self, other):
        '''
        Compare two tasks's id and return the comparation result
        Parameters:
        -------
            other: Task object
                other task id
        Return:
        -------
            True : bool
                The task.id is smaller than the other.id
            False : bool
                The task.id is equal or greater than the other.id
        '''
        return self.id < other.id    
    

