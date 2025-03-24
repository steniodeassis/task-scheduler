class TaskSchedulerNoPrinting:
    '''
    A Task Scheduler Using Priority Queues for each task's utility value
    Attributes:
    -------
        tasks: lst
            List of Task objects to be inserted in the scheduler
        priority_queue : MaxHeapq object
            Priority queue used to store the task's value
        task_fixed : lst
            List of fixed tasks
        task_flexibel : lst
            List of flexbile tasks
        breaktime : int
            Break time between taskes
        hours : dic
            Tasks stored for each time slot

    '''
    def __init__(self, tasks):
        self.tasks = tasks
        self.priority_queue = MaxHeapq()    
        self.task_fixed = []
        self.task_flexible = []
        for task in self.tasks:
            if task.fixed == False:
                self.task_fixed.append(task)
            else:
                self.task_flexible.append(task)
                
        self.breaktime = 5
        self.hours = {}
        # for task in self.tasks:
        #     self.hours[task.expected_start] = [] #set the time slots
             
    def print_self(self):
        '''
        Print the tasks' description and duration. 
        It also warns about dependencies when existent.
        
        Parameters:
        -------
            None
        Return:
        -------
            None
        '''
        print("Tasks added to the simple scheduler:")
        print("--------------------------------------")
        for t in self.tasks:
            print(f"➡️'{t.description}', duration = {t.duration} mins.")   
            if len(t.dependencies)>0:
                print(f"\t ⚠️ This task depends on others!")     
                     
    def set_hours(self, task=None, new_time=None):
        '''
        Set the hours and task for each hour. 
        It also rearranges the tasks in the case there are overlapping times 
        by using tasks' flexibity and value.
        
        Parameters:
        -------
            task : Task object
                Task to be considered
            new_time : int
                Time for the class to happen
        Return:
        -------
            None
        '''
        # add a new time slot in self.hours if the task is flexible
        if task != None and new_time != None and task.fixed == False:
            if new_time not in self.hours:
                self.hours[new_time] = []
                self.hours[new_time].append(task)
                task.expected_start = new_time
            else:
                # use the utility value to update the task's time in case of overlapping by making the task happen 30 min early
                self.set_hours(task, new_time = new_time - 30/(task.value))
                
        # if the task is fixed, add the time slot expected by the use and don't change it in case of overlapping
        elif task != None and new_time != None and task.fixed == True:
            self.hours[new_time] = []
            self.hours[new_time].append(task)
            task.expected_start = new_time
        
        # if there are two tasks that coincide their starting and ending time, they should adjust their time based on their flexibility and value
        for task1 in self.tasks:
            for task2 in self.tasks:
                if task2 != task1:
                    if task1.expected_start < task2.expected_start and (task1.expected_start+task1.duration+self.breaktime) > (task2.expected_start):
                        # when only one of them is flexible
                        if task1.fixed == False and task2.fixed == True:
                            self.set_hours(task1, new_time = new_time - 30/(task1.value))
                            
                        # when only the other one is flexible
                        if task2.fixed == False and task1.fixed == True:
                            self.set_hours(task2, new_time = new_time + 30/(task2.value))
                        
                        # when both are flexible, the tiebreaker is the their utility value
                        if task1.fixed == False and task2.fixed == False:
                            if task1.value < task2.value:
                                self.set_hours(task1, new_time = new_time - 30/(task1.value))
                                
                            if task1.value > task2.value:
                                self.set_hours(task2, new_time = new_time + 30/(task2.value))
        

    def dependencies_organizer(self):
        '''
        Organize the time between dependencies of fixed tasks so that it comes before the fixed classes.
        Because fixed tasks can not be shuffled around, 
        its dependencies should always come before them.
        
        Parameters:
        -------
            None
        Return:
        -------
            None
        '''
        for fixedtask in self.task_fixed:
            for dependency in fixedtask.dependencies:
                for task in self.tasks:
                    if task.id == dependency and (task.expected_start + task.duration + self.breaktime) > fixedtask.expected_start:
                        # call set_hours to rearrange the new time
                        self.set_hours(task, task.expected_start - (30/task.value))
                                
            
    def get_tasks_ready(self):
        '''
        Set the algorithm to begin the process of scheduling
        by pushing the tasks' values in the priority queue, 
        by calling set_hours for each task and by calling the dependencies_organizer.
        
        Parameters:
        -------
            None
        Return:
        -------
            None
        '''
        for task in self.tasks:
            # If the task has no dependencies and is not yet in the queue
            if task.completed == False: 
                # Push task into the priority queue
                self.priority_queue.heappush(task.value) # it should add task.value to the priority queue instead of id
                self.set_hours(task, task.expected_start)
        self.dependencies_organizer()
                
    
    def check_unscheduled_tasks(self):
        '''
        Check whether there is any task not completed.
        
        Parameters:
        -------
            None
        Return:
        -------
            True : bool
                At least one task is not completed
            False : bool
                All tasks are completed
        '''
        for task in self.tasks:
            if task.completed == False:
                return True
        return False   
    
    def format_time(self, time):
        '''
        Format the time from only minute to display in hours and minute.
        It rounds the time not to count the seconds.
        
        Parameters:
        -------
            time : int
                Time in minutes
        Return:
        -------
            f"{round(time)//60}h{round(time)%60:02d}" : str
                Time in hours and minutes.
        '''
        return f"{round(time)//60}h{round(time)%60:02d}"
    
    def run_scheduler(self):
        '''
        Run the scheduler, by performing the get_tasks_ready method 
        and using the priority_queue as a preference for which task to compute first.
        
        The scheduler uses task_list as a way to quick storing place 
        for tasks and its computed time (from set_hours).
        
        Parameters:
        -------
            None
            
        Return:
        -------
            scheduler : str
                The scheduler in chronologic order.
            
        '''
        # set a tracking list for tasks and times
        task_list = [[] for i in self.tasks] 
        # prepare tasks
        self.get_tasks_ready()
