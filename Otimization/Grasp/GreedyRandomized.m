function current_solution=GreedyRandomized(G,n, r)
% G:        graph of the network
% n:        number of nodes of the solution
% r:        parameter of the Greedy Randomized method
    
    E = 1:numnodes(G);
    current_solution = [];
    for i= 1:n
        R= [];
        for j= E
            R= [R ; j ConnectedNP(G,[current_solution j])];
        end
        R= sortrows(R,2);
        e= R(randi(r),1);
        current_solution= [current_solution e];
        E= setdiff(E,e);
    end
end 