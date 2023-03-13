"""Run this file as main to reset the highscores. If for whatever reason you
Ran this game with Python 3 and then decided to run it with Python 2 later,
it may be necessary to reset this, as pickle protocols are slightly different."""
import pickle

def reset_scores(afile):
    """Resets my highscores to factory presets."""
    blank = [("Mekire",16000,10)]+[("EMPTY",0,0) for i in range(4)]
    with open(afile,"wb") as myfile:
        pickle.dump(blank,myfile)
    return blank

##########################
if __name__ == "__main__":
    reset_scores("highs.dat")