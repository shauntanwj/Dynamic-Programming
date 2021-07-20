# Question 1: Athlete work schedule

def max_elem(lst):
    
    """
    Input: a list of integers
    Output: the maximum integers in the list
    
    This function finds the maximum integer in a list of integers. 
    It loops through each integer in the list and compare it, and find the maximum integer.
    
    Example: max_elm([3,1,27,42,23]) returns 42
    
    Best and Worst Time complexity: O(N) where N is the length of the list
    Space Complexity: O(N) where N is the size of the input list
    Auxilliary Space Complexity: O(1)
    """
    
    max_element = lst[0]
    for i in range(1,len(lst)):
        if lst[i] > max_element:
            max_element = lst[i]
    return max_element

def takeFirst(elem):
    
    """
    Input: a tuple
    Output: the first element of the tuple
    
    This function returns the first element of the input tuple.
    
    Example: takeFirst((6,20)) returns 6
    
    Best and Worst Time Complexity: O(1)
    Space Complexity: O(N) where N is the size of the tuple
    Auxilliary Space Complexity: O(1)
    """
    
    return elem[0]

def best_schedule(weekly_income, competitions): 
    
    """
    Input: weekly_income, a list of non-negative integers. competitions, a list of tuples which each tuple 
           contains 3 non-negative integers, (start_time, end_time, winnings)
    Output: an integer which is the maximum amount of money that can earned
    
    The way I approach this question is first create tuple which contain 3 non-negative integers for each integer for weekly_income. For example,
    [1,2,3] becomes [(0,0,1), (1,1,2), (2,2,3)]. Then add them together with the competitions, work_plus_event. It will then sort the work_plus_event
    based on the first element of the tuple which is the start_time. Then create a memo list. The first element in the memo is the 
    base case which is 0. Then loop through each work_plus_event, and check for each start_time and end_time for each tuple. If the end_day 
    is greater than the weekly income, means that it will end in a week which doesn't exist, then it will just go to the next element. 
    Then, it will have a second loop that loop through the previous tuple until the base case, to check which previous tuple can be accepted
    by the current tuple, the end day of previous event equals to the previous day of the current event (does not overlap the current start_day).
    Then it will calculate the profit of it and check whether it is larger than the current profit. Then, it will 
    fill the memo with the current maximum amount of money that the current tuple can earned. Then, it will get the maximum profit of 
    all those profit in the memo.
    
    work_plus_event: the tuples for weekly_income and competitions
    previous_day: previous day of the current start_day
    current_profit: the profit earned by the current event
    
    Time Complexity: O(N^2) where N is the total number of elements in weekly income and competitions together.
    Space Complexity: O(N) where N is the total number of elements in weekly income and competitions together.
    Auxilliary Time Complexity: O(N) where N is the total number of elements in weekly income and competitions together.
    """
    
    # if weekly_income is empty, returns 0
    if len(weekly_income) == 0:
        return 0 
    
    # creating tuples for the integers in weekly_income
    for i in range(len(weekly_income)):
        weekly_income[i] = (i,i,weekly_income[i])
        
    work_plus_event = [(0,0,0)]
    work_plus_event += weekly_income + competitions
    work_plus_event.sort(key=takeFirst)     # sort the work_plus_event list
    
    memo = [-1] * (len(work_plus_event))       # initializing the memo
    memo[0] = 0         # initializing the base case
    
    for i in range(1,len(work_plus_event)):
        start_day = work_plus_event[i][0]
        end_day = work_plus_event[i][1]
        
        # check if the end_day is greater than the week
        if end_day > len(weekly_income):
            continue
        
        previous_day = work_plus_event[i][0] - 1
        current_profit = work_plus_event[i][2]
        max_profit = 0
        
        # loop from the previous tuple all the way to the first tuple
        for j in range(i-1, -1, -1):
            previous_end = work_plus_event[j][1]             # the previous tuple/event end day
            previous_optimal_profit = memo[j]       # previous optimal profit which can be earned from the previous tuple
            profit_earned = 0
            
            if previous_day < 0:
                max_profit = current_profit
                break
            
            if previous_end == previous_day:
                profit_earned = current_profit + previous_optimal_profit    # the total of working the current event and the previous event
                if profit_earned > max_profit:      # check if the profit earned is greater than the maximum profit
                    max_profit = profit_earned
            profit_earned = 0
        
        # insert the max_profit to the current memo position    
        memo[i] = max_profit
        max_profit = 0
    return max_elem(memo)


# Question 2: Sales Itinerary

def max_element_tpl(lst):
    
    """
    Input: a list of tuples
    Output: the tuples which has the largest first element
    
    This function takes a list of tuples as input and returns the tuples which has the 
    largest first element. It will first assign the first tuple in the list as the maximum then
    loop from the second tuple to the last tuple in the list t and compare each tuple's
    first element and find the largest first element of all tuples.
    
    Example:[(10,2), (100,1), (5,3)] returns (100,1)
    
    max_element: the largest first element of the tuple
    max_tuple: the tuple which has the largest first element
    
    Best and Worst Time complexity: O(N) where N is the length of the input list.
    Space Complexity: O(N) where N is the size/length of the input list.
    Axilliary Space Complexity: O(1)
    """
    
    max_element = lst[0][0] 
    max_tuple = lst[0]       
    for i in range(1,len(lst)):
        if lst[i][0] >= max_element:    # check if the current tuple's first element is larger than the max_element
            max_element = lst[i][0]
            max_tuple = lst[i]
    return max_tuple

