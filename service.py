import time
import xbmc
import xbmcaddon
import xbmcgui
import os
import random

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
wavFile = os.path.join(addon.getAddonInfo('path'), 'sound.wav')
taskFile = os.path.join(addon.getAddonInfo('path'), 'tasks.txt')
playerFile = os.path.join(addon.getAddonInfo('path'), 'players.txt')

with open(taskFile, mode='r', encoding="utf-8") as f:
    weights, tasks = map(list, zip(* map(lambda x: (int(x[0]), x[1]), map(lambda x:  x.split("|") ,  f.read().splitlines()))))

with open(playerFile, mode='r', encoding="utf-8") as f:
    playerList = f.read().splitlines()

def showTask():
    player1, player2 = random.sample(playerList, 2)
    task = random.choices(population=tasks, weights=weights, k=1 )[0].replace('#PLAYER1', player1).replace('#PLAYER2', player2)
    return xbmcgui.Dialog().yesno(addonname, task, "Done", "New Task")


if __name__ == '__main__':
    monitor = xbmc.Monitor()

    while not monitor.abortRequested():

        # Sleep for 5 minutes + random delay
        if monitor.waitForAbort(300 + random.randint(0,200)):
            # Abort was requested while waiting. We should exit
            break
        xbmc.log("Trigger new Task! %s" % time.time(), level=xbmc.LOGINFO)

        # Pause player if playing
        wasPaused = False
        player = xbmc.Player()
        if player.isPlaying():
            player.pause()
            wasPaused = True

        xbmc.executebuiltin('InhibitScreenSaver(true)')
        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Input.ButtonEvent", "params": { "button": "leftshift", "keymap": "KB" }, "id": 1}')
        xbmc.playSFX(wavFile)

        # Loop until task is done or abort was requestet
        while not monitor.abortRequested():
            newTask = showTask()
            if not newTask:
                break

        # End pause if player was paused before
        if wasPaused:
            player.pause()
        xbmc.executebuiltin('InhibitScreenSaver(false)')
        xbmc.executebuiltin('ActivateScreensaver')
