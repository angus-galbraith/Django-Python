
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
import time
 
import pygame
from PIL import Image
import random, math
from itertools import product
import sys, os
 
# hides errors in console
sys.stdout = os.devnull
sys.stderr = os.devnull
 
pygame.init()
clock = pygame.time.Clock()
fps = 60
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")
 
# define fonts
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)
 
alien_cooldown = 1000  # bullet cooldown in milliseconds
last_count = pygame.time.get_ticks()
last_alien_shot = pygame.time.get_ticks()
 
# define colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
 
# load image
bg = pygame.image.load("bg.png")
screen_rect = bg.get_rect()
 
 
def draw_bg():
    screen.blit(bg, (0, 0))
 
 
# define function for creating text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
 
 
################ space invaders things ###############################################################################
# create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.health_start = health
        self.health_remaining = health
        self.image = pygame.image.load("ship.png")
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.xmin = self.rect.width // 2  # Compute Spaceship x range.
        self.xmax = screen_width - self.xmin
        self.last_shot = pygame.time.get_ticks()
 
    def move(self, xpos):
        self.xpos = xpos
        self.rect.centerx = max(self.xmin, min(self.xmax, xpos))
 
    def update(self):
        # set a cooldown variable
        cooldown = 500  # milliseconds
        game_over = 0
        # record current time
        time_now = pygame.time.get_ticks()
        # shoot, get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            weapon_list = ["bullet.png", "flash.png", "rocket.png"]
            chosen = random.choice(weapon_list)
            if level == 1:
                # single bullet
                bullet = Bullets(self.rect.centerx, self.rect.top, chosen)
                bullet_group.add(bullet)
                self.last_shot = time_now
            else:
                # double bullets
                bullet_1 = Bullets(self.rect.centerx - 43, self.rect.top, chosen)
                bullet_2 = Bullets(self.rect.centerx + 43, self.rect.top, chosen)
                bullet_group.add(bullet_1, bullet_2)
                self.last_shot = time_now
 
        # update mask
        self.mask = pygame.mask.from_surface(self.image)
 
        # draw health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (
                self.rect.x, (self.rect.bottom + 10),
                int(self.rect.width * (self.health_remaining / self.health_start)),
                15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3, "yellow")
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over
 
 
# create player
spaceship = Spaceship(screen_width / 2, screen_height - 100, 3)
paddle_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
 
 
# create Bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, chosen):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.chosen = chosen
        self.image = pygame.image.load(chosen)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
 
    def hit_endboss(self):
        x = self.rect.centerx
        y = self.rect.centery
        return x, y
 
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        hits = pygame.sprite.spritecollide(self, alien_group, True, pygame.sprite.collide_mask)
        if hits:
            self.kill()
            for alien in hits:
                x, y = alien.hit()
                if self.chosen == "rocket.png":
                    explosion = Explosion(x, y, 4, "yellow")
                    explosion_group.add(explosion)
                    hits_rocket_expl_and_aliens = pygame.sprite.spritecollide(explosion, alien_group, True,
                                                                              pygame.sprite.collide_mask)
                    if hits_rocket_expl_and_aliens:
                        for alien in hits_rocket_expl_and_aliens:
                            x, y = alien.hit()
                            explosion_red = Explosion(x, y, 2, "red")
                            explosion_group.add(explosion_red)
                else:
                    explosion = Explosion(x, y, 2, "yellow")
                    explosion_group.add(explosion)
 
 
# create Aliens class
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y, move_direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("alien" + str(random.randint(1, 6)) + ".png")
        self.x = x
        self.y = y
        self.move_direction = move_direction
        self.rect = self.image.get_rect()
        self.rect.center = x, y
 
    def hit(self):
        x = self.rect.centerx
        y = self.rect.centery
        self.kill()
        return x, y
 
    def update(self, move_direction):
        self.rect.x += self.move_direction
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.move_direction = -self.move_direction
            self.rect.y += 20
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            spaceship.health_remaining = -5
        if pygame.sprite.spritecollide(self, paddle_group, False, pygame.sprite.collide_mask):
            draw_text('GAME OVER!', font40, white, int(screen_width / 2 - 100),
                      int(screen_height / 2 + 50))
 
 
