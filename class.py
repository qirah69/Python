import random

class MyList:
    list = []
    def __init__(self, initialize_with_random = False):
        if initialize_with_random:
            n = random.randint(1, 10)
            self.list = [random.randint(10, 50) for _ in range(n)]
        else:
            self.list = []
    
    def _validate_instance(self,value):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        
    def __str__(self):
        return ' '.join(map(str, self.list))
    
    def __getitem__(self, index):
        if 0 <= index < len(self.list):
            return self.list[index]
        return None

    def __setitem__(self, index, value):
        self._validate_instance(value)
        if 0 <= index < len(self.list):
            self.list[index] = value

    def _append(self, value):
        self._validate_instance(value)
        self.list.append(value)

    def _insert(self, index, value):
        self._validate_instance(value)
        if index >= len(self.list):
            self.list.append(value)
        else:
            self.list.insert(index, value)
    
    def __delitem__(self, index):
        if 0 <= index < len(self.list):
            del self.list[index]
    
    def _del_by_value(self, value):
        self._validate_instance(value)
        if value in self.list:
            del self.list[self.list.index(value)]
    
    def __contains__(self, value):
        self._validate_instance(value)
        return value in self.list
    
    def _return_first_instance(self, value, start_index=0, end_index=None):
        self._validate_instance(value)
        if end_index is None:
            end_index = len(self.list) - 1
        for i in range(start_index, end_index + 1):
            if i < len(self.list) and self.list[i] == value:
                return self.list[i]
        raise ValueError(f"{value} not found in the specified range")
    
    def __len__(self):
        return len(self.list)
    
    def slice(self, start_index, end_index):
        return self.list[start_index:end_index]
    
    def __iter__(self):
        return iter(self.list)

    def _rotate_by_value_to_right(self, value):
        if 0 <= value < len(self.list):
            self.list = self.list[-value:] + self.list[:-value]
        else:
            raise IndexError("Rotation value out of range")

lst = MyList(True)
print(str(lst))
print(lst[2])
print(lst.slice(1,4))
for i in lst:
    print(i)
print(lst._rotate_by_value_to_right(2))