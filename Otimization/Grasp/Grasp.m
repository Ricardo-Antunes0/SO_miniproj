function [best_value, exec_time, iterations] = Grasp(G,n,r,time)
    start_time = tic;
    current_solution = GreedyRandomized(G,n,r);
    [best_solution, best_value]= SA_HC(G,current_solution);
    iterations = 1;
        
    while (toc(start_time) < time)
        iterations = iterations + 1;
        current_solution = GreedyRandomized(G,n,r);
        [current_solution, current_value]= SA_HC(G,current_solution);
        if current_value < best_value
            best_value = current_value;
            best_solution = current_solution;
        end
    end
    exec_time = toc(start_time);
end