from typing import Any, SupportsIndex, Union


class main_extra(list):

    @staticmethod
    def __get_type_lst(lst: list) -> list:
        """
        Get the types of elements in this list
        :param lst:
        :return:
        """
        if not isinstance(lst, list):
            return [type(lst)]

        result_lst: list = []

        if len(lst) == 0:
            return [Any]

        for _i in range(len(lst)):
            if type(lst[_i]) is type:
                result_lst.append(lst[_i])
            else:
                result_lst.append(type(lst[_i]))
        return list(set(result_lst))

    def _type_check(self) -> None:
        self._i2: int = 0
        try:
            for self._i in range(0, len(self)):
                if type(self[self._i2]) not in self.type_lst:
                    self.remove(self[self._i2])
                    self._i2 -= 1
                self._i2 += 1
        except IndexError:
            pass

    def _lock_check(self, __index: SupportsIndex):
        # 此时self._i表示的是比第n个锁住的元素下标大
        self._i = 0
        while __index > self._lock_lst[self._i]:
            self._i += 1
        for self._i2 in range(self._i, len(self._lock_lst)):
            self._lock_lst[self._i2] -= 1

    def _lock_check2(self):
        self._lock_lst = list(map(lambda x: x - 1, self._lock_lst))

    def __init__(self, *args, **kwargs):
        """
        This class is part of the advanced_list!
        DON'T USE THIS CLASS!
        """
        self._i = None
        self._i2 = None
        self._i3 = None
        self._type_dic = {}
        self._lock_lst = []
        self._lck_tmp_lst = None
        self._lck_tmp_lst2 = None
        self._tmp_lock_lst = None
        self._tmp_find_int = None
        self._tmp_iter = None
        self._copy_self = None
        self._result_lst = None
        self._scope_of_impact = None
        self._scope_of_impact_element = None
        self.type_lst = []
        self.auto_replenishment = self.lock_all = bool(kwargs.get("auto_replenishment"))
        self.lock_all = bool(kwargs.get("lock_all"))
        if not bool(kwargs.get("writable")):
            self.writable = True
        else:
            self.writable = bool(kwargs.get("writable"))
        self.use_type: bool = bool(kwargs.get("use_type"))
        self.ignore_error: bool = bool(kwargs.get("ignore_error"))
        self.no_prompt: bool = bool(kwargs.get("no_prompt"))
        _t = kwargs.get("type")
        self._None_t = False
        self._B_T_arg = False

        if args != () and len(args) == 1 and isinstance(list(args)[0], list):
            super().__init__(list(args)[0])
            self._B_T_arg = True
            self._T_arg = list(args)[0]
        else:
            super().__init__(args)

        if not self.use_type:
            self.type_lst = [Any]
            return

        if _t is None:
            self._None_t = True
        if isinstance(_t, list):
            if len(_t) > 0:
                for _i in range(len(_t)):
                    if not (type(_t[_i]) is type):
                        self._type_dic[_i] = type(_t[_i])
                    else:
                        self._type_dic[_i] = _t[_i]
            else:
                self._type_dic[0] = Any
        else:
            if self._B_T_arg:
                self.type_lst = self.__get_type_lst(self._T_arg)
            else:
                self.type_lst = self.__get_type_lst(list(args))
        if not self._None_t:
            for _i in range(len(self._type_dic)):
                self.type_lst.append(self._type_dic[_i])

        self._type_check()

    def __getattr__(self, item):
        if item.startsith("_"):
            raise AttributeError(f"{item} is a private attribute")
        return super().__getattr__(item)

    def type(self, _t: Union[list, Any] = None):
        """
        ENG(translator):Re-determine the list of allowed variable types based on the types within the given parameters\n
        ZH CN：根据此形参（内）的类型来重新决定允许的变量类型的列表
        :param _t:
        :return:
        """
        if not self.use_type:
            self.type_lst = [Any]
            return
        if _t is None:
            _t = self
        self.type_lst = self.__get_type_lst(_t)

        self._type_check()

    def lock(self, __index: int = None, writable: bool = True) -> None:
        """
        ENG(translator): This Function will lock element in the list, if __index is None, all element will lock. Warning! sort function cannot use when locked.\n
        ZH CN：这个函数会把列表内__index下标的元素"上锁", 无法更改（如果__index为None，则上锁所有元素），当上锁时,sort将不能使用！
        :param __index: Ths subscript of element you want to lock
        :param writable: if False, then the append,insert,extend cannot work.
        :return:
        """
        self.writable = bool(writable)

        if __index is None:
            self.lock_all = True
        else:
            if not isinstance(__index, int):
                if self.ignore_error:
                    if not self.no_prompt:
                        print(f"Parameters cannot be {type(__index)}")
                else:
                    raise TypeError(f"Parameters cannot be {type(__index)}")

        if __index > len(self)-1 or __index < -len(self)+1:
            if self.ignore_error:
                print("list index out of range")
            else:
                raise IndexError("list index out of range")
        else:
            self._lock_lst.append(__index)

        if len(self._lock_lst) == len(self):
            self.lock_all = True

    class LockError(ValueError):
        pass

    def view_lock_list(self) -> list:
        """
        Return lock_list
        :return:
        """
        return self._lock_lst

    def unlock(self, __index: int = None, writable: bool = True) -> None:
        """
        Unlock element.
        :param __index: Ths subscript of element you want to unlock
        :param writable: if False, then the append,insert,extend cannot work.
        :return:
        """
        self.writable = bool(writable)

        if __index is None:
            self._lock_lst.clear()
            self.lock_all = False
        else:
            if __index not in self._lock_lst:
                if __index > len(self) - 1 or __index < -len(self) + 1:
                    if self.ignore_error:
                        print("list index out of range")
                    else:
                        raise IndexError("list index out of range")
                if self.ignore_error:
                    if not self.no_prompt:
                        print("This elements is not lock!")
                else:
                    raise ValueError("This elements is not lock!")
            else:
                self._lock_lst.remove(__index)

    def replace(self, __o_obj=None, __n_obj=None, start: int = 0, end: int = None, step: int = 1, None_mode: bool = False) -> None:
        """
        Replace the elements in list.

        (When the __o_obj is None, all elements in the start to end range are replaced (locked elements are not deleted))

        (When the __n_obj is None, the original element is deleted)

        (If the element is locked, it is retained)
        :param __o_obj: original element
        :param __n_obj: new element
        :param start: the index of start
        :param end: the index of end
        :param step: the step of range
        :param None_mode: if you want to replace the None to other, please open this mode
        """
        if self.lock_all:
            if self.ignore_error:
                if not self.no_prompt:
                    print("All elements is locked, The replace function cannot be called")
            else:
                raise self.LockError("All elements is locked, The replace function cannot be called")

        if step < 1:
            raise ValueError("step cannot less than 1")

        if end is None:
            end = len(self)
        elif not isinstance(end, int) or end > len(self):
            end = len(self)

        if start > end:
            raise ValueError("start cannot more than end")
        self._scope_of_impact = []
        try:
            if __o_obj is None and not None_mode:
                for self._i in range(start, end, step):
                    if __n_obj is None:
                        if self._i not in self._lock_lst:
                            self._scope_of_impact.append(self._i)
                    else:
                        if self._i not in self._lock_lst:
                            super().__setitem__(self._i, __n_obj)
            else:
                for self._i in range(start, end, step):
                    if super().__getitem__(self._i) is __o_obj:
                        if __n_obj is None:
                            if self._i not in self._lock_lst:
                                self._scope_of_impact.append(self._i)
                        else:
                            if self._i not in self._lock_lst:
                                super().__setitem__(self._i, __n_obj)
            if __n_obj is None and len(self._scope_of_impact) != 0:
                self._scope_of_impact = list(reversed(self._scope_of_impact))
                for self._i in range(len(self._scope_of_impact)):
                    super().pop(self._i)
                self._scope_of_impact = list(reversed(self._scope_of_impact))
            if len(self._scope_of_impact) != 0 and len(self._lock_lst) != 0:
                self._i = 0
                while self._scope_of_impact[0] > self._lock_lst.__getitem__(self._i):
                    self._i += 1
                self._i3 = 1
                for self._i2 in range(self._i, len(self._lock_lst)):
                    self._lock_lst[self._i2] -= self._i3
                    self._i3 += 1
        except IndexError:
            pass

    def index_pro(self, item: Any, start: int = 0, end: int = None, first: bool = False) -> Union[int, tuple]:
        """
        Year, the index pro.
        Return index of value.
        Raises ValueError if the value is not present.
        :param item:
        :param start:
        :param end:
        :param first:
        :return:
        """
        if end is None:
            end = len(self)
        self._result_lst = []

        for self._i in range(start, end, 1):
            if super().__getitem__(self._i) is item:
                if first:
                    return self._i
                self._result_lst.append(self._i)

        if len(self._result_lst) != 0:
            return tuple(self._result_lst)
        else:
            raise ValueError(f"{item} is not in advanced_list")

    def only_copy_list(self) -> list:
        """
        Return a shallow copy of the list.
        """
        return super().copy()

    def end(self) -> int:
        """
        Return the subscript of last element.
        """
        self._tmp_iter = iter(self)
        self._i = -1
        try:
            while True:
                next(self._tmp_iter)
                self._i += 1
        except StopIteration:
            if self._i == -1:
                return 0
            else:
                return self._i
