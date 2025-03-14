from consts import WIDTH, HEIGHT, Direction

def is_valid(center_x: int, center_y: int):
    """Checks if given position is within bounds

    Inputs
    ------
    center_x (int): x-coordinate
    center_y (int): y-coordinate

    Returns
    -------
    bool: True if valid, False otherwise
    """
    return center_x > 0 and center_y > 0 and center_x < WIDTH - 1 and center_y < HEIGHT - 1

def command_generator(states, obstacles):
    """
    This function takes in a list of states and generates a list of commands for the robot to follow
    
    Inputs
    ------
    states: list of State objects
    obstacles: list of obstacles, each obstacle is a dictionary with keys "x", "y", "d", and "id"

    Returns
    -------
    commands: list of commands for the robot to follow
    """

    # Convert the list of obstacles into a dictionary with key as the obstacle id and value as the obstacle
    obstacles_dict = {ob['id']: ob for ob in obstacles}
    
    # Initialize commands list
    commands = []

    # Iterate through each state in the list of states
    for i in range(1, len(states)):
        steps = "1"  # Default step size

        # If previous state and current state are the same direction,
        if states[i].direction == states[i - 1].direction:
            # Forward - Must be (east facing AND x value increased) OR (north facing AND y value increased)
            if (states[i].x > states[i - 1].x and states[i].direction == Direction.EAST) or (states[i].y > states[i - 1].y and states[i].direction == Direction.NORTH):
                commands.append("FW0{}".format(steps))
            # Forward - Must be (west facing AND x value decreased) OR (south facing AND y value decreased)
            elif (states[i].x < states[i-1].x and states[i].direction == Direction.WEST) or (
                    states[i].y < states[i-1].y and states[i].direction == Direction.SOUTH):
                commands.append("FW0{}".format(steps))
            # Backward - All other cases where the previous and current state is the same direction
            else:
                commands.append("BW0{}".format(steps))

            # If any of these states has a valid screenshot ID, then add a SNAP command as well to take a picture
            if states[i].screenshot_id != -1:
                current_ob_dict = obstacles_dict[states[i].screenshot_id]
                current_robot_position = states[i]

                # Obstacle facing WEST, robot facing EAST
                if current_ob_dict['d'] == 6 and current_robot_position.direction == 2:
                    if current_ob_dict['y'] > current_robot_position.y:
                        commands.append(f"SNAP{states[i].screenshot_id}_L")
                    elif current_ob_dict['y'] == current_robot_position.y:
                        commands.append(f"SNAP{states[i].screenshot_id}_C")
                    elif current_ob_dict['y'] < current_robot_position.y:
                        commands.append(f"SNAP{states[i].screenshot_id}_R")
                    else:
                        commands.append(f"SNAP{states[i].screenshot_id}")
                
                # Obstacle facing EAST, robot facing WEST
                elif current_ob_dict['d'] == 2 and current_robot_position.direction == 6:
                    if current_ob_dict['y'] > current_robot_position.y:
                        commands.append(f"SNAP{states[i].screenshot_id}_R")
                    elif current_ob_dict['y'] == current_robot_position.y:
                        commands.append(f"SNAP{states[i].screenshot_id}_C")
                    elif current_ob_dict['y'] < current_robot_position.y:
                        commands.append(f"SNAP{states[i].screenshot_id}_L")
                    else:
                        commands.append(f"SNAP{states[i].screenshot_id}")

                # Obstacle facing NORTH, robot facing SOUTH
                elif current_ob_dict['d'] == 0 and current_robot_position.direction == 4:
                    if current_ob_dict['x'] > current_robot_position.x:
                        commands.append(f"SNAP{states[i].screenshot_id}_L")
                    elif current_ob_dict['x'] == current_robot_position.x:
                        commands.append(f"SNAP{states[i].screenshot_id}_C")
                    elif current_ob_dict['x'] < current_robot_position.x:
                        commands.append(f"SNAP{states[i].screenshot_id}_R")
                    else:
                        commands.append(f"SNAP{states[i].screenshot_id}")

                # Obstacle facing SOUTH, robot facing NORTH
                elif current_ob_dict['d'] == 4 and current_robot_position.direction == 0:
                    if current_ob_dict['x'] > current_robot_position.x:
                        commands.append(f"SNAP{states[i].screenshot_id}_R")
                    elif current_ob_dict['x'] == current_robot_position.x:
                        commands.append(f"SNAP{states[i].screenshot_id}_C")
                    elif current_ob_dict['x'] < current_robot_position.x:
                        commands.append(f"SNAP{states[i].screenshot_id}_L")
                    else:
                        commands.append(f"SNAP{states[i].screenshot_id}")
            continue

        # If previous state and current state are not the same direction, it means that there will be a turn command involved
        # Assume there are 4 turning command: FR, FL, BL, BR (the turn command will turn the robot 90 degrees)
        # FR00 | FR30: Forward Right;
        # FL00 | FL30: Forward Left;
        # BR00 | BR30: Backward Right;
        # BL00 | BL30: Backward Left;

        # Facing north previously
        if states[i - 1].direction == Direction.NORTH:
            if states[i].direction == Direction.EAST:
                if states[i].y > states[i - 1].y:
                    commands.append("FR0{}".format(steps))
                else:
                    commands.append("BL0{}".format(steps))
            elif states[i].direction == Direction.WEST:
                if states[i].y > states[i - 1].y:
                    commands.append("FL0{}".format(steps))
                else:
                    commands.append("BR0{}".format(steps))
            # elif states[i].direction == Direction.NORTH_EAST:
            #     commands.append("FWD_NE0{}".format(steps))
            #     commands.append("TURN_NORTH")
            # elif states[i].direction == Direction.NORTH_WEST:
            #     commands.append("FWD_NW0{}".format(steps))
            #     commands.append("TURN_NORTH")
            # else:
            #     raise Exception("Invalid turning direction")

        elif states[i - 1].direction == Direction.EAST:
            if states[i].direction == Direction.NORTH:
                if states[i].y > states[i - 1].y:
                    commands.append("FL0{}".format(steps))
                else:
                    commands.append("BR0{}".format(steps))
            elif states[i].direction == Direction.SOUTH:
                if states[i].y > states[i - 1].y:
                    commands.append("BL0{}".format(steps))
                else:
                    commands.append("FR0{}".format(steps))
            # elif states[i].direction == Direction.SOUTH_EAST:
            #     commands.append("FWD_SE0{}".format(steps))
            #     commands.append("TURN_EAST")
            # elif states[i].direction == Direction.NORTH_EAST:
            #     commands.append("FWD_NE0{}".format(steps))
            #     commands.append("TURN_EAST")
            # else:
            #     raise Exception("Invalid turning direction")

        elif states[i - 1].direction == Direction.SOUTH:
            if states[i].direction == Direction.EAST:
                if states[i].y > states[i - 1].y:
                    commands.append("BR0{}".format(steps))
                else:
                    commands.append("FL0{}".format(steps))
            elif states[i].direction == Direction.WEST:
                if states[i].y > states[i - 1].y:
                    commands.append("BL0{}".format(steps))
                else:
                    commands.append("FR0{}".format(steps))
            # elif states[i].direction == Direction.SOUTH_EAST:
            #     commands.append("FWD_SE0{}".format(steps))
            #     commands.append("TURN_SOUTH")
            # elif states[i].direction == Direction.SOUTH_WEST:
            #     commands.append("FWD_SW0{}".format(steps))
            #     commands.append("TURN_SOUTH")
            # else:
            #     raise Exception("Invalid turning direction")

        elif states[i - 1].direction == Direction.WEST:
            if states[i].direction == Direction.NORTH:
                if states[i].y > states[i - 1].y:
                    commands.append("FR0{}".format(steps))
                else:
                    commands.append("BL0{}".format(steps))
            elif states[i].direction == Direction.SOUTH:
                if states[i].y > states[i - 1].y:
                    commands.append("BR0{}".format(steps))
                else:
                    commands.append("FL0{}".format(steps))
            # elif states[i].direction == Direction.NORTH_WEST:
            #     commands.append("FWD_NW0{}".format(steps))
            #     commands.append("TURN_WEST")
            # elif states[i].direction == Direction.SOUTH_WEST:
            #     commands.append("FWD_SW0{}".format(steps))
            #     commands.append("TURN_WEST")
            # else:
            #     raise Exception("Invalid turning direction")
        else:
            raise Exception("Invalid position")

        # If any of these states has a valid screenshot ID, then add a SNAP command as well to take a picture
        if states[i].screenshot_id != -1:
            current_ob_dict = obstacles_dict[states[i].screenshot_id]
            current_robot_position = states[i]

            # Obstacle facing WEST, robot facing EAST
            if current_ob_dict['d'] == 6 and current_robot_position.direction == 2:
                if current_ob_dict['y'] > current_robot_position.y:
                    commands.append(f"SNAP{states[i].screenshot_id}_L")
                elif current_ob_dict['y'] == current_robot_position.y:
                    commands.append(f"SNAP{states[i].screenshot_id}_C")
                elif current_ob_dict['y'] < current_robot_position.y:
                    commands.append(f"SNAP{states[i].screenshot_id}_R")
                else:
                    commands.append(f"SNAP{states[i].screenshot_id}")
            
            # Obstacle facing EAST, robot facing WEST
            elif current_ob_dict['d'] == 2 and current_robot_position.direction == 6:
                if current_ob_dict['y'] > current_robot_position.y:
                    commands.append(f"SNAP{states[i].screenshot_id}_R")
                elif current_ob_dict['y'] == current_robot_position.y:
                    commands.append(f"SNAP{states[i].screenshot_id}_C")
                elif current_ob_dict['y'] < current_robot_position.y:
                    commands.append(f"SNAP{states[i].screenshot_id}_L")
                else:
                    commands.append(f"SNAP{states[i].screenshot_id}")

            # Obstacle facing NORTH, robot facing SOUTH
            elif current_ob_dict['d'] == 0 and current_robot_position.direction == 4:
                if current_ob_dict['x'] > current_robot_position.x:
                    commands.append(f"SNAP{states[i].screenshot_id}_L")
                elif current_ob_dict['x'] == current_robot_position.x:
                    commands.append(f"SNAP{states[i].screenshot_id}_C")
                elif current_ob_dict['x'] < current_robot_position.x:
                    commands.append(f"SNAP{states[i].screenshot_id}_R")
                else:
                    commands.append(f"SNAP{states[i].screenshot_id}")

            # Obstacle facing SOUTH, robot facing NORTH
            elif current_ob_dict['d'] == 4 and current_robot_position.direction == 0:
                if current_ob_dict['x'] > current_robot_position.x:
                    commands.append(f"SNAP{states[i].screenshot_id}_R")
                elif current_ob_dict['x'] == current_robot_position.x:
                    commands.append(f"SNAP{states[i].screenshot_id}_C")
                elif current_ob_dict['x'] < current_robot_position.x:
                    commands.append(f"SNAP{states[i].screenshot_id}_L")
                else:
                    commands.append(f"SNAP{states[i].screenshot_id}")

    # Final command is the stop command (FIN)
    commands.append("FIN")  

    # Compress commands if there are consecutive forward or backward commands
    compressed_commands = [commands[0]]

    for i in range(1, len(commands)):
        # If both commands are BW
        if commands[i].startswith("BW") and compressed_commands[-1].startswith("BW"):
            # Get the number of steps of previous command
            steps = int(compressed_commands[-1][2:])
            # If steps are not 90, add 10 to the steps
            if steps < 9:
                compressed_commands[-1] = "BW0{}".format(steps + 1)
                continue
            else:
                compressed_commands[-1] = "BW{}".format(steps + 1)
                continue

        # If both commands are FW
        elif commands[i].startswith("FW") and compressed_commands[-1].startswith("FW"):
            # Get the number of steps of previous command
            steps = int(compressed_commands[-1][2:])
            # If steps are not 90, add 10 to the steps
            if steps < 9:
                compressed_commands[-1] = "FW0{}".format(steps + 1)
                continue
            else:
                compressed_commands[-1] = "FW{}".format(steps + 1)
                continue
        
        # Otherwise, just add as usual
        compressed_commands.append(commands[i])
    
    print(compressed_commands)
    return compressed_commands