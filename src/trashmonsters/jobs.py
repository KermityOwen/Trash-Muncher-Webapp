from .models import TrashMonsters
from .serializer import TMSerializer


from schedule import Scheduler
import time, threading, schedule
import json, os

from .viewset import cached_leader



def decrTeamLeaders():
    TMs = TrashMonsters.objects.all()
    for TM in TMs:
        # HOLY FUCK THIS IS HORRIBLE. can be optimized with pointers but python is fucked
        if TM.Team1_Score > TM.Team2_Score:
            if TM.Team1_Score > TM.Team3_Score:
                autoRemoveScore(tm_id=TM.TM_ID, rem_team=1)
            elif TM.Team1_Score == TM.Team3_Score:
                autoRemoveScore(tm_id=TM.TM_ID, rem_team=cached_leader.get(TM.TM_ID))

        elif TM.Team1_Score == TM.Team2_Score:
            if TM.Team1_Score > TM.Team3_Score:
                autoRemoveScore(tm_id=TM.TM_ID, rem_team=1)
            else:
                autoRemoveScore(tm_id=TM.TM_ID, rem_team=cached_leader.get(TM.TM_ID))

        elif TM.Team2_Score > TM.Team3_Score:
            autoRemoveScore(tm_id=TM.TM_ID, rem_team=2)
            # print("TM: %d, Winning Team: %d"%(TM.TM_ID, 2))


def autoRemoveScore(tm_id, rem_team):
    try:
        TM = TrashMonsters.objects.get(TM_ID=tm_id)
        # so ugly but only way without refactoring the whole db for trashmonsters
        if rem_team == 1:
            TM.Team1_Score -= 1
        elif rem_team == 2:
            TM.Team2_Score -= 1
        elif rem_team == 3:
            TM.Team3_Score -= 1
        else:
            print("Error: Invalid team")
        TM.save()
        print("Scheduled trash eating!")
    except:
        print("Error: Something went wrong!")


def run_continuously(self, interval=21600):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                # self.run_pending()
                # autoRemoveScore(tm_id=1, team1=1)
                try:
                    decrTeamLeaders()
                except:
                    print("Bruh get this yeeyee ass code out of here")
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run


Scheduler.run_continuously = run_continuously


def start_scheduler():
    scheduler = Scheduler()
    scheduler.run_continuously()
    # scheduler.every().second.do(autoRemoveScore(tm_id=1, team1=1))