# create Alien Bullets class
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = x, y
 
    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            # reduce spaceship health
            spaceship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1, "yellow")
            explosion_group.add(explosion)
 
 
# create Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        if color == "yellow":
            for num in range(1, 8):
                img = pygame.image.load(f"explosion{num}.png")
                # ship is hit
                if size == 1:
                    img = pygame.transform.scale(img, (20, 20))
                # alien is hit
                if size == 2:
                    img = pygame.transform.scale(img, (100, 100))
                # ship gameover
                if size == 3:
                    img = pygame.transform.scale(img, (160, 160))
                # rocket hits alien
                if size == 4:
                    img = pygame.transform.scale(img, (500, 500))
                # add the image to the list
                self.images.append(img)
                self.index = 0
                self.image = self.images[self.index]
                self.rect = self.image.get_rect()
                self.rect.center = x, y
                self.counter = 0
                # add the image to the list
        if color == "red":
            # rocketExplosion hits alien, it occurs a red explosion
            for num1 in range(1, 8):
                img = pygame.image.load(f"explosion2_{num1}.png")
                img = pygame.transform.scale(img, (100, 100))
                # add the image to the list
                self.images.append(img)
                self.index = 0
                self.image = self.images[self.index]
                self.rect = self.image.get_rect()
                self.rect.center = x, y
                self.counter = 0
 
    def update(self):
        explosion_speed = 3
        # update explosion animation
        self.counter += 1
 
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
 
        # if the animation is complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()
 
 
# create sprite groups
spaceship_group = pygame.sprite.Group()
spaceship_group.add(spaceship)
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
# a different red explosion
explosion_red_group = pygame.sprite.Group()
 
 
def create_aliens(rows, cols, move_direction):
    # generate aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 100, move_direction)
            alien_group.add(alien)
 
 
