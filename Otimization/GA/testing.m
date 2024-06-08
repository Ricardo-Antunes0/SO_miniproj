Nodes= load('Nodes200.txt');
Links= load('Links200.txt');
L= load('L200.txt');
nNodes= size(Nodes,1);
nLinks= size(Links,1);
G=graph(L);


% This program is to test the GA algorithm with different parameters 

populationValues = [100,200];
mutation_prob = [0.1,0.5];
mValues = [1,10,50];
maxTime = 60;
cValues = [8,10,12];

for c = cValues
    for population_size = populationValues
        for m = mValues
            for prob = mutation_prob
                [best_solution,generation_count,time_found, exec_time] = GA(G,c,population_size,prob,m,maxTime);
                fprintf("\nResults for c = %d; pop_size =%d;  m = %d; mut_prob= %f \n",c,population_size,m,prob);
                fprintf('Objective value: %d\n', best_solution);
                fprintf('Running time: %.3f seconds\n', exec_time);
                fprintf('The time which was found the best solution: %.3f',time_found);
                fprintf(' Number of population generated (iterations): %d\n',generation_count);
            end
        end
    end
end