class Order:
    '''
    Patience:
      If an order is rejected by all of the couriers in the system within a
      predetermined amount of time, then that order is not delivered and it
      leaves the system. That is, each order has a duration value, which
      shows how long it waits until it is assigned to a courier and the delivery
      process begins. If it is not delivered within a specified period, it
      leaves the system. This assumption is inline with the observations in
      practice where each customer typically has patience level and leaves
      the system if he/she is not served within certain amount of time.
    '''
    def __init__(self, origin, destination, patience=10):
        self.origin = origin  # (x, y)
        self.destination = destination  # (x, y)
        self.patience = patience
        self.assigned = False
        self.status = 'pending'  # 'pending', 'in_transit', 'delivered', 'rejected'