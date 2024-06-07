Nodes= load('Nodes200.txt');
Links= load('Links200.txt');
L= load('L200.txt');
nNodes= size(Nodes,1);
nLinks= size(Links,1);
G=graph(L);

population_size = 100;
mutation_prob = 0.1;
mValues = [1,10,100];
attempts = 10;
maxTime = 60;
cValues = [8,10,12];

for m = mValues
    for c = cValues
        min = inf;
        max = 0;
        average = 0;
        exec_time_media = 0;
        for i = 1:attempts
            [best_solution,generation_count,time_found, exec_time,count] = GA(G,c,population_size,mutation_prob,m,maxTime);
            if(best_solution < min)
                min = best_solution;
            end
            if(best_solution > max)
                max = best_solution;    
            end
            average = average + best_solution;
            exec_time_media = exec_time_media + exec_time;
        end
        fprintf("Results for c = %d on %d runs\nmin: %d\nmax: %d\naverage: %.3f\n",c,attempts,min,max,average/attempts);
        fprintf('Running time: %d seconds\n', exec_time);
        fprintf('The time which was found the best solution: %d',time_found);
    end
end