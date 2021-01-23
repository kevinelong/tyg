from blit import *
source = [
[1,0,0,1],
[0,1,1,0],
[0,1,1,0],
[1,0,0,1]
]
target = [
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0]
]
blit_wrap(source,target,5,5)
for row in target:
  for value in row:
    print(value,end="")
  print("")

