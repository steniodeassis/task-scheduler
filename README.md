# task-scheduler
A task scheduler using priority queues and OOP.


## Algorithm Strategy

The priority queue is a particularly well-suited data structure to prioritize tasks because of
 its structure. A priority queue is one of the many applications of heaps, a tree data
 structure where each of its operations has a time complexity of O(lg n) for the worst-case
 output. The only case where there is a complexity of O(n lg n) is when we are building
 heaps from a non-heapified data structure. Using priority queues is also preferred over a
 sorted list because of another main property of a heap. Using a heap, we can access the
 max (for a Max-Heap) of a set of elements with a complexity of O(1); however, if we are
 getting the first element in a heap and then updating the heap, the complexity of O(lg n).
 Since we are performing one task at a time, the use of heap is more efficient in
 complexity when compared to list sorting. For example, calling insertion sort for each
 new list update has an average complexity of O(n^2), worse than using the heap O(lg n).
 Because of these and other heap properties, a priority queue is more suited to build a task
 scheduler than a list.
 Each task has its utility value which should be considered when building the heap. The
 value will be weighed differently for each type of task (whether there are dependencies or
 it is flexible). For example, tasks that should happen at a specific time will have more
 priority and, therefore, a higher utility value than tasks that do not have a fixed time to
 happen.
 Organizing the tasks as part of a unified schedule using just one priority queue is better.
 Two priority queues may make things harder since we need another system to inform
 which priority queue to follow at different times. Here, the priority queue is used to
 access the task utility value, which helps set and rearrange the tasks' time.
 
 
 There are three main classes, or object blueprints. The first one is the Max Heap class,
 which has the max-heap properties, such as heap-push (add a new element to the heap),
 pop, which takes the maximum element out of the heap; and heapify, which creates a new
 heap out of an array from a given index. Heap is a tree data structure where the parent
 will always be greater than the children. This data structure stores and access each task’s
 utility value. The second class is the Task class, which will input each task. Its attributes
 are specific to each task, such as id (a number to refer to the task), description, expected
 starting time, duration, flexibility (if the task is fixed in a time slot or not), dependencies
 (the other tasks’ ids that the task depends on); and value, which is the utility value for
 each class, based on its flexibility and number of dependencies. The last class is the
 TaskScheduler, which will take each class Task’s object and compute the most efficient
 schedule. There are two classes for each task and the scheduler because the first one has
the attribute for each task individually. While the second one has the scheduler attributes,
 so they can be treated separately.
 The code will compute the schedule based mainly on two task attributes: utility value and
 expected time. The algorithm adds the utility value in a heap and sets the times by
 checking if they are overlapping. The tiebreaker will be the value and flexibility of each
 class. If the task is flexible and there is an overlap, one of them will be shifted to earlier
 or later. Fixed tasks are always kept the same. When there is only one task for each time
 slot, the scheduler will start displaying the tasks. The scheduler will prioritize the tasks
 with higher priority (utility). Therefore they will be added first to the scheduler list. Then
 the tasks will be displayed in chronological order.
 
 The utility value represents how much of a task can have its time shifted by the scheduler
 in case of task overlapping. It is a number in the range [0.1, 1]. Classes with a utility
 value equal to 1 can only have their class shifted in terms of 1-time duration in relation to
 its expected time to start, meaning they will be shifted in a smaller range than tasks with
 lower utility. For consistency, fixed tasks always have utility equal to 1, even though they
 are never shifted. For each number of dependencies the task has, the utility will decrease
 from 1 at a rate of 0.1. For example, a task with two dependencies will have a utility
 equal to (1 - 2*(0.1)) = 0.8. Then they will be able to shift time in terms of the task
 duration divided by the value times, then in a more extensive possible range. Therefore,
 the smaller utility will increase how much the task can be shifted in minutes. The task
 will be shifted backward until it reaches an unoccupied time slot. Flexible classes with no
 dependencies have values equal to 0.9, which is smaller than the fixed tasks' utility and
 consistent with the possible range of values.
 The reason for the values is that a class with many dependencies needs to be considered
 flexible enough so that its dependencies can happen before it. And also because of the
 necessary causality between tasks.
 The number of dependencies is limited to 9 to calculate the task value; however, if a task
 has ten dependencies or more, the algorithm will set the value as 0.1 (the minimum
 bound). Below, there is a utility formula U(X) for the four cases. In the formula, X is the
 task, X.dependencies is the number of dependencies of X, and X.fixed evaluates whether
 the task is fixed (True) or flexible (False).

$$
\begin{aligned}
U(X) &= 1 \quad &\text{for } X.\text{dependencies} = 0 \text{ and } X.\text{fixed} = \text{True} \\
U(X) &= 0.9 \quad &\text{for } X.\text{dependencies} = 0 \text{ and } X.\text{fixed} = \text{False} \\
U(X) &= 1 - (X.\textit{dependencies} \cdot 0.1) \quad &\text{for } 9 \geq X.\text{dependencies} > 0 \text{ and } X.\text{fixed} = \text{False} \\
U(X) &= 0.1 \quad &\text{for } X.\text{dependencies} > 9 \text{ and } X.\text{fixed} = \text{False}
\end{aligned}
$$



 
