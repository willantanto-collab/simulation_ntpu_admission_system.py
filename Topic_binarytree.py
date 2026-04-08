#To review all the topics learn about practical CS python in Bina Bangsa School.

def InsertNode(Current, NewItem):
    global RootPointer, FreeNode, TreeArray
    
    # 1. Check if tree is full (only on the very first call)
    if RootPointer == -1:
        RootPointer = FreeNode
        TreeArray[FreeNode][0] = -1
        TreeArray[FreeNode][1] = NewItem
        TreeArray[FreeNode][2] = -1
        FreeNode += 1
    else:
        # 2. Recursive Logic
        if NewItem < TreeArray[Current][1]:
            # Try to go Left
            if TreeArray[Current][0] == -1:
                TreeArray[Current][0] = FreeNode
                TreeArray[FreeNode][0] = -1
                TreeArray[FreeNode][1] = NewItem
                TreeArray[FreeNode][2] = -1
                FreeNode += 1
            else:
                InsertNode(TreeArray[Current][0], NewItem)
        else:
            # Try to go Right
            if TreeArray[Current][2] == -1:
                TreeArray[Current][2] = FreeNode
                TreeArray[FreeNode][0] = -1
                TreeArray[FreeNode][1] = NewItem
                TreeArray[FreeNode][2] = -1
                FreeNode += 1
            else:
                InsertNode(TreeArray[Current][2], NewItem)




#recursion binary tree

def InsertNode(Pointer, NewItem):
    global FreeNode, TreeArray
    
    # Base Case: We found an empty slot (-1)
    if Pointer == -1:
        # Create the new node at the current FreeNode index
        TempPointer = FreeNode
        TreeArray[TempPointer][0] = -1      # Left
        TreeArray[TempPointer][1] = NewItem # Data
        TreeArray[TempPointer][2] = -1      # Right
        FreeNode += 1
        return TempPointer # Return this new index to the caller
    
    # Recursive Case: Decide to go Left or Right
    if NewItem < TreeArray[Pointer][1]:
        # Update the Left Pointer with whatever the recursion returns
        TreeArray[Pointer][0] = InsertNode(TreeArray[Pointer][0], NewItem)
    else:
        # Update the Right Pointer with whatever the recursion returns
        TreeArray[Pointer][2] = InsertNode(TreeArray[Pointer][2], NewItem)
        
    return Pointer # Return the current pointer to keep the tree linked

