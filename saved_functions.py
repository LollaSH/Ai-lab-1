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