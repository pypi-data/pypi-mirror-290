import os,socket
import time,subprocess
import click
import struct

@click.command()
@click.option('--disk','-d',default='sda,sdb')
@click.option('--time_l','-t',default=10,help="停止活动指定时长后进入休眠 默认10分钟")
@click.option('--sleep_cmd','-p',default='sudo hdparm')
def main(disk,time_l,sleep_cmd):
    oldstate = 'none'
    nt = 0
    disk = [i.strip() for i in disk.split(',')]
    st = time.time()
    i = 0
    while True:
        i += 1
        for di in disk:
            newstate = subprocess.getoutput(f'grep {di} /proc/diskstats')
            print(newstate)
            if oldstate == newstate:
                nt += 1
                if nt == time_l:
                    ott = subprocess.getoutput(f'{sleep_cmd} -C /dev/{di}')
                    if ott.find('standby') == -1:
                        os.system(f'{sleep_cmd} -y /dev/{di}')
                        print(f'standby disk: {di}')
            else:
                nt = 0
                oldstate = newstate 
            time.sleep(0.1)
        tt = st+i*60 - time.time()
        if tt < 0:
            tt = 60
        if tt>70:
            tt = 60
        print('sleep ',tt)
        time.sleep(tt)

if __name__=='__main__':
    main()