from containers import DataContainer
from single_callables import (AtomicCallable,
                              AtomicHandler,
                              AtomicDispatchSetter,
                              SideEffectCallable,
                              SideEffectHandler,
                              DispatchSetter)
from collection_callables import CallablesChain, CallableDispatcher
from loop_callables import CallableConditionalLooper
import typing


def double_the_list(some_list):
    if type(some_list) != list:
        raise TypeError("this function is for lists only")
    return some_list + some_list


def double_the_list_values(some_list):
    if type(some_list) != list:
        raise TypeError("this function is fod lists of numbers only")
    new_list = [i*2 for i in some_list]
    return new_list


def make_list_of_ones(value):
    return [1]*value


callable_1 = AtomicCallable(double_the_list)
callable_2 = AtomicCallable(double_the_list_values)
callable_3 = AtomicCallable(sum)
callable_4 = AtomicCallable(make_list_of_ones)

container = DataContainer([1, 2, 3])
print(container.__dict__)

for callable in (callable_1, callable_2, callable_3):
    container = callable(container)
    # print(container.data)
    print(container.__dict__)
print(container.data)

container_2 = DataContainer([1, 2, 3])
chain_of_callables = CallablesChain(
    callable_1, callable_2, callable_3)
container_2 = chain_of_callables(container_2)
print(container_2.data)

extended_chain_of_callables = CallablesChain(
    chain_of_callables, callable_4, chain_of_callables)

print("#"*20)

container = DataContainer([1, 2, 3])
container = extended_chain_of_callables(container)
print(container.__dict__)

print("#"*20)

inappropriate_container = DataContainer([{1: "first"}])
inappropriate_container = chain_of_callables(inappropriate_container)
print(inappropriate_container.__dict__)

# when there is an error

inappropriate_container = DataContainer([{1: "first"}], wayback_mode=True)

callable_4 = AtomicCallable(double_the_list)
callable_5 = AtomicCallable(double_the_list_values)
callable_6 = AtomicCallable(sum)

for callable in (callable_4, callable_5, callable_6):
    inappropriate_container = callable(inappropriate_container)

print(inappropriate_container.__dict__)
# simple dispatch

container_with_dispatch = DataContainer([2, 7, 9], dispatch_key="extended")

dispatch_dict = {"short": AtomicCallable(double_the_list),
                 "extended": extended_chain_of_callables}
dispatcher = CallableDispatcher(dispatch_dict)
container_with_dispatch = dispatcher(container_with_dispatch)
print(container_with_dispatch.__dict__)

# chains arithmetic

list_of_funcs = [lambda x:x*2, lambda x:x % 5, lambda x:x+3, lambda x:x *
                 28, lambda x:f"result is {x}", lambda x:x*3, lambda x: x+"grrr"]

chain = CallablesChain.from_funcs_list(list_of_funcs)

value = DataContainer(666)

result = chain(value)

print(result.data)

# Semiramis and Collatz dispatcher style
print("dispatcher style")
dict_of_callables = {
    "3k+1": AtomicCallable(lambda k: 3*k+1), "/2": AtomicCallable(lambda k: k//2)}
callable_dispatcher = CallableDispatcher(dict_of_callables)
dispatch_setter = DispatchSetter(
    dispatch_key_func=lambda container: "/2" if container.data % 2 == 0 else "3k+1")
console_printer = SideEffectCallable(lambda container: print(container.data))
chain = CallablesChain(dispatch_setter, callable_dispatcher, console_printer)


starting_container = DataContainer(69)
loop_until_eq_1 = CallableConditionalLooper(
    chain, break_func=lambda container: container.data == 1)
container_after = loop_until_eq_1(starting_container)
print(container_after.__dict__)


# Semiramis and Collatz handler style
print("handler style")
starting_container = DataContainer(69)

div_2 = AtomicHandler(lambda k: k//2, check_if_appliable=lambda container: container.data % 2 == 0, metadata_func=lambda container: {
                      "last_operation": "success"}, metadata_func_if_nonappliable=lambda container: {"last_operation": "pass"})

mul_3_add_1 = AtomicHandler(lambda k: k*3 + 1, check_if_appliable=lambda container: container.data % 2 == 1, metadata_func=lambda container: {
                            "last_operation": "success"}, metadata_func_if_nonappliable=lambda container: {"last_operation": "pass"})

printer = SideEffectHandler(lambda x: print(x.data),
                            check_if_appliable=lambda container: container.metadata[
                                "last_operation"] == "success"
                            )  # TODO:fix it

chain = CallablesChain(mul_3_add_1, printer, div_2, printer,)


loop_until_eq_1 = CallableConditionalLooper(
    chain, break_func=lambda container: container.data == 1)
container_after = loop_until_eq_1(starting_container)
print(container_after.__dict__)
