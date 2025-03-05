17/9/34
started this project

18/9
started changelog, did much. fill both these entries out better when awake

19/9
added more structure and cards

20/9
more progress, but always late/bz so forget to say everything
changed action tuples to reference rather than index
decided that summon takes card template to clone and not lambda card factory.
this will use more memory and processing, but likely not enough to be bad, and it makes complex/nested summons much easier

21/9
speperated Card into Summon and Spell
finally converted insta nested stack code into delay queue event handler

22/9
improved event handler
added more triggers such as start/end turn
made more triggers into actions such as card draw
added clusterbomb and ultraslime

26/9
GUI exists. Had some issues with deepcopy but got there. need to make cleaner and improve GUI. is absolute bare bones rn. but it works

9/2
it has been too long, getting back into this is tough. increased window size and removed autoplay

5/3
added bezier curve cursor targeting. yet to tie into actual card targeting.

# TODO
consider queue system becoming priority queue so some things like death and tap can have extra sorting to order. only implement if needed. current queue system may be adequate
enhance cards visually and make draggable