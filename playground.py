self_list = ['animals', 'block_lego', 'music_dancing', 'play_set',
            'puppet_doll', 'transportation', 'abc_mouse',
            'puzzle', 'paint', 'play_dough', 'dry_erase',
            'sensory_table', 'dress_up', 'tlc_market',
            'play_food', 'indoor_slide', 'indoor_structure',
            'hoops', 'board_game', 'marker_crayon', 'chalk_board',
            'scissor_glue', 'light_table']

print(self_list[0])



name = ['mike', 'john', 'steve']
age = [20, 32, 19]
for i in range(len(name)):
    exec("%s = %d" %(name[i], age[i]))
print(mike)
print(john)
print(steve)

mood_list = ['kind', 'playful', 'sharing', 'caring', 'rough', 'hitting']

class MoodModel():

    def __init__(self, on_date, child_id, kind, playful, sharing, caring, rough, hitting):
        self.on_date = on_date
        self.child_id = child_id
        self.kind = kind
        self.playful = playful
        self.sharing = sharing
        self.caring = caring
        self.rough = rough
        self.hitting = hitting


mood = MoodModel(False,False,False,False,False,False,False,False)

for i in range(len(mood_list)):
    exec("mood.%s = True" %(mood_list[i]))
    exec("print(mood.%s)" %(mood_list[i]))

self.animal = data['animal']
self.block_lego = data['block_lego']
self.music_dancing = data['music_dancing']
self.play_set = data['play_set']
self.puppet_doll = data['puppet_doll']
self.transportation = data['transportation']
self.abc_mouse = data['abc_mouse']
self.puzzle = data['puzzle']
self.paint = data['paint']
self.play_dough = data['play_dough']
self.dry_erase = data['dry_erase']
self.sensory_table = data['sensory_table']
self.dress_up = data['dress_up']
self.tlc_market = data['tlc_market']
self.play_food = data['play_food']
self.indoor_slide = data['indoor_slide']
self.indoor_structure = data['indoor_structure']
self.hoop = data['hoop']
self.board_game = data['board_game']
self.market_crayon = data['marker_crayon']
self.chalk_board = data['chalk_board']
self.scissor_glue = data['scissor_glue']
self.light_table = data['light_table']