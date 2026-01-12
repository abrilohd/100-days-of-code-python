print( '''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/[TomekK]
*******************************************************************************
 '''
      )

print("Welcome To Tresure Island Game->")
print("Your mission is to find the Treasure.")
choise_1 = input("You\'re in the crossroad .where do you want to go? 'right' or 'left'").lower()
if choise_1 == "left":
    choise_2 = input('You\'ve come to a lake. There is an island in the middle of the lake . type "wait" to wait for a boat . Type "swim" across . ').lower()
    if choise_2 == "wait":
        choise_3 = input("You arrive at the island unharmed . There is a House with 3 doors. One red, one yellow, and one blue. which color do you choose? ").lower()
        if choise_3 == "red" :
            print("You go In the Fire room.Game Over")
        elif choise_3 == "yellow":
            print("you found the Treasure . You Win   !!!!!")
        elif choise_3 == "blue":
            print("You GO in Wrong direction. Game Over.!")
        else :
            print("You enter the wrong choise . Game Over.!")
    if choise_2 == "swim":
        print("Attacked by trout.Game Over.")
elif choise_1 == "right":
    print("Fall into a hole.Game Over.")
else :
    print("Fall into a hole.Game Over.")

print('''
                                                                                                    
                                                                                                    
                                               ,:                                                   
                                               ,:                                                   
                   1f.                                                                              
                   ,:                                                                               
               ,i                                                                                   
               .,             ,                                                                    ;
                             .f.                                                                   :
                             ,L,                                       ,1,                          
                             ;C:                                       ,t,                          
                             iLi                                  ;:                                
      ;1:                   :LLfi:.  :.                           ,,                                
      iCi                     GGGGG;0@88880GCCi.                                                            
                   .,        ,GGGGG08@@@@@@@@@@0C1,                                                         
                   .1i       GGGGGLCG0888@@888@@@@8C;                                                       
                     f1     : GGGGGCffLLLL0G888@888@@@L.                                                     
 ,                    :GiGGGGGGGGGG1CLCLLLfff0@@@@@@@88@G,                                                    
 .                    .fLGGGGGGGGGGGGGGGfLLCCfL@GffL0888@@@@@8@G:         .tC:                                      
                      .LCGGGGGGGGGGGGGGGGLfLLf0@LffffffLLLLLLLLLL.         ;i.                                      
                        ;G1GGGGGGGGGG,GGGGGLLLfL@Gfffffffffffffffff.                                                  
                     :LiGGGGGGGGG GGGGG.LffffLffffffffffffLLffff,                                      :i          
                   ,i,GGGGGGGGGGGGGGGfCfffffffffffLCG00888GCf;.                                      .          
                   ,       GGGGGGGGGGiCLLfLLffLG08@@@@@@@@@@L,.                                                 
                         :GGGGGLCCLfLLf08800000000GGG1                                                   
                          .fGGGGGLCLfLLffffffffffffffL,                                                   
                          ;GGGGGLLLLLLLCCLLLfffLLLft:                                                    
                          ;GGGGGf1tfLLLLLfLLftt1i;,                                                      
                        :ff,GGGGG .,:;;iL1,.                                                            
                       ;Lt.         :f,                                                             
                  ,1i ;Li            ,1,                                                            
                  ,fi:t,               .                                                            
                     :                                                                              
                                                                                                    
                                                                                                    
           ,t;                                                        ,.                            
           .i:                                                       ,Lf                            
                                                                      .                             '''
)
print("you found the Treasure . You Win   !!!!!")

