class Unlockable:
    def __init__(self):
        """
        Initialize Unlockable object.
        """
        self.skins = {
            "classic": {"unlocked": True, "price": 0},
            "neon": {"unlocked": False, "price": 100},
            "retro": {"unlocked": False, "price": 200}
        }
        self.bonuses = {
            "double_score": {"unlocked": False, "price": 50},
            "extra_life": {"unlocked": False, "price": 150}
        }
        self.balance = 0

    def unlock_skin(self, skin_name, balance):
        """
        Unlock skin.

        Args:
        skin_name (str): Skin name.
        balance (int): Player balance.
        Returns:
        bool: Unlock success.
        """
        if skin_name in self.skins and not self.skins[skin_name]["unlocked"]:
            price = self.skins[skin_name]["price"]
            if balance >= price:
                self.skins[skin_name]["unlocked"] = True
                return True
        return False

    def unlock_bonus(self, bonus_name, balance):
        """
        Unlock bonus.

        Args:
        bonus_name (str): Bonus name.
        balance (int): Player balance.
        Returns:
        bool: Unlock success.
        """
        if bonus_name in self.bonuses and not self.bonuses[bonus_name]["unlocked"]:
            price = self.bonuses[bonus_name]["price"]
            if balance >= price:
                self.bonuses[bonus_name]["unlocked"] = True
                return True
        return False

    def update_balance(self, amount):
        """
        Update player balance.

        Args:
        amount (int): Balance change.
        """
        self.balance += amount