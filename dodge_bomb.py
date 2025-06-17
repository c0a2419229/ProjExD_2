import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1100, 650
DELTA = {  #移動量辞書
    pg.K_UP: (0, -5), 
    pg.K_DOWN: (0, +5), 
    pg.K_LEFT: (-5, 0), 
    pg.K_RIGHT: (+5, 0),
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
        if rct.top < 0 or HEIGHT < rct. bottom:
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
        if check_bound(kk_rct) != (True, True) :  #こうかとん画面外判定
            kk_rct.center = kk_now
        screen.blit(kk_img, kk_rct)

        # 爆弾移動
        bb_rct.move_ip(vx, vy)
        if check_bound(bb_rct) != (True, True):  #爆弾画面外判定
            if bb_rct.left < 0 or bb_rct.right > WIDTH:
                vx *= -1
            if bb_rct.top < 0 or bb_rct.bottom > HEIGHT:
                vy *= -1
        screen.blit(bb_img, bb_rct)

        # ディスプレイ更新
        pg.display.update()
        if kk_rct.colliderect(bb_rct):
            return
        tmr += 1
        clock.tick(100)
        



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