def best_itinerary(profit, quarantine_time, home):
    
    """
    Input: profit, a list of list. quarantine_time, a list of non-negative integers. home the starting working city
    Output: an integer which is the maximum amout of money that can be earned
    
    This function will be using 2 different memo to find the maximum amout of money that can be earned. 
    First memo will save the maximum amount of money that can be earned by the salesperson in the current day and city. 
    Second memo will contain the city that the salesperson earned the optimal amount of money. 
    Both memo will be filled up row by row starting from the bottom. The base case of both memo is 0, the last row of the and first column will be 
    filled with the base case.
     
    When filling up the memo, the function will look at the bottom left diagonal city, bottom city and botom right diagonal city in memo_2.
    Bottom city is representing the salesperson is working in the same city. 
    Then it will check whether from the current city, the salesperson can be able to reach the bottom left diagonal city and botom right diagonal city.
    If the salesperson can reach those city, then it will get the work there and earned the profit.
    Lastly, the function will include all these three profit working from three different city and append them into a list.
    Each profit will be in a tuple which save (the profit, the city which the salesperson worked in).
    The function will then call max_element_tpl to get the maximum profit from these thress profits.
    Then, it will fill up the memo_1 and memo_2 accordingly.
    
    I code this function in a way that the salesperson must work in the last day, he/she can't be in quarantine or travelling
    
    num_of_days: the number of days the salesperson is working
    memo_1: the maximum amount of money that can be earned by the salesperson in the current day and city. 
    memo_2: the city that the salesperson earned the optimal amount of money. 
    
    Time Complexity: O(ND) where N is the number of cities and D is the number of days. 
    Space Complexity: O(ND) where N is the number of cities and D is the number of days. 
    Auxilliary Space Complexity: O(ND) where N is the number of cities and D is the number of days. 
    """
    
    num_of_days = len(profit)
    memo_1 = []
    memo_2 = []
    
    # Initializing memo_1
    for i in range(len(profit)+1):
        nested_lst = [0] * (len(quarantine_time)+1)
        memo_1.append(nested_lst)
    
    # Initializing memo_1 
    for i in range(len(profit)+1):
        nested_lst = [0] * (len(quarantine_time)+1)
        memo_2.append(nested_lst)

    # Initialize the second last row of both memo 
    for day in range(len(memo_1)-2,len(memo_1)-3, -1):
        for city in range(1, len(quarantine_time)+1):
            memo_1[day][city] = profit[day][city-1]
            memo_2[day][city] = city
    
    # Loop through each day then each city (row by row then column by column)        
    for day in range(len(memo_1)-3,-1,-1):
        for city in range(1,len(quarantine_time) + 1):
            work_same_day = (memo_1[day+1][city] + profit[day][city-1], city)      # the profit the salesperson earned if working at the same city
            travel_to_left_city = (0,-1)    # the profit the salesperson earned if he travel to the left city 
            travel_to_right_city = (0,-1)   # the profit the salesperson earned if he travel to the right city 
            lst_value = []          # the list to store all three different profit 
            
            # if city < 2 that means the salesperson is at city 0 which is the most left city/first city 
            # thus look at the bottom right diagonal city only
            # then it will check whether the salesperson will be able to reach the right diagonal city 
            # after considering the time of travelling and quarantine
            # if start_work(the day of start working after travelling and quarantine) > the number of days
            # then the salesperson can't reach the city
            if city < 2:    
                right_diagonal_city = memo_2[day+1][city+1]
                qua_time = quarantine_time[right_diagonal_city-1]
                total_travel_step = abs(right_diagonal_city - city)
                start_work = day + qua_time + total_travel_step
                
                # check if the salesperson can reach the bottom right diagonal city
                if start_work < len(memo_1)-1:
                    travel_to_right_city = (memo_1[start_work][right_diagonal_city],right_diagonal_city)
                    
            # if city == len(quarantine_time) that means the salesperson is at the last city which is the most right city
            # thus look at the bottom left diagonal city only     
            elif city == len(quarantine_time):
                left_diagonal_city = memo_2[day+1][city-1]
                qua_time = quarantine_time[left_diagonal_city-1]
                total_travel_step = abs(left_diagonal_city - city)
                start_work = day + qua_time + total_travel_step
                
                # check if the salesperson can reach the bottom right diagonal city
                if start_work < len(memo_1)-1:
                    travel_to_left_city = (memo_1[start_work][left_diagonal_city],left_diagonal_city)
            
            # the salesperson is able to move left or right city.        
            else:
                right_diagonal_city = memo_2[day+1][city+1]
                qua_time_right = quarantine_time[right_diagonal_city-1]
                total_travel_step_right = abs(right_diagonal_city - city)
                start_work_right = day + qua_time_right + total_travel_step_right
                
                left_diagonal_city = memo_2[day+1][city-1] # 1
                qua_time_left = quarantine_time[left_diagonal_city-1] # 3
                total_travel_step_left = abs(left_diagonal_city - city) # 2
                start_work_left = day + qua_time_left + total_travel_step_left
                
                # check if the salesperson will be able to reach both bottom left and right diagonal city
                if start_work_right < len(memo_1)-1:
                    travel_to_right_city = (memo_1[start_work_right][right_diagonal_city],right_diagonal_city)
                if start_work_left < len(memo_1)-1:
                    travel_to_left_city = (memo_1[start_work_left][left_diagonal_city],left_diagonal_city)
            
            # append the profit tuples into the list       
            lst_value.append(work_same_day) 
            lst_value.append(travel_to_left_city)
            lst_value.append(travel_to_right_city)  

            # max_tuple will have the maximum amount of money and the city
            max_tuple = max_element_tpl(lst_value)
             
            memo_1[day][city] = max_tuple[0]
            memo_2[day][city] = max_tuple[1]
            
    return memo_1[0][home+1]
















