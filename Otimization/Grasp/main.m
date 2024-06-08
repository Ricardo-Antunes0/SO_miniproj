Nodes= load('Nodes200.txt');
Links= load('Links200.txt');
L= load('L200.txt');
nNodes= size(Nodes,1);
nLinks= size(Links,1);
G=graph(L);


rValues = [2,3,4,10,30,50];
cValues = [8,10,12];
attempts = 10;
maxTime = 60;

for r = rValues
    for c = cValues
        min = inf;
        max = 0;
        average = 0;
        for i = 1:attempts
            [best_solution,exec_time,iterations] = Grasp(G,c,r,maxTime);
            if(best_solution < min)
                min = best_solution;
            end
            if(best_solution > max)
                max = best_solution;    
            end
            average = average + best_solution;
            disp(exec_time);
            disp(best_solution);
        end
        fprintf("\nResults for c = %d r=%d on %d runs\n max: %d\n min: %d\naverage: %.3f\n",c,r,attempts,max,min,average/attempts);
    end
end