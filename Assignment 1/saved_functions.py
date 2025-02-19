def allowed_moves(board, player):
    d = np.ones((8,8), dtype=int)
    
    for i in range(8):
        for j in range(8):
            if board[i, j] == player:
                flips = 0
                for hp in range(i+1, 8):
                    b = board[hp, j]
                    if b == -player:
                        flips+=1
                    elif b == 0 and flips != 0:
                        d[hp, j] = 0
                        flips = 0
                        break
                    elif b == player:
                        flips = 0
                        break
                    elif b == 0 and flips == 0:
                        break
                flips = 0
                for hn in reversed(range(0, i)):
                    b = board[hn, j]
                    if b == -player:
                        flips+=1
                    elif b == 0 and flips != 0:
                        d[hn, j] = 0
                        flips = 0
                        break
                    elif b == player:
                        flips = 0
                        break
                    elif b == 0 and flips == 0:
                        break
                flips = 0
                for vp in range(j + 1, 8):
                    b = board[i, vp]
                    if b == -player:
                        flips+=1
                    elif b == 0 and flips != 0:
                        d[i, vp] = 0
                        flips = 0
                        break
                    elif b == player:
                        flips = 0
                        break
                    elif b == 0 and flips == 0:
                        break
                flips = 0
                for vn in reversed(range(0, j)):
                    b = board[i, vn]
                    if b == -player:
                        flips+=1
                    elif b == 0 and flips != 0:
                        d[i, vn] = 0
                        flips = 0
                        break
                    elif b == player:
                        flips = 0
                        break
                    elif b == 0 and flips == 0:
                        break
                
    
    
    empty = list(zip(*np.where(d == 0)))

    return empty




# def possible_moves(board, player):
#     d = np.ones((8,8), dtype=int)
    
#     md = dict()
    
    
#     for i in range(8):
#         for j in range(8):
#             if board[i, j] == player:
#                 flips = 0
#                 flipped = set()
#                 for hp in range(i+1, 8):
#                     b = board[hp, j]
#                     if b == -player:
#                         flipped.add((hp, j))
#                         flips+=1
#                     elif b == 0 and flips != 0:
#                         pos = (hp, j)
#                         if pos in md:
#                             md[pos] = md[pos].union(flipped)
#                         else:
#                             md[pos] = flipped.copy()
#                         flips = 0
#                         break
#                     elif b == player:
#                         flips = 0
#                         break
#                     elif b == 0 and flips == 0:
#                         break
#                 flips = 0
#                 flipped = set()
#                 for hn in reversed(range(0, i)):
#                     b = board[hn, j]
#                     if b == -player:
#                         flipped.add((hn, j))
#                         flips+=1
#                     elif b == 0 and flips != 0:
#                         pos = (hn, j)
#                         if pos in md:
#                             md[pos] = md[pos].union(flipped)
#                         else:
#                             md[pos] = flipped.copy()
#                         flips = 0
#                         break
#                     elif b == player:
#                         flips = 0
#                         break
#                     elif b == 0 and flips == 0:
#                         break
#                 flips = 0
#                 flipped = set()
#                 for vp in range(j + 1, 8):
#                     b = board[i, vp]
#                     if b == -player:
#                         flipped.add((i, vp))
#                         flips+=1
#                     elif b == 0 and flips != 0:
#                         pos = (i, vp)
#                         if pos in md:
#                             md[pos] = md[pos].union(flipped)
#                         else:
#                             md[pos] = flipped.copy()
#                         flips = 0
#                         break
#                     elif b == player:
#                         flips = 0
#                         break
#                     elif b == 0 and flips == 0:
#                         break
#                 flips = 0
#                 flipped = set()
#                 for vn in reversed(range(0, j)):
#                     b = board[i, vn]
#                     if b == -player:
#                         flipped.add((i, vn))
#                         flips+=1
#                     elif b == 0 and flips != 0:
#                         pos = (i, vn)
#                         if pos in md:
#                             md[pos] = md[pos].union(flipped)
#                         else:
#                             md[pos] = flipped.copy()
#                         flips = 0
#                         break
#                     elif b == player:
#                         flips = 0
#                         break
#                     elif b == 0 and flips == 0:
#                         break
                

#     moves = [
#         { 'player': player, 'put': slot, 'flipped': flipped }
#         for slot, flipped in md.items()
#     ]

#     return moves

# def allowed_moves(board, player):
#     d = np.ones((8,8), dtype=int)
    
#     md = dict()
    
    
#     for i in range(8):
#         for j in range(8):
#             if board[i, j] == player:
#                 flips = 0
#                 flipped = set()
#                 for hp in range(i+1, 8):
#                     b = board[hp, j]
#                     if b == -player:
#                         flipped.add((hp, j))
#                         flips+=1
#                     elif b == 0 and flips != 0:
#                         pos = (hp, j)
#                         if pos in md:
#                             md[pos] = md[pos].union(flipped)
#                         else:
#                             md[pos] = flipped.copy()
#                         flips = 0
#                         break
#                     elif b == player:
#                         flips = 0
#                         break
#                     elif b == 0 and flips == 0:
#                         break
#                 flips = 0
#                 flipped = set()
#                 for hn in reversed(range(0, i)):
#                     b = board[hn, j]
#                     if b == -player:
#                         flipped.add((hn, j))
#                         flips+=1
#                     elif b == 0 and flips != 0:
#                         pos = (hn, j)
#                         if pos in md:
#                             md[pos] = md[pos].union(flipped)
#                         else:
#                             md[pos] = flipped.copy()
#                         flips = 0
#                         break
#                     elif b == player:
#                         flips = 0
#                         break
#                     elif b == 0 and flips == 0:
#                         break
#                 flips = 0
#                 flipped = set()
#                 for vp in range(j + 1, 8):
#                     b = board[i, vp]
#                     if b == -player:
#                         flipped.add((i, vp))
#                         flips+=1
#                     elif b == 0 and flips != 0:
#                         pos = (i, vp)
#                         if pos in md:
#                             md[pos] = md[pos].union(flipped)
#                         else:
#                             md[pos] = flipped.copy()
#                         flips = 0
#                         break
#                     elif b == player:
#                         flips = 0
#                         break
#                     elif b == 0 and flips == 0:
#                         break
#                 flips = 0
#                 flipped = set()
#                 for vn in reversed(range(0, j)):
#                     b = board[i, vn]
#                     if b == -player:
#                         flipped.add((i, vn))
#                         flips+=1
#                     elif b == 0 and flips != 0:
#                         pos = (i, vn)
#                         if pos in md:
#                             md[pos] = md[pos].union(flipped)
#                         else:
#                             md[pos] = flipped.copy()
#                         flips = 0
#                         break
#                     elif b == player:
#                         flips = 0
#                         break
#                     elif b == 0 and flips == 0:
#                         break
    
#     return md
