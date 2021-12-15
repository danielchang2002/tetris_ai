from genetic_controller import * 

def run_genetic_experiments(): 
    pop_size = [8,10,15]
    for i in pop_size:
        run_X_epochs(num_epochs=5, num_trials=2, pop_size=i, survival_rate=.2, num_elite=2, logging_file=f'genetic/data_{i}')

if __name__ =='__main__':
    run_genetic_experiments()
