import sys
import json
from datetime import datetime, timedelta
import runpy
import os
import argparse
from typing import Optional
import socket
import pytz


def write_stdout(s: str, flush: bool = True):
    '''写入stdout并刷新, 只能向 stdout 发送事件列表生成器协议信息'''
    sys.stdout.write(s)
    if flush:
        sys.stdout.flush()


def print(*values, sep=' ', end='\n', file=None, flush=True):
    '''重写print函数, 默认输出到stderr并刷新'''
    if file is None:
        file = sys.stderr
    file.write(sep.join(map(str, values)) + end)
    if flush:
        file.flush()


class SendEventlistenerMsg:
    '''发送事件侦听器消息
    参考： http://supervisord.org/events.html#event-listener-notification-protocol
    '''
    
    @staticmethod
    def ready():
        '''通知处于事件状态的事件侦听器，它已准备好接收事件'''
        write_stdout('READY\n')
    
    @staticmethod
    def ok():
        '''通知事件侦听器已成功处理事件'''
        write_stdout('RESULT 2\nOK')
    
    @staticmethod
    def fail():
        '''将假定侦听器未能处理该事件，并且该事件将在稍后重新缓冲并再次发送'''
        write_stdout('RESULT 4\nFAIL')


def parse_notif(line: str) -> Optional[dict]:
    '''解析事件通知'''  
    if not line or ':' not in line:
        return None
    notif = dict([ x.split(':') for x in line.split() ])
    for k, v in notif.items():
        try:
            notif[k] = int(v)
        except ValueError:
            try:
                notif[k] = float(v)
            except ValueError:
                pass
    return notif


def get_msg(tzinfo: pytz.BaseTzInfo) -> dict:
    '''获取事件通知'''
    line = sys.stdin.readline()
    headers = parse_notif(line)
    data = payload = None
    if headers['len']:
        line = sys.stdin.read(headers['len'])
        if '\n' in line:
            line, data = line.split('\n', 1)
        payload = parse_notif(line)
    msg = {
        'hostname': socket.gethostname(),
        'time': datetime.now(tz=tzinfo).isoformat(),
        'time_zone': tzinfo.zone,
        'headers': headers,
        'payload': payload,
        'data': data,
    }
    return msg


def handle_msg(msg: dict, run_path: str = None, context: dict = None) -> bool:
    '''处理事件通知
    eventname: http://supervisord.org/events.html#event-types'''
    print(json.dumps(msg))
    if run_path and os.path.exists(run_path):
        try:
            runpy.run_path(run_path, init_globals={
                'MSG': msg,
                'print': print,
                'CONTEXT': context,
            }, run_name=None)
        except BaseException as e:
            print(str(e))
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Supervisor 事件侦听器",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-p", "--handle_msg_py", default=None, help='处理消息的python文件，会传入全局变量MSG/CONTEXT，留空不执行')
    parser.add_argument("-t", "--time_zone", default='Asia/Shanghai', help='时区')
    parser.add_argument("-i", "--minimum_interval", type=int, default=7200, help='一个事件再次通知的最小间隔时间, 单位秒。修复其他进程后建议重启这个监听器保证相同事件可以再次通知')
    args = parser.parse_args()
    
    tzinfo = pytz.timezone(args.time_zone)
    context = {}  # handle_msg_py 可用的全局变量
    events_final_notif_date: dict[tuple, datetime] = {}  # 事件最后通知时间
    minimum_interval = timedelta(seconds=args.minimum_interval)
    while 1:
        SendEventlistenerMsg.ready()
        msg = get_msg(tzinfo)
        event = (
            msg.get('hostname'),
            (msg.get('headers') or {}).get('eventname'),
            (msg.get('payload') or {}).get('processname'),
            (msg.get('payload') or {}).get('groupname'),
            (msg.get('payload') or {}).get('from_state'),
        )
        if event in events_final_notif_date and datetime.now() - events_final_notif_date[event] < minimum_interval:
            print(f'{event} 事件通知间隔时间短于 {args.minimum_interval} 秒，忽略')
            SendEventlistenerMsg.ok()
        elif handle_msg(msg, args.handle_msg_py, context):
            events_final_notif_date[event] = datetime.now()
            SendEventlistenerMsg.ok()
        else:
            SendEventlistenerMsg.fail()


if __name__ == '__main__':
    main()
