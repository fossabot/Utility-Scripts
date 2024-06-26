# Python 3
import os, re, glob, json, hashlib, time
start = time.time()

with open("deletefiles.txt", 'r') as f:
    for line in f.readlines():
        try:
            os.remove(line.strip())
        except Exception as e:
            print(f"Error: {e}")
print("Delete done! ({:.2f}s)\n".format(time.time() - start))
os.remove("deletefiles.txt")

hd = []
with open("hdifffiles.txt", 'r') as f:
    for line in f.readlines():
        hd.append(re.findall(r'"(.*?)"', line)[1])
for i in hd:
    os.system("hpatchz.exe -f " + i + " " + i + ".hdiff " + i)
    os.remove(i + ".hdiff")
print("\nPatch done! ({:.2f}s)\nWaiting for MD5 calculation...".format(time.time() - start))
os.remove("hdifffiles.txt")

hdpath = os.path.dirname(hd[0])
md5txt = glob.glob(os.path.join(hdpath, 'AudioV_*'))
with open(md5txt[0], 'r') as f:
    for line in f.readlines():
        path = os.path.join(hdpath, json.loads(line)['Path'])
        with open(path, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        if md5 != json.loads(line)['Md5']:
            print("有文件校验失败：" + path + "\n\n程序退出...")
            exit(1)
print("MD5 verification completed, all files are correct.\nUpdate done! ({:.2f}s)\n".format(time.time() - start))
print("Press any key to exit...")
import msvcrt
msvcrt.getch()
