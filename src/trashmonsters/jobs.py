from .models import TrashMonsters
from .serializer import TMSerializer


from schedule import Scheduler
import time, threading, schedule

def autoRemoveScore(tm_id, team1=0, team2=0, team3=0):
    try:
        TM = TrashMonsters.objects.get(TM_ID = tm_id)
        TM.Team1_Score += team1
        TM.Team2_Score += team2
        TM.Team3_Score += team3
        TM.save()

        print("Debug make sure this is working %d"%(tm_id))
    except:
        print("Error: TM_ID not found")




def run_continuously(self, interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                #self.run_pending()
                autoRemoveScore(tm_id=1, team1=1)
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously

def start_scheduler():
    scheduler = Scheduler()
    scheduler.run_continuously()
    #scheduler.every().second.do(autoRemoveScore(tm_id=1, team1=1))
    

