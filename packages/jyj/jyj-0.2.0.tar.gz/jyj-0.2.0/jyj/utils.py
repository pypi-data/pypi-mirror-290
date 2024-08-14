import os, time, logging

logging.basicConfig(
    level=logging.WARN, format="%(asctime)s - %(levelname)s - %(message)s"
)
info = logging.info


def tail(file):
    interval = 0.1

    def file_info(print_=False):
        file_info = os.stat(file)
        if print_:
            info(f"文件信息：{file_info}")
        return file_info

    f = open(file, "r", encoding="utf-8")
    f.seek(0, 2)
    finfo = file_info(print_=True)
    mtime = finfo.st_mtime
    fsize = finfo.st_size

    while True:
        try:
            if os.stat(file).st_mtime == mtime:
                info(f"文件未更新，当前游标位置：{f.tell()}")
                time.sleep(interval)
                continue

            else:
                info(f"文件已更新，当前游标位置：{f.tell()}")

                if os.stat(file).st_size < fsize:
                    info(f"监测到文件大小缩小：{fsize} -> {os.stat(file).st_size}")
                    info(f"将重新打开文件：{file}，目前游标位置：{f.tell()}")
                    f.close()
                    f = open(file, "r", encoding="utf-8")
                    f.seek(0, 2)
                    fsize = os.stat(file).st_size
                    mtime = os.stat(file).st_mtime
                    info(f"文件已重新打开，当前游标位置：{f.tell()}")
                    continue

                elif os.stat(file).st_mtime >= mtime:
                    # 若不含回车，则 continue
                    pos = f.tell()
                    lines = "".join(f.readlines())
                    if "\n" not in lines:
                        f.seek(pos)
                        info(f"新字符串中不包含回车，恢复游标位置：{pos}")
                        time.sleep(interval)
                        continue
                    else:
                        yield lines.removesuffix("\n")
                        mtime = os.stat(file).st_mtime
                        fsize = os.stat(file).st_size
                        continue

        except Exception as e:
            logging.warn(e)
            time.sleep(interval)


if __name__ == "__main__":
    for line in tail("/root/proj/jyj/tests/test.log"):
        print(line)
