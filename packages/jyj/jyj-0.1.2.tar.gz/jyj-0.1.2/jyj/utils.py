import os, time


def tail(log_file=f"{os.path.dirname(__file__)}/test.log"):
    def _tail(f):
        f.seek(0, 2)
        # inode = os.fstat(f.fileno()).st_ino
        fsize = os.fstat(f.fileno()).st_size

        while True:
            line = f.readline()
            if not line:
                print(f"未读取到新行，当前游标位置：{f.tell()}")
                time.sleep(0.5)
                # if os.stat(log_file).st_ino != inode:
                if os.stat(log_file).st_size < fsize:
                    print(f"监测到文件大小缩小：{fsize} -> {os.stat(log_file).st_size}")
                    print(f"将重新打开文件：{log_file}，目前游标位置：{f.tell()}")
                    f.close()
                    f = open(log_file, "r", encoding="utf-8")
                    f.seek(0, 2)
                    print(f"文件已重新打开，当前游标位置：{f.tell()}")
                    # inode = os.fstat(f.fileno()).st_ino
                    fsize = os.fstat(f.fileno()).st_size
                    print(f"当前文件大小：{fsize}")
                continue
            elif line:
                yield line, f.tell()

    for line, pos in _tail(open(log_file, "r", encoding="utf-8")):
        print(pos, line, end="")
