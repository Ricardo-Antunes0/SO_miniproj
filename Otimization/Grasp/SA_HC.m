function [current_solution, current_value]=SA_HC(G,current_solution)
    % G:                 graph of the network
    % current_solution:  A solution
   
    nNodes = numnodes(G);
    improved = true;
    current_value = ConnectedNP(G,current_solution);
    
    while improved
        improved = false;
        others= setdiff(1:nNodes,current_solution);
        
        best_neighbor_value = inf;
     
        for a = current_solution
            for b = others
                neighbor_solution= [setdiff(current_solution,a), b];
                neighbor_value = ConnectedNP(G,neighbor_solution);
         
                if neighbor_value < best_neighbor_value
                    best_neighbor_value = neighbor_value;
                    best_neighbor_solution = neighbor_solution;
                end
            end
        end
        if best_neighbor_value < current_value
            current_value = best_neighbor_value;
            current_solution = best_neighbor_solution;
            improved = true;
        end
    end
end