def play_space_invaders(level, move_direction):
    game_over = 0
    last_count = pygame.time.get_ticks()
    last_alien_shot = pygame.time.get_ticks()
    create_aliens(4, 10, move_direction)
    countdown = 3
    run = True
    while run:
        clock.tick(fps)
        # draw background
        draw_bg()
        # space invaders single bullets level
        if countdown == 0:
            # create random alien bullets
            # record current time
            time_now = pygame.time.get_ticks()
            # shoot
            if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(
                    alien_group) > 0:
                attacking_alien = random.choice(alien_group.sprites())
                alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
                alien_bullet_group.add(alien_bullet)
                last_alien_shot = time_now
 
            # check if all the aliens have been killed
            if len(alien_group) == 0:
                game_over = 1
                level += 1
            if len(spaceship_group) == 0:
                game_over = -1
            if game_over == 0:
                # update spaceship
                game_over = spaceship.update()
                # update sprite groups
                bullet_group.update()
                alien_group.update(move_direction)
                alien_bullet_group.update()
                explosion_group.update()
                explosion_red_group.update()
            else:
                if game_over == -1:
                    draw_text('GAME OVER!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
                if game_over == 1:
                    draw_text('YOU WIN!', font40, white, int(screen_width / 2 - 100),
                              int(screen_height / 2 + 50))
                    return level
 
        if countdown > 0:
            draw_text('GET READY!', font40, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
            draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
            count_timer = pygame.time.get_ticks()
            if count_timer - last_count > 1000:
                countdown -= 1
                last_count = count_timer
 
        # draw sprite groups
        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)
        alien_bullet_group.draw(screen)
        explosion_group.draw(screen)
        explosion_red_group.draw(screen)
        # event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEMOTION:
                # space invaders level
                spaceship.move(event.pos[0])
        pygame.display.flip()
    pygame.quit()
 
 
# breakout things #############################################################
TEXT_COLOR = (255, 255, 255)
FOREGROUND = (0, 0, 0)  # Recolor image pixels that are this color
TRANSPARENT = (255, 255, 255)  # Make image pixels this color transparent
BALL_COLOR = (255, 255, 255)
PADDLE_COLOR = (255, 255, 255)
BALL_IMAGE = "ball.png"
PADDLE_IMAGE = "paddle.png"
 
 
def create_image(file, color=None):
    """
    Create image from a file.  If color is specified, replace all FOREGROUND
    pixels with color pixels.  Modify image so TRANSPARENT colored pixels are
    transparent.
    """
    if color:
        # Recolor the image
        image = Image.open(file).convert("RGB")
        for xy in product(range(image.width), range(image.height)):
            if image.getpixel(xy) == FOREGROUND:
                image.putpixel(xy, color)
        image = pygame.image.fromstring(image.tobytes(), image.size, "RGB")
    else:
        image = pygame.image.load(file)
    image.set_colorkey(TRANSPARENT)
    return image.convert()
 
 
class EnhancedSprite(pygame.sprite.Sprite):
    def __init__(self, image, group=None, **kwargs):
        super().__init__(**kwargs)
        self.image = image
        self.rect = image.get_rect()
        if group is not None:
            group.add(self)
 
    def at(self, x, y):
        """Convenience method for setting my position"""
        self.x = x
        self.y = y
        return self
 
    # Properties below expose properties of my rectangle so you can use
    # self.x = 10 or self.centery = 30 instead of self.rect.x = 10
    @property
    def x(self):
        return self.rect.x
 
    @x.setter
    def x(self, value):
        self.rect.x = value
 
    @property
    def y(self):
        return self.rect.y
 
    @y.setter
    def y(self, value):
        self.rect.y = value
 
    @property
    def centerx(self):
        return self.rect.centerx
 
    @centerx.setter
    def centerx(self, value):
        self.rect.centerx = value
 
    @property
    def centery(self):
        return self.rect.centery
 
    @centery.setter
    def centery(self, value):
        self.rect.centery = value
 
    @property
    def right(self):
        return self.rect.right
 
    @right.setter
    def right(self, value):
        self.rect.right = value
 
    @property
    def bottom(self):
        return self.rect.bottom
 
    @bottom.setter
    def bottom(self, value):
        self.rect.bottom = value
 
    @property
    def width(self):
        return self.rect.width
 
    @property
    def height(self):
        return self.rect.height
 
 
class Paddle(EnhancedSprite):
    """The sprite the player moves around to redirect the ball"""
    group = pygame.sprite.Group()
 
    def __init__(self, x, y, health):
        super().__init__(create_image(PADDLE_IMAGE, PADDLE_COLOR), self.group)
        self.x = x
        self.y = y
        self.health_start = health
        self.health_remaining = health
        self.image = pygame.image.load("paddle.png")
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.xmin = self.rect.width // 2  # Compute Spaceship x range.
        self.xmax = screen_width - self.xmin
        self.last_shot = pygame.time.get_ticks()
 
    def move(self, xpos):
        """Move to follow the cursor.  Clamp to window bounds"""
        self.rect.centerx = max(self.xmin, min(self.xmax, xpos))
 
 
class LifeCounter():
    """Keep track of lives count.  Display lives remaining using ball image"""
 
    def __init__(self, x, y, count=5):
        self.x, self.y = x, y
        self.image = create_image(BALL_IMAGE, BALL_COLOR)
        self.spacing = self.image.get_width() + 5
        self.group = pygame.sprite.Group()
        self.reset(count)
 
    def reset(self, count):
        """Reset number of lives"""
        self.count = count
        for c in range(count - 1):
            EnhancedSprite(self.image, self.group).at(self.x + c * self.spacing, self.y)
 
    def __len__(self):
        """Return number of lives remaining"""
        return self.count
 
    def kill(self):
        """Reduce number of lives"""
        if self.count > 1:
            self.group.sprites()[-1].kill()
        self.count = max(0, self.count - 1)
 
 
class Ball(EnhancedSprite):
    """Ball bounces around colliding with walls, paddles and bricks"""
    group = pygame.sprite.Group()
 
    def __init__(self, paddle, lives, speed=5):
        super().__init__(create_image(BALL_IMAGE, BALL_COLOR), self.group)
        self.paddle = paddle
        self.lives = lives
        self.speed = speed
        self.dx = self.dy = 0
        self.xfloat = self.yfloat = 0
        self.xmax = screen_width - self.rect.width
        self.ymax = paddle.bottom - self.rect.height
        self.reset(0)
 
    def at(self, x, y):
        self.xfloat = x
        self.yfloat = y
        return super().at(x, y)
 
    def reset(self, score=None):
        """Reset for a new game"""
        self.active = False
        if score is not None:
            self.score = score
 
    def start(self):
        """Start moving the ball in a random direction"""
        angle = random.random() - 0.5  # Launch angle limited to about +/-60 degrees
        self.dx = self.speed * math.sin(angle)
        self.dy = -self.speed * math.cos(angle)
        self.active = True
 
    def move(self):
        """Update the ball position.  Check for collisions with bricks, walls and the paddle"""
        hit_status = 0
        if not self.active:
            # Sit on top of the paddle
            self.at(self.paddle.centerx - self.width // 2, self.paddle.y - self.height - 2)
            return self
 
        # Did I hit some bricks?  Update the bricks and the score
        x1, y1 = self.xfloat, self.yfloat
        x2, y2 = x1 + self.dx, y1 + self.dy
        if (xhits := pygame.sprite.spritecollide(self.at(x2, y1), alien_group, True, pygame.sprite.collide_mask)):
            self.dx = -self.dx
            hit_status += 1
        if (yhits := pygame.sprite.spritecollide(self.at(x1, y2), alien_group, True, pygame.sprite.collide_mask)):
            self.dy = -self.dy
            hit_status += 2
        # hits = pygame.sprite.spritecollide(self, alien_group, True, pygame.sprite.collide_mask)
 
        if xhits or yhits:
            for alien in xhits or yhits:
                x, y = alien.hit()
                explosion = Explosion(x, y, 2, "yellow")
                explosion_group.add(explosion)
 
        # Did I hit a wall?
        if x2 <= 0 or x2 >= self.xmax:
            self.dx = -self.dx
            hit_status += 4
        if y2 <= 0:
            self.dy = abs(self.dy)
            hit_status += 8
 
        # Did I get past the paddle?
        if (y2 >= self.paddle.y) and ((self.x > self.paddle.right) or (self.right < self.paddle.x)):
            self.lives.kill()
            self.active = False
        elif self.dy > 0 and pygame.Rect.colliderect(self.at(x2, y2).rect, self.paddle.rect):
            # I hit the paddle.  Compute angle of reflection
            bangle = math.atan2(-self.dx, self.dy)  # Ball angle of approach
            pangle = math.atan2(self.centerx - self.paddle.centerx, 30)  # Paddle angle
            rangle = (pangle - bangle) / 2  # Angle of reflection
            self.dx = math.sin(rangle) * self.speed
            self.dy = -math.cos(rangle) * self.speed
            hit_status += 16
 
        if hit_status > 0:
            self.at(x1, y1)
        else:
            self.at(x2, y2)
 
 
def play_breakout(level, move_direction):
    game_over = 0
    paddle = Paddle(screen_width / 2, screen_height - 100, 3)
    paddle_group.add(paddle)
    lives = LifeCounter(10, screen_height - 30)
    ball = Ball(paddle, lives)
    ball_group.add(ball)
    last_count = pygame.time.get_ticks()
    create_aliens(3, 10, move_direction)
    countdown = 3
    run = True
    while run:
        p = pygame.mouse.get_pos()
        clock.tick(fps)
        # draw background
        draw_bg()
        # breakout level
        if countdown == 0:
            # create random alien bullets
            # record current time
            time_now = pygame.time.get_ticks()
            # in breakout levels aliens shouldn't shoot
 
            # check if all the aliens have been killed
            if len(alien_group) == 0:
                paddle.kill()
                ball.kill()
                # game_over = 1
                level += 1
                return level
            if game_over == 0:
                # update paddle
                game_over = paddle.move(p[0])
                # update sprite groups
                alien_group.update(level)
            else:
                if game_over == -1:
                    draw_text('GAME OVER!', font40, white, int(screen_width / 2 - 100),
                              int(screen_height / 2 + 50))
                if game_over == 1:
                    draw_text('YOU WIN!', font40, white, int(screen_width / 2 - 100),
                              int(screen_height / 2 + 50))
 
        if countdown > 0:
            draw_text('GET READY!', font40, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
            draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
            count_timer = pygame.time.get_ticks()
            if count_timer - last_count > 1000:
                countdown -= 1
                last_count = count_timer
 
        # update explosion group
        alien_group.update(move_direction)
        explosion_group.update()
        paddle_group.update()
        ball_group.update()
        # draw sprite groups
        alien_group.draw(screen)
        explosion_group.draw(screen)
        paddle_group.draw(screen)
        ball_group.draw(screen)
        # event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEMOTION:
                # breakout level
                paddle.move(event.pos[0])
            elif event.type == pygame.MOUSEBUTTONUP:
                if not ball.active:
                    ball.start()
        ball.move()
        pygame.display.flip()
    pygame.quit()
 
 
##### end boss things ##############################################################
# level = 0
end_boss_cooldown = 4000  # bullet cooldown in milliseconds
end_boss_centerx = screen_width / 2
end_boss_centery = 220
end_boss_center = end_boss_centerx, end_boss_centery
bullet_group = pygame.sprite.Group()
 
 
# Create EndBoss class
class EndBoss(pygame.sprite.Sprite):
    def __init__(self, center, health):
        super().__init__()
        self.center = center
        self.health_start = health
        self.health_remaining = health
        self.image = pygame.image.load("ship_4.png")
        self.rect = self.image.get_rect()
        self.rect.center = center
 
    def update(self):
        if pygame.sprite.spritecollide(self, bullet_group, True, pygame.sprite.collide_mask):
            x, y = Bullets.hit_endboss(self)
            explosion = Explosion(x, y, 2, "yellow")
            end_boss_explosion_group.add(explosion)
            # reduce spaceship health
            end_boss.health_remaining -= 2
 
        # draw health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.top - 15), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (
                self.rect.x, (self.rect.top - 15),
                int(self.rect.width * (self.health_remaining / self.health_start)),
                15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 4, "yellow")
            explosion_group.add(explosion)
            end_boss_gun.kill()
            self.kill()
 
 
end_boss_laser_group = pygame.sprite.Group()
 
 
class EndBossGun(pygame.sprite.Sprite):
    def __init__(self, center, angle=0):
        super().__init__()
        self.image = pygame.image.load("gun4.png")
        self.gun_image = self.image.copy()
        self.rect = self.gun_image.get_rect()
        self.center = center
        self.rect.center = self.center
        # guns is (x, y) position of gun relative to center of spaceship.
        self.guns = [pygame.math.Vector2(12, 70), pygame.math.Vector2(-12, 70)]
        self.lasers = pygame.sprite.Group()
        self.angle = angle
        self.last_shot = pygame.time.get_ticks()
 
    def aim(self, p):
        # Rotate end_boss' gun
        x_dist = p[0] - end_boss_centerx
        y_dist = end_boss_centery - (screen_height - 100)
        self.angle = math.degrees(math.atan2(y_dist, x_dist)) + 90
        self.image = pygame.transform.rotate(self.gun_image, self.angle)
        self.rect = self.image.get_rect(center=(end_boss_centerx, end_boss_centery))
        return self.angle
 
    def fire(self, angle):
        """Fire a laser."""
        for gun in self.guns:
            origin = pygame.math.Vector2(end_boss_center) + gun.rotate(-angle)
            end_boss_laser = EndBossLaser(angle, origin)
            end_boss_laser_group.add(end_boss_laser)
 
 
class EndBossLaser(pygame.sprite.Sprite):
    """A laser shot from the spaceship."""
 
    def __init__(self, angle, origin):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("endbosslaser.png")
        clean_laser_image = self.image.copy()
        self.rect = clean_laser_image.get_rect()
        """Fire laser.
        angle : angle in degrees the gun is pointing.
        origin : origin of my path (end of gun).
        """
        self.angle = angle
        self.image = pygame.transform.rotate(clean_laser_image, angle)
        self.origin = origin
        self.rect.center = origin
        self.unit_vector = pygame.math.Vector2(math.sin(self.angle / 180 * math.pi),
                                               math.cos(self.angle / 180 * math.pi))
        self.distance = 23
 
    def update(self):
        """Update position."""
        self.distance += 1
        if self.distance > 500:
            self.kill()
        else:
            self.rect.center = self.origin + self.unit_vector * self.distance
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            # reduce spaceship health
            spaceship.health_remaining -= 0.5
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1, "yellow")
            explosion_group.add(explosion)
            if spaceship.health_remaining <= 0:
                spaceship.kill()
 
 
end_boss_group = pygame.sprite.Group()
end_boss = EndBoss(end_boss_center, 300)
end_boss_gun = EndBossGun(end_boss_center, 0)
end_boss_group.add(end_boss)
end_boss_group.add(end_boss_gun)
end_boss_explosion_group = pygame.sprite.Group()
 
 
def play_end_boss_level():
    game_over = 0
    last_count = pygame.time.get_ticks()
    last_end_boss_shot = pygame.time.get_ticks()
    countdown = 3
    run = True
    while run:
        p = pygame.mouse.get_pos()
        clock.tick(fps)
        draw_bg()
        if countdown == 0:
            angle = end_boss_gun.aim(p)
            time_now = pygame.time.get_ticks()
            if time_now - last_end_boss_shot > end_boss_cooldown and len(end_boss_group) > 0:
                end_boss_gun.fire(angle)
                last_end_boss_shot = time_now
            if len(end_boss_group) == 0:
                end_boss_gun.kill()
                game_over = 1
            if len(spaceship_group) == 0:
                draw_text('GAME OVER!', font40, white, int(screen_width / 2 - 100),
                          int(screen_height / 2 + 50))
            if game_over == 0:
                spaceship.update()
                bullet_group.update()
                end_boss_group.update()
                # end_boss_gun_group.update()
                explosion_group.update()
                end_boss_laser_group.update()
                end_boss_explosion_group.update()
            else:
                if game_over == -1:
                    draw_text('GAME OVER!', font40, (255, 255, 255), int(screen_width / 2 - 100),
                              int(screen_height / 2 + 50))
                if game_over == 1:
                    draw_text('YOU SAVED THE EARTH!', font40, (255, 255, 255), int(screen_width / 2 - 100),
                              int(screen_height / 2 + 50))
        if countdown > 0:
            draw_text('GET READY!', font40, (255, 255, 255), int(screen_width / 2 - 110), int(screen_height / 2 + 50))
            draw_text(str(countdown), font40, (255, 255, 255), int(screen_width / 2 - 10), int(screen_height / 2 + 100))
            count_timer = pygame.time.get_ticks()
            if count_timer - last_count > 1000:
                countdown -= 1
                last_count = count_timer
 
        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        explosion_group.draw(screen)
        end_boss_group.draw(screen)
        end_boss_laser_group.draw(screen)
        end_boss_explosion_group.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
 
        spaceship.move(p[0])
        pygame.display.flip()
 
 
####################################################################################
# game_over = 0  # 0 is no game over, 1 means player has won, -1 means player has lost
space_invaders_levels = [1, 3, 5, 7]
breakout_levels = [2, 4, 6]
end_boss_level = [8]
level = 1
move_direction = 1
for i in range(1, 9):
    if level in space_invaders_levels:
        level = play_space_invaders(level, move_direction)
    else:
        if level in breakout_levels:
            level = play_breakout(level, move_direction)
        if level in end_boss_level:
            play_end_boss_level()