from stageType import StageType;

#class that creates a Stage object
class StageTracker(object):
    def __init__ (self, stage_number: StageType, level_number: int):
        self.stage_number = stage_number
        self.level_number = level_number

    def get_stage_number(self):
        return self.stage_number
    
    def get_level_number(self):
        return self.level_number
    
    def move_onto_next_stage(self):
        if self.stage_number == StageType.TUTORIAL:
            self.stage_number = StageType.LEVEL_1
            self.level_number = 0
        elif self.stage_number == StageType.LEVEL_1:
            self.stage_number = StageType.LEVEL_2
            self.level_number = 0
        else:
            self.stage_number = StageType.TUTORIAL
            self.level_number = 0

    def move_to_right_room(self):
        self.level_number = self.level_number + 1
    def move_to_left_room(self):
        self.level_number = self.level_number - 1
    def move_to_above_room(self):
        self.level_number = self.level_number - 3
    def move_to_below_room(self):
        self.level_number = self.level_number + 3