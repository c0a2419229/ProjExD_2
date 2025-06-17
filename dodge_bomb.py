import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {  #移動量辞書
    pg.K_UP: (0, -5), 
    pg.K_DOWN: (0, +5), 
    pg.K_LEFT: (-5, 0), 
    pg.K_RIGHT: (+5, 0),
}

HOUKOU = {
    (+5, 0): pg.transform.flip(pg.image.load("ex2/fig/3.png"), True, False),
    (+5, +5): pg.transform.flip(pg.image.load("ex2/fig/3.png"), True, False), 
    (+5, -5): pg.transform.flip(pg.image.load("ex2/fig/3.png"), True, False), 
    (0, +5): pg.transform.rotozoom(pg.image.load("ex2/fig/3.png"), 90, 0.9), 
    (0, -5): pg.transform.rotozoom(pg.image.load("ex2/fig/3.png"), 270, 0.9), 
    (-5, 0): pg.transform.rotozoom(pg.image.load("ex2/fig/3.png"), 0, 0.9), 
    (-5, +5): pg.transform.rotozoom(pg.image.load("ex2/fig/3.png"), 45, 0.9), 
    (-5, -5): pg.transform.rotozoom(pg.image.load("ex2/fig/3.png"), 315, 0.9), 
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")  
    # こうかとん表示 
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    # 時間
    clock = pg.time.Clock()
    tmr = 0
    # 爆弾表示
    bb_img = pg.Surface((20, 20))  #空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  #赤い円
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect() 
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  
    vx, vy = +5, +5
    
    
    #爆弾の巨大化
    def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
        bb_accs = [a for a in range(1, 11)]
        bb_imgs = []
        for r in range(1, 11):
            bb_img = pg.Surface((20*r, 20*r))
            pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
            bb_img.set_colorkey((0, 0, 0))
            bb_imgs.append(bb_img)
        return bb_imgs, bb_accs
    
    
    #ブラックアウト画面
    def gameover(screen:pg.Surface) -> None:
        #ブラックアウト
        ba_img = pg.Surface((1100, 650))
        pg.draw.rect(ba_img, (0, 0, 0), (0, 0, 1100, 650))
        ba_img.set_alpha(200)
        screen.blit(ba_img, [0, 0])
        #泣きこうかとん
        nk_img = pg.image.load(("fig/8.png"))
        nk_img2 = pg.image.load(("fig/8.png"))
        screen.blit(nk_img, [330, 280])
        screen.blit(nk_img2, [710, 280])
        #gameover表示
        fonto = pg.font.Font(None, 80)
        txt = fonto.render("Game Over", True, (255, 255, 255))
        screen.blit(txt, [390, 290])
        pg.display.update()
        time.sleep(5)  

    # こうかとん方向転換   
    def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
        if sum_mv == (0, 0):
            img = kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
            return img
        else:
            img = HOUKOU[sum_mv]
            if sum_mv == ((0, +5) or (0, -5)):
                img = pg.transform.flip(img, True, False)
            elif sum_mv == ((+5, 0), (+5, +5)):
                img = pg.transform.flip(img, False, True)
                img = pg.transform.flip(img, False, True)
            return img
        
                    

    

    #画面外判定関数
    def check_bound(rct:pg.Rect) -> tuple[bool, bool]:
        """
        引数：こうかとんRect or 爆弾Rect
        戻り値：横方向・縦方向の真理値タプル（True：画面内 / False：画面外）
        Rectオブジェクトのleft, right, top, bottomの値から画面内・外を判断する
        """
        x, y = True, True
        if rct.left < 0 or WIDTH < rct.right:
            x = False
        if rct.top < 0 or HEIGHT < rct.bottom:
            y = False
        return x, y
            

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        # こうかとん移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_now = kk_rct.center
        kk_rct.move_ip(sum_mv)
        kk_img = get_kk_img((0, 0))
        kk_img = get_kk_img(tuple(sum_mv))
        if check_bound(kk_rct) != (True, True) :  #こうかとん画面外判定
            kk_rct.center = kk_now
        screen.blit(kk_img, kk_rct)

        # 爆弾移動
        bb_imgs, bb_accs = init_bb_imgs()
        avx = bb_accs[min(tmr//500, 9)]
        avy = bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        yoko, tate = check_bound(bb_rct)  #爆弾画面外判定
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        bb_rct.move_ip(vx*avx, vy*avy)
        screen.blit(bb_img, bb_rct)

        # ディスプレイ更新
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        pg.display.update()
        
        tmr += 1
        clock.tick(50)
        



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