#         print("\n\t\t🌻🌞 Good morning sunshine!🌞🌻\n\tLet's get ready together for a new and fresh day!\n")
        while self.priority_queue.heap != []:
            # tasks with the highest value are added first to the task_list
            current_value = self.priority_queue.heappop()
            for task in self.tasks:
                if task.value == current_value:
                    task_list[task.id] = [task.expected_start, task]
                    
        # tracks the total time           
        total_time = 0           
        while self.check_unscheduled_tasks():
            # set min_time to point each task from the first to the last one
            min_time = float('inf')
            for task in task_list:
                if task[0] < min_time:
                    min_time = task[0]
            # in order, print the statement for each task and hours
            for task in task_list:
                if task[0] == min_time:
#                     print(f"⏲  Next task at {self.format_time(min_time)}")
#                     print(f"\tstarted '{task[1].description}' for {task[1].duration} mins")
#                     print(f"\t✅ task completed!\n") 
                    total_time += task[1].duration
                    task[1].completed = True
                    task_list.remove(task)
#         print(f"\nWOW! You completed all planned tasks today in {total_time//60}h{total_time%60:02d}min!!!\n\t\t✨ So proud of you!✨")
                

import random
import time
import matplotlib.pyplot as plt

max_input_size = 300
n_list = range(0, max_input_size)
experiments = 50
tasks_number = 10

avg_runtime = []
tasks = []
for input_size in n_list:
    runtime = []
    random_number = random.randint(1, tasks_number)
    tasks.append(Task(id=input_size, description=f'input_size', expected_start=random_number*60, duration=input_size, dependencies=[], fixed=False))
     
    for _ in range(experiments):
        start_timer = time.process_time()
        task_scheduler = TaskSchedulerNoPrinting(tasks)
        task_scheduler.run_scheduler()
        runtime.append(time.process_time()-start_timer)
        
    avg_runtime.append(sum(runtime)/len(runtime))
    
    
#plotting
fig, ax = plt.subplots()
ax.plot(n_list, avg_runtime, color='red')
plt.title('Average runtime TaskScheduler using MaxHeapq'.format(k))
plt.xlabel('Number of tasks')
plt.ylabel('Average runtime (seconds)')
plt.show()
