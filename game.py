from tkinter import Toplevel

class MashOption():
    def __init__(self, cat, val):
        self.category = cat
        self.value = val

class Game():
    def __init__(self, options:list[MashOption], spiral:int):
        self.num = spiral
        self.original = [MashOption("house", x) for x in ["mansion", "apartment", "shack", "house"]]
        self.original += options[:]
        self.remaining = self.original[:]
        self.removed = []
        
        self.categories = []
        [self.categories.append(x.category) for x in self.original 
         if x.category not in self.categories]
        self.final = {k:"" for k in self.categories}
        
    def isfinal(self):
        for cat in self.categories:
            xed = [x for x in self.removed if x.category == cat]
            if len(xed) == 3:
                pick = [x for x in self.original if x not in self.removed and x.category == cat][0]
                #print("selected: ", pick.value)
                self.final[cat] = pick.value
                self.removed.append(pick)
                if pick in self.remaining:
                    self.remaining.remove(pick)

    def reorder_list(self, nxt):
        indx = self.remaining.index(nxt)
        if indx > 0:
            temp = self.remaining[indx:] + self.remaining[:indx-1] 
        else:
            temp = self.remaining[indx:-1]     
        self.remaining = temp
        #print("after re-order:", [x.value for x in self.remaining])

    def pad_list(self):
        padded = (self.remaining + self.remaining)*round(self.num/len(self.remaining))
        return padded
    
    def run(self):
        while self.remaining != []:
            self.isfinal()
            i = self.num - 1
            #print("remaining:", len(self.remaining), [x.value for x in self.remaining])
            if len(self.remaining) <= self.num and len(self.remaining) > 1:
                temp_opts = self.pad_list()
                #print("removed: ", temp_opts[i].value)
                self.removed.append(temp_opts[i])
                self.reorder_list(temp_opts[i+1])
            elif len(self.remaining) > 1:
                #print("removed: ", self.remaining[i].value)
                self.removed.append(self.remaining[i])
                self.reorder_list(self.remaining[i+1])

def test_setup():
        car = ["car1", "car2", "car3", "car4"]
        job = ['career1', 'career2', 'career3', 'career4']
        money = ['salary1', 'salary2', 'salary3', 'salary4']
        partner = ['spouse1', 'spouse2', 'spouse3', 'spouse4']
        kids = ['kids1', 'kids2', 'kids3', 'kids4']
        res = []
        [res.append(MashOption(x[i][:-1], x[i])) for x in [car, job, money, partner, kids] for i in range(4)]
        return res
