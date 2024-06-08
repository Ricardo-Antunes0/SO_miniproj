Nodes= load('Nodes200.txt');
Links= load('Links200.txt');
L= load('L200.txt');
nNodes= size(Nodes,1);
nLinks= size(Links,1);
G=graph(L);


% This program is to test the GRASP algorithm with different parameters 

rValues = [2,3,4,10,30,50];
cValues = [8,10,12];
maxTime = 60;

for r = rValues
    for c = cValues    
        [best_solution,exec_time, iterations] = Grasp(G,c,r,maxTime);
        fprintf("Results for r = %d;  c = %d; \n",r,c);
        fprintf('Objective value: %d\n', best_solution);
        fprintf('Running time: %.2f seconds\n', exec_time);
        fprintf('Number of iterations: %d',iterations);
    end
end
