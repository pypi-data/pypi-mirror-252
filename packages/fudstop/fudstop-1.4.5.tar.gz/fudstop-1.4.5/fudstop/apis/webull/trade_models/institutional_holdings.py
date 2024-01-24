import pandas as pd

class InstitutionHolding:
    def __init__(self, data):
        self.institution_holding = InstitutionStat(data['institutionHolding'])



class InstitutionStat:
    def __init__(self, data):
        self.stat = Stat(data['institutionHolding']['stat'])
        self.new_position = Position(data['institutionHolding']['newPosition'])
        self.increase = Position(data['institutionHolding']['increase'])
        self.sold_out = Position(data['institutionHolding']['soldOut'])
        self.decrease = Position(data['institutionHolding']['decrease'])


        self.data_dict = { 
            'holding_ratio': self.stat.holding_ratio,
            'holding_count_change': self.stat.holding_count_change,
            'holding_ratio_change': self.stat.holding_ratio_change,
            'holding_count': self.stat.holding_count,
            'holding_ratio': self.stat.holding_ratio,
            'new': self.new_position,
            'increase': self.increase,
            'sold_out': self.sold_out,
            'decrease': self.decrease
        }


        self.as_dataframe = pd.DataFrame(self.data_dict, index=[0])
class Stat:
    def __init__(self, data):
        self.holding_count = data.get('holdingCount', None)
        self.holding_count_change = data.get('holdingCountChange', None)
        self.holding_ratio = data.get('holdingRatio', None)
        self.holding_ratio_change = data.get('holdingRatioChange', None)
        self.institutional_count = data.get('institutionalCount', None)

    def to_dict(self):
        return {
            'holdingCount': self.holding_count,
            'holdingCountChange': self.holding_count_change,
            'holdingRatio': self.holding_ratio,
            'holdingRatioChange': self.holding_ratio_change,
            'institutionalCount': self.institutional_count,
        }

class Position:
    def __init__(self, data):
        self.holding_count_change = data.get('holdingCountChange', None)
        self.institutional_count = data.get('institutionalCount', None)

    def to_dict(self):
        return {
            'holdingCountChange': self.holding_count_change,
            'institutionalCount': self.institutional_count,
        }
