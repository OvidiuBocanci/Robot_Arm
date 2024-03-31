
def list_of_moves(moves_list):

    new_list=[]
    prev_pos = 0
    for index, pos in enumerate(moves_list):
        if index == 0:

            new_list.append(pos)
            prev_pos = pos

        else:
            value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5 = prev_pos
            value_stepper = pos[0]
            dif1 = prev_pos[1]-pos[1]
            dif2 = prev_pos[2]-pos[2]
            dif3 = prev_pos[3]-pos[3]
            dif4 = prev_pos[4]-pos[4]
            dif5 = prev_pos[5]-pos[5]
            dif_list = [dif1, dif2, dif3, dif4, dif5]
            max_dif = max(abs(num) for num in dif_list)

            if max_dif == 0:
                new_list.append((value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5))
            else:
                for nr in range(max_dif):

                    if dif1 < 0:
                        value_servo1 += 1
                        dif1 = value_servo1 - pos[1]
                    elif dif1 > 0:
                        value_servo1 -= 1
                        dif1 = value_servo1 - pos[1]

                    if dif2 < 0:
                        value_servo2 += 1
                        dif2 = value_servo2 - pos[2]
                    elif dif2 > 0:
                        value_servo2 -= 1
                        dif2 = value_servo2 - pos[2]

                    if dif3 < 0:
                        value_servo3 += 1
                        dif3 = value_servo3 - pos[3]
                    elif dif3 > 0:
                        value_servo3 -= 1
                        dif3 = value_servo3 - pos[3]

                    if dif4 < 0:
                        value_servo4 += 1
                        dif4 = value_servo4 - pos[4]
                    elif dif4 > 0:
                        value_servo4 -= 1
                        dif4 = value_servo4 - pos[4]

                    if dif5 < 0:
                        value_servo5 += 1
                        dif5 = value_servo5 - pos[5]
                    elif dif5 > 0:
                        value_servo5 -= 1
                        dif5 = value_servo5 - pos[5]
                    new_list.append((value_stepper, value_servo1, value_servo2, value_servo3, value_servo4, value_servo5))
            prev_pos = pos
    return new_list











