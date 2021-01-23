def blit(source,target,ox,oy):
  for sy in range(len(source)):
    for sx in range(len(source[0])):
      target[sy+oy][sx+ox] = source[sy][sx]

def blit_wrap(source,target,ox,oy):
  for sy in range(len(source)):
    for sx in range(len(source[0])):
      target[(sy+oy) % len(target)][(sx+ox) % len(target[0])] = source[sy][sx]

