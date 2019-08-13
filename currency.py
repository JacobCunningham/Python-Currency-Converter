class Currency:

    def __init__(self, amount, kind):
        self.amount = amount
        self.type = kind.upper()
    
    def __str__(self):
        return f"{self.amount:.2f} {self.type}"