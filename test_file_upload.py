from config import GATE_ID,DEVICE_ID,FTP_HOST, USER_NAME, USER_PASSWD, TIMEID_FORMAT
import os
from io import BytesIO
import ftplib
import cv2
import pytz
from datetime import datetime

ist = pytz.timezone('Asia/Jakarta')

def datetime_format():
    '''
    Extract daterime now to get year month day hour minute second and microsecond now
    '''
    datetime_now    = datetime.now(ist)
    year            = str(datetime_now.year)
    month           = '0'+str(datetime_now.month) if len(str(datetime_now.month)) == 1 else str(datetime_now.month)
    day             = '0'+str(datetime_now.day) if len(str(datetime_now.day)) == 1 else str(datetime_now.day)
    hour            = '0'+str(datetime_now.hour) if len(str(datetime_now.hour)) == 1 else str(datetime_now.hour)
    minute          = '0'+str(datetime_now.minute) if len(str(datetime_now.minute)) == 1 else str(datetime_now.minute)
    second          = '0'+str(datetime_now.second) if len(str(datetime_now.second)) == 1 else str(datetime_now.second)
    microsecond     = '0'+str(datetime_now.microsecond) if len(str(datetime_now.microsecond)) == 1 else str(datetime_now.microsecond)
    return year, month, day, hour, minute, second, microsecond

def chdir(ftp_path, ftp_conn):
    dirs = [d for d in ftp_path.split('/') if d != '']
    for p in dirs:
        print(p)
        check_dir(p, ftp_conn)


def check_dir(dir, ftp_conn):
    filelist = []
    ftp_conn.retrlines('LIST', filelist.append)
    found = False

    for f in filelist:
        if f.split()[-1] == dir and f.lower().startswith('d'):
            found = True

    if not found:
        ftp_conn.mkd(dir)
    ftp_conn.cwd(dir)

def img_upload(img,time_id):
    try:
        year, month, day, hour, _, _,_ = datetime_format()
        dest_path = f'{GATE_ID}/{year}/{month}/{day}'
        """Transfer file to FTP."""
        # Connect
        print("Connecting to FTP...")
        session = ftplib.FTP(FTP_HOST, USER_NAME, USER_PASSWD)
        session.set_pasv(False)
        # Change to target dir
        chdir(dest_path,session)

        # Transfer file
        name = time_id.strftime(TIMEID_FORMAT)[:-4]
        file_name  = f'{DEVICE_ID}{name}.jpg'
        print("Transferring %s to %s..." % (file_name,dest_path))
        retval, buffer = cv2.imencode('.jpg', img)
        flo = BytesIO(buffer)
        session.storbinary('STOR %s' % os.path.basename(dest_path+file_name), flo)
        print("Closing session.")
        # Close session
        session.quit()
    except:
        return 'upload file error'
def video_upload(name):
    try:
        #name = time_id.strftime(TIMEID_FORMAT)[:-4]
        year, month, day, hour, _, _,_ = datetime_format()
        dest_path = f'/{GATE_ID}/{year}/{month}/{day}/'
        """Transfer file to FTP."""
        # Connect
        print("Connecting to %s..." % (FTP_HOST))
        session = ftplib.FTP(FTP_HOST, USER_NAME, USER_PASSWD)

        # Change to target dir
        chdir(dest_path,session)

        # Transfer file
        file_name = name+'.avi'
        print("Transferring %s to %s..." % (file_name,dest_path))
        with open('results/'+file_name, "rb") as file:
            session.storbinary('STOR %s' % os.path.basename(dest_path+file_name), file)
        
        # Close session
        session.quit()
        return dest_path+file_name
    except:
        print('error: upload file error')
        return 'error: upload file error'


""" img = cv2.imread(os.path.join(os.getcwd(), '1647774265.jpg'))
if img is None:
    print('image empty')
else:
    img_upload(img,datetime.now(),'GATE09','container1') """
print(video_upload('test'))