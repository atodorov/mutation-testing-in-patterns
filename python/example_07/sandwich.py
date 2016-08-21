class Sandwich(object):
    def __init__(self, meat = None, bread = None):
        """
            @meat  - string
            @bread - string

            Parameters identify the type of ingredients used.
        """
        self.meat = meat
        self.bread = bread

    def __eq__(self, other):
        if not other:
            return False

        return self.meat == other.meat and self.bread == other.bread

    def __ne__(self, other):
        return not self == other

class SandwichWithMayoAndEggs(Sandwich):
    def __init__(self, meat = None, bread = None, mayo=True, eggs=2):
        super(self.__class__, self).__init__(meat, bread)
        self.mayo = mayo
        self.eggs = eggs

    def __eq__(self, other):
        if not other:
            return False

        return self.meat == other.meat and self.bread == other.bread and \
                self.mayo == other.mayo and self.eggs == other.eggs
