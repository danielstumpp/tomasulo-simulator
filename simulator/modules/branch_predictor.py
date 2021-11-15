class BranchPredictor:
    def __init__(self):
        self.predictors = [False]*8
        self.BTB = [0]*8

    def get_prediction(self, branch_PC):
        '''
        Returns taken, target_address 
        '''
        pred_idx = branch_PC % 8
        return self.predictors[pred_idx], self.BTB[pred_idx]

    def update_predictor(self, branch_PC, taken, target):
        pred_idx = branch_PC % 8
        self.BTB[pred_idx] = target
        self.predictors[pred_idx] = taken

        # TODO: call this in func_units