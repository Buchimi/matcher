import random
from typing import FrozenSet, Literal, Set
from pydantic import BaseModel
from hungarian_algorithm import algorithm
from typing import List


interests = ["anime", "games", "soccer", "volleyball", "basketball", "summer"]
class Participant(BaseModel):
    name : str
    sex : Literal["M" , "F"]
    wants : Literal["M" , "F"]
    

    def __hash__(self):  # make hashable BaseModel subclass
        return hash((type(self),) + tuple(self.model_dump(include={"name", "sex", "wants"})))


    def want_eachother(self, other_participant:"Participant"):
        return self.sex == other_participant.wants and self.wants == other_participant.sex

    def is_straight(self):
        return self.sex == "F" and self.wants == "M" or self.sex == "M" and self.wants == "F"

    def is_lesbian(self):
        return self.sex == "F" and self.wants == "F"
        
    def is_gay(self):
        return self.sex == "M" and self.wants == "M"
    
    def calculate_match(self, other : "Participant", interests : dict[str, dict["Participant", int]], randomize=False, previous_matchings:Set[FrozenSet["Participant"]]=set() ):
        tally = 0
        fs = frozenset([self, other])
        if fs in previous_matchings:
            return -1000
        if randomize:
            return random.randint(0, 25) * len(interests)
        for interest in interests.keys():
            mine = interests[interest].get(self, 0)
            theirs = interests[interest].get(other, 0)
            tally += mine * theirs
        return tally
    
mike = Participant(name="Michael", sex="M", wants="F")
jane = Participant(name="Jane", sex="F", wants="M" )

participants = [mike, Participant(name="Pelumi", sex="M", wants="F"), jane, Participant(name="Julia", sex="F", wants="M")]

def divide_up_participants(all_participants : List[Participant]):
    straight_guys = list(filter(lambda participant : participant.sex == "M" ,all_participants))
    straight_girls = list(filter(lambda participant : participant.sex == "F" ,all_participants))

    lesbians = list(filter(lambda participant : participant.is_lesbian(), all_participants))
    gay_ppl = list(filter(lambda participant : participant.is_gay(), all_participants))
    
    return (straight_guys, straight_girls, lesbians, gay_ppl)

def equal_distribution(participants : List[Participant]):
    list1 = []
    list2 = []
    for participant in participants:
        if len(list1) == len(list2):
            list1.append(participant)
        else: 
            list2.append(participant)
    return list1, list2

def matching(participants : List[Participant], interests : List[str]):
    
    mapping: dict[Participant , dict[str, int]] = {}
    for participant in  participants:
        if participant not in mapping:
            mapping[participant] = {}
        for interest in interests:
            score = random.randint(1, 5)
            mapping[participant][interest] = score

    hungarian_graph = {}

    for participant in participants:
        if participant.sex == "F":
            continue
        hungarian_graph[participant] = {}

        section = hungarian_graph[participant]
        
        for other_participant in participants:
            if other_participant.sex == "M":
                continue
            print(other_participant)

            section[other_participant] = 0

            if not participant.want_eachother(other_participant) :
                section[other_participant] = -200
            else:
                # They would date eachother
                tally = 0
                for interest in interests:
                    tally += mapping[participant][interest] * mapping[other_participant][interest]
                section[other_participant] = tally


    # print(hungarian_graph)
    result = algorithm.find_matching(hungarian_graph)
    return result

def matching_new(participants1 : List[Participant], participants2: List[Participant], 
                 interests : dict[str, dict[Participant, int]], previous_matchings : Set[FrozenSet[ Participant]], randomize = False):
    hungarian_graph = {}
    for participant in participants1:
        hungarian_graph[participant] = {}
        for other in participants2:
            hungarian_graph[participant][other] = participant.calculate_match(other=other, interests=interests, randomize=randomize, previous_matchings=previous_matchings)
    return algorithm.find_matching(hungarian_graph)

def generate_interest_dict(interests : List[str]) -> dict[str, dict[Participant, int]]:
    res = {}
    for interest in interests:
        res[interest] = {}
    return res

st =frozenset([mike, jane])

previous_matchings  = set()
previous_matchings.add(st)
print(previous_matchings)
guys, girls, _, __ = divide_up_participants(participants)
interests_dict = generate_interest_dict(interests=interests)
for i in range (1):
    res = matching_new(guys, girls, interests=interests_dict, randomize=True, previous_matchings=previous_matchings) 
    print(res)
    # for matching in res:
    #     print(matching[0])
        # if matching[0].name == "Michael":
        #     print("yes")