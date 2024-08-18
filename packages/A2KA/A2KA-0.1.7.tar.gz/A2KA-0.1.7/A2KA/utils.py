def loop_find(target, str, start=0):
    li = []
    while True:
        beg = target.find(str, start)
        if beg == -1:
            break
        li.append(beg)
        start = beg + 1
    return li



def save_mydict(dict, name):
    # 字典保存
    import pickle
    f_save = open(name + '.pkl', 'wb')
    pickle.dump(dict, f_save)
    f_save.close()


def load_mydict(name):
    import pickle
    # # 读取
    f_read = open(name + '.pkl', 'rb')
    dict2 = pickle.load(f_read)
    f_read.close()
    return dict2

