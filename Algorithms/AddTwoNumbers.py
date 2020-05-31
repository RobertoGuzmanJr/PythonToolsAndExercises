"""

ADD TWO NUMBERS:

You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example:

Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8
Explanation: 342 + 465 = 807.

"""

class Solution:
    def toNumber(self,l):
        s = ""
        current = l
        while current:
            s +=str(current.val)
            current = current.next
        t = s[::-1]
        return int(t)            
    
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        x1 = self.toNumber(l1)
        x2 = self.toNumber(l2)
        y = str(x1 + x2)
        previous = None
        head = None
        for c in y[::-1]:
            current = ListNode(int(c))
            if previous is None:
                previous = current
                head = current
            else:
                previous.next = current
                previous = current
        return head  
