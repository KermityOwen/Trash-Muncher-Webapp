from .models import TrashMonsters
from .serializer import TMSerializer


from schedule import Scheduler
import time, threading, schedule
import json, os

from .viewset import cached_leader


def decrTeamLeaders():
    """
    Determines which team's score should be decremented
    based on if they are the leader for the TrashMonster.
    Used to incentivise players to keep revisiting that TrashMonster to
    keep the lead
    """
    TMs = TrashMonsters.objects.all()
    for TM in TMs:
        """
        Game functionality to reduce the each TrashMonsters leading
        team's current score by one
        """
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
    """
    Decrements a team's score by one

    Parameters:
    tm_id (int) - ID of the TrashMonster
    rem_team (int) - ID of the leading team
    """
    try:
        TM = TrashMonsters.objects.get(TM_ID=tm_id)
        # so ugly but only way without refactoring the whole db for trashmonsters
        if rem_team == 1 and TM.Team1_Score >= 1:
            TM.Team1_Score -= 1
        elif rem_team == 2 and TM.Team2_Score >= 1:
            TM.Team2_Score -= 1
        elif rem_team == 3 and TM.Team3_Score >= 1:
            TM.Team3_Score -= 1
        else:
            print("Error: Invalid team or Team already has 0 Score")
        TM.save()
        print("Scheduled trash eating!")
    except:
        print("Error: Something went wrong!")


def run_continuously(self, interval=21600):
    """
    Schedules the thread running to decrease a team's score

    Parameters:
    interval (int) - Time that the thread will sleep for before continuing
    """
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
    """
    Initialises the scheduler and begins threading
    """
    scheduler = Scheduler()
    scheduler.run_continuously()
    # scheduler.every().second.do(autoRemoveScore(tm_id=1, team1=1))
