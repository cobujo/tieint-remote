

def batcher(test_list: list, batch_size=10):
    if len(test_list) <= batch_size:
        return func_on_batch(test_list)




def func_on_batch(sublist):
    try:
