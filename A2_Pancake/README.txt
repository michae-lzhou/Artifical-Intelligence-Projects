Acknowledgment:
    CS 131 Slides, Stack Overflow, Google, Assignment Specifications

Implemented:
    A complete A* algorithm, UCS algorithm, and additional
    customization/preference settings towards the beginning

Assumptions:
    1. There are no duplicate pancakes allowed
    2. Each pancake is a unique number from 1 to len(pnck_list)
            i.e. A stack of 5 pancakes will have pancake sizes: 1, 2, 3, 4, 5

Architecture:
    NOTE: 'state' refers to a list or tuple of the current order of pancake sizes
    The architecture of the program is the same as the structure specified in
    the course lecture slides. The data structures used for both A* and UCS
    algorithms include 1) "pnck_list": list of pancake sizes; 2) "frontier": priority
    queue of tuples of state + cost, ordered by cost; 3) "cost": dictionary of
    key-value pairs (state : total cost); 4) "visited": set of all explored
    states; 5) "parent": dictionary of key-value pairs (child state: parent
    state).

    The A* algorithm and the UCS algorithm are implemented together, with a
    boolean value that determines whether or not the forward cost is added to
    the search. They are not two separate functions.

Testing:
    How to run: python main.py

    1. The program is highly customizable, with many different togglable settings
    within the executable. The instructions within the program should be
    intuitive enough, the following are a more comprehensive list of
    documentation of these togglable settings.
        a) Indicate how many pancakes: The user can either 1) randomly generate a
        list of valid pancake sizes between 1 and 30 pancakes or 2) indicate the
        number of pancakes to test
        b) Indicate custom list: If the user picks option 2) in step a), the
        user can then decide whether to 1) custom-describe the ordering of the
        pancakes or 2) randomly generate the order of indicated number of
        pancakes.
        c) Enter individual values: If the user picks option 1) in step b), the
        program will step through and allow the user to input individual values
        (see 2. below with regards to error-handling)
        d) Display debug info: The user has the ability to decide whether they
        want to generate a comprehensive list of debug information or skip it to
        reduce the amount of overwhelming information
        e) UCS vs A*: The user has the ability to decide whether they would like
        to run the UCS algorithm or the A* algorithm.
    2. The program has error-handling capabilities, and will terminate the
    program when an invariant (described in the assumpmtions) is violated.

    *** To supply pre-determined list of pancakes for testing, input: [# of
    pancakes] --> y --> [value] --> [value] --> ... ***

Time:
    5 hours